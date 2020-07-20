# Program to measure similarity between
# two sentences using cosine similarity.
import ast
from operator import itemgetter

from django.forms import model_to_dict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from ..models import Jobs
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
import pickle
import json

from ..parsers.parseAcademicPositions import parseUrl
from ..helpers.DBhelper import saveJobsFromUrlToDB


stop_words = set(stopwords.words('english'))


def getOnlyNouns(document):
    blob = TextBlob(document)
    Xnew = ""
    for w in blob.noun_phrases:
        Xnew += w + " "
    return Xnew

def removeStopWords(document):
    Xnew = ""
    for w in word_tokenize(document):
        if w not in stop_words:
            Xnew += w + " "
    return Xnew

def calculateCosineSim(X,Y,vectorizer,withoutStopWords=False,onlyNouns=False):

    if onlyNouns:
        X=getOnlyNouns(X)
        Y=getOnlyNouns(Y)

    if withoutStopWords:
        X=removeStopWords(X)
        Y=removeStopWords(Y)


    tfidf1=vectorizer.transform([X])
    tfidf2=vectorizer.transform([Y])
    similarity=cosine_similarity(tfidf1,tfidf2)
    return similarity


def updateVectorizer(withoutStopWords=True,onlyNouns=True,withFields=True):
    docs = []
    for job in Jobs.objects.all():
        desc1 = job.jobdescription
        if withFields:
            j1fields = json.loads((job.fields))
            for field in j1fields:
                desc1 += " " + field
        if onlyNouns:
            desc1=getOnlyNouns(desc1)
        docs.append(desc1)


    if withoutStopWords:
        tfidf = TfidfVectorizer(stop_words=stop_words)
    else:
        tfidf = TfidfVectorizer()
    vectorizer=tfidf.fit(docs)

    pickle.dump(vectorizer, open("vectorizer("+str(withoutStopWords)+str(onlyNouns)+str(withFields)+").pickle", "wb"))

def updateAllVectorizers():
    updateVectorizer(True,True,True)
    updateVectorizer(False,True,True)
    updateVectorizer(False,False,True)
    updateVectorizer(False,False,False)
    updateVectorizer(True,False,True)
    updateVectorizer(True,False,False)
    updateVectorizer(True,True,False)
    updateVectorizer(False,True,False)


def calculateJobSimilarity(job,job2,vectorizer,withoutStopWords=True,onlyNouns=True,withFields=True):


    desc1 = job.jobdescription
    desc2 = job2.jobdescription

    if withFields:
        j1fields = json.loads((job.fields))
        j2fields = json.loads((job.fields))
        for field in j1fields:
            desc1 += " " + field

        for field in j2fields:
            desc2 += " " + field

    return calculateCosineSim(desc1, desc2, vectorizer, withoutStopWords=withoutStopWords, onlyNouns=onlyNouns)


wirelessids=[1601, 1606, 158, 1615, 1616, 1617, 1618, 1619, 1620, 1621, 1622, 166, 187, 189, 190, 194, 218, 226, 242, 248, 254, 259, 271, 277, 278, 294, 332, 336, 350, 442, 489, 490, 500, 513, 514, 520, 560, 587, 603, 607,614, 625, 691, 116, 733, 734, 737, 767, 769, 798, 810, 815, 852, 854, 858, 860, 862, 868, 898, 980, 1018, 1024, 1026, 1028, 1044, 1045, 1087, 1095, 1147, 1167, 1211, 1324, 1394, 1399, 1433, 1441, 1448, 1454, 1485, 1496, 1503, 1544, 1551, 1561, 1563]
bigdataids=[192, 277, 278, 459, 460, 461, 116, 858, 862, 1091, 1131, 1164, 1165, 1229, 1239, 1240, 1241, 1242, 1243, 1244, 1245, 1246, 1247, 1248, 1249, 1250, 1251, 1255, 1256, 1257, 1258, 1259, 1338, 1412, 1442, 1523, 1524, 1525, 1623, 1526, 1527, 1528, 1529, 1530, 1531, 1532, 1533, 1534, 1535, 1536, 1537, 1538, 1539, 1540, 1541, 1542, 1543, 1573, 1574, 1575, 1576]
compvisionids=[1601, 109, 1597, 1624, 1625, 1626, 1627, 1628, 1629, 1602, 1630, 1603, 1591, 151, 164, 236, 237, 277, 278, 311, 390, 449, 451, 475, 523, 540, 574, 599, 113, 651, 656, 663, 116, 703, 110, 712, 117, 118, 122, 125, 813, 80, 81, 819, 48, 49, 44, 830, 75, 838, 71, 72, 61, 57, 58, 74, 858, 862, 864, 50, 64, 68, 953, 46, 960, 94, 1048, 45, 1091, 1094, 1105, 59, 1122, 1154, 1216, 1223, 1267, 1325, 1376, 60, 1414, 41, 1447]

