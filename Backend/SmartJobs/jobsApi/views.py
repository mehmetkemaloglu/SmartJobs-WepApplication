from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from rest_framework import status

from .parsers import parseAcademicPositions, parseUniversityPositions, parseTimesHigherEducation
from rest_framework.views import APIView
from rest_framework.response import Response
from .helpers import DBhelper, SearchHelper
from .Recommendation import Document_Similarity
from .models import Jobs, Liked, Person, Label, Query, Recommendation,QueryJob,SearchHistoryQuery, Visited
from .serializers import JobsSerializer
from django.forms.models import model_to_dict
import json
from .Recommendation import ScheduledJob


class jobsAP(APIView):
    def get(self, request):
        req = parseSearchRequest(request.GET)
        data = SearchHelper.searchJob(req[0], req[1], req[2], req[3], parseAllPages=req[4], recent=False)
        ids = DBhelper.saveJobsToDB(data)
        jobs = Jobs.objects.filter(jid__in=ids)
        data = []
        for job in jobs:
            data.append(model_to_dict(job))
        return Response(data)


class jobsTHE(APIView):
    def get(self, request):
        req = parseSearchRequest(request.GET)
        data = parseTimesHigherEducation.searchJob(req[0], req[1], req[2], req[3], [],
                                                   req[4])  # Write True as another parameter for only recent jobs
        return Response(data)


class jobsUP(APIView):
    def get(self, request):
        req = parseSearchRequest(request.GET)
        data = parseUniversityPositions.search(req[0], req[1], req[2], req[3], [],
                                               req[4])  # Write True as another parameter for only recent jobs
        return Response(data)


