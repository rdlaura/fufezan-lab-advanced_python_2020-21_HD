import pandas as pd
import datetime
import ssl
import json
import urllib

import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default = 'browser'


def get_open_covid_data(covid_url):
    ssl._create_default_https_context = ssl._create_unverified_context

    covid_json_unformated = urllib.request.urlopen(covid_url).read().decode('utf-8')
    covid_json = json.loads(covid_json_unformated)
    cdf = pd.DataFrame(covid_json['records'])

    cdf.rename(
        columns={
            'dateRep': 'rep_date',
            'countriesAndTerritories': 'region',
            'geoId': 'geo_id',
            'countryterritoryCode': 'region_code',
            'popData2019': 'pop_2019',
            'continentExp': 'continent',
            'Cumulative_number_for_14_days_of_COVID-19_cases_per_100000': '14d_incidence'
        },
        inplace=True
    )
    return cdf


def fix_types_and_format(df):
    df['date_reported'] = pd.to_datetime(df['rep_date'], format='%d/%m/%Y', errors='raise')  # fix date format
    # first: 31/12/2019 (min)
    # latest: 14/12/2020 (max)
    df['14d_incidence'] = pd.to_numeric(df['14d_incidence'])  # convert 14 day incidence into float64

    beginning = df.date_reported[df.date_reported.idxmin()]
    df['delta_t'] = df.date_reported - beginning
    return df


def clean_df(df):
    # clean na
    df.dropna(inplace=True)

    # clean neg values
    for i in ['deaths', 'cases', '14d_incidence']:
        clean = df[df[i] >= 0]

    return clean


def give_fluctuation(df):
    help_lst = []

    for continent, cont_continent in df.groupby('continent'):
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
    return fluctuation


def print_overall_fluctuation(fluctuation):
    # overall fluctuation
    o_a_dec = (
        fluctuation['highest decrease region'].iloc[fluctuation['decrease'].idxmin], min(fluctuation['decrease']))
    o_a_inc = (
        fluctuation['highest increase region'].iloc[fluctuation['increase'].idxmax], max(fluctuation['increase']))

    print('The region with the overall lowest fluctuation of the 14 days incidence was ' + str(o_a_dec[0]) +
          ' with a decrease of ' + str(o_a_dec[1]))
    print('The region with the overall highest fluctuation of the 14 days incidence was ' + str(o_a_inc[0]) +
          ' with an increase of ' + str(round(o_a_inc[1], 2)))
    return


def plot_continent_14d_ic(df, continent):
    continent = 'Europe'
    continent_grp = df.groupby('continent').get_group(continent)

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

    fig.show()
    return


# def plot_smoothed_continent_14d_ic(df, continent):
#     return


def radial_plot(df, country_lst):
    df['death_rate_per_100k'] = (df.deaths/df.pop_2019) * 100000
    df_sort = df.sort_values('date_reported')
    df['radial_time'] = df_sort.delta_t.dt.days

    fig = go.Figure()
    for i in country_lst:

        radial = []
        theta = []

        country_cont = df.groupby('region').get_group(i)
        for r in range(country_cont.shape[0]):
            radial.append(country_cont.iloc[r, 14])  # 'death_rate_per_100k'
            theta.append((country_cont.iloc[r, 15]/country_cont.shape[0])*360)  # 'radial_time'

        fig.add_trace(go.Scatterpolargl(
            r=radial,
            theta=theta,
            name=i,
            mode='markers'
        ))

    fig.update_layout(title={
        'text': 'death rate per 100,000'
    })
    fig.show()
    return


if __name__ == '__main__':
    # initiate and process data set
    covid_url = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/json/'
    cdf = get_open_covid_data(covid_url)
    cdf = fix_types_and_format(cdf)
    cdf = clean_df(cdf)

    # dataframe showing highest in- and decrease by continent
    fluctuation = give_fluctuation(cdf)

    # plots
    plot_continent_14d_ic(cdf, 'Europe')

    countries = ['Italy', 'Germany', 'Sweden', 'Greece']
    radial_plot(cdf, countries)
