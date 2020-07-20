import pyodbc
from django.db import connection
from ..parsers import parseAcademicPositions
import re
import json

#jobs is a list of dictionaries
def saveJobsToDB(jobs):
    ids=[]
    for j in jobs:
        ids.append(saveJob(j))
    return ids

def saveJob(j):
    from ..models import Jobs
    dbjob=Jobs.objects.filter(id=j["id"],website=j["website"])
    if len(dbjob)>0:
        #print(dbjob[0].jid)
        return dbjob[0].jid
    else:
        toRemove = ["variant", "dateString", "Job types"]
        d = {}
        for i in j:
            if i not in toRemove:
                d[re.sub("\s", "_", i.lower())] = j[i]
            if i == "Fields":
                d["fields"] = json.dumps(j[i])

        job = Jobs(**d)
        job.save()
        return job.jid

def saveJobsFromUrlToDB(url,allJobs=False):

    jobs = parseAcademicPositions.parseUrl(url, allJobs)
    #print(len(jobs).__str__()+" jobs length")
    return saveJobsToDB(jobs)

def execSql(command,query=True):

    #print(cnxn)
    try:
        cursor = connection.cursor()
        table_names = [x[2] for x in cursor.tables(tableType='TABLE')]
        print(table_names)
        print(cursor.execute(command))
        #cursor.execute("select * from jobs")
        results=[]
        if query:
            row=cursor.fetchone()
            while row:
                results.append(row)
                #print(row)
                row=cursor.fetchone()
            return results
        else:
            return True
    except Exception as e:
        print(e.__str__())
        return False


def connect():
    cnxn = pyodbc.connect("""Driver={ODBC Driver 17 for SQL Server};Server=tcp:smartjobsserver.database.windows.net,1433;"
        "Database=SmartJobs;Uid={bera};Pwd={smartjobs123_};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"""
        )
    return cnxn

