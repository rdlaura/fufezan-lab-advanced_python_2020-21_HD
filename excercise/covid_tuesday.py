import pandas as pd
import datetime
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

# rename columns
print(cdf.info())
cdf.rename(
    columns={
        "dateRep": "rep_date",
        "countriesAndTerritories": "region",
        "geoId": "geo_id",
        "countryterritoryCode": "region_code",
        "popData2019": "pop_2019",
        "continentExp": "continent",
        "notification_rate_per_100000_population_14-days": "14d_incidence"
    },
    inplace=True
)

# get the types straight
cdf['date_reported'] = pd.to_datetime(cdf['rep_date'])
cdf['date_reported'].dt.day.head()

cdf["14d_incidence"] = pd.to_numeric(cdf["14d_incidence"])  # convert 14 day incidence into float64

# add new column for delta time --> delta time since start of recording
# find start of recording
# cdf.date_reported.idxmin()  # Out: Timestamp('2020-01-06 00:00:00')
strg_date = cdf.date_reported[cdf.date_reported.idxmin()]

cdf["delta_t"] = cdf.date_reported - strg_date

# spot shit and fix it
cdf.dropna(inplace=True)  # 10433 to 10195

# cdf = cdf[cdf.cases_weekly >= 0 and cdf.deaths_weekly >= 0 and cdf.pop_2019 >= 0 and cdf["14d_incidence"] >= 0]
cdf = cdf[cdf.cases_weekly >= 0]
cdf = cdf[cdf.deaths_weekly >= 0]
cdf = cdf[cdf.pop_2019 >= 0]
cdf = cdf[cdf["14d_incidence"] >= 0]

# drop cdf.cases_weekly --> 10187
# drop deaths_weekly --> 10185
# drop pop_2019 --> 10185
# drop 14d_incidence --> 10182
# summed up: dropped 251 rows


# firstly drop everything from 2021 --> 9119
# cdf = cdf[cdf.date_reported.dt.year <= 2020]

# check for dates
# today = datetime.datetime.now()  # Out: datetime.datetime(2021, 2, 10, 14, 50, 45, 791778)
# dates might be from 2020, 12, 14 --> using that as ref point
cut = pd.to_datetime('2020-12-14 00:00:00')

# cdf.date_reported <= cut --> False for 424 (after running year)
cdf = cdf[cdf.date_reported < cut]  # < because from day cut no more data was fed, idxmax afterwards --> 2020 12 10

# group
# grp_col = ['continent', 'region', 'date_reported', 'delta_t', '14d_incidence']
# grp = cdf[grp_col].groupby(['continent', 'region'])
#
# for continent, cont_continent in grp:
#     # print(continent)
#     for region, cont_region in cont_continent:
#         # print(region)
#         d = cont_region['14d_incidence'].diff().fillna(0)
#         min_d = min(d)  # decrease
#         max_d = max(d)  # increase

# a new attempt
# note all data from 2020, so in one year
help_lst = []

for continent, cont_continent in cdf.groupby('continent'):
    for region, cont_region in cont_continent.groupby('region'):
        d = cont_region.set_index('delta_t').sort_index()['14d_incidence'].diff().fillna(0)
        min_d = min(d)  # decrease
        max_d = max(d)  # increase
        help_lst.append([continent, region, min_d, max_d])

# transform into dataframe
frame = pd.DataFrame(help_lst, columns=['continent', 'region', 'decrease', 'increase'])

# find the max de- and increase
help_lst_cont = []

for continent, cont_continent in frame.groupby('continent'):
    r_dec = frame.region.iloc[cont_continent.decrease.idxmin]
    dec = min(cont_continent.decrease)
    r_inc = frame.region.iloc[cont_continent.increase.idxmax]
    inc = max(cont_continent.increase)
    help_lst_cont.append([continent, r_dec, dec, r_inc, inc])

fluctuation = pd.DataFrame(help_lst_cont,
                           columns=['continent', 'highest decrease region', 'decrease',
                                    'highest increase region', 'increase'])
