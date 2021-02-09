import pandas as pd
import ssl
import json
import urllib

# retrieve covid data from ecdc

covid_url = "https://opendata.ecdc.europa.eu/covid19/casedistribution/json/"

ssl._create_default_https_context = ssl._create_unverified_context

covid_json_unformated = urllib.request.urlopen(covid_url).read().decode("utf-8")
covid_json = json.loads(covid_json_unformated)
cdf = pd.DataFrame(covid_json['records'])

# print(cdf.sample(10))

