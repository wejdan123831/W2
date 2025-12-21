import pandas as pd 
#from pathlib import Path

df = pd.read_csv("C:\Users\w\Documents\my_csv_project\week2-data-work\data\row\users.csv"
                 
                 )
print(df)
dtype ={"user_id" : str}
                 #if we want change data type for one colume we pass the new data type as dict 