def getQueryResults():
    """
    global wirelessids
    wirelessids=saveJobsFromUrlToDB("https://academicpositions.com/find-jobs/all-in-all-by-all-in-all/wireless/1",True)
    global bigdataids
    bigdataids=saveJobsFromUrlToDB("https://academicpositions.com/find-jobs/all-in-all-by-all-in-all/big%20data/1",True)
    global compvisionids
    compvisionids=saveJobsFromUrlToDB("https://academicpositions.com/find-jobs/all-in-all-by-all-in-all/computer%20vision/1",True)
    """

    """
    global wirelessids
    wirelessids = saveJobsFromUrlToDB("https://academicpositions.com/find-jobs/all-in-all-by-all-in-all/integrated%20circuit/1",
                                      True)
    global bigdataids
    bigdataids = saveJobsFromUrlToDB("https://academicpositions.com/find-jobs/all-in-Quantum%20Computing-by-all-in-all/all/1",
                                     True)

    global compvisionids
    compvisionids = saveJobsFromUrlToDB(
        "https://academicpositions.com/find-jobs/all-in-Literature-by-all-in-all/all/1", True)
    """

    global wirelessids
    wirelessids = saveJobsFromUrlToDB("https://academicpositions.com/find-jobs/all-in-Biochemistry-by-all-in-all/all/1",
                                      True)
    global bigdataids
    bigdataids = saveJobsFromUrlToDB("https://academicpositions.com/find-jobs/all-in-Educational%20Assessment-by-all-in-all/all/1",
                                     True)

    global compvisionids
    compvisionids = saveJobsFromUrlToDB(
        "https://academicpositions.com/find-jobs/all-in-Computer%20Communications%20(Networks)-by-all-in-all/all/1", True)




    print(wirelessids)
    print(bigdataids)
    print(compvisionids)


def calcError(vectorizer,jobs,q1length,querydict,f,withoutStopWords=True,onlyNouns=True,withFields=True,popindex=0,empCheck=False):

    alljobs=jobs[:]
    q1jobs=alljobs[0:q1length]
    job = q1jobs.pop(popindex)
    alljobs.pop()
    jj = []

    #vectorizer = pickle.load(open("vectorizer("+str(withoutStopWords)+str(onlyNouns)+str(withFields)+").pickle", "rb"))
    #vectorizer = pickle.load(open("TfIdfvectorizer.pickle", "rb"))

    count=0
    if empCheck:
        for q1 in q1jobs:
            if q1.employer==job.employer:
                count+=1

    for j in alljobs:

        if (not empCheck) or j.employer!=job.employer:
            dct = {}
            dct["job"] = j
            dct["val"] = calculateJobSimilarity(job, j, vectorizer,withoutStopWords, onlyNouns, withFields)[0][0]
            jj.append(dct)

    newlist = sorted(jj, key=itemgetter('val'), reverse=True)
    errorsum = 0
    for i in range(len(newlist)):
        if "q1" in querydict[newlist[i]["job"].jid]:
            errorsum += i

    print("count is : "+str(count)+" "+job.name)
    size = q1length-count-1
    errorsum -= size * (size - 1) / 2
    errorsum /= size

    #f.write("===================================================================================================\n")

    f.write("withoutStopWords="+str(withoutStopWords)+" onlyNouns="+str(onlyNouns)+" withFields="+str(withFields)+"\n")
    f.write("Error measure: " + str(errorsum) + "\n\n")
    """
    for j in newlist:
        job2 = j["job"]
        f.write(str(querydict[job2.jid]) + " " + job2.name + " " + str(job2.jid) + " " + str(j["val"]) + "\n")
    """
    #f.write("===================================================================================================\n")
    return errorsum

