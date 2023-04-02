import pandas as pd

# Création du dictionnaire avec les données
data = {'nom': ['Alice', 'Bob', 'Charlie', 'David'],
        'age': [25, 30, 35, 40],
        'ville': ['Paris', 'Londres', 'New York', 'Tokyo']}

# Création du DataFrame
df = pd.DataFrame(data)

# Affichage du DataFrame
print(df)