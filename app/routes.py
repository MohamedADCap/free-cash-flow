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
        return redirect(url_for('main.saisie_options_simulation'))

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


# Exemple de liste des composants pour le formulaire
COMPOSANTS = [
    "Recettes d’exploitation",
    "Recettes de Gestion",
    "Achat Matières",
    "Autres Achats & Charges Externes",
    "Impôts et Taxes",
    "Charges & Salaires",
    "Autre Charges"
]
import logging
# Configuration de base des logs
logging.basicConfig(level=logging.INFO)

@main.route('/saisie-options-simulation', methods=['GET', 'POST'])
def saisie_options_simulation():
    if request.method == 'POST':
        try:
            # Log des en-têtes et données de la requête
            logging.info(f"En-têtes de la requête : {request.headers}")
            logging.info(f"Données brutes de la requête : {request.data}")
            logging.info(f"Données du formulaire : {request.form}")
            logging.basicConfig(level=logging.DEBUG)

            entreprise = request.form['entreprise']
            version = request.form['version']
            mois_simulation_FRF = request.form['mois_simulation_FRF']
            date_jour = request.form['date_jour']  # Ajout de la récupération de la date_jour

            print(entreprise)
            print(version)
            # Log des valeurs principales
            logging.info(f"Entreprise: {entreprise}")
            logging.info(f"Version: {version}")
            logging.info(f"Mois de simulation: {mois_simulation_FRF}")
            logging.info(f"Date du jour: {date_jour}")  # Log de la date_jour
            logging.basicConfig(level=logging.DEBUG)

            # Préparer les valeurs pour chaque composant
            valeurs = {
                "formule_recettes_exploitation": request.form.get('formule_recettes_exploitation', ""),
                "formule_recettes_gestion": request.form.get('formule_recettes_gestion', ""),
                "formule_achat_matieres": request.form.get('formule_achat_matieres', ""),
                "formule_autres_achats_charges_externes": request.form.get('formule_autres_achats_charges_externes', ""),
                "formule_impots_taxes": request.form.get('formule_impots_taxes', ""),
                "formule_charges_salaires": request.form.get('formule_charges_salaires', ""),
                "formule_autre_charges": request.form.get('formule_autre_charges', ""),
                "courbe_recettes_exploitation": request.form.get('courbe_recettes_exploitation', ""),
                "courbe_recettes_gestion": request.form.get('courbe_recettes_gestion', ""),
                "courbe_achat_matieres": request.form.get('courbe_achat_matieres', ""),
                "courbe_autres_achats_charges_externes": request.form.get('courbe_autres_achats_charges_externes', ""),
                "courbe_impots_taxes": request.form.get('courbe_impots_taxes', ""),
                "courbe_charges_salaires": request.form.get('courbe_charges_salaires', ""),
                "courbe_autre_charges": request.form.get('courbe_autre_charges', "")
            }

            # Log des valeurs reçues pour vérification
            logging.info(f"Valeurs reçues : {valeurs}")
            print(valeurs)
            # Connexion à la base de données SQLite
            conn = sqlite3.connect('app.db')
            cursor = conn.cursor()

            # Insertion dans la table parametres_simulation
            cursor.execute('''
                INSERT INTO parametres_simulation (
                    entreprise, version, mois_simulation_FRF, date_jour,
                    formule_recettes_exploitation, formule_recettes_gestion, 
                    formule_achat_matieres, formule_autres_achats_charges_externes, 
                    formule_impots_taxes, formule_charges_salaires, 
                    formule_autre_charges, courbe_recettes_exploitation, 
                    courbe_recettes_gestion, courbe_achat_matieres, 
                    courbe_autres_achats_charges_externes, courbe_impots_taxes, 
                    courbe_charges_salaires, courbe_autre_charges
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                entreprise, version, mois_simulation_FRF, date_jour,  # Ajout de date_jour
                valeurs["formule_recettes_exploitation"], valeurs["formule_recettes_gestion"],
                valeurs["formule_achat_matieres"], valeurs["formule_autres_achats_charges_externes"],
                valeurs["formule_impots_taxes"], valeurs["formule_charges_salaires"],
                valeurs["formule_autre_charges"], valeurs["courbe_recettes_exploitation"],
                valeurs["courbe_recettes_gestion"], valeurs["courbe_achat_matieres"],
                valeurs["courbe_autres_achats_charges_externes"], valeurs["courbe_impots_taxes"],
                valeurs["courbe_charges_salaires"], valeurs["courbe_autre_charges"]
            ))

            # Sauvegarder les modifications et fermer la connexion
            conn.commit()
            conn.close()

            flash("Les options de simulation ont été enregistrées avec succès.", "success")
            return redirect(url_for('main.index'))

        except Exception as e:
            logging.error(f"Erreur lors du traitement de la requête: {str(e)}")
            flash(f"Une erreur est survenue lors de l'enregistrement des options de simulation: {str(e)}", "danger")

        return redirect(url_for('main.index'))

    return render_template('saisie_options_simulation.html', composants=COMPOSANTS)


if __name__ == '__main__':
    main.run(debug=True)