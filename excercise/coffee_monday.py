import pandas as pd
import numpy as np
import plotly
import plotly.graph_objects as go

df = pd.read_csv("../data/arabica_data_cleaned.csv", index_col=0)

# unnamed zero column where from? because csv file numbered
# index_col = 0 --> first column used as index

# pd.set_option("max_columns", 100)
# print(df.head())

# drop some categorical columns
# print(df.info())

# selecting the wanted columns
espresso = df[["Country.of.Origin", "Producer", "Processing.Method"]]

# reassigning well formated names
columns = ["country_of_origin", "producer", "processing_method"]
espresso.columns = columns

# plot
# for c in espresso.columns:
#     # print(espresso[c].value_counts())
#     counts = espresso[c].value_counts()
#
#     # print(counts.axes)
#     # print(counts.values)
#
#     # x_lst = counts.axes  # it could be so easy
#     # y_lst = counts.values
#
#     x_lst = espresso[c].dropna().unique()
#     y_lst = []
#     for i in x_lst:
#         y_lst.append(counts.loc[i])
#
#     print(x_lst)
#     print(y_lst)
#
#     data = [
#         go.Bar(
#             x=x_lst,
#             y=y_lst
#         )
#     ]
#
#     layout = {
#         "title": {
#             "text": f"Histogram of {c}"
#         },
#         "xaxis": {
#             "title": c.replace("_", " ")
#         },
#         "yaxis": {
#             "title": "count"
#         }
#     }
#
#     fig = go.Figure(data=data, layout=layout)
#     fig.show()
#     print("yay")
#     break

# print(espresso)

# identify
# more than 10 and less than 30 entries
# cnt_c = espresso["country_of_origin"].value_counts()
# low = None
# high = None
# for i in range(cnt_c.size):
#     if cnt_c.values[i] <= 30 and high is None:
#         high = i
#     elif cnt_c.values[i] < 10 and low is None:  # < 10 or 11, open for interpretation
#         low = i
# print(cnt_c[high:low])

# most entries producer
# count values are sorted in decreasing order, the first row (after title row) therefore holds the max
# prd_c = espresso["producer"].value_counts()
# print(prd_c[:1])

# most and least common processing method
pr_m_c = espresso["processing_method"].value_counts()
print(pr_m_c)
print(pr_m_c[:1])
print(pr_m_c[pr_m_c.size-1:pr_m_c.size])  # ugly but it works

