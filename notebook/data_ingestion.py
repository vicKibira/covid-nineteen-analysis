import pandas as pd
from sqlalchemy import create_engine
import os

# Change the working directory to the directory containing the script
#os.chdir(os.path.dirname(os.path.abspath(__file__)))

connection_url = "postgresql://root:root@172.21.0.2:5432/covidnineteen"
engine = create_engine(connection_url)
engine.connect()

# df = pd.read_csv('country_wise_latest.csv')

df_iter = pd.read_csv('country_wise_latest.csv', chunksize=100000, iterator=True)

df = next(df_iter)

df.to_sql(name='covid_datatable', con=engine, if_exists='replace')







