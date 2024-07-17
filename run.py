from app import create_app

# Create the Flask application instance
app = create_app()

# This block is only executed if the script is run directly
# It starts the Flask development server with debugging enabled
if __name__ == "__main__":
    app.run(debug=True)