def cosineSimTest(empCheck=False):

    global wirelessids
    global bigdataids
    global compvisionids

    wirelessjobs=Jobs.objects.filter(jid__in=wirelessids)
    bigdatajobs=Jobs.objects.filter(jid__in=bigdataids)
    compvisionjobs=Jobs.objects.filter(jid__in=compvisionids)


    querydict={}
    for w in wirelessjobs:
        if w.jid not in querydict:
            querydict[w.jid]=["q1"]
        else:
            querydict[w.jid].append("q1")

    for b in bigdatajobs:
        if b.jid not in querydict:
            querydict[b.jid]=["q2"]
        else:
            querydict[b.jid].append("q2")

    for c in compvisionjobs:
        if c.jid not in querydict:
            querydict[c.jid]=["q3"]
        else:
            querydict[c.jid].append("q3")

    alljobs=[]
    alljobs.extend(wirelessjobs)
    alljobs.extend(bigdatajobs)
    alljobs.extend(compvisionjobs)

    err1=0
    err2=0
    err3=0
    err4=0
    err5=0
    err6=0
    err7=0
    err8=0

    vectorizer1 = pickle.load(open("vectorizer(TrueTrueTrue).pickle", "rb"))
    vectorizer2 = pickle.load(open("vectorizer(TrueTrueFalse).pickle", "rb"))
    vectorizer3 = pickle.load(open("vectorizer(TrueFalseTrue).pickle", "rb"))
    vectorizer4 = pickle.load(open("vectorizer(TrueFalseFalse).pickle", "rb"))
    vectorizer5 = pickle.load(open("vectorizer(FalseTrueTrue).pickle", "rb"))
    vectorizer6 = pickle.load(open("vectorizer(FalseFalseTrue).pickle", "rb"))
    vectorizer7 = pickle.load(open("vectorizer(FalseTrueFalse).pickle", "rb"))
    vectorizer8 = pickle.load(open("vectorizer(FalseFalseFalse).pickle", "rb"))

    f = open("similarity_results1.txt", "w+")
    size=len(wirelessjobs)
    for i in range(size):
        f.write("===============================================================\n")
        job=wirelessjobs[i]
        f.write(str(job.jid) + " " + job.name + "\n")
        err1+=calcError(vectorizer1,alljobs,len(wirelessjobs),querydict,f,withoutStopWords=True,onlyNouns=True,withFields=True,popindex=i,empCheck=empCheck)
        err2 +=calcError(vectorizer2,alljobs,len(wirelessjobs),querydict,f,withoutStopWords=True,onlyNouns=True,withFields=False,popindex=i,empCheck=empCheck)
        err3 +=calcError(vectorizer3,alljobs,len(wirelessjobs),querydict,f,withoutStopWords=True,onlyNouns=False,withFields=True,popindex=i,empCheck=empCheck)
        err4 +=calcError(vectorizer4,alljobs,len(wirelessjobs),querydict,f,withoutStopWords=True,onlyNouns=False,withFields=False,popindex=i,empCheck=empCheck)
        err5 +=calcError(vectorizer5,alljobs,len(wirelessjobs),querydict,f,withoutStopWords=False,onlyNouns=True,withFields=True,popindex=i,empCheck=empCheck)
        err6 +=calcError(vectorizer6,alljobs,len(wirelessjobs),querydict,f,withoutStopWords=False,onlyNouns=False,withFields=True,popindex=i,empCheck=empCheck)
        err7 +=calcError(vectorizer7,alljobs,len(wirelessjobs),querydict,f,withoutStopWords=False,onlyNouns=True,withFields=False,popindex=i,empCheck=empCheck)
        err8 +=calcError(vectorizer8,alljobs,len(wirelessjobs),querydict,f,withoutStopWords=False,onlyNouns=False,withFields=False,popindex=i,empCheck=empCheck)
        f.write("===============================================================\n")
        print("here" + str(i))

    err1/=size
    err2/=size
    err3/=size
    err4/=size
    err5/=size
    err6/=size
    err7/=size
    err8/=size

    f.write("err1 average: "+str(err1)+"\n")
    f.write("err2 average: "+str(err2)+"\n")
    f.write("err3 average: "+str(err3)+"\n")
    f.write("err4 average: "+str(err4)+"\n")
    f.write("err5 average: "+str(err5)+"\n")
    f.write("err6 average: "+str(err6)+"\n")
    f.write("err7 average: "+str(err7)+"\n")
    f.write("err8 average: "+str(err8)+"\n")

    f.close()


