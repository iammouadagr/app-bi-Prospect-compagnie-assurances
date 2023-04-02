
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

# Turn interactive plotting off
plt.ioff()


# read input text and put data inside a data frame
def create_profile_graph(file,info):
    data = pd.read_csv("../data/{}.csv".format(file),encoding="ISO-8859-1")
    data.set_index('index', inplace=True)
    data = data.add_prefix("profile_")
    # data = data[(data < info["bounds"][0]).any(axis=1) | (data > info["bounds"][1]).any(axis=1)]
    ax=data.plot(kind='line', figsize=(15,8),  use_index=True)

    plt.title(info["title"])
    plt.xlabel(info["x_label"])
    plt.ylabel(info["y_label"])
    ax.set_xticks(range(len(data.index)))
    ax.set_xticklabels(data.index, rotation=90)
    plt.savefig('../fig/visualisation_{}'.format(file),bbox_inches='tight')


info_kmeans = {"title": "Caractéristiques des profils de classes avec Kmeans ", "x_label":"", "y_label": "Valeurs", "bounds":(-1,1)}
create_profile_graph("profile",info_kmeans)
info_kmeans_cah = {"title": "Caractéristiques des profils de classes avec (Kmeans+CAH)  ", "x_label":"", "y_label": "Valeurs", "bounds":(-5,5)}
create_profile_graph("profile_cah",info_kmeans_cah)



# read input text and put data inside a data frame
def create_profile_single_graph(file,info):
    data = pd.read_csv("../data/single/{}.csv".format(file),encoding="ISO-8859-1")
    data.set_index('index', inplace=True)
    data = data.add_prefix("profile_")
    print(data.head())
    print(list(data.columns))
    data = data.sort_values(by=list(data.columns))
    ax=data.plot(kind='line', figsize=(8,5),  use_index=True)

    plt.title(info["title"])
    plt.xlabel(info["x_label"])
    plt.ylabel(info["y_label"])
    

    ax.set_xticks(range(len(data.index)))
    ax.set_xticklabels(data.index, rotation=45)
    plt.savefig('fig/visualisation_{}'.format(file),bbox_inches='tight')
    plt.close()


# info = {"title": "", "x_label":"", "y_label": "", "bounds":(-1,1)}
# create_profile_single_graph("profile_0",info)