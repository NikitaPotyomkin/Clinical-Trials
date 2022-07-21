import pandas as pd
df = pd.read_csv("Conditions.csv")
df.loc['Total']= df.sum(numeric_only=True, axis=0)
df.to_csv("Conditions1.csv")
sum_up = df.iloc[-1].to_csv('Conditions_sum_up.csv')



