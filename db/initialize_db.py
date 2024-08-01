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
        CREATE TABLE IF NOT EXISTS company_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            category TEXT NOT NULL,
            sub_category TEXT NOT NULL,
            amount TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')

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
        INSERT INTO company_data (company_name, category, sub_category, amount, date)
        VALUES 
        ('MICHELIN', 'Recette exploitation', 'exploitation', '100', '20230101'),
        ('ENGIE', 'Achat de marchandise', 'marchandise', '200', '20230201'),
        ('CAPGEMINI', 'Conseils', 'Service numerique', '300', '20230201')
    ''')
    
    conn.commit()
    conn.close()
    print("SQLite database initialized with sample data.")

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
