from app import create_app

# Create the app instance
app = create_app()

# This is what gunicorn will import
if __name__ == "__main__":
    app.run()