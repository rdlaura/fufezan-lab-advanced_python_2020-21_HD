import csv
from collections import Counter
import plotly
import plotly.graph_objects as go

with open("../data/GP183_human.fasta") as gp:
    gp = csv.DictReader(gp, delimiter=",")
    for line in gp:
        print(line)
        break


def aa_count(fasta_data):
    sq = ""
    for help_line in fasta_data:
        if not help_line.startswith(">"):
            sq += help_line.replace("\n", "")
    return Counter(sq)


