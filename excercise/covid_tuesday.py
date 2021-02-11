import pandas as pd
import datetime
import ssl
import json
import urllib

import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default = "browser"

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
cdf['date_reported'] = pd.to_datetime(cdf['rep_date'], format='%d/%m/%Y', errors='raise')  # fix date format
# cdf['date_reported'].dt.day.head()

cdf["14d_incidence"] = pd.to_numeric(cdf["14d_incidence"])  # convert 14 day incidence into float64

# add new column for delta time --> delta time since start of recording
# find start of recording
# cdf.date_reported.idxmin()  # Out: Timestamp('2020-01-06 00:00:00')
strg_date = cdf.date_reported[cdf.date_reported.idxmin()]

cdf["delta_t"] = cdf.date_reported - strg_date

# spot shit and fix it
cdf.dropna(inplace=True)  # 10647 to 10408

# cdf = cdf[cdf.cases_weekly >= 0 and cdf.deaths_weekly >= 0 and cdf.pop_2019 >= 0 and cdf["14d_incidence"] >= 0]
cdf = cdf[cdf.cases_weekly >= 0]  # 10400
cdf = cdf[cdf.deaths_weekly >= 0]  # 10398
cdf = cdf[cdf.pop_2019 >= 0]
cdf = cdf[cdf["14d_incidence"] >= 0]  # 10395

# check for too new dates
# today = datetime.datetime.now()  # Out: datetime.datetime(2021, 2, 10, 14, 50, 45, 791778)
cut = pd.to_datetime(datetime.datetime.now())
print('today is the ' + str(cut))

# cdf.date_reported <= cut
cdf = cdf[cdf.date_reported < cut]  # 10395 --> no cuts because dates checked in correctly

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
# help_lst = []
#
# for continent, cont_continent in cdf.groupby('continent'):
#     for region, cont_region in cont_continent.groupby('region'):
#         d = cont_region.set_index('delta_t').sort_index()['14d_incidence'].diff().fillna(0)
#         min_d = min(d)  # decrease
#         max_d = max(d)  # increase
#         help_lst.append([continent, region, min_d, max_d])
#
# # transform into dataframe
# frame = pd.DataFrame(help_lst, columns=['continent', 'region', 'decrease', 'increase'])
#
# # find the max de- and increase
# help_lst_cont = []
#
# for continent, cont_continent in frame.groupby('continent'):
#     r_dec = frame.region.iloc[cont_continent.decrease.idxmin]
#     dec = min(cont_continent.decrease)
#     r_inc = frame.region.iloc[cont_continent.increase.idxmax]
#     inc = max(cont_continent.increase)
#     help_lst_cont.append([continent, r_dec, dec, r_inc, inc])
#
# fluctuation = pd.DataFrame(help_lst_cont,
#                            columns=['continent', 'highest decrease region', 'decrease',
#                                     'highest increase region', 'increase'])

# overall fluctuation
# o_a_dec = (fluctuation['highest decrease region'].iloc[fluctuation['decrease'].idxmin], min(fluctuation['decrease']))
# o_a_inc = (fluctuation['highest increase region'].iloc[fluctuation['increase'].idxmax], max(fluctuation['increase']))

# attempt considering year

help_lst = []

for continent, cont_continent in cdf.groupby('continent'):
    for region, cont_region in cont_continent.groupby('region'):
        for year, cont_year in cont_region.groupby('year'):
            d = cont_year.set_index('delta_t').sort_index()['14d_incidence'].diff().fillna(0)
            min_d = min(d)  # decrease
            max_d = max(d)  # increase
            help_lst.append([continent, year, region, min_d, max_d])

# transform into dataframe
frame_by_year = pd.DataFrame(help_lst, columns=['continent', 'year', 'region', 'decrease', 'increase'])

# find the max de- and increase
help_lst_cont = []

for year, cont_year in frame_by_year.groupby('year'):
    r_dec = frame_by_year.region.iloc[cont_year.decrease.idxmin]
    dec = min(cont_year.decrease)
    r_inc = frame_by_year.region.iloc[cont_year.increase.idxmax]
    inc = max(cont_year.increase)
    help_lst_cont.append([year, r_dec, dec, r_inc, inc])

fluctuation_by_year = pd.DataFrame(help_lst_cont,
                                   columns=['year', 'highest decrease region', 'decrease',
                                            'highest increase region', 'increase'])

# print('The region with the overall lowest flucuation of the 14 days incidence was ' + str(o_a_dec[0]) +
#       ' with a decrease of ' + str(o_a_dec[1]))
# print('The region with the overall highest flucuation of the 14 days incidence was ' + str(o_a_inc[0]) +
#       ' with an increase of ' + str(round(o_a_inc[1], 2)))

# plot incidence of european countries
continent = 'Europe'
continent_grp = cdf.groupby('continent').get_group(continent)

# create figure and add trace for each country
fig = go.Figure()

for region, cont_region in continent_grp.groupby('region'):
    fig.add_trace(go.Scatter(
        x=cont_region.set_index('delta_t').sort_index()['date_reported'],
        y=cont_region.set_index('delta_t').sort_index()['14d_incidence'],
        mode='lines',
        name=region
    ))

fig.update_layout({
    "title": {
        "text": '14 day incidence in ' + str(continent)
    },
    "xaxis": {
        "title": 'Time'
    },
    "yaxis": {
        "title": '14 day incidence'
    }
})

# fig.show()  # done --> yay

# smoothed version of the plot avg 3 months
