import os
import sqlite3
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def init_sqlite():
    """
    Initialize SQLite database by creating necessary tables if they don't exist.
    """
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parametrage_nature_mouvements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code_typ TEXT NOT NULL,
            categorie_mouvement TEXT NOT NULL,
            code_nat TEXT NOT NULL,
            nature_mouvement TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parametres_generaux (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_entreprise TEXT NOT NULL,
            nom_entreprise TEXT NOT NULL,
            devise TEXT NOT NULL,
            langue TEXT NOT NULL,
            annee_exercice TEXT NOT NULL,
            mois_debut_simulation TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS soldes_intermediaires_gestion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entreprise TEXT NOT NULL,
            date_mouvement TEXT NOT NULL,
            categorie_mouvement TEXT NOT NULL,
            nature_mouvement TEXT NOT NULL,
            libelle_mouvement TEXT NOT NULL,
            montant TEXT NOT NULL
        )
    ''')


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parametres_simulation (
        entreprise TEXT NOT NULL,
        version TEXT NOT NULL,
        mois_simulation_FRF TEXT NOT NULL,
        date_jour TEXT,
        formule_recettes_exploitation TEXT,
        formule_recettes_gestion TEXT,
        formule_achat_matieres TEXT,
        formule_autres_achats_charges_externes TEXT,
        formule_impots_taxes TEXT,
        formule_charges_salaires TEXT,
        formule_autre_charges TEXT,
        courbe_recettes_exploitation TEXT,
        courbe_recettes_gestion TEXT,
        courbe_achat_matieres TEXT,
        courbe_autres_achats_charges_externes TEXT,
        courbe_impots_taxes TEXT,
        courbe_charges_salaires TEXT,
        courbe_autre_charges TEXT,
        PRIMARY KEY (entreprise, version, mois_simulation_FRF)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courbes (
        entreprise TEXT NOT NULL,
        version TEXT NOT NULL,
        mois_simulation_FRF TEXT NOT NULL,
        date_jour TEXT,
        mois_prevision TEXT NOT NULL,
        taux_recettes_exploitation TEXT,
        taux_recettes_gestion TEXT,
        taux_achat_matieres TEXT,
        taux_autres_achats_charges_externes TEXT,
        taux_impots_taxes TEXT,
        taux_charges_salaires TEXT,
        taux_autre_charges TEXT,
        PRIMARY KEY (entreprise, version, mois_simulation_FRF, mois_prevision)
        )
    ''')

    conn.commit()
    conn.close()


    print("SQLite database initialized.")

def init_postgres():
    """
    Initialize PostgreSQL database by creating necessary tables if they don't exist.
    """
    conn = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT')
    )
    cursor = conn.cursor()
    
    # Read and execute SQL script for PostgreSQL
    with open('db/init_postgres.sql') as f:
        cursor.execute(f.read())
    
    conn.commit()
    cursor.close()
    conn.close()
    print("PostgreSQL database initialized.")

if __name__ == "__main__":
    # Determine the type of database to initialize based on the environment variable
    db_type = os.getenv('DB_TYPE', 'sqlite')
    
    if db_type == 'postgres':
        init_postgres()
    else:
        init_sqlite()
