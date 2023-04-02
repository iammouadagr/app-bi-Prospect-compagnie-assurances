import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

# Turn interactive plotting off
plt.ioff()


# read input text and put data inside a data frame
def create_result_grapth(file,info):
    data = pd.read_csv("../data/{}.csv".format(file),encoding="ISO-8859-1")
    data.set_index('label', inplace=True)
    # data = data[(data < info["bounds"][0]).any(axis=1) | (data > info["bounds"][1]).any(axis=1)]
    ax=data.plot(kind='bar', figsize=(15,8),  use_index=True)
    ax.set_ylim([0, 1])
    ax.grid(True, color='black', alpha=0.05)

    plt.title(info["title"])
    plt.xlabel(info["x_label"])
    plt.ylabel(info["y_label"])
    ax.set_xticks(range(len(data.index)))
    ax.set_xticklabels(data.index, rotation=90)
    plt.savefig('../fig/resultat_{}'.format(file),bbox_inches='tight')


def create_result_graph_suppervised(file,info):
    data = pd.read_csv("../data/{}.csv".format(file),encoding="ISO-8859-1")
    data.set_index('index', inplace=True)
    # data = data[(data < info["bounds"][0]).any(axis=1) | (data > info["bounds"][1]).any(axis=1)]
    ax=data.plot(kind='bar', figsize=(15,8),  use_index=True)
    ax.grid(True, color='black', alpha=0.05)

    plt.title(info["title"])
    plt.xlabel(info["x_label"])
    plt.ylabel(info["y_label"])
    ax.set_xticks(range(len(data.index)))
    ax.set_xticklabels(data.index, rotation=90)
    plt.savefig('../fig/resultat_{}'.format(file),bbox_inches='tight')

def make_result():
    info_kmeans = {"title": "Kmeans metrics", "x_label":"", "y_label": "Valeurs"}
    create_result_grapth("kmeans_score",info_kmeans)
    info_kmeans_cah = {"title": "Classification mixte (CAH+Kmeans) metrics", "x_label":"", "y_label": "Valeurs"}
    create_result_grapth("kmeans_cah_score",info_kmeans_cah)
    create_result_graph_suppervised("rdforest_categorical_numerical_report",info_kmeans_cah)


if __name__ == "__main__" :
    make_result()