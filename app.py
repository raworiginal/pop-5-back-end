from flask import Flask
from dotenv import load_dotenv
from blueprints import auth_bp, topics_bp

load_dotenv()

app = Flask(__name__)
app.register_blueprint(auth_bp)
app.register_blueprint(topics_bp)

if __name__ == "__main__":
    app.run(debug=True)
