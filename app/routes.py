from flask import Blueprint, render_template, request, redirect, url_for, flash, Flask, jsonify
import pandas as pd
import sqlite3
 
main = Blueprint('main', __name__)
 
#app = Flask(__name__)

@main.route('/')
def index():
    return render_template('accueil.html')
 
@main.route('/select-action', methods=['POST'])
def select_action():
    action = request.form['action']
    if action == 'params':
        return redirect(url_for('main.saisie_parametres_generaux'))
    if action == 'upload_nature_mvm':
        return redirect(url_for('main.parametre_nature_mvm_upload'))
    elif action == 'mouvements':
        return redirect(url_for('main.saisie_mouvements'))
    elif action == 'simulate':
        return redirect(url_for('main.saisie_options_simulation'))
    elif action == 'courbes':
        return redirect(url_for('main.courbes'))
 
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'xlsx'
 
@main.route('/parametre-nature-mvm-upload', methods=['GET', 'POST'])
def parametre_nature_mvm_upload():
    if request.method == 'POST':
        file = request.files.get('file')
       
        if file and allowed_file(file.filename):
            try:
                # Lire le fichier Excel dans un DataFrame
                df = pd.read_excel(file)
               
                # Connexion à la base de données SQLite
                conn = sqlite3.connect('app.db')
                cursor = conn.cursor()
               
                # Insérer les données dans la table
                for index, row in df.iterrows():
                    cursor.execute('''
                        INSERT INTO parametrage_nature_mouvements (code_typ, categorie_mouvement, code_nat, nature_mouvement)
                        VALUES (?, ?, ?, ?)
                    ''', (row['code_typ'], row['categorie_mouvement'], row['code_nat'], row['nature_mouvement']))
               
                # Commit et fermeture de la connexion
                conn.commit()
                cursor.close()
                conn.close()
               
                # Message de succès
                flash('File successfully uploaded and data inserted', 'success')
            except Exception as ex:
                # Rollback et message d'erreur en cas de problème
                conn.rollback()
                cursor.close()
                conn.close()
                flash(f'File upload failed: {ex}', 'danger')
        else:
            flash('Invalid file format. Please upload an .xlsx file.', 'danger')
       
        return redirect(url_for('main.index'))
   
    return render_template('parametre_nature_mvm_upload.html')
 
 
 
from flask import render_template, request, redirect, url_for, flash
import sqlite3
 
@main.route('/saisie-parametres-generaux', methods=['GET', 'POST'])
def saisie_parametres_generaux():
    devises, langues = get_items()

    if request.method == 'POST':
        # Récupérer les valeurs du formulaire
        id_entreprise = request.form['id_entreprise']
        nom_entreprise = request.form['nom_entreprise']
        devise = request.form['devise']
        langue = request.form['langue']
        annee_exercice = request.form['annee_exercice']
        mois_debut_simulation = request.form['mois_debut_simulation']
 
        try:
            # Connexion à la base de données et insertion des données
            conn = sqlite3.connect('app.db')
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO parametres_generaux (id_entreprise, nom_entreprise, devise, langue, annee_exercice, mois_debut_simulation)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (id_entreprise, nom_entreprise, devise, langue, annee_exercice, mois_debut_simulation))
           
            conn.commit()  # Sauvegarde les modifications
            flash('Les paramètres ont été enregistrés avec succès', 'success')
       
        except Exception as ex:
            # Effectuer un rollback si une erreur survient
            if conn:
                conn.rollback()
            flash(f'Échec de l\'enregistrement des paramètres : {ex}', 'danger')
       
        finally:
            # Toujours fermer la connexion
            if cursor:
                cursor.close()
            if conn:
                conn.close()
 
        return redirect(url_for('main.index'))
 
    # En cas de méthode GET, récupérer les données à afficher
    def get_data_from_spg():
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
       
        cursor.execute("SELECT * FROM parametres_generaux")
        rows = cursor.fetchall()
       
        conn.close()
        return rows
 
    # Récupérer les données pour les afficher
    data = get_data_from_spg()
   
    # Rendre le template avec les données
    return render_template('saisie_parametres_generaux.html', data=data, devises=devises, langues=langues)
 
 
 
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
 
