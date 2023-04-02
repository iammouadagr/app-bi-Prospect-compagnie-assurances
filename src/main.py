from clean_dataset import clean_supervised, clean_unsupervised
import subprocess

def clean_dataset():
    print("####  Préparation des données  ####")
    clean_supervised()
    clean_unsupervised()


if __name__ == "__main__" :
    print("------------------------------------")
    clean_dataset()
    print("------------------------------------")
    print("####  Classification non supervisée  ####")
    subprocess.run(["python", "unsupervise.py"])
    print("------------------------------------")
    print("####  Classification supervisée  ####")
    subprocess.run(["python", "supervised.py"])

