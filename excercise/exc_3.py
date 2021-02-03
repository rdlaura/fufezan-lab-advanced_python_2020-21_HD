import csv
from collections import Counter
import plotly
import plotly.graph_objects as go
import pandas as pd


def get_sq(uniprot_data):
    sq = ""
    for help_line in uniprot_data:
        if not help_line.startswith(">"):
            sq += help_line.replace("\n", "")
    return sq


def get_mapping_dict(aap_data):
    mppg_dict = {}
    for i in aap_data.index:
        aap_data_scl = aap_data.iloc[i]
        key = aap_data_scl["1-letter code"]
        value = aap_data_scl["hydropathy index (Kyte-Doolittle method)"]
        mppg_dict[key] = value
    return mppg_dict


# print(get_mapping_dict(aap_df))


# def get_hpy_idx_lst(sq, mppg_dict):
#     hpy_idx = []
#     cnt_dict = Counter(sq)
#     aa_list = list(cnt_dict.keys())
#     # print(aa_list)
#
#     i = 0
#     while i < len(aa_list):
#         key = aa_list[i]
#         prd = mppg_dict[key] * cnt_dict[key]
#         hpy_idx = hpy_idx + [prd]
#         i += 1
#     return hpy_idx


def get_hpy_sq(sq, mppg_dict):
    i = 0
    hpy_sq = []
    while i < len(list(sq)):
        hpy_sq += [mppg_dict[sq[i]]]
        i += 1
    return hpy_sq

# todo later
# def get_aa_name(sq,aa_data):


# B
with open("../data/GP183_human.fasta") as gp:
    sq_gp183 = get_sq(gp)
aap_df = pd.read_csv("../data/amino_acid_properties.csv")
mppg_dict = get_mapping_dict(aap_df)
# print(get_hpy_idx_lst(sq_gp183, mppg_dict))

# print(get_hpy_sq(sq_gp183, mppg_dict))

# C
# enumerate every position --> create every aa as a single
nb_sq = []
for pos, aa in enumerate(sq_gp183):
    nb_sq.append(aa + str(pos))

data = [
    go.Bar(
        x=nb_sq,
        y=get_hpy_sq(sq_gp183, mppg_dict),
        hovertext=aap_df["Name"]
    )
]

layout = {
    "title": {
        "text": "Hydropathy Indeces"
    },
    "xaxis": {
        "title": "GP183 sequence"
    },
    "yaxis": {
        "title": "Hydropathy Index"
    }
}

fig = go.Figure(data=data, layout=layout)
fig.show()


# D
# def sldg_wdw (sq, mppg_dict, wd):
#     avg_hpy = []
#     for pos, aa in enumerate(sq):
#         help = 0
#         for i in sq[pos:pos+wd]:
#             help += mppg_dict[i]
#         avg_help = help/wd
#         avg_hpy += [avg_help]
#     return avg_hpy
#
#
# avg_data = [
#     go.Bar(
#         x=nb_sq,
#         y=sldg_wdw(sq_gp183, mppg_dict, 20),
#     )
# ]
#
# layout = {
#     "title": {
#         "text": "Averaged Hydropathy Indeces with Sliding Window Width 20"
#     },
#     "xaxis": {
#         "title": "GP183 sequence"
#     },
#     "yaxis": {
#         "title": "Hydropathy Index"
#     }
# }

fig = go.Figure(data=avg_data, layout=layout)
fig.show()
# fig.write_image("sldg_wd_5.pdf")

# if __name__ == "__main__":