@main.route('/courbes', methods=['GET', 'POST'])
def courbes():
    if request.method == 'POST':
        try:
            # Log des en-têtes et données de la requête
            logging.info(f"En-têtes de la requête : {request.headers}")
            logging.info(f"Données brutes de la requête : {request.data}")
            logging.info(f"Données du formulaire : {request.form}")
            logging.basicConfig(level=logging.DEBUG)
 
            id_entreprise = request.form['ientreprise']
            version = request.form['version']
            mois_simulation_FRF = request.form['mois_simulation_FRF']
            date_jour = request.form['date_jour']
 
            print(entreprise)
            print(version)
            # Log des valeurs principales
            logging.info(f"Entreprise: {entreprise}")
            logging.info(f"Version: {version}")
            logging.info(f"Mois de simulation: {mois_simulation_FRF}")
            logging.info(f"Date du jour: {date_jour}")
            logging.basicConfig(level=logging.DEBUG)
 
            # Préparer les valeurs pour chaque composant
            valeurs = {
                "month_01": request.form.get('month_01', ""),
                "rate_01": request.form.get('rate_01', ""),
                "month_02": request.form.get('month_02', ""),
                "rate_02": request.form.get('rate_02', ""),
            }
 
            # Log des valeurs reçues pour vérification
            logging.info(f"Valeurs reçues : {valeurs}")
            print(valeurs)
            # Connexion à la base de données SQLite
            conn = sqlite3.connect('app.db')
            cursor = conn.cursor()
 
            # Insertion dans la table parametres_simulation
            cursor.execute('''
                INSERT INTO courbes (
                    entreprise, version, mois_simulation_FRF, date_jour,
                    Mois_prevision, taux_recettes_exploitation
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                entreprise, version, mois_simulation_FRF, date_jour,
                valeurs["month_01"], valeurs["rate_01"]
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
    else:
        conn = sqlite3.connect('app.db')
        cur = conn.cursor()
        res = cur.execute("SELECT entreprise, version, mois_simulation_FRF, date_jour FROM parametres_simulation")
        #todo : vérifier si la requête renvoie au moins 1 enreg.
        data = res.fetchone()
        print(f"data={data}")
        entreprise = data[0]
        version = data[1]
        mois_simulation_FRF = data[2]
        date_jour = data[3]
        print(f"entreprise          = {entreprise}")
        print(f"version             = {version}")
        print(f"mois_simulation_FRF = {mois_simulation_FRF}")
        print(f"date_jour           = {date_jour}")
        return render_template('courbes.html', entreprise=entreprise, version=version, mois_simulation_FRF=mois_simulation_FRF, date_jour=date_jour)

# Autocomplete des champs ID Entreprise et Nom Entreprise
@main.route('/autocomplete', methods=['GET'])
def autocomplete():
    idinput = request.args.get('p') 
    search = request.args.get('q')
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    # Condition selon l'input remonté en paramètre
    if idinput == 'id_entreprise':
        res = cur.execute('SELECT DISTINCT id_entreprise FROM parametres_generaux WHERE id_entreprise LIKE ?', ('%' + search + '%',))
        results = [row['id_entreprise'] for row in res.fetchall()]
    elif idinput == 'nom_entreprise':
        res = cur.execute('SELECT DISTINCT nom_entreprise FROM parametres_generaux WHERE nom_entreprise LIKE ?', ('%' + search + '%',))
        results = [row['nom_entreprise'] for row in res.fetchall()]
    conn.close()
    return jsonify(results)

# Récupération des devises et langues pour alimentation des listes déroulantes
def get_items():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT shortcut, name FROM devises")
    devises = cursor.fetchall()
    cursor.execute("SELECT shortcut, name FROM langues")
    langues = cursor.fetchall()
    conn.close()
    return devises, langues

if __name__ == '__main__':
    main.run(debug=True)    