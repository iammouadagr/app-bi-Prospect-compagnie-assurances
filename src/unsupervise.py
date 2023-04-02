import pandas as pd
import matplotlib.pyplot as plt
import clean_dataset
# Turn interactive plotting off
plt.ioff()

clean_dataset.clean_unsupervised()
# read input text and put data inside a data frame
data = pd.read_csv("../data/base_prospect_unsuppervised.csv",encoding="ISO-8859-1")
# prospect =  pd.DataFrame(prospect)
data['risque'] = data['risque'].astype(object)
data['ca_total_FL'] = data['ca_total_FL'].astype(object)
data['effectif'] = data['effectif'].astype(object)
from sklearn.preprocessing import OneHotEncoder
encoder = OneHotEncoder(handle_unknown="ignore")
feature_names  = data.columns.values[2:-1]
X = data[feature_names]
#La liste des caisses régionales
lst_caisse=data['code_cr'].unique()
X_cat = X.select_dtypes(exclude=['float64','int64'])
X_cat = pd.get_dummies(X_cat)
columns_cat = X_cat.columns
#Traitement des variable binaire et ordinale separement
# ordi_col = ["ca_total_FL"]

# X_ordinal = X[ordi_col]
# X_binaire = X.select_dtypes(exclude=['float64','int64']).drop(columns=ordi_col)

# encoder.fit(X_binaire)
# X_binaire = encoder.transform(X_binaire).toarray()

# X_cat = pd.concat([pd.DataFrame(X_binaire), X_ordinal], axis=1)
from sklearn.preprocessing import StandardScaler
# Normalize numeric data data
scaler = StandardScaler()
X_num = X.select_dtypes(include=['float64','int64']).drop(columns=['chgt_dir'])
x_columns = X_num.columns
X_num_norm = scaler.fit_transform(X_num)
X_num_norm = pd.DataFrame(X_num_norm, columns=x_columns)
#Concat numeric and categorical features
columns_num_cat = pd.concat([X_num_norm, X_cat], axis=1).columns
X_num_cat = pd.concat([pd.DataFrame(X_num_norm), X_cat], axis=1).to_numpy()

from sklearn.cluster import KMeans
matrice_corr = X.corr()
# Compute R-square, i.e. V_inter/V
from R_square_clustering import r_square
# Plot elbow graphs for KMeans using R square and purity scores
lst_k=range(2,20)
lst_rsq = []
lst_purity = []
for k in lst_k:
    est=KMeans(n_clusters=k)
    est.fit(X_num_cat)
    lst_rsq.append(r_square(X_num_cat, est.cluster_centers_,est.labels_,k))
    
fig = plt.figure()
plt.plot(lst_k, lst_rsq, 'bx-')
plt.xlabel('k')
plt.ylabel('RSQ')
plt.title('The Elbow Method showing the optimal k')
plt.savefig('../fig/k-means_elbow_method')
plt.close()

from time import time
from sklearn import metrics
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def bench_k_means(kmeans, name, data, labels):
    """Benchmark to evaluate the KMeans initialization methods.

    Parameters
    ----------
    kmeans : KMeans instance
        A :class:`~sklearn.cluster.KMeans` instance with the initialization
        already set.
    name : str
        Name given to the strategy. It will be used to show the results in a
        table.
    data : ndarray of shape (n_samples, n_features)
        The data to cluster.
    labels : ndarray of shape (n_samples,)
        The labels used to compute the clustering metrics which requires some
        supervision.
    """
    t0 = time()
    estimator = make_pipeline(StandardScaler(), kmeans).fit(data)
    fit_time = time() - t0
    results = [name, fit_time, estimator[-1].inertia_]

    # Define the metrics which require only the true labels and estimator
    # labels
    clustering_metrics = [
        metrics.homogeneity_score,
        metrics.completeness_score,
        metrics.v_measure_score,
        metrics.adjusted_rand_score,
        metrics.adjusted_mutual_info_score,
    ]
    results += [m(labels, estimator[-1].labels_) for m in clustering_metrics]

    # The silhouette score requires the full dataset
    results += [
        metrics.silhouette_score(
            data,
            estimator[-1].labels_,
            metric="euclidean",
            sample_size=300,
        )
    ]

    # Show the results
    formatter_result = (
        "{:9s}\t{:.3f}s\t{:.0f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}"
    )
    print(formatter_result.format(*results))
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

