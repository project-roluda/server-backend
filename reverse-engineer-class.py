import pandas as pd 
from src.prediction import Patient

df = pd.read_csv("static/full_data.csv")
for i, row in df.iterrows():
    if df.loc[i].values[100] != "COPD":
        x = Patient()
        r1, r2 = x.post_data_to_azure(df.loc[i].values[:100])
        print(r1.content)
        print(r2.content)
        print()