def cosineSimTest2(empCheck=False):

    global wirelessids
    global bigdataids
    global compvisionids

    wirelessjobs=Jobs.objects.filter(jid__in=bigdataids)
    bigdatajobs=Jobs.objects.filter(jid__in=wirelessids)
    compvisionjobs=Jobs.objects.filter(jid__in=compvisionids)


    querydict={}
    for w in wirelessjobs:
        if w.jid not in querydict:
            querydict[w.jid]=["q1"]
        else:
            querydict[w.jid].append("q1")

    for b in bigdatajobs:
        if b.jid not in querydict:
            querydict[b.jid]=["q2"]
        else:
            querydict[b.jid].append("q2")

    for c in compvisionjobs:
        if c.jid not in querydict:
            querydict[c.jid]=["q3"]
        else:
            querydict[c.jid].append("q3")

    alljobs=[]
    alljobs.extend(wirelessjobs)
    alljobs.extend(bigdatajobs)
    alljobs.extend(compvisionjobs)

    err1=0
    err2=0
    err3=0
    err4=0
    err5=0
    err6=0
    err7=0
    err8=0

    vectorizer1 = pickle.load(open("vectorizer(TrueTrueTrue).pickle", "rb"))
    vectorizer2 = pickle.load(open("vectorizer(TrueTrueFalse).pickle", "rb"))
    vectorizer3 = pickle.load(open("vectorizer(TrueFalseTrue).pickle", "rb"))
    vectorizer4 = pickle.load(open("vectorizer(TrueFalseFalse).pickle", "rb"))
    vectorizer5 = pickle.load(open("vectorizer(FalseTrueTrue).pickle", "rb"))
    vectorizer6 = pickle.load(open("vectorizer(FalseFalseTrue).pickle", "rb"))
    vectorizer7 = pickle.load(open("vectorizer(FalseTrueFalse).pickle", "rb"))
    vectorizer8 = pickle.load(open("vectorizer(FalseFalseFalse).pickle", "rb"))

    f = open("similarity_results2.txt", "w+")
    size = len(wirelessjobs)
    for i in range(size):
        f.write("===============================================================\n")
        job = wirelessjobs[i]
        f.write(str(job.jid) + " " + job.name + "\n")
        err1 += calcError(vectorizer1, alljobs, len(wirelessjobs), querydict, f, withoutStopWords=True, onlyNouns=True,
                          withFields=True, popindex=i, empCheck=empCheck)
        err2 += calcError(vectorizer2, alljobs, len(wirelessjobs), querydict, f, withoutStopWords=True, onlyNouns=True,
                          withFields=False, popindex=i, empCheck=empCheck)
        err3 += calcError(vectorizer3, alljobs, len(wirelessjobs), querydict, f, withoutStopWords=True, onlyNouns=False,
                          withFields=True, popindex=i, empCheck=empCheck)
        err4 += calcError(vectorizer4, alljobs, len(wirelessjobs), querydict, f, withoutStopWords=True, onlyNouns=False,
                          withFields=False, popindex=i, empCheck=empCheck)
        err5 += calcError(vectorizer5, alljobs, len(wirelessjobs), querydict, f, withoutStopWords=False, onlyNouns=True,
                          withFields=True, popindex=i, empCheck=empCheck)
        err6 += calcError(vectorizer6, alljobs, len(wirelessjobs), querydict, f, withoutStopWords=False,
                          onlyNouns=False, withFields=True, popindex=i, empCheck=empCheck)
        err7 += calcError(vectorizer7, alljobs, len(wirelessjobs), querydict, f, withoutStopWords=False, onlyNouns=True,
                          withFields=False, popindex=i, empCheck=empCheck)
        err8 += calcError(vectorizer8, alljobs, len(wirelessjobs), querydict, f, withoutStopWords=False,
                          onlyNouns=False, withFields=False, popindex=i, empCheck=empCheck)
        f.write("===============================================================\n")
        print("here" + str(i))

    err1/=size
    err2/=size
    err3/=size
    err4/=size
    err5/=size
    err6/=size
    err7/=size
    err8/=size

    f.write("err1 average: "+str(err1)+"\n")
    f.write("err2 average: "+str(err2)+"\n")
    f.write("err3 average: "+str(err3)+"\n")
    f.write("err4 average: "+str(err4)+"\n")
    f.write("err5 average: "+str(err5)+"\n")
    f.write("err6 average: "+str(err6)+"\n")
    f.write("err7 average: "+str(err7)+"\n")
    f.write("err8 average: "+str(err8)+"\n")

    f.close()