print(82 * "_")
print("init\t\ttime\tinertia\thomo\tcompl\tv-meas\tARI\tAMI\tsilhouette")
n_cluster = 5
kmeans = KMeans(init="k-means++", n_clusters=n_cluster, n_init=15, random_state=0)
labels = kmeans.fit(X_num_cat).labels_

bench_k_means(kmeans=kmeans, name="k-means++", data=X_num_cat, labels=labels)
k_centroids = kmeans.cluster_centers_
# print(kmeans.cluster_centers_)
for index, centroid in enumerate(k_centroids):
    profiles = pd.DataFrame([centroid], columns=columns_num_cat).transpose().reset_index()
    # Rename the index column to the original column name
    # print(centroid,index)
    profiles.to_csv("../data/profile_{}.csv".format(index), index=False)

profiles = pd.DataFrame(k_centroids, columns=columns_num_cat).transpose().reset_index()
col = ["{}".format(i) for i in range(n_cluster)]
profiles_col = ["index"]
profiles_col.extend(col)
profiles.columns=profiles_col
# Rename the index column to the original column name
profiles.to_csv("../data/profile.csv", index=False)



#Define a large number of cluster with kmeans  
n_clusters_mix = 60
kmeans_mixed = KMeans(init="k-means++", n_clusters=n_clusters_mix, n_init=20, random_state=0)
labels_mix = kmeans.fit(X_num_cat).labels_
bench_k_means(kmeans=kmeans_mixed, name="k-means++", data=X_num_cat, labels=labels)
#Get clusters centroid to use in a CAH.
k_centroids = kmeans_mixed.cluster_centers_

#hierarchical clustering dendogram to determinate the number of clusters to form
from scipy.cluster.hierarchy import dendrogram, linkage

lst_labels  = [i for i in range(0, n_clusters_mix)]
linkage_matrix = linkage(k_centroids, 'ward')

fig = plt.figure()
dendrogram(
    linkage_matrix,
    labels=lst_labels
)
plt.title('Hierarchical Clustering Dendrogram (Ward)')
plt.xlabel('sample index')
plt.ylabel('distance')
plt.tight_layout()
plt.savefig('../fig/hierarchical-clustering')
plt.close()
#Agglomerative clustering using centroid of kmeans clustering 
from sklearn.cluster import AgglomerativeClustering
#After analysing the created dendogram we choose 5 as the number of clusters
n_cluster_cah = 9
print("Compute unstructured hierarchical clustering...")
ward = AgglomerativeClustering(n_clusters=n_cluster_cah, linkage="ward").fit(k_centroids)
labels = ward.labels_
#Compute silhouettes score
silhouette_avg = metrics.silhouette_score(k_centroids, labels)
#Compute silhouettes score
davies_bouldin_score=metrics.davies_bouldin_score(k_centroids, labels)
# print("Les indices de silhouettes :", silhouettes)
print("L'indice de silhouette moyen est :", silhouette_avg)
print("L'indice de davies_bouldin_score moyen est :", davies_bouldin_score)


#Save the cluster's profil for further analysis
from scipy.cluster.hierarchy import ward, fcluster

classes =fcluster(linkage_matrix, t=n_cluster_cah, criterion='maxclust')
classes_indice = []
for i in range(1,n_cluster_cah+1):
    classes_indice.append(k_centroids[[j for j, val in enumerate(classes) if val == i]])
profil_cah = pd.DataFrame(classes_indice[0], columns=columns_num_cat).mean(axis=0)
arr = []
for i in range(0,n_cluster_cah):
    arr.append(pd.DataFrame(classes_indice[i]).mean(axis=0).values)
profile_cah = pd.DataFrame(arr,columns=list(columns_num_cat)).transpose().reset_index()
profile_cah.to_csv("../data/profile_cah.csv", index=False)

