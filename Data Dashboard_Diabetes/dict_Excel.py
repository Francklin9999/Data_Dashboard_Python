import pandas as pd
import statsmodels.api as sm
import seaborn as sns

def main():
    con = pd.read_excel("Excel_Projet.xlsx")
    con.rename(columns={"Unnamed: 0" : "Pays"}, inplace=True)
    Y = con["Prévalence au diabète (%)"]
    x = con[
        ["PIB du pays (B$US)",
        "Âge médian (années)",
        "% d'bésité (IMC > 30)",
        "Nombre d'heures de travail/sem",
        "Rapport Homme/Femme",]
        ]
    X = sm.add_constant(x)
    ks = sm.OLS(Y, X)
    ks_res = ks.fit()
    p_value = ks_res.summary()
    print(p_value)

#Convertir Pays a Prevalence
def fPays_Prevalence(x):
    y = dict_Pays_Prevalence.get(x)
    return y

#Convertir Pays a PIB
def fPays_PIB(x):
    y = dict_Pays_PIB.get(x)
    return y

#Convertir Pays a Age
def fPays_Age(x):
    y = dict_Pays_Age.get(x)
    return y

#Convertir Pays a Obesite
def fPays_Obesite(x):
    y = dict_Pays_Obesite.get(x)
    return y

#Convertir Pays a Travail
def fPays_Travail(x):
    y = dict_Pays_Travail.get(x)
    return y

#Convertir Pays a Rapport
def fPays_Rapport(x):
    y = dict_Pays_Rapport.get(x)
    return y

#Donnée excel 
excel_file = "Excel_Projet.xlsx"
df = pd.read_excel(excel_file)
new_dict = df.to_dict()

#Pays
Pays = (new_dict["Pays"])
list_Pays = []
for i in range(len(Pays)):
    list_Pays.append(Pays[i])

#Prévalence au diabète (%)
Prevalence = (new_dict["Prévalence au diabète (%)"])
list_Prevalence = []
for i in range(len(Prevalence)):
    list_Prevalence.append(Prevalence[i]) 
#Dictionnaire Pays/Prevalence
list_Pays_Prevalence = []
for i in range(len(Pays)):
    list_Pays_Prevalence.append(f"{list_Pays[i]} : {list_Prevalence[i]}")
dict_Pays_Prevalence = {entry.split(' : ')[0]: entry.split(' : ')[1] for entry in list_Pays_Prevalence}

#PIB du pays (B$US)
PIB = (new_dict["PIB du pays (B$US)"])
list_PIB = []
for i in range(len(PIB)):
    list_PIB.append(PIB[i]) 
#Dictionnaire Pays/PIB
list_Pays_PIB = []
for i in range(len(Pays)):
    list_Pays_PIB.append(f"{list_Pays[i]} : {list_PIB[i]}")
dict_Pays_PIB = {entry.split(' : ')[0]: entry.split(' : ')[1] for entry in list_Pays_PIB}
  
#Âge médian (années)
Age = (new_dict["Âge médian (années)"])
list_Age = []
for i in range(len(Age)):
    list_Age.append(Age[i]) 
#Dictionnaire Pays/Age
list_Pays_Age = []
for i in range(len(Age)):
    list_Pays_Age.append(f"{list_Pays[i]} : {list_Age[i]}")
dict_Pays_Age = {entry.split(' : ')[0]: entry.split(' : ')[1] for entry in list_Pays_Age}

#% d'obésité (IMC > 30)
Obesite = (new_dict["% d'bésité (IMC > 30)"])
list_Obesite = []
for i in range(len(Obesite)):
    list_Obesite.append(Obesite[i]) 
#Dictionnaire Pays/Obesite
list_Pays_Obesite = []
for i in range(len(Pays)):
    list_Pays_Obesite.append(f"{list_Pays[i]} : {list_Obesite[i]}")
dict_Pays_Obesite = {entry.split(' : ')[0]: entry.split(' : ')[1] for entry in list_Pays_Obesite}

#Nombre d'heures de travail/sem
Travail = (new_dict["Nombre d'heures de travail/sem"])
list_Travail = []
for i in range(len(Travail)):
    list_Travail.append(Travail[i]) 
#Dictionnaire Pays/Travail
list_Pays_Travail = []
for i in range(len(Age)):
    list_Pays_Travail.append(f"{list_Pays[i]} : {list_Travail[i]}")
dict_Pays_Travail = {entry.split(' : ')[0]: entry.split(' : ')[1] for entry in list_Pays_Travail}

#Rapport Homme/Femme
Rapport = (new_dict["Rapport Homme/Femme"])
list_Rapport = []
for i in range(len(Rapport)):
    list_Rapport.append(Rapport[i]) 
#Dictionnaire Pays/Rapport
list_Pays_Rapport = []
for i in range(len(Pays)):
    list_Pays_Rapport.append(f"{list_Pays[i]} : {list_Rapport[i]}")
dict_Pays_Rapport = {entry.split(' : ')[0]: entry.split(' : ')[1] for entry in list_Pays_Rapport}


if __name__ == "__main__":
    main()








