def cosineSimTest3(empCheck=False):

    global wirelessids
    global bigdataids
    global compvisionids

    wirelessjobs=Jobs.objects.filter(jid__in=compvisionids)
    bigdatajobs=Jobs.objects.filter(jid__in=bigdataids)
    compvisionjobs=Jobs.objects.filter(jid__in=wirelessids)


    querydict={}
    for w in wirelessjobs:
        if w.jid not in querydict:
            querydict[w.jid]=["q1"]
        else:
            querydict[w.jid].append("q1")

    for b in bigdatajobs:
        if b.jid not in querydict:
            querydict[b.jid]=["q2"]
        else:
            querydict[b.jid].append("q2")

    for c in compvisionjobs:
        if c.jid not in querydict:
            querydict[c.jid]=["q3"]
        else:
            querydict[c.jid].append("q3")

    alljobs=[]
    alljobs.extend(wirelessjobs)
    alljobs.extend(bigdatajobs)
    alljobs.extend(compvisionjobs)

    err1=0
    err2=0
    err3=0
    err4=0
    err5=0
    err6=0
    err7=0
    err8=0

    vectorizer1 = pickle.load(open("vectorizer(TrueTrueTrue).pickle", "rb"))
    vectorizer2 = pickle.load(open("vectorizer(TrueTrueFalse).pickle", "rb"))
    vectorizer3 = pickle.load(open("vectorizer(TrueFalseTrue).pickle", "rb"))
    vectorizer4 = pickle.load(open("vectorizer(TrueFalseFalse).pickle", "rb"))
    vectorizer5 = pickle.load(open("vectorizer(FalseTrueTrue).pickle", "rb"))
    vectorizer6 = pickle.load(open("vectorizer(FalseFalseTrue).pickle", "rb"))
    vectorizer7 = pickle.load(open("vectorizer(FalseTrueFalse).pickle", "rb"))
    vectorizer8 = pickle.load(open("vectorizer(FalseFalseFalse).pickle", "rb"))

    f = open("similarity_results3.txt", "w+")
    size = len(wirelessjobs)
    for i in range(size):
        f.write("===============================================================\n")
        job = wirelessjobs[i]
        f.write(str(job.jid) + " " + job.name + "\n")
        err1 += calcError(vectorizer1, alljobs, len(wirelessjobs), querydict, f, withoutStopWords=True, onlyNouns=True,
                          withFields=True, popindex=i, empCheck=empCheck)
        err2 += calcError(vectorizer2, alljobs, len(wirelessjobs), querydict, f, withoutStopWords=True, onlyNouns=True,
                          withFields=False, popindex=i, empCheck=empCheck)
        err3 += calcError(vectorizer3, alljobs, len(wirelessjobs), querydict, f, withoutStopWords=True, onlyNouns=False,
                          withFields=True, popindex=i, empCheck=empCheck)
        err4 += calcError(vectorizer4, alljobs, len(wirelessjobs), querydict, f, withoutStopWords=True, onlyNouns=False,
                          withFields=False, popindex=i, empCheck=empCheck)
        err5 += calcError(vectorizer5, alljobs, len(wirelessjobs), querydict, f, withoutStopWords=False, onlyNouns=True,
                          withFields=True, popindex=i, empCheck=empCheck)
        err6 += calcError(vectorizer6, alljobs, len(wirelessjobs), querydict, f, withoutStopWords=False,
                          onlyNouns=False, withFields=True, popindex=i, empCheck=empCheck)
        err7 += calcError(vectorizer7, alljobs, len(wirelessjobs), querydict, f, withoutStopWords=False, onlyNouns=True,
                          withFields=False, popindex=i, empCheck=empCheck)
        err8 += calcError(vectorizer8, alljobs, len(wirelessjobs), querydict, f, withoutStopWords=False,
                          onlyNouns=False, withFields=False, popindex=i, empCheck=empCheck)
        f.write("===============================================================\n")
        print("here" + str(i))

    err1/=size
    err2/=size
    err3/=size
    err4/=size
    err5/=size
    err6/=size
    err7/=size
    err8/=size

    f.write("err1 average: "+str(err1)+"\n")
    f.write("err2 average: "+str(err2)+"\n")
    f.write("err3 average: "+str(err3)+"\n")
    f.write("err4 average: "+str(err4)+"\n")
    f.write("err5 average: "+str(err5)+"\n")
    f.write("err6 average: "+str(err6)+"\n")
    f.write("err7 average: "+str(err7)+"\n")
    f.write("err8 average: "+str(err8)+"\n")

    f.close()




