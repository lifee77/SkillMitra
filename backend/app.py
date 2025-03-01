import os
from flask import Flask
from routes.data_routes import data_bp
from routes.media_routes import media_bp
from routes.recommendation_routes import recommendation_bp
from routes.home_routes import home_bp  # Import home route

app = Flask(__name__)

# Ensure required directories exist
os.makedirs('temp', exist_ok=True)
os.makedirs('outputs', exist_ok=True)

# Register blueprints
app.register_blueprint(home_bp)  # Register the homepage route
app.register_blueprint(data_bp, url_prefix='/data')
app.register_blueprint(media_bp, url_prefix='/media')
app.register_blueprint(recommendation_bp, url_prefix='/recommendation')

if __name__ == '__main__':
    app.run(debug=True)
