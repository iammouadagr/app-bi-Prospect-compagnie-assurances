import pandas as pd
from sklearn.impute import SimpleImputer


def clean_unsupervised():

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

    # Remplace les valeurs inferieurs à 7 par 7 dans la colonne risque
    data.loc[data['risque'] < 7, 'risque'] = 7
    data.loc[(data['risque'] >= 7) & (data['risque'] <= 9), 'risque'] = 2
    data.loc[(data['risque'] >9) & (data['risque'] <= 12), 'risque'] = 1
    data.loc[(data['risque'] >12) & (data['risque'] <= 15), 'risque'] = 0

    # Forme 3 categories: Faible, moyen, eleve
    data['risque'] = data['risque'].astype(str)
    data.loc[data['risque'] == "0", 'risque'] = "faible"
    data.loc[data['risque'] == "1", 'risque'] = "moyen"
    data.loc[data['risque'] == "2", 'risque'] = "eleve"



    #Forme des categories d'entreprises suivant leurs chiffres d'affaire, on priorise le chiffre d'affaire sur l'effectif pour donner le chiffre d'affaire
    data.loc[data['ca_total_FL'] < 2000, 'effectif'] = 1
    data.loc[(data['ca_total_FL'] >= 2000) & (data['ca_total_FL'] <50000), 'effectif'] = 2
    data.loc[(data['ca_total_FL'] >=50000) & (data['ca_total_FL'] < 1500000), 'effectif'] = 3
    data.loc[(data['ca_total_FL'] >=1500000) , 'effectif'] = 4 


    data.loc[data['ca_total_FL'] < 2000, 'ca_total_FL'] = 1
    data.loc[(data['ca_total_FL'] >= 2000 ) & (data['ca_total_FL'] <50000), 'ca_total_FL'] = 2
    data.loc[(data['ca_total_FL'] >=50000) & (data['ca_total_FL'] < 1500000), 'ca_total_FL'] = 3
    data.loc[(data['ca_total_FL'] >=1500000) , 'ca_total_FL'] = 4


    data['ca_total_FL'] = data['ca_total_FL'].astype(str)
    data.loc[data['ca_total_FL'] == "1", 'ca_total_FL'] = "MIC"
    data.loc[data['ca_total_FL'] == "2", 'ca_total_FL'] = "PME"
    data.loc[data['ca_total_FL'] == "3", 'ca_total_FL'] = "ETI"
    data.loc[data['ca_total_FL'] == "4", 'ca_total_FL'] = "GE"


    data['effectif'] = data['effectif'].astype(str)
    data.loc[data['effectif'] == "1", 'effectif'] = "MIC"
    data.loc[data['effectif'] == "2", 'effectif'] = "PME"
    data.loc[data['effectif'] == "3", 'effectif'] = "ETI"
    data.loc[data['effectif'] == "4", 'effectif'] = "GE"

    # Supprimer toutes les lignes dans la colonne ratio_benef qui ont des valeurs supérieures à 100
    data = data[data['ratio_benef'] <= 100]

    # Remplacer toutes les valeurs NA dans la colonne evo_risque par la valeur médiane
    data['evo_risque'] = imputer.fit_transform(data[['evo_risque']])
    data['evo_risque'] = data['evo_risque'].astype(int)

    imputer = SimpleImputer(strategy='most_frequent')
    data['chgt_dir'] = imputer.fit_transform(data[['chgt_dir']])
    data['chgt_dir'] = data['chgt_dir'].astype(int)


    #Remplace les valeurs blancs par la mode
    imputer = SimpleImputer(strategy='most_frequent')
    data['type_com'] = imputer.fit_transform(data[['type_com']])
    data['type_com'] = data['type_com']


    # Exporter le nouveau dataset en format CSV
    data.to_csv("../data/base_prospect_unsuppervised.csv", index=False)



