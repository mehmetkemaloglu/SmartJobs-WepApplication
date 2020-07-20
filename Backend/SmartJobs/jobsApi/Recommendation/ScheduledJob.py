
from ..helpers import SearchHelper
import json
import pickle


#sameEmployerThreshold=0.408
#diffEmployerThreshold=0.037
sameEmployerThreshold=0.7
diffEmployerThreshold=0.20
def recommend(newjobs,personid,vectorizer):
    from ..models import Liked, Jobs,Recommendation
    from .Document_Similarity import calculateJobSimilarity
    #Recommendation.objects.filter(personid=personid).delete()
    recommendedJobs=[]
    liked=Liked.objects.filter(personid=personid).values("jobjid")
    likedjobs=Jobs.objects.filter(jid__in=liked)
    for likedjob in likedjobs:
        for newjob in newjobs:

            cossim=calculateJobSimilarity(likedjob,newjob,vectorizer,True,True)
            if likedjob.employer==newjob.employer:
                if cossim>sameEmployerThreshold:
                    recommendedJobs.append(newjob.jid)
            else:
                if cossim>diffEmployerThreshold:
                    recommendedJobs.append(newjob.jid)


    recs=[]
    for nj in newjobs:
        rec = Recommendation()
        rec.personid = personid
        rec.jid = nj.jid
        if nj.jid in recommendedJobs:
            rec.recommended = 1
        else:
            rec.recommended=0
        recs.append(rec)

    rr=Recommendation.objects.bulk_create(recs)

    return recommendedJobs

def start():
    print("called")
    vectorizer = pickle.load(open("TfIdfvectorizer.pickle", "rb"))
    from ..models import Query,Jobs
    queries=Query.objects.all()
    from ..helpers.DBhelper import saveJobsToDB

    for q in queries:
        loc=[]
        if q.location!="":
            loc.append(q.location)
        newjobs=SearchHelper.searchJob(q.keyword,json.loads(q.jobtypes),json.loads(q.fields),loc,parseAllPages=True,recent=True)
        ids=saveJobsToDB(newjobs)
        jobs=Jobs.objects.filter(jid__in=ids)
        recommend(jobs,q.personid,vectorizer)


def deneme():
    from ..models import Liked, Jobs
    vectorizer = pickle.load(open("TfIdfvectorizer.pickle", "rb"))
    rec=recommend(Jobs.objects.filter(jid__lte=100), 2, vectorizer)
    for r in rec:
        print(str(r.jid)+" "+r.name)

