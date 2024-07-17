from setuptools import setup, find_packages

setup(
    name='free_cash_flow_calculator',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'psycopg2-binary',
        'pandas',
        'SQLAlchemy',
        'python-dotenv',
        'pyspark',
        'databricks-cli',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'initialize_db=db.initialize_db:main'
        ],
    },
)
