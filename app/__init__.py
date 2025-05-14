from flask import Flask , render_template

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')  
    
    @app.route('/')
    def home():
        return render_template('index.html')

    from app.routes.upload import upload_routes
    from app.routes.monitoring import monitoring_routes

    app.register_blueprint(upload_routes, url_prefix='/upload')
    app.register_blueprint(monitoring_routes, url_prefix='/monitoring')

    return app