class likeJob(APIView):

    def get(self, request):
        pid = getPersonId(request, "get")
        if pid:
            pid = int(request.query_params["personid"])
            likedIds = Liked.objects.filter(personid=pid).values("jobjid")
            likedJobs = Jobs.objects.filter(jid__in=likedIds)
            serializer = JobsSerializer(likedJobs, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "User not logged in"}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        try:
            pid = getPersonId(request, "post")

            if pid:
                jid = DBhelper.saveJob(request.data["job"])
                likedbefore = Liked.objects.filter(personid=pid, jobjid=jid)
                if len(likedbefore) > 0:
                    return Response({"message": "User had already liked this job"},
                                    status=status.HTTP_405_METHOD_NOT_ALLOWED)
                else:
                    like = Liked()
                    like.personid = pid
                    like.jobjid = jid
                    like.save()
                return Response({"jid": jid}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "User not logged in"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"message": e.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            pid = getPersonId(request, "delete")
            if pid:
                jid = request.data["jid"]
                Liked.objects.filter(jobjid=jid, personid=pid).delete()
                return Response({"message": "Successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "User not logged in"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"message": e.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class labels(APIView):

    def get(self, request):
        try:
            pid = getPersonId(request, "get")
            if pid:
                if "jid" in request.query_params:
                    labels = Label.objects.filter(personid=pid, jobjid=request.query_params["jid"]).values(
                        "name").distinct()
                else:
                    labels = Label.objects.filter(personid=pid).values("name").distinct()

                labelnames = [lab["name"] for lab in labels]
                return Response(labelnames)
            else:
                return Response({"message": "User not logged in"}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({"message": e.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:

            pid = getPersonId(request, "post")
            if pid:
                lab = Label()
                lab.personid = pid
                lab.jobjid = DBhelper.saveJob(request.data["job"])
                lab.name = request.data["labelname"]
                labeledbefore = Label.objects.filter(personid=pid, jobjid=lab.jobjid, name=lab.name)
                if len(labeledbefore) > 0:
                    return Response({"message": "User had already labeled this job with this label"},
                                    status=status.HTTP_405_METHOD_NOT_ALLOWED)
                else:
                    lab.save()
                    return Response({"jid": lab.jobjid}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "User not logged in"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"message": e.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            pid = getPersonId(request, "delete")
            if pid:
                label = request.data["label"]
                if "jid" in request.data:
                    jid = request.data["jid"]
                    Label.objects.filter(jobjid=jid, personid=pid, name=label).delete()
                else:
                    Label.objects.filter(personid=pid, name=label).delete()
                return Response({"message": "Successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "User not logged in"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"message": e.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class jobs(APIView):

    def get(self, request):
        # get detils of a job
        if "jid" in request.query_params:
            jid = int(request.query_params["jid"])
            job = Jobs.objects.filter(jid=jid)

            if len(job) > 0:
                pid = getPersonId(request, "get")
                job = model_to_dict(job[0])
                if pid:

                    liked = Liked.objects.filter(personid=pid, jobjid=job["jid"])
                    job["liked"] = len(liked) > 0
                    vis=Visited()
                    vis.personid=pid
                    vis.jid=job["jid"]
                    vis.save()
                return Response(job)
            else:
                return Response({"message": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            pid = getPersonId(request, "get")
            # get saved jovs
            if pid:

                if "label" in request.query_params:
                    labels = Label.objects.filter(personid=pid, name=request.query_params["label"])
                else:
                    labels = Label.objects.filter(personid=pid)
                jids = []
                labmapping = {}
                for label in labels:
                    jids.append(label.jobjid)
                    if label.jobjid in labmapping:
                        labmapping[label.jobjid].append(label.name)
                    else:
                        labmapping[label.jobjid] = [label.name]

                jobs = Jobs.objects.filter(jid__in=jids)
                jobdicts = []
                for job in jobs:
                    for l in labmapping[job.jid]:
                        dicti = model_to_dict(job)
                        dicti["label"] = l
                        jobdicts.append(dicti)
                """
                for label in labels:
                    jobs=Jobs.objects.filter(jid=label.jobjid)
                    if len(jobs)>0:
                        job=jobs[0]
                        dicti=model_to_dict(job)
                        dicti["label"]=label.name
                        jobs.append(dicti)
                """
                return Response(jobdicts)
            else:
                return Response({"message": "User not logged in"}, status=status.HTTP_401_UNAUTHORIZED)


class query(APIView):

    # get saved queries
    def get(self, request):
        try:
            pid = getPersonId(request, "get")
            if pid:
                qs = Query.objects.filter(personid=pid)
                queries = []
                for q in qs:
                    dicti = model_to_dict(q)
                    dicti["fields"] = json.loads(dicti["fields"])
                    dicti["jobtypes"] = json.loads(dicti["jobtypes"])
                    queries.append(dicti)
                return Response(queries)
            else:
                return Response({"message": "User not logged in"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"message": e.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # save query
    def post(self, request):
        try:
            pid = getPersonId(request, "post")
            if pid:
                query = Query()
                query.personid = pid
                req = parseSearchRequest(request.data)
                # print(req[3])
                locarr = req[3]
                if len(locarr) > 0:
                    query.location = req[3][0]
                else:
                    query.location = ""
                query.fields = json.dumps(req[2])
                query.jobtypes = json.dumps(req[1])
                query.keyword = req[0]
                savedbefore = Query.objects.filter(personid=pid, keyword=query.keyword, fields=query.fields,
                                                   jobtypes=query.jobtypes, location=query.location)
                if len(savedbefore) > 0:
                    return Response({"message": "User had already saved this query"},
                                    status=status.HTTP_405_METHOD_NOT_ALLOWED)
                else:
                    query.save()
                    return Response({"message": "Successful"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "User not logged in"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"message": e.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            pid = getPersonId(request, "delete")
            if pid:
                qid = request.data["id"]
                Query.objects.filter(id=qid).delete()
                return Response({"message": "Successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "User not logged in"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"message": e.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class inbox(APIView):
    def get(self, request):

        pid = getPersonId(request, "get")
        if pid:
            recs0 = Recommendation.objects.filter(personid=pid)
            visit= [q["jid"] for q in Visited.objects.filter(personid=pid).values("jid").distinct()]
            mapping = {}

            for rec in recs0:
                if rec.jid in mapping:
                    mapping[rec.jid] += rec.recommended
                else:
                    mapping[rec.jid] = rec.recommended

            jobs = Jobs.objects.filter(jid__in=list(mapping.keys())).order_by("-jid")
            retjobs = []

            for job in jobs:
                jj = model_to_dict(job)
                jj["recommended"] = mapping[(job.jid)]
                jj["visited"] = job.jid in visit
                retjobs.append(jj)

            return Response(retjobs)
        else:
            return Response({"message": "User not logged in"}, status=status.HTTP_401_UNAUTHORIZED)


class signup(APIView):
    def post(self, request):
        try:
            person = Person()
            person.name = request.data["name"]
            if Person.objects.filter(name=person.name).count() >0:
                return Response({"message": "Username is not available!"}, status=status.HTTP_201_CREATED)
            else:
                person.password = request.data["password"]
                person.save()
                return Response({"message": "Successful"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": e.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class signin(APIView):
    def post(self, request):
        try:
            personid = Person.objects.filter(name=request.data["name"], password=request.data["password"])
            pid = personid[0].id
            return Response(pid)
        except Exception as e:
            return Response({"message": e.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class searchhistoryquery(APIView):

    # get history queries
    def get(self, request):
        try:
            qs = SearchHistoryQuery.objects.all()
            queries = []
            for q in qs:
                dicti = model_to_dict(q)
                queries.append(dicti)
            return Response(queries)

        except Exception as e:
            return Response({"message": e.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # save search query
    def post(self, request):
        try:
            query = SearchHistoryQuery()
            req = parseSearchRequest(request.data)
            # print(req[3])
            locarr = req[3]
            if len(locarr) > 0:
                query.location = req[3][0]
            else:
                query.location = ""
            query.fields = json.dumps(req[2])
            query.jobtypes = json.dumps(req[1])
            query.keyword = req[0]
            query.save()
            return Response({"message": "Successful"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"message": e.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class getsearchhistory(APIView):
    def get(self, request):
        try:
            jobids = []
            jobs = []
            if "queryid" in request.query_params:
                jid = int(request.query_params["queryid"])
                jobquery = QueryJob.objects.filter(queryid=jid).values_list('jobid', flat=True)

                jobs = Jobs.objects.filter(jid__in=jobquery)
                jobdicts = []
                for job in jobs:
                    dicti = model_to_dict(job)
                    jobdicts.append(dicti)

                return Response(jobdicts)
                """
                for abc in jobquery:
                    jobs.append(Jobs.objects.filter(jid=int(abc)))

                    serializer = JobsSerializer(jobs, many=True)
                #print(jid)

                print(jobquery[0].jobid)

                for j in jobquery:
                    print(j.jobid)
                    jobids.append(j.jobid)

                for i in jobids:
                    jobs.append(Jobs.objects.filter(jid=i))

                return Response(serializer.data)
"""
        except Exception as e:
            return Response({"message": e.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def startScheduled(request):
    ScheduledJob.start()
    return HttpResponse(json.dumps({"message": "Scheduled Job executed!"}), content_type="application/json")


def index(request):
    # DBhelper.saveJobsFromUrlToDB("https://academicpositions.com/find-jobs/all-in-all-by-all-in-all/Temporary%20academic%20staff%2C%20Qualitative%20research%20methods/1")
    # Jobs.objects.all().delete()
    # DBhelper.saveJobsFromUrlToDB("https://academicpositions.com/find-jobs/all-in-all-by-all-in-all/wireless/1",allJobs=True)
    # DBhelper.saveJobsFromUrlToDB("https://academicpositions.com/find-jobs/all-in-Cyber%20Security-by-all-in-Europe/all/1")
    # Document_Similarity.calcSim()

    # json=parseAcademicPositions.parse()
    # req = parseSearchRequest(request)
    # json2= parseTimesHigherEducation.searchJob(req[0], req[1], req[2], req[3], [], req[4])
    # jobs=parseTimesHigherEducation.parseUrl("https://www.timeshighereducation.com/unijobs/listings/arts-and-humanities/senior-management-and-heads-of-department/#browsing",True)
    # jobs=parseAcademicPositions.parseUrl("https://academicpositions.com/find-jobs/all-in-Computer%20Science-by-all-in-all/all/1",True,True)
    # str(parseAcademicPositions.deneme("https://academicpositions.com/ad/medical-university-vienna/2020/phd-program-molecular-cellular-and-clinical-allergology/145686"))

    # parseAcademicPositions.getHTMLOfJobsInDatabase()

    return HttpResponse("""
    <div class="block fix-text job-description">
<p><strong>School/Department </strong>Cranfield Defence and Security<br/>
<strong>Based at </strong>Shrivenham, Oxfordshire - Cranfield Defence and Security<br/>
<strong>Hours of work </strong>37 hours per week, normally worked Monday to Friday. Flexible working will be considered<br/>
<strong>Contract type </strong>Fixed term contract<br/>
<strong>Fixed Term Period </strong>Fixed Term Contract for two years<br/>
<strong>Salary </strong>£43,351 to £48,323 per annum with additional performance related pay up to £60,403 per annum<br/>
<strong>Apply by </strong>12/07/2020</p>
<p><strong>Role Description</strong></p>
<p>Cranfield University Cranfield Defence and Security welcomes applications from Senior Research Fellows.    </p>
<p>As the UK’s only exclusively postgraduate university, Cranfield’s world-class expertise, large-scale facilities and unrivalled industry partnerships is creating leaders in technology and management globally.  Our distinctive expertise is in our deep understanding of technology and management and how these work together to benefit the world. </p>
<p>Our people are our most valuable resource and everyone has a role to play in shaping the future of our university, developing our learners, and transforming the businesses we work with. Learn more about Cranfield and our unique impact here: <a data-mz="" href="https://www.cranfield.ac.uk/about/working-at-cranfield" rel="no-follow">Working life at Cranfield</a>. </p>
<p>Our shared, stated values help to define who we are and underpin everything we do: Ambition; Impact; Respect; and Community. To find out more please visit our website: <a data-mz="" href="https://www.cranfield.ac.uk/about/about" rel="no-follow">https://www.cranfield.ac.uk/about/about</a> </p>
<p>The Centre for Defence Chemistry has been working on propellants, explosives and pyrotechnic research for decades. We are interested in all aspects of defence manufacturing, vulnerability, combustion, and life assessment of energetic materials. The Centre is home to an enviable range of facilities for the analysis and characterization, testing, ageing and disposal of a wide range of materials including explosives, propellants, pyrotechnics, fuels and polymers. <a data-mz="" href="https://www.cranfield.ac.uk/centres/centre-for-defence-chemistry" rel="no-follow">https://www.cranfield.ac.uk/centres/centre-for-defence-chemistry</a> </p>
<p>This role holder’s research aims to build validated models that describe the onset and subsequent growth of reaction, particularly for explosives under cook-off conditions.  A Senior Research Fellow is required, in order to support research and a fully-funded PhD researcher is scheduled to begin in October 2020, who will focus on development of computer models for slow decomposition in early cook-off. </p>
<p><strong>The role holder will:</strong></p>
<ul>
<li>Lead research into computer model development, maintaining emphasis on both experimental and theoretical aspects of research, and building a new research area</li>
<li>Actively carry out research in support of an existing research contract</li>
<li>Work closely with CfDC Manufacturing Group in formulations development</li>
<li>Build research collaboration with AWE formulations development team</li>
<li>Co-supervise existing PhD students, and gain new PhD researchers</li>
</ul>
<p>You will hold a PhD or equivalent in a chemistry-related field with experience of computer model development for decomposition chemistry and microstructural mechanisms.  Experience in Project Management and supervising research students is also required. </p>
<p>You will have subject matter expertise in cook-off experiments, modelling and model development; sound knowledge of opportunities for novel developments in the context of your area and an understanding of the contemporary challenges facing the defence sector in the UK and further afield.</p>
<p>In return, the successful applicant will have exciting opportunities for career development in this key position, and to support world leading research and education, joining a supportive team and environment.</p>
<p>At Cranfield we value Diversity and Inclusion, and aim to create and maintain a culture in which everyone can work and study together harmoniously with dignity and respect and realise their full potential.  </p>
<p>Our equal opportunities and diversity monitoring has shown that that women and minority ethnic groups are currently underrepresented within the university and so we actively encourage applications from eligible candidates from these groups.</p>
<p>We actively consider flexible working options such as part-time, compressed or flexible hours and/or an element of homeworking, and commit to exploring the possibilities for each role.  To find out more, please visit <a data-mz="" href="https://www.cranfield.ac.uk/about/working-at-cranfield/diversity" rel="no-follow">https://www.cranfield.ac.uk/about/working-at-cranfield/diversity</a></p>
<p>For an informal discussion, please contact Chris Stennett at <a data-mz="" href="mailto:c.stennett@cranfield.ac.uk" rel="no-follow">c.stennett@cranfield.ac.uk</a>. </p>
</div>
    """)


def parseSearchRequest(request):
    allJobs = True
    keyword = request.get("keyword", "")
    jobtypes = request.get("jobtypes", "").split(",")
    locations = request.get("locations", "").split(",")
    fields = request.get("fields", "").split(",")
    if request.get("allJobs", "") == "false":
        allJobs = False

    if (jobtypes == ['']):
        jobtypes = []
    if (locations == ['']):
        locations = []
    if (fields == ['']):
        fields = []

    if (len(fields) > 0 and "Electrical Engineering" in fields[0]):
        fields[0] = "Electrical Engineering"
        fields.append("Electronics")

    return (keyword, jobtypes, fields, locations, allJobs)


def getPersonId(request, reqtype):
    if reqtype == "get":
        if "personid" in request.query_params:
            return int(request.query_params["personid"])
    else:
        if "personid" in request.data:
            return int(request.data["personid"])
    return False



