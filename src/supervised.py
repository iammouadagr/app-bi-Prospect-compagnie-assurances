import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Turn interactive plotting off
plt.ioff()

# read input text and put data inside a data frame
data = pd.read_csv("../data/base_prospect_suppervised.csv",encoding="ISO-8859-1")
# prospect =  pd.DataFrame(prospect)
data['risque'] = data['risque'].astype(object)
data['ca_total_FL'] = data['ca_total_FL'].astype(object)
data['effectif'] = data['effectif'].astype(object)

y = data['rdv']

from sklearn.preprocessing import OneHotEncoder
encoder = OneHotEncoder(handle_unknown="ignore")

feature_names  = data.columns.values[2:-1]
X = data[feature_names]
#La liste des caisses régionales
lst_caisse=data['code_cr'].unique()

X_cat = X.select_dtypes(exclude=['float64','int64'])

X_cat = pd.get_dummies(X_cat)
cat_columns = X_cat.columns


# X.dtypes
from sklearn.preprocessing import StandardScaler
# Normalize data
scaler = StandardScaler()
X_num = X.select_dtypes(include=['float64','int64']).drop(columns=['chgt_dir'])
num_columns = X_num.columns
X_num_norm = scaler.fit_transform(X_num)
# num_cat_columns = pd.concat([X_num_norm, X_cat], axis=1).columns
X_num_cat = pd.concat([pd.DataFrame(X_num_norm), X_cat], axis=1)
num_cat_columns = num_columns.tolist()
num_cat_columns.extend(cat_columns.tolist())

from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score, cross_validate

from sklearn.model_selection import cross_val_predict
from sklearn import metrics
from sklearn.model_selection import GridSearchCV

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

from sklearn.preprocessing import StandardScaler



# create an instance of the RandomForestClassifier class
rdforest = RandomForestClassifier(class_weight='balanced',random_state=42,max_depth=6,min_samples_leaf=2, min_samples_split=10, n_estimators=50) #min_samples_leaf=2, min_samples_split=10, n_estimators=50
# define a grid of hyperparameters to search over
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

lst_classif = [rdforest]
lst_classif_names = ['Random Forest']
class_names = list(map(str, data['rdv'].unique()))


def accuracy_score(X,y):
    for clf,name_clf in zip(lst_classif,lst_classif_names):
        # grid_search = GridSearchCV(clf, param_grid, cv=5, n_jobs=-1)
        # grid_search.fit(X, y)

        # # print the best hyperparameters and the corresponding validation score
        # print("Best Hyperparameters:", grid_search.best_params_)
        # print("Validation Score:", grid_search.best_score_)
        skf = StratifiedKFold(n_splits=5,shuffle=True)
        scores = cross_val_score(clf, X, y, cv=skf)
        pass


def confusion_matrix(X,y, datatype):
    for clf,name_clf in zip(lst_classif,lst_classif_names):
        predicted = cross_val_predict(clf, X, y, cv=5) 
        print("Accuracy of "+name_clf+" classifier on cross-validation: %0.2f" % metrics.accuracy_score(y, predicted))
        cm = metrics.confusion_matrix(y, predicted)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm,display_labels=class_names)
        disp.plot()
        plt.savefig('../fig/confusion_matrix_{}'.format(datatype))
        plt.close()
    pass


def important_features(X,columns,type_features):
    importances = rdforest.feature_importances_
    forest_importances = pd.Series(importances, index=columns)
    std = np.std([tree.feature_importances_ for tree in rdforest.estimators_], axis=0)
    fig, ax = plt.subplots()
    fig.set_size_inches(6,8)
    forest_importances.plot.bar(yerr=std, ax=ax)
    ax.set_title("Feature importances using MDI")
    ax.set_ylabel("Mean decrease in impurity")
    fig.tight_layout()
    plt.savefig('../fig/important_features_{}'.format(type_features))
    plt.close()

from sklearn import tree
# Plot decision tree for one of the trees in the forest
def plot_decision_tree(X,y,columns,type_tree):
    plt.figure(figsize=(20,10))
    tree.plot_tree(rdforest.estimators_[0], feature_names=columns, class_names=class_names, filled=True,fontsize=9)
    plt.subplots_adjust(hspace=3)
    plt.savefig('../fig/decision_tree_{}'.format(type_tree))
    plt.close()

    #Large plotting for interpretation
    plt.figure(figsize=(100,10))
    tree.plot_tree(rdforest.estimators_[0], feature_names=columns, class_names=class_names, filled=True,fontsize=11)
    plt.subplots_adjust(hspace=3)
    plt.savefig('../fig/decision_tree_{}_large'.format(type_tree))
    plt.close()


X_lists = [X_num_norm, X_cat.to_numpy(), X_num_cat.to_numpy()]
data_columns = [num_columns,cat_columns, num_cat_columns]
data_type_label = ["numerical","categorical", "categorical_numerical"]
zipped_data = list(zip(X_lists, data_columns, data_type_label))
for X_data, columns, label in zipped_data:
    rdforest.fit(X_data, y)
    accuracy_score(X_data, y)
    confusion_matrix(X_data, y,label)
    plot_decision_tree(X_data, y, columns , label)
    important_features(X_data,columns,label)