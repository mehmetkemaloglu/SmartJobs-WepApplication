from .helperConstants import countries


country_continent={
    "Europe":["France","Belgium","Germany","Switzerland","United Kingdom","Finland","Luxembourg","Netherlands","Sweden","Austria","Norway","Italy","Denmark"
              ,"Ireland","Portugal","Spain","Slovakia","Russia","Estonia","Slovenia"],
    "Asia":["Saudi Arabia","China","Oman","Qatar","Kuwait","Iraq","Vietnam","Hong Kong","South Korea","Singapore","Taiwan","Japan","Lebanon","Turkey","United Arab Emirates"],
    "North America":["United States","Canada"],
    "Africa":["Botswana","Ghana"],
    "Oceania":[],
    "South America":[]

}


def getContinent(country):
    for dict in countries:
        if dict["name"]==country:
            return dict["continent"]
    return ""