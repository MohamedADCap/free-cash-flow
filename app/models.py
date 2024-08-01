from app import db

class CompanyData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    sub_category = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(255), nullable=False)

# Model for Parametrage_Nature_Mouvements
class ParametrageNatureMouvements(db.Model):
    __tablename__ = 'Parametrage_Nature_Mouvements'
    CODE_TYP = db.Column(db.String(50), primary_key=True)
    CATEGORIE_MOUVEMENT = db.Column(db.String(100), nullable=False)
    CODE_NAT = db.Column(db.String(50), primary_key=True)
    NATURE_MOUVEMENT = db.Column(db.String(100), nullable=False)

# Model for Soldes_Intermediaires_Gestion
class SoldesIntermediairesGestion(db.Model):
    __tablename__ = 'Soldes_Intermediaires_Gestion'
    id = db.Column(db.Integer, primary_key=True)
    Entreprise = db.Column(db.String(100), nullable=False)
    Date_mouvement = db.Column(db.Date, nullable=False)
    Categorie_mouvement = db.Column(db.String(100), nullable=False)
    Nature_mouvement = db.Column(db.String(100), nullable=False)
    Libelle_mouvement = db.Column(db.String(200), nullable=False)
    Montant = db.Column(db.Float, nullable=False)

class SimulationConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    config_name = db.Column(db.String(255), nullable=False)
    rules = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class GeneralParams(db.Model):
    __tablename__ = 'general_params'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, unique=True, nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    language = db.Column(db.String(10), nullable=False)
    fiscal_year = db.Column(db.Integer, nullable=False)
    start_month = db.Column(db.String(10), nullable=False)