#type entreprise                effectif                CA
#microentreprises               <10                     < 2 000 000
#PME                            10 - 249               [ 2 000 000 - 50 000 000 ]
#ETI                            250 - 4999             [ 50 000 000 -  1 500 000 000 ] 
#GE                             5000 - plus            [ 1 500 000 000 - plus ] 
                  
def clean_suppervised():

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

    # Remplace les valeurs inferieurs à 7 par 7 dans la colonne risque
    data.loc[data['risque'] < 7, 'risque'] = 7
    data.loc[(data['risque'] >= 7) & (data['risque'] <= 9), 'risque'] = 2
    data.loc[(data['risque'] >9) & (data['risque'] <= 12), 'risque'] = 1
    data.loc[(data['risque'] >12) & (data['risque'] <= 15), 'risque'] = 0

    # Forme 3 categories: Faible, moyen, eleve
    data['risque'] = data['risque'].astype(str)
    data.loc[data['risque'] == "0", 'risque'] = "faible"
    data.loc[data['risque'] == "1", 'risque'] = "moyen"
    data.loc[data['risque'] == "2", 'risque'] = "eleve"



    #Forme des categories d'entreprises suivant leurs chiffres d'affaire, on priorise le chiffre d'affaire sur l'effectif pour donner le chiffre d'affaire
    data.loc[data['ca_total_FL'] < 2000, 'effectif'] = 1
    data.loc[(data['ca_total_FL'] >= 2000) & (data['ca_total_FL'] <50000), 'effectif'] = 2
    data.loc[(data['ca_total_FL'] >=50000) & (data['ca_total_FL'] < 1500000), 'effectif'] = 3
    data.loc[(data['ca_total_FL'] >=1500000) , 'effectif'] = 4 


    data.loc[data['ca_total_FL'] < 2000, 'ca_total_FL'] = 1
    data.loc[(data['ca_total_FL'] >= 2000 ) & (data['ca_total_FL'] <50000), 'ca_total_FL'] = 2
    data.loc[(data['ca_total_FL'] >=50000) & (data['ca_total_FL'] < 1500000), 'ca_total_FL'] = 3
    data.loc[(data['ca_total_FL'] >=1500000) , 'ca_total_FL'] = 4


    data['ca_total_FL'] = data['ca_total_FL'].astype(str)
    data.loc[data['ca_total_FL'] == "1", 'ca_total_FL'] = "MIC"
    data.loc[data['ca_total_FL'] == "2", 'ca_total_FL'] = "PME"
    data.loc[data['ca_total_FL'] == "3", 'ca_total_FL'] = "ETI"
    data.loc[data['ca_total_FL'] == "4", 'ca_total_FL'] = "GE"


    data['effectif'] = data['effectif'].astype(str)
    data.loc[data['effectif'] == "1", 'effectif'] = "MIC"
    data.loc[data['effectif'] == "2", 'effectif'] = "PME"
    data.loc[data['effectif'] == "3", 'effectif'] = "ETI"
    data.loc[data['effectif'] == "4", 'effectif'] = "GE"

    # Supprimer toutes les lignes dans la colonne ratio_benef qui ont des valeurs supérieures à 100
    data = data[data['ratio_benef'] <= 100]

    # Remplacer toutes les valeurs NA dans la colonne evo_risque par la valeur médiane
    data['evo_risque'] = imputer.fit_transform(data[['evo_risque']])
    data['evo_risque'] = data['evo_risque'].astype(int)

    imputer = SimpleImputer(strategy='most_frequent')
    data['chgt_dir'] = imputer.fit_transform(data[['chgt_dir']])
    data['chgt_dir'] = data['chgt_dir'].astype(int)


    #Remplace les valeurs blancs par la mode
    imputer = SimpleImputer(strategy='most_frequent')
    data['type_com'] = imputer.fit_transform(data[['type_com']])
    data['type_com'] = data['type_com']


    # Exporter le nouveau dataset en format CSV
    data.to_csv("../data/base_prospect_suppervised.csv", index=False)

clean_suppervised()
clean_unsupervised()