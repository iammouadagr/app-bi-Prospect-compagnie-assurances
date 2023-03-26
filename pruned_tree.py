from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split

# Charger les données iris
iris = load_iris()
X = iris.data
y = iris.target

# Séparer les données en ensembles de formation et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

# Créer un arbre de décision
tree = DecisionTreeClassifier(random_state=0)

# Ajuster l'arbre de décision sur les données d'entraînement
tree.fit(X_train, y_train)

# Afficher l'arbre de décision avant pruning
plot_tree(tree)

# Faire des prédictions sur l'ensemble de test
y_pred = tree.predict(X_test)

# Calculer l'exactitude du modèle avant pruning
accuracy_before_pruning = accuracy_score(y_test, y_pred)
print('Accuracy before pruning:', accuracy_before_pruning)

# Déterminer la valeur optimale d'alpha à l'aide de la validation croisée
path = tree.cost_complexity_pruning_path(X_train, y_train)
ccp_alphas, impurities = path.ccp_alphas, path.impurities
cv_scores = []
for alpha in ccp_alphas:
    pruned_tree = DecisionTreeClassifier(random_state=0, ccp_alpha=alpha)
    scores = cross_val_score(pruned_tree, X_train, y_train, cv=5)
    cv_scores.append(scores.mean())

optimal_alpha = ccp_alphas[cv_scores.index(max(cv_scores))]

# Créer un nouvel arbre de décision avec la valeur optimale d'alpha et ajuster sur les données d'entraînement
pruned_tree = DecisionTreeClassifier(random_state=0, ccp_alpha=optimal_alpha)
pruned_tree.fit(X_train, y_train)

# Afficher l'arbre de décision après pruning
plot_tree(pruned_tree)

# Faire des prédictions sur l'ensemble de test
y_pred_pruned = pruned_tree.predict(X_test)

# Calculer l'exactitude du modèle après pruning
accuracy_after_pruning = accuracy_score(y_test, y_pred_pruned)
print('Accuracy after pruning:', accuracy_after_pruning)