#updateAllVectorizers()
#cosineSimTest()
#cosineSimTest2()
#cosineSimTest3()
#getQueryResults()
#calcSim(True,True)
#calcSim(False)





def calcSim(withoutStopWords=False,onlyNouns=False):


    vectorizer=pickle.load(open("TfIdfvectorizer.pickle", "rb"))


    liked=[43]   #wireless sensor
    #liked=[18]    #başarılı
    f = open("similarity_results.txt", "w+")

    print("here")
    allJobs=Jobs.objects.all()
    #allJobs=Jobs.objects.filter(jid__lte=50)
    print("got data")

    jj=[]
    for job in allJobs:
        if job.jid in liked:

            for job2 in allJobs:
                if job.name != job2.name and job.employer != job2.employer:
                    desc1=job.jobdescription
                    desc2=job2.jobdescription

                    j1fields=json.loads((job.fields))
                    j2fields=json.loads((job.fields))
                    for field in j1fields:
                        desc1+=" "+field

                    for field in j2fields:
                        desc2+=" "+field

                    #val=calculateCosineSim(job.jobdescription,job2.jobdescription,vectorizer)
                    #val2=calculateCosineSim(job.jobdescription,job2.jobdescription,vectorizer,withoutStopWords=withoutStopWords)
                    #val3=calculateCosineSim(job.jobdescription,job2.jobdescription,vectorizer,onlyNouns=onlyNouns)
                    val4=calculateCosineSim(desc1,desc2,vectorizer,withoutStopWords=withoutStopWords,onlyNouns=onlyNouns)

                    dct={}
                    dct["job"]=job2
                    dct["val"]=val4[0][0]
                    jj.append(dct)
                    print("here")

                        #f.write(job.name+" //"+job2.name+" "+str(job2.jid)+" "+str(val4)+"\n")


            #f.write("\n\n\n")
            #if val>0.7 and job.name!=job2.name:
             #   print(job.name+" /////"+job2.name+"\n")
    newlist = sorted(jj, key=itemgetter('val'), reverse=True)
    for j in newlist:
        job2=j["job"]
        f.write(job2.name +" " + str(job2.jid) + " " + str(j["val"]) + "\n")

    f.close()
