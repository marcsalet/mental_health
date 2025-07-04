import streamlit as st
from load import load_csv, load_to_duckdb

st.title("📊 Dashboard minimal de test")

uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"])

if uploaded_file:
    st.write("✅ Fichier uploadé, lecture en cours...")
    
    df = load_csv(uploaded_file)
    
    st.subheader("Aperçu du CSV")
    st.write(df.head())  # Affiche même si dataframe est petit
    
    con = load_to_duckdb(df)
    
    result = con.execute("SELECT COUNT(*) as nb_lignes FROM sales").fetchdf()
    
    st.subheader("✅ Nombre de lignes chargées dans DuckDB")
    st.write(result)
    
    con.close()
else:
    st.write("⏳ En attente d'un fichier CSV...")
