import pandas as pd
import duckdb

def load_csv(uploaded_file):
    df = pd.read_csv(uploaded_file)
    return df

def load_to_duckdb(df):
    con = duckdb.connect(database='data.duckdb', read_only=False)
    con.execute("CREATE OR REPLACE TABLE data AS SELECT * FROM df")
    return con
