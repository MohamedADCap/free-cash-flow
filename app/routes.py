from flask import Blueprint, render_template, request, redirect, url_for, flash
import pandas as pd
import sqlite3

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/select-action', methods=['POST'])
def select_action():
    action = request.form['action']
    if action == 'params':
        return redirect(url_for('main.saisie_parametres_generaux'))
    elif action == 'mouvements':
        return redirect(url_for('main.saisie_mouvements'))
    elif action == 'simulate':
        return redirect(url_for('main.select_company_simulate'))

@main.route('/select-company-upload')
def select_company_upload():
    connection = sqlite3.connect('app.db')
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT company_name FROM company_data")
    companies = cursor.fetchall()
    cursor.close()
    connection.close()

    if not companies:
        flash("No companies found in the database.")
    else:
        company_names = [company[0] for company in companies]

    return render_template('select_company_upload.html', companies=company_names)

@main.route('/upload', methods=['POST'])
def upload_file():
    company_name = request.form['company_name']
    file = request.files['file']
    if file and company_name:
        try:
            df = pd.read_excel(file)
            conn = sqlite3.connect('app.db')
            cursor = conn.cursor()

            for index, row in df.iterrows():
                # Vérification de la nature et de la typologie des mouvements
                cursor.execute("""
                    SELECT 1 FROM parametrage_nature_mouvements
                    WHERE code_typ = ? AND code_nat = ?
                """, (row['code_typ'], row['code_nat']))
                if not cursor.fetchone():
                    flash(f"Invalid movement type or category at row {index + 1}")
                    return redirect(url_for('main.index'))
                
                # Vérification de l'entreprise
                if row['entreprise'] != company_name:
                    flash(f"Invalid company name at row {index + 1}")
                    return redirect(url_for('main.index'))

                # Vérification que le montant est une valeur numérique
                if not isinstance(row['montant'], (int, float)):
                    flash(f"Invalid amount at row {index + 1}")
                    return redirect(url_for('main.index'))

                # Insertion des données si tous les contrôles sont validés
                cursor.execute("""
                    INSERT INTO soldes_intermediaires_gestion (entreprise, date_mouvement, categorie_mouvement, nature_mouvement, libelle_mouvement, montant)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (row['entreprise'], row['date_mouvement'], row['categorie_mouvement'], row['nature_mouvement'], row['libelle_mouvement'], row['montant']))

            conn.commit()
            cursor.close()
            conn.close()
            flash('File successfully uploaded and data inserted')
        except Exception as ex:
            conn.rollback()
            flash(f'File upload failed: {ex}')
    else:
        flash('Please select a company and a file')
    return redirect(url_for('main.index'))

@main.route('/saisie-parametres-generaux', methods=['GET', 'POST'])
def saisie_parametres_generaux():
    if request.method == 'POST':
        id_entreprise = request.form['id_entreprise']
        nom_entreprise = request.form['nom_entreprise']
        devise = request.form['devise']
        langue = request.form['langue']
        annee_exercice = request.form['annee_exercice']
        mois_debut_simulation = request.form['mois_debut_simulation']

        try:
            conn = sqlite3.connect('app.db')
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO parametres_generaux (id_entreprise, nom_entreprise, devise, langue, annee_exercice, mois_debut_simulation)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (id_entreprise, nom_entreprise, devise, langue, annee_exercice, mois_debut_simulation))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Parameters successfully saved')
        except Exception as ex:
            conn.rollback()
            flash(f'Failed to save parameters: {ex}')
        return redirect(url_for('main.index'))
    
    return render_template('saisie_parametres_generaux.html')

@main.route('/saisie-mouvements', methods=['GET', 'POST'])
def saisie_mouvements():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            try:
                df = pd.read_excel(file)
                conn = sqlite3.connect('app.db')
                cursor = conn.cursor()

                for index, row in df.iterrows():
                    print(f"Processing row {index + 1}:")
                    print(f" - categorie_mouvement: {row['categorie_mouvement']}")
                    print(f" - nature_mouvement: {row['nature_mouvement']}")
                    # Vérification de la nature et de la typologie des mouvements
                    cursor.execute("""
                        SELECT 1 FROM parametrage_nature_mouvements
                        WHERE code_typ = ? AND code_nat = ?
                    """, (row['categorie_mouvement'], row['nature_mouvement']))
                    if not cursor.fetchone():
                        flash(f"Invalid movement category or nature at row {index + 1}")
                        return redirect(url_for('main.index'))


                    cursor.execute("""
                        INSERT INTO soldes_intermediaires_gestion (entreprise, date_mouvement, categorie_mouvement, nature_mouvement, libelle_mouvement, montant)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (row['entreprise'], row['date_mouvement'], row['categorie_mouvement'], row['nature_mouvement'], row['libelle_mouvement'], row['montant']))

                conn.commit()
                cursor.close()
                conn.close()
                flash('File successfully uploaded and data inserted', "success")
            except Exception as ex:
                flash(f'File upload failed: {ex}', "error")
        else:
            flash('Please upload a file', "error")
        return redirect(url_for('main.index'))

    return render_template('saisie_mouvements.html')

@main.route('/simulate', methods=['POST'])
def simulate():
    company_name = request.form['company_name']
    month = request.form['month']
    if company_name and month:
        flash(f'Simulation for {company_name} for month {month} triggered')
    else:
        flash('Please select a company and a month')
    return redirect(url_for('main.index'))
