import streamlit as st
from load import load_csv, load_to_duckdb
import plotly.express as px

st.title("📊 Dashboard santé mentale des étudiants")

uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"])

if uploaded_file:
    st.write("✅ Fichier uploadé, lecture en cours...")

    df = load_csv(uploaded_file)

    st.subheader("Aperçu du CSV")
    st.write(df.head())

    # Vérifie les colonnes
    st.write("Colonnes du CSV (pour vérification) :", df.columns.tolist())

    # Créer la table dans DuckDB (nom : mental_health)
    con = load_to_duckdb(df)
    con.execute("CREATE OR REPLACE TABLE mental_health AS SELECT * FROM df")

    # KPI: Nombre total de lignes
    result = con.execute("SELECT COUNT(*) as nb_lignes FROM mental_health").fetchdf()

    lignes = result.loc[0, 'nb_lignes']  #int contenant le nombre total de lignes
    st.subheader("✅ Nombre de réponses dans le dataset : " + str(lignes))


    # KPI: répartition Yes/No pour la dépression
    query = """
        SELECT UPPER("Do you have Depression?") as depression, COUNT(*) as nb
        FROM mental_health
        GROUP BY UPPER("Do you have Depression?")
    """
    df_depression = con.execute(query).fetchdf() #crée un df df_depression avec deux colonnes 'depression' et 'nb', et deux lignes : yes et no


    total = df_depression['nb'].sum()     #retourne le nombre total
    df_depression['percentage'] = (df_depression['nb'] / total * 100).round(0)  # en % avec 0 décimales


    # Affichage du graphe
    st.subheader("📈 Répartition des réponses à la question 'Do you have Depression?'")
    fig = px.bar(
        df_depression,
        x='depression',
        y='percentage',
        color='depression',
        text=df_depression['percentage'].astype(str) + '%',  # texte affiché sur les barres
        labels={'depression': 'Réponse', 'nb': 'Nombre d\'étudiants'},
        title='Répartition des étudiants déclarant une dépression (Yes/No)'
    )
    st.plotly_chart(fig)


        # Nouveau KPI : répartition par genre parmi ceux en dépression
    df_dep_gender = con.execute("""
        SELECT "Choose your gender" as gender, COUNT(*) as nb
        FROM mental_health
        WHERE UPPER("Do you have Depression?") = 'YES'
        GROUP BY "Choose your gender"
    """).fetchdf()

    # calcul du pourcentage
    total_dep = df_dep_gender['nb'].sum()
    df_dep_gender['percentage'] = (df_dep_gender['nb'] / total_dep * 100).round(2)

    # affichage du camembert
    st.subheader("🥧 Répartition par genre parmi les étudiants déclarant une dépression")
    fig_pie = px.pie(
        df_dep_gender,
        names='gender',
        values='percentage',
        color='gender',
        title="Répartition par genre (en %)",
        hover_data=['nb']
    )
    fig_pie.update_traces(textinfo='percent+label')
    st.plotly_chart(fig_pie)


    con.close()

else:
    st.write("⏳ En attente d'un fichier CSV...")

