import duckdb
import pandas as pd

db = duckdb.connect(database=':memory:')

db.execute("create table data as select * from read_csv_auto('data/students_mental_health.csv')")

data = db.execute("select * from data").fetchall()

df = pd.read_csv('data/students_mental_health.csv')


col = db.execute("PRAGMA table_info('data')").fetchdf()
print(col)

#test hello world tout ça  