import sys
import csv
import pandas
import itertools
from scipy import special
from collections import Counter
from itertools import combinations

def get_categories(categories_file):
    with open(categories_file, 'r') as f:
        reader = csv.reader(f)
        return [cat[0] for cat in reader]


def get_annotations(annotations_file):
    annotations = pandas.read_csv(annotations_file, header=None, index_col=0)
    I, U = annotations.shape
    return I, U, [list(annot.values()) for annot in annotations.to_dict(orient="records")]


def compute_sum_nip(S, U, item_annotations):
    nip = 0
    for pair in S:
        binary_pairs = [(1 if pair[0] in annot else 0, 1 if pair[1] in annot else 0) for annot in item_annotations]
        for user_pair in combinations(range(0, U), 2):
            if binary_pairs[user_pair[0]][0] == binary_pairs[user_pair[1]][0] and binary_pairs[user_pair[0]][1] == binary_pairs[user_pair[1]][1]:
                nip += 1
    return float(nip)


def compute_observed_agreement(S, U, I, annotations):
    Pi_list = [compute_sum_nip(S, U, annot) / (len(S) * special.comb(U, 2)) for annot in annotations]
    return float(sum(Pi_list)) / float(I)


def compute_P_pgu(I, given_pair, annot_by_users, G):
    list_P_pgu = []
    for user in annot_by_users:
        binary_pairs = [(1 if given_pair[0] in annot else 0, 1 if given_pair[1] in annot else 0) for annot in user]
        nb_bin_pairs = Counter([(sorted(bin_pair)[0], sorted(bin_pair)[1]) for bin_pair in binary_pairs])
        P_pgu = {}
        for g in G:
            try:
                P_pgu[g] = float(nb_bin_pairs[g]) / I
            except KeyError:
                P_pgu[g] = 0.0
        list_P_pgu.append(P_pgu)
    return list_P_pgu


def compute_expected_agreement(S, U, I, annotations):
    G = [(0, 0), (0, 1), (1, 1)]
    annot_by_users = [[annot[i] for annot in annotations] for i in range(0, U)]
    list_P_p = []
    for pair in S:
        list_P_pgu = compute_P_pgu(I, pair, annot_by_users, G)
        list_P_pg = []
        for g in G:
            P_pg = 0
            for user_pair in combinations(range(0, U), 2):
                P_pg += list_P_pgu[user_pair[0]][g] * list_P_pgu[user_pair[1]][g]
            P_pg /= special.comb(U, 2)
            list_P_pg.append(P_pg)
        list_P_p.append(sum(list_P_pg))
    return sum(list_P_p) / len(S)


def compute_agreement(S, U, I, annotations):
    Po = compute_observed_agreement(S, U, I, annotations)
    Pe = compute_expected_agreement(S, U, I, annotations)
    return Po, Pe, (Po - Pe) / (1.0 - Pe)


### MAIN PROGRAM
try:
    categories = get_categories(sys.argv[1])
    S = list(itertools.combinations(categories, 2))
    I, U, annotations = get_annotations(sys.argv[2])
    Po, Pe, Am = compute_agreement(S, U, I, annotations)
    print("Observed agreement (Po): {}".format(Po))
    print("Chance agreement (Pe): {}".format(Pe))
    print("Agreement measure (Am): {}".format(Am))
except IndexError:
    print("Message d'aide")
