import pandas as pd
df = pd.read_csv(r"scraped_otodom.csv")
pd.set_option("display.max_columns", None)
# dealing with data types and missing values (convert to numeric values if possible and drops rows if it's not possible)
df['Czynsz'] = df['Czynsz'].replace('Zapytaj', 0)
df['Czynsz'] = df['Czynsz'].str.replace(' ', '').str.replace(',', '.')
try:
    df['Czynsz'] = df['Czynsz'].astype(float)
except ValueError:
    mask = pd.to_numeric(df['Czynsz'], errors='coerce').isna()
    df = df.drop(df[mask].index)
df['Price'] = pd.to_numeric(df['Price'].str.replace(',', '.').str.replace(' ', ''), errors='coerce')
df.dropna(subset=['Price'], inplace=True)
df['Rooms'] = pd.to_numeric(df['Rooms'], errors='coerce', downcast='integer')
df.dropna(subset=['Rooms'], inplace=True)
df['Area'] = df['Area'].str.replace(',', '.').astype(float)
# check of missing values
missing_values = df.isna().sum()
# create a new columns
df['Czynsz'] = df['Czynsz'].astype(float)
df['Full_price'] = df['Price'] + df['Czynsz']
# leave rows, where districts are actual Warsaw's districts
list_of_actual_districts = ["Bemowo", "Białołęka", "Bielany", "Mokotów", "Ochota", "Praga-Południe", "Praga-Północ", "Rembertów", "Śródmieście", "Targówek", "Ursus", "Ursynów", "Wawer", "Wesoła", "Wilanów", "Włochy", "Wola", "Żoliborz"]
index_to_drop = df[~df['District'].isin(list_of_actual_districts)].index
df.drop(index_to_drop, inplace=True)
# remove rows with 'building'= Zapytaj
df = df[df['Building'] != 'Zapytaj']
# remove unnecessary columns
df = df.drop(['Price','Czynsz','Name','Street'], axis=1)
df.to_csv('clean_otodom.csv', index=False)
