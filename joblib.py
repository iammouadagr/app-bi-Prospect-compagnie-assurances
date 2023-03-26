from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.externals import joblib  # import joblib pour sauvegarder le modèle

rdforest = RandomForestClassifier(class_weight='balanced',random_state=42,max_depth=15)

# Sélection des features numériques pour la normalisation
X_num = X.select_dtypes(include=['float64','int64']).drop(columns=['chgt_dir'])
x_columns = X_num.columns

# Normalisation des données
scaler = StandardScaler()
X_num_norm = scaler.fit_transform(X_num)

# Entraînement du modèle avec la validation croisée
predicted = cross_val_predict(rdforest, X_num_norm, y, cv=5)

# Sauvegarde du modèle entraîné
joblib.dump(rdforest, 'rdforest_model.joblib')

# Visualisation de l'arbre de décision
tree_model = joblib.load('rdforest_model.joblib')
tree.plot_tree(tree_model.estimators_[0], filled=True, feature_names=x_columns)  # utilisez le premier arbre dans le forest