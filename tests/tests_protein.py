import needcoffee.protein as tf  # test folder
from needcoffee.protein import Protein  # test class

import pytest
import pandas as pd
import plotly.graph_objects as go


def test_get_lookup_dict():
    df_test = pd.read_csv("../data/amino_acid_properties.csv")
    lookup_dict = tf.get_lookup_dict(df_test)
    assert lookup_dict == {
        'Name': {'A': 'Alanine', 'R': 'Arginine', 'N': 'Asparagine', 'D': 'Aspartic acid', 'C': 'Cysteine',
                 'E': 'Glutamic acid', 'Q': 'Glutamine', 'G': 'Glycine', 'H': 'Histidine', 'I': 'Isoleucine',
                 'L': 'Leucine', 'K': 'Lysine', 'M': 'Methionine', 'F': 'Phenylalanine', 'P': 'Proline', 'S': 'Serine',
                 'T': 'Threonine', 'W': 'Tryptophan', 'Y': 'Tyrosine', 'V': 'Valine'},
        '3-letter code': {'A': 'Ala', 'R': 'Arg', 'N': 'Asn', 'D': 'Asp', 'C': 'Cys', 'E': 'Glu', 'Q': 'Gln',
                          'G': 'Gly', 'H': 'His', 'I': 'Ile', 'L': 'Leu', 'K': 'Lys', 'M': 'Met', 'F': 'Phe',
                          'P': 'Pro', 'S': 'Ser', 'T': 'Thr', 'W': 'Trp', 'Y': 'Tyr', 'V': 'Val'},
        '1-letter code': {'A': 'A', 'R': 'R', 'N': 'N', 'D': 'D', 'C': 'C', 'E': 'E', 'Q': 'Q', 'G': 'G', 'H': 'H',
                          'I': 'I', 'L': 'L', 'K': 'K', 'M': 'M', 'F': 'F', 'P': 'P', 'S': 'S', 'T': 'T', 'W': 'W',
                          'Y': 'Y', 'V': 'V'},
        'Molecular Weight': {'A': 89.1, 'R': 174.2, 'N': 132.12, 'D': 133.11, 'C': 121.16, 'E': 147.13, 'Q': 146.15,
                             'G': 75.07, 'H': 155.16, 'I': 131.18, 'L': 131.18, 'K': 146.19, 'M': 149.21, 'F': 165.19,
                             'P': 115.13, 'S': 105.09, 'T': 119.12, 'W': 204.23, 'Y': 181.19, 'V': 117.15},
        'Molecular Formula': {'A': 'C3H7NO2', 'R': 'C6H14N4O2', 'N': 'C4H8N2O3', 'D': 'C4H7NO4', 'C': 'C3H7NO2S',
                              'E': 'C5H9NO4', 'Q': 'C5H10N2O3', 'G': 'C2H5NO2', 'H': 'C6H9N3O2', 'I': 'C6H13NO2',
                              'L': 'C6H13NO2', 'K': 'C6H14N2O2', 'M': 'C5H11NO2S', 'F': 'C9H11NO2', 'P': 'C5H9NO2',
                              'S': 'C3H7NO3', 'T': 'C4H9NO3', 'W': 'C11H12N2O2', 'Y': 'C9H11NO3', 'V': 'C5H11NO2'},
        'Residue Formula': {'A': 'C3H5NO', 'R': 'C6H12N4O', 'N': 'C4H6N2O2', 'D': 'C4H5NO3', 'C': 'C3H5NOS',
                            'E': 'C5H7NO3', 'Q': 'C5H8N2O2', 'G': 'C2H3NO', 'H': 'C6H7N3O', 'I': 'C6H11NO',
                            'L': 'C6H11NO', 'K': 'C6H12N2O', 'M': 'C5H9NOS', 'F': 'C9H9NO', 'P': 'C5H7NO',
                            'S': 'C3H5NO2', 'T': 'C4H7NO2', 'W': 'C11H10N2O', 'Y': 'C9H9NO2', 'V': 'C5H9NO'},
        'Residue Weight': {'A': 71.08, 'R': 156.19, 'N': 114.11, 'D': 115.09, 'C': 103.15, 'E': 129.12, 'Q': 128.13,
                           'G': 57.05, 'H': 137.14, 'I': 113.16, 'L': 113.16, 'K': 128.18, 'M': 131.2, 'F': 147.18,
                           'P': 97.12, 'S': 87.08, 'T': 101.11, 'W': 186.22, 'Y': 163.18, 'V': 99.13},
        'pka1': {'A': 2.34, 'R': 2.17, 'N': 2.02, 'D': 1.88, 'C': 1.96, 'E': 2.19, 'Q': 2.17, 'G': 2.34, 'H': 1.82,
                 'I': 2.36, 'L': 2.36, 'K': 2.18, 'M': 2.28, 'F': 1.83, 'P': 1.99, 'S': 2.21, 'T': 2.09, 'W': 2.83,
                 'Y': 2.2, 'V': 2.32},
        'pka2': {'A': 9.69, 'R': 9.04, 'N': 8.8, 'D': 9.6, 'C': 10.28, 'E': 9.67, 'Q': 9.13, 'G': 9.6, 'H': 9.17,
                 'I': 9.6, 'L': 9.6, 'K': 8.95, 'M': 9.21, 'F': 9.13, 'P': 10.6, 'S': 9.15, 'T': 9.1, 'W': 9.39,
                 'Y': 9.11, 'V': 9.62},
        'pkaX': {'A': nan, 'R': 12.48, 'N': nan, 'D': 3.65, 'C': 8.18, 'E': 4.25, 'Q': nan, 'G': nan, 'H': 6.0,
                 'I': nan, 'L': nan, 'K': 10.53, 'M': nan, 'F': nan, 'P': nan, 'S': nan, 'T': nan, 'W': nan, 'Y': 10.07,
                 'V': nan},
        'pI': {'A': 6.0, 'R': 10.76, 'N': 5.41, 'D': 2.77, 'C': 5.07, 'E': 3.22, 'Q': 5.65, 'G': 5.97, 'H': 7.59,
               'I': 6.02, 'L': 5.98, 'K': 9.74, 'M': 5.74, 'F': 5.48, 'P': 6.3, 'S': 5.68, 'T': 5.6, 'W': 5.89,
               'Y': 5.66, 'V': 5.96},
        'hydropathy index (Kyte-Doolittle method)': {'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5, 'E': -3.5,
                                                     'Q': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5, 'L': 3.8, 'K': -3.9,
                                                     'M': 1.9, 'F': 2.8, 'P': -1.6, 'S': -0.8, 'T': -0.7, 'W': -0.9,
                                                     'Y': -1.3, 'V': 4.2},
        'Accessible surface': {'A': 44.1, 'R': 159.2, 'N': 80.8, 'D': 76.3, 'C': 56.4, 'E': 99.2, 'Q': 100.6, 'G': 0.0,
                               'H': 98.2, 'I': 90.9, 'L': 92.8, 'K': 139.1, 'M': 95.3, 'F': 107.4, 'P': 79.5, 'S': 57.5,
                               'T': 73.4, 'W': 143.4, 'Y': 119.1, 'V': 73.0}}


