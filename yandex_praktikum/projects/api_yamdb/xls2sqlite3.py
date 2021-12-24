import sqlite3
import pandas as pd

filename = './data/YaMDb'

con = sqlite3.connect('db.sqlite3')

dfs = pd.read_excel('./data/YaMDb.xlsx', sheet_name=None)
for table, df in dfs.items():
    df.to_sql(table, con, index=False, if_exists='replace')
    
con.commit()
con.close()
