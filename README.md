# Free Cash Flow Calculator

This project is a web application designed to calculate the free cash flow of a company based on historical monthly data and simulate future months according to specific rules. It's currently at the Proof of Concept stage.

## Azure Deployed Target vs. Local Analog

### Azure Deployed Target

The application is deployed on Azure using the following managed services:
- Azure App Service for hosting the Flask web application.
- Azure Database for PostgreSQL for storing data.
- Databricks Workspace for performing data processing and simulations.

### Local Analog

For local development and testing, the following setup is recommended:
- Python environment managed with virtualenv or conda.
- SQLite database for local storage.
- Apache Spark for data processing (local mode).
- Mocking calls to Azure Blob Storage for local development.

## Setting Up the Environment (Windows)

1. Clone the repository:
   ```bash
   git clone https://gitlab.lafabric.ovh/your-username/free-cash-flow.git



2. Navigate to the project directory:
cd free-cash-flow

3. Create and activate a virtual environment:
python -m venv venv
venv\Scripts\activate

4. Install dependencies:
pip install -r requirements.txt

5. Set up environment variables:

    Create a .env file in the project root.
    Define environment variables such as SECRET_KEY, DB_TYPE (set to sqlite), etc.


6. Initialize the SQLite database:
python manage.py db upgrade

7. Configure the local PySpark environment:

    Download Apache Spark from the official website: https://spark.apache.org/downloads.html
    Extract the Spark archive to a directory on your local machine.
    Add the Spark bin directory to your system PATH.
    Set the SPARK_HOME environment variable to the Spark installation directory.
    Optionally, configure PySpark to use a local mode by setting the PYSPARK_MASTER environment variable to local[*].


## Mocking Azure Blob Storage

For local development, you can mock calls to Azure Blob Storage with a local storage path. Follow these steps:

    Create a local directory to serve as the mock storage:

    bash

mkdir mock_storage

Set the environment variable AZURE_STORAGE_CONNECTION_STRING to a connection string pointing to the mock storage:

bash

export AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=http;AccountName=your_mock_account;AccountKey=your_mock_key;BlobEndpoint=http://localhost:10000/your_container"

Use this local storage path for testing file upload and download functionality in your application.


## Testing the Application Locally
1. Start the Flask development server:

2. Access the application in your web browser at http://localhost:5000.