def test_get_data():
    protein_test = Protein('P32249', tf.get_lookup_dict(pd.read_csv("../data/amino_acid_properties.csv")))
    sq = protein_test.get_data()
    assert sq == 'MDIQMANNFTPPSATPQGNDCDLYAHHSTARIVMPLHYSLVFIIGLVGNLLALVVIVQNRKKINSTTLYSTNLVISDILFTTALPTRIAYYAMGFDWRIGDALCRITALVFYINTYAGVNFMTCLSIDRFIAVVHPLRYNKIKRIEHAKGVCIFVWILVFAQTLPLLINPMSKQEAERITCMEYPNFEETKSLPWILLGACFIGYVLPLIIILICYSQICCKLFRTAKQNPLTEKSGVNKKALNTIILIIVVFVLCFTPYHVAIIQHMIKKLRFSNFLECSQRHSFQISLHFTVCLMNFNCCMDPFIYFFACKGYKRKVMRMLKRQVSVSISSAVKSAPEENSREMTETQMMIHSKSSNGK'


def test_map():
    protein_test = Protein('P32249', tf.get_lookup_dict(pd.read_csv("../data/amino_acid_properties.csv")))
    prop_val_sq = protein_test.map('pka1')
    assert prop_val_sq == [2.28, 1.88, 2.36, 2.17, 2.28, 2.34, 2.02, 2.02, 1.83, 2.09, 1.99, 1.99, 2.21, 2.34, 2.09,
                           1.99, 2.17, 2.34, 2.02, 1.88, 1.96, 1.88, 2.36, 2.2, 2.34, 1.82, 1.82, 2.21, 2.09, 2.34,
                           2.17, 2.36, 2.32, 2.28, 1.99, 2.36, 1.82, 2.2, 2.21, 2.36, 2.32, 1.83, 2.36, 2.36, 2.34,
                           2.36, 2.32, 2.34, 2.02, 2.36, 2.36, 2.34, 2.36, 2.32, 2.32, 2.36, 2.32, 2.17, 2.02, 2.17,
                           2.18, 2.18, 2.36, 2.02, 2.21, 2.09, 2.09, 2.36, 2.2, 2.21, 2.09, 2.02, 2.36, 2.32, 2.36,
                           2.21, 1.88, 2.36, 2.36, 1.83, 2.09, 2.09, 2.34, 2.36, 1.99, 2.09, 2.17, 2.36, 2.34, 2.2, 2.2,
                           2.34, 2.28, 2.34, 1.83, 1.88, 2.83, 2.17, 2.36, 2.34, 1.88, 2.34, 2.36, 1.96, 2.17, 2.36,
                           2.09, 2.34, 2.36, 2.32, 1.83, 2.2, 2.36, 2.02, 2.09, 2.2, 2.34, 2.34, 2.32, 2.02, 1.83, 2.28,
                           2.09, 1.96, 2.36, 2.21, 2.36, 1.88, 2.17, 1.83, 2.36, 2.34, 2.32, 2.32, 1.82, 1.99, 2.36,
                           2.17, 2.2, 2.02, 2.18, 2.36, 2.18, 2.17, 2.36, 2.19, 1.82, 2.34, 2.18, 2.34, 2.32, 1.96,
                           2.36, 1.83, 2.32, 2.83, 2.36, 2.36, 2.32, 1.83, 2.34, 2.17, 2.09, 2.36, 1.99, 2.36, 2.36,
                           2.36, 2.02, 1.99, 2.28, 2.21, 2.18, 2.17, 2.19, 2.34, 2.19, 2.17, 2.36, 2.09, 1.96, 2.28,
                           2.19, 2.2, 1.99, 2.02, 1.83, 2.19, 2.19, 2.09, 2.18, 2.21, 2.36, 1.99, 2.83, 2.36, 2.36,
                           2.36, 2.34, 2.34, 1.96, 1.83, 2.36, 2.34, 2.2, 2.32, 2.36, 1.99, 2.36, 2.36, 2.36, 2.36,
                           2.36, 2.36, 1.96, 2.2, 2.21, 2.17, 2.36, 1.96, 1.96, 2.18, 2.36, 1.83, 2.17, 2.09, 2.34,
                           2.18, 2.17, 2.02, 1.99, 2.36, 2.09, 2.19, 2.18, 2.21, 2.34, 2.32, 2.02, 2.18, 2.18, 2.34,
                           2.36, 2.02, 2.09, 2.36, 2.36, 2.36, 2.36, 2.36, 2.32, 2.32, 1.83, 2.32, 2.36, 1.96, 1.83,
                           2.09, 1.99, 2.2, 1.82, 2.32, 2.34, 2.36, 2.36, 2.17, 1.82, 2.28, 2.36, 2.18, 2.18, 2.36,
                           2.17, 1.83, 2.21, 2.02, 1.83, 2.36, 2.19, 1.96, 2.21, 2.17, 2.17, 1.82, 2.21, 1.83, 2.17,
                           2.36, 2.21, 2.36, 1.82, 1.83, 2.09, 2.32, 1.96, 2.36, 2.28, 2.02, 1.83, 2.02, 1.96, 1.96,
                           2.28, 1.88, 1.99, 1.83, 2.36, 2.2, 1.83, 1.83, 2.34, 1.96, 2.18, 2.34, 2.2, 2.18, 2.17, 2.18,
                           2.32, 2.28, 2.17, 2.28, 2.36, 2.18, 2.17, 2.17, 2.32, 2.21, 2.32, 2.21, 2.36, 2.21, 2.21,
                           2.34, 2.32, 2.18, 2.21, 2.34, 1.99, 2.19, 2.19, 2.02, 2.21, 2.17, 2.19, 2.28, 2.09, 2.19,
                           2.09, 2.17, 2.28, 2.28, 2.36, 1.82, 2.21, 2.18, 2.21, 2.21, 2.02, 2.34, 2.18]


def test_map_sld_wdw():
    protein_test = Protein('P32249', tf.get_lookup_dict(pd.read_csv("../data/amino_acid_properties.csv")))
    avg_prop_val_sq = protein_test.map_sld_wdw('pka1', 10)
    assert avg_prop_val_sq == [2.127, 2.098, 2.1089999999999995, 2.094, 2.1109999999999998, 2.0919999999999996,
                               2.0569999999999995, 2.072, 2.1039999999999996, 2.123, 2.1019999999999994,
                               2.0989999999999998, 2.088, 2.1029999999999998, 2.0889999999999995, 2.114, 2.097, 2.062,
                               2.0490000000000004, 2.056, 2.102, 2.123, 2.1710000000000003, 2.1670000000000003,
                               2.1750000000000003, 2.1399999999999997, 2.194, 2.194, 2.193, 2.2049999999999996, 2.207,
                               2.222, 2.1689999999999996, 2.1729999999999996, 2.181, 2.216, 2.216, 2.2659999999999996,
                               2.2800000000000002, 2.2609999999999997, 2.2609999999999997, 2.2649999999999997, 2.316,
                               2.316, 2.312, 2.3099999999999996, 2.3099999999999996, 2.3099999999999996, 2.293, 2.293,
                               2.2739999999999996, 2.2559999999999993, 2.2399999999999998, 2.2399999999999998, 2.21,
                               2.199, 2.1719999999999997, 2.149, 2.1679999999999997, 2.1859999999999995, 2.19, 2.181,
                               2.165, 2.165, 2.195, 2.21, 2.222, 2.2009999999999996, 2.2009999999999996,
                               2.2169999999999996, 2.179, 2.1789999999999994, 2.186, 2.1839999999999997,
                               2.1879999999999997, 2.1509999999999994, 2.139, 2.168, 2.168, 2.166, 2.203,
                               2.2139999999999995, 2.239, 2.2329999999999997, 2.231, 2.215, 2.1939999999999995,
                               2.2600000000000002, 2.2410000000000005, 2.243, 2.257, 2.2249999999999996,
                               2.2249999999999996, 2.2329999999999997, 2.195, 2.229, 2.2769999999999997, 2.203,
                               2.2199999999999998, 2.2199999999999998, 2.218, 2.2129999999999996, 2.199, 2.199,
                               2.2049999999999996, 2.197, 2.181, 2.206, 2.206, 2.202, 2.1719999999999997,
                               2.1719999999999997, 2.1800000000000006, 2.1529999999999996, 2.147, 2.174, 2.175, 2.177,
                               2.131, 2.1159999999999997, 2.097, 2.1499999999999995, 2.1559999999999997, 2.179, 2.215,
                               2.161, 2.139, 2.139, 2.168, 2.171, 2.19, 2.1719999999999997, 2.174, 2.1599999999999997,
                               2.1449999999999996, 2.1989999999999994, 2.2190000000000003, 2.165, 2.182,
                               2.1799999999999997, 2.212, 2.226, 2.186, 2.2039999999999997, 2.1700000000000004,
                               2.1659999999999995, 2.2299999999999995, 2.284, 2.286, 2.3, 2.249, 2.2510000000000003,
                               2.272, 2.245, 2.298, 2.2649999999999997, 2.2179999999999995, 2.2179999999999995, 2.218,
                               2.1879999999999997, 2.2039999999999997, 2.1979999999999995, 2.202, 2.211,
                               2.1919999999999993, 2.212, 2.21, 2.193, 2.1740000000000004, 2.2079999999999997,
                               2.2179999999999995, 2.186, 2.193, 2.194, 2.197, 2.1769999999999996, 2.1449999999999996,
                               2.1089999999999995, 2.111, 2.0940000000000003, 2.0940000000000003, 2.116, 2.109,
                               2.1260000000000003, 2.1049999999999995, 2.189, 2.223, 2.276, 2.2929999999999997, 2.308,
                               2.3329999999999997, 2.311, 2.2729999999999997, 2.2729999999999997, 2.3079999999999994,
                               2.245, 2.241, 2.241, 2.2039999999999997, 2.206, 2.2079999999999997, 2.248,
                               2.3009999999999997, 2.3009999999999997, 2.303, 2.279, 2.267, 2.252, 2.2699999999999996,
                               2.2699999999999996, 2.2299999999999995, 2.1900000000000004, 2.1719999999999997,
                               2.1719999999999997, 2.1189999999999998, 2.1399999999999997, 2.1290000000000004, 2.142,
                               2.143, 2.124, 2.13, 2.133, 2.151, 2.1239999999999997, 2.16, 2.161, 2.173, 2.173, 2.187,
                               2.1719999999999997, 2.1879999999999997, 2.207, 2.2049999999999996, 2.232, 2.215, 2.206,
                               2.2209999999999996, 2.223, 2.227, 2.261, 2.2789999999999995, 2.2929999999999997, 2.291,
                               2.2379999999999995, 2.268, 2.2949999999999995, 2.255, 2.2020000000000004, 2.175,
                               2.1379999999999995, 2.122, 2.072, 2.072, 2.123, 2.127, 2.127, 2.1479999999999997, 2.147,
                               2.166, 2.203, 2.2009999999999996, 2.2369999999999997, 2.2409999999999997,
                               2.2239999999999993, 2.1709999999999994, 2.1559999999999997, 2.141, 2.1420000000000003,
                               2.15, 2.133, 2.111, 2.114, 2.095, 2.095, 2.0940000000000003, 2.0940000000000003, 2.075,
                               2.1090000000000004, 2.1090000000000004, 2.1109999999999998, 2.151, 2.112,
                               2.0780000000000003, 2.07, 2.12, 2.095, 2.148, 2.159, 2.125, 2.0869999999999997, 2.053,
                               2.0669999999999997, 2.08, 2.0989999999999998, 2.055, 2.058, 2.005, 2.013,
                               2.0309999999999997, 2.0309999999999997, 2.0119999999999996, 2.05, 2.05, 2.04, 2.086,
                               2.1069999999999998, 2.142, 2.1229999999999998, 2.121, 2.1700000000000004,
                               2.2150000000000003, 2.1979999999999995, 2.2300000000000004, 2.248, 2.232, 2.229, 2.228,
                               2.243, 2.246, 2.2459999999999996, 2.239, 2.258, 2.2510000000000003, 2.236,
                               2.2520000000000002, 2.2670000000000003, 2.268, 2.257, 2.27, 2.2369999999999997,
                               2.2350000000000003, 2.218, 2.199, 2.1990000000000003, 2.182, 2.169, 2.1790000000000003,
                               2.167, 2.152, 2.162, 2.16, 2.1689999999999996, 2.1950000000000003, 2.21, 2.175, 2.177,
                               2.167, 2.179, 2.181, 2.174, 2.191, 2.181, 1.953, 1.717, 1.535, 1.314, 1.0959999999999999,
                               0.875, 0.6539999999999999, 0.45199999999999996, 0.21800000000000003]


