from ..parsers import parseUniversityPositions,parseTimesHigherEducation,parseAcademicPositions
from ..helpers import DBhelper
def searchJob(keyword,jobtypes,fields,locations,parseAllPages=True,recent=False):
    data1=parseAcademicPositions.searchJob(keyword,jobtypes,fields,locations, [], parseAllPages,recent=recent)
    data2=parseTimesHigherEducation.searchJob(keyword,jobtypes,fields,locations, [], parseAllPages,recent=recent)
    data3=parseUniversityPositions.search(keyword,jobtypes,fields,locations, [], parseAllPages,recent=recent)
    data1.extend(data2)
    data1.extend(data3)

    return data1