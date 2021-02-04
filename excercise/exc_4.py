import csv
from collections import Counter
import plotly
import plotly.graph_objects as go
import pandas as pd
import itertools
import requests


def get_lookup_dict(aap_data):
    """
    build dict out of aminoacid properties dataframe
    :param aap_data:
    :return: lookup_dict: holdes mapping dicts for diff properties
    """
    lookup_dict = {}
    for i in aap_data.columns:
        # define dict in dict for each property
        lookup_dict[i] = {}
        for j in aap_data.index:
            key = aap_data.iloc[j]["1-letter code"]
            value = aap_data.iloc[j][str(i)]
            lookup_dict[i][key] = value
    return lookup_dict


class protein(object):
    # todo: documentation

    def __init__(self, protein_id, lookup_dict):
        self.protein_id = protein_id
        self.lookup_dict = lookup_dict
        self.sq = self.get_data()

    def get_data(self):
        """
        [A] pulls sq form uniprot given an id
        name inspired by paul for prettyness
        :param protein_id: identifying code used by uniprot to assign a specific pos to the protein that is being looked up
        :return: said proteins sq
        """

        url = "https://www.uniprot.org/uniprot/" + self.protein_id + ".fasta?fil=reviewed:yes"
        # not entirely sure why
        r = requests.get(url)

        # maybe integrate protein name later
        protein_file = "../data/" + self.protein_id + ".fasta"

        # Paul

        # with open(protein_file, "wb") as file:
        #     file.write(r.content)
        #     file.close()  # ?? doesnt with close the file anyways

        # with open(protein_file) as file:
        #     sq = []
        #     file_dict = csv.reader(file, delimiter="\n")
        #     for line in file_dict:
        #         if ">" not in line[0]:
        #             sq = sq + line[0]
        #         else:
        #             # seq_list.append(seq)
        #             sq = ""

        # recycle from exc_3
        with open(protein_file) as file:
            sq = ""
            for help_line in file:
                if not help_line.startswith(">"):
                    sq += help_line.replace("\n", "")

        self.sq = sq
        return str(self.sq)

    def map(self, prop):
        """
        [B] builds a list of values using the sq and mapping dict to link sq and values
        # :param lookup_dict: dictionary mapping aa in 1 letter code to value for each property
        :param prop: property to be analysed
        :return: prop_val_sq: property value sq
        """
        prop_val_sq = []
        for i in range(len(list(self.sq))):
            prop_val_sq += [self.lookup_dict[prop][self.sq[i]]]
        return prop_val_sq

    def map_sld_wdw(self, prop, wd):
        """
        [D] builds list of property values following sq using a sliding window
        # :param lookup_dict: dictionary mapping aa in 1 letter code to value for each property
        :param prop: property to be analysed
        :param wd: width of analysing window
        :return:
        """
        avg_prop_val_sq = []
        for pos, aa in enumerate(list(self.sq)):
            help = 0
            for i in self.sq[pos:pos + wd]:
                help += self.lookup_dict[prop][i]
            avg_help = help / wd
            avg_prop_val_sq += [avg_help]
        return avg_prop_val_sq

    # [C] plot
    def plot(self, prop, sld=False, wd=None):
        nb_sq = []
        # val_sq = []

        # print(self.sq)
        # print(type(self.sq))

        for pos, aa in enumerate(self.sq):
            nb_sq.append(str(pos))
            # nb_sq.append(aa + str(pos))

        if not sld:
            val_sq = self.map(prop)
            info = None
        if sld:
            val_sq = self.map_sld_wdw(prop, wd)
            info = " using a sliding window of the width " + str(wd)

        data = [
            go.Bar(
                x=nb_sq,
                y=val_sq
            )
        ]

        layout = {
            "title": {
                "text": str(prop) + info
            },
            "xaxis": {
                "title": "sequence"
            },
            "yaxis": {
                "title": str(prop)
            }
        }

        fig = go.Figure(data=data, layout=layout)
        fig.show()


if __name__ == "__main__":
    lookup_dict = get_lookup_dict(pd.read_csv("../data/amino_acid_properties.csv"))
    # print(lookup_dict)

    # [E] P32249
    gpcr183 = protein("P32249", lookup_dict)
    # print(type(gpcr183.get_data()))  # str

    gpcr183.plot("hydropathy index (Kyte-Doolittle method)", sld=True, wd=10)
    print("HUURRA")
