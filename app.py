from flask import Flask
from flask_cors import CORS
from routes.student_routes import student_bp
from routes.course_routes import course_bp
from routes.grade_routes import grade_bp

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests for all routes

# Register blueprints
app.register_blueprint(student_bp)
app.register_blueprint(course_bp)
app.register_blueprint(grade_bp)

@app.route('/')
def index():
    return {"message": "Educational Administration API is running"}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)