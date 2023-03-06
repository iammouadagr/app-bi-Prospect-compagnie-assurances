import pandas as pd
from sklearn.impute import SimpleImputer

# Charger le dataset
data = pd.read_csv("../data/base_prospect.csv",encoding="ISO-8859-1")

# Transformer les valeurs négatives en valeurs positives dans les colonnes ca_total_FL et ca_export_FK
data[['ca_total_FL', 'ca_export_FK']] = data[['ca_total_FL', 'ca_export_FK']].abs()

# Remplacer les valeurs de la colonne ca_export_FK qui excèdent les valeurs dans la colonnes ca_total_FL sur la même ligne par la valeur du ca_total_FL
data['ca_export_FK'] = data[['ca_total_FL', 'ca_export_FK']].min(axis=1)

# Remplacer les valeurs de la colonne risque qui sont sur la forme x-y par (x+y)/2
data['risque'] = data['risque'].apply(lambda x: (int(x.split('-')[0]) + int(x.split('-')[1]))/2 if isinstance(x, str) and '-' in x else x)

# Remplacer toutes les valeurs NA dans la colonne risque par la valeur médiane
imputer = SimpleImputer(strategy='median')
data['risque'] = imputer.fit_transform(data[['risque']])
data['risque'] = data['risque'].astype(int)

# Supprimer toutes les lignes dans la colonne ratio_benef qui ont des valeurs supérieures à 100
data = data[data['ratio_benef'] <= 100]

# Remplacer toutes les valeurs NA dans la colonne evo_risque par la valeur médiane
data['evo_risque'] = imputer.fit_transform(data[['evo_risque']])
data['evo_risque'] = data['evo_risque'].astype(int)

imputer = SimpleImputer(strategy='most_frequent')
data['chgt_dir'] = imputer.fit_transform(data[['chgt_dir']])
data['chgt_dir'] = data['chgt_dir'].astype(int)


# Exporter le nouveau dataset en format CSV
data.to_csv("../data/base_prospect_clean.csv", index=False)