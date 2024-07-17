from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.utils import upload_file_to_blob
from app.models import CompanyData, SimulationConfig, db
import sqlite3
import pandas as pd


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/select-action', methods=['POST'])
def select_action():
    action = request.form['action']
    if action == 'upload':
        return redirect(url_for('main.select_company_upload'))
    elif action == 'simulate':
        return redirect(url_for('main.select_company_simulate'))

@main.route('/select-company-upload')
def select_company_upload():
    
    # Connect to the SQLite database
    connection = sqlite3.connect('app.db')
 
    # Create a cursor object
    cursor = connection.cursor()
 
    # Execute a SQL query to select all rows from a table
    cursor.execute("SELECT DISTINCT company_data.company_name AS company_data_company_name FROM company_data")
 
    # Fetch all rows from the executed query
    companies = cursor.fetchall()
 
    # Iterate through the rows and print them
    for row in companies:
     print(row)
 
    # Close the cursor and connection
    cursor.close()
    connection.close()

    if not companies:
        print("No companies found in the database.")
    else:
        # Transform tuples into a list of company names
         company_names = [company[0] for company in companies]

        # Print company names for debugging
         for company_name in company_names:
             print(f"Found company: {company_name}  ")

    return render_template('select_company_upload.html', companies=company_names)
         
@main.route('/upload', methods=['POST'])
def upload_file(): 
    company_name =  request.form['company_name']
    file = request.files['file']
    if file and company_name:
        try:
            df = pd.read_excel(file)
            print(df.head())

            # Connexion à la base de données SQLite
            conn = sqlite3.connect('app.db')
            cursor = conn.cursor()

            # Insertion des données ligne par ligne
            for index, row in df.iterrows():
                
                cursor.execute("""
                    INSERT INTO company_data (company_name, category, sub_category, amount, date)
                    VALUES (?, ?, ?, ?, ?)
                """, (row['company_name'], row['category'], row['sub_category'],row['amount'], row['date']))

            # Valider la transaction pour sauvegarder les changements
            conn.commit()
            cursor.close()
            conn.close()
            flash('File successfully uploaded and data inserted')
        except Exception as ex:
            # En cas d'erreur, annuler la transaction
            conn.rollback()
            flash(f'File upload failed: {ex}')
    else:
        flash('Please select a company and a file')
    return redirect(url_for('main.index'))

#            for index, row in df.iterrows():
#                company_data = CompanyData(
#                    company_name=row['company_name'],
#                    category=row['category'],
#                    sub_category=row['sub_category'],
#                    amount=row['amount'],
#                    date=row['date']
#                )
#                db.session.add(company_data)
#                
#            db.session.commit()
#            flash('File successfully uploaded and data inserted')
#        except Exception as ex:
#            db.session.rollback()
#            flash(f"File upload failed: {ex}")
#    else:
#        flash('Please select a company and a file')
#    return redirect(url_for('main.index'))


#@main.route('/upload', methods=['POST'])
#def upload_file():
 #   company_name = request.form['company_name']
  #  file = request.files['file']
   # if file and company_name:
  #      try:
  #          filename = f"{company_name}/{file.filename}"
  #          upload_file_to_blob(file, filename)
#            flash('File successfully uploaded')
#        except Exception as ex:
#            flash(f"File upload failed: {ex}")
#    else:
#        flash('Please select a company and a file')
#    return redirect(url_for('main.index'))

@main.route('/select-company-simulate')
def select_company_simulate():
    # Retrieve all companies for selection
    companies = db.session.query(CompanyData.company_name).distinct().all()
    return render_template('select_company_simulate.html', companies=companies)

@main.route('/simulate', methods=['POST'])
def simulate():
    company_name = request.form['company_name']
    month = request.form['month']
    if company_name and month:
        # Here, you would trigger the Databricks notebook for the simulation
        flash(f'Simulation for {company_name} for month {month} triggered')
    else:
        flash('Please select a company and a month')
    return redirect(url_for('main.index'))
