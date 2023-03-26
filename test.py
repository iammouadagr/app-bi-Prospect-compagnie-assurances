import pandas as pd

# Créer un ensemble de données de démonstration
data = pd.DataFrame({'couleur': ['rouge', 'vert', 'bleu', 'rouge', 'bleu']})

# Utiliser la fonction get_dummies pour convertir la variable catégorielle "couleur"
# en variables binaires
data_dummies = pd.get_dummies(data, columns=['couleur'])

# Afficher l'ensemble de données transformé
print(data_dummies)



from sklearn.preprocessing import OneHotEncoder
encoder = OneHotEncoder(handle_unknown="ignore")



# Disjonction with OneHotEncoder
encoder.fit(data)
X_cat = encoder.transform(data).toarray()

print(X_cat)
