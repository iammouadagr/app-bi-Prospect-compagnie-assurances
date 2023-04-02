
import subprocess

from clean_dataset import clean_supervised, clean_unsupervised
from profile_analysis import make_profile
from resultat_graph import make_result

def clean_dataset():
    print("####  Préparation des données  ####")
    clean_supervised()
    clean_unsupervised()


def result_interpretation():
    print("####  Interprétation des profiles  ####")
    make_profile()
    print("####  Interprétation des métrics  ####")
    make_result()

if __name__ == "__main__" :
    print("------------------------------------")
    clean_dataset()
    print("------------------------------------")
    print("####  Analyse descriptive  ####")
    subprocess.run(["python", "analyse_descriptive.py"])
    print("------------------------------------")
    print("####  Classification non supervisée  ####")
    subprocess.run(["python", "unsupervise.py"])
    subprocess.run(["python", "profile_analysis.py"])
    print("------------------------------------")
    print("####  Classification supervisée  ####")
    subprocess.run(["python", "supervised.py"])
    print("------------------------------------")
    make_result()
    print("------------------------------------")
    result_interpretation()