def test_plot():
    # without sliding window
    protein_test = Protein('P32249', tf.get_lookup_dict(pd.read_csv("../data/amino_acid_properties.csv")))
    fig = protein_test.plot('pka1')

    nb_sq_test = []
    for pos, aa in enumerate(protein_test.get_data()):
        nb_sq_test.append(str(pos))

    val_sq_test = protein_test.map('pka1')

    data_test = [
        go.Bar(
            x=nb_sq_test,
            y=val_sq_test
        )
    ]

    layout_test = {
        "title": {
            "text": 'pka1'
        },
        "xaxis": {
            "title": "sequence"
        },
        "yaxis": {
            "title": 'pka1'
        }
    }

    assert fig == go.Figure(data=data_test, layout=layout_test)


def test_plot_2():
    # with sliding window
    protein_test = Protein('P32249', tf.get_lookup_dict(pd.read_csv("../data/amino_acid_properties.csv")))
    fig = protein_test.plot('pka1', sld=True, wd=10)

    nb_sq_test = []
    for pos, aa in enumerate(protein_test.get_data()):
        nb_sq_test.append(str(pos))

    val_sq_test = protein_test.map_sld_wdw('pka1', 10)

    data_test = [
        go.Bar(
            x=nb_sq_test,
            y=val_sq_test
        )
    ]

    layout_test = {
        "title": {
            "text": 'pka1 using a sliding window of the width 10'
        },
        "xaxis": {
            "title": "sequence"
        },
        "yaxis": {
            "title": 'pka1'
        }
    }

    assert fig == go.Figure(data=data_test, layout=layout_test)

# pytest --cov-report html --cov=needcoffee tests/
