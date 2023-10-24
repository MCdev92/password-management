from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Passwords

app = Flask(__name__)
api = Api(app)

class PasswordRes(Resource):
    def get(self, password_id):
         # Retrieve a password by its ID
        db = SessionLocal()
        password = db.query(Passwords).filter(Passwords.id == password_id).first()
        db.close()
        
        if password:
            # Convert the password object to a dictionary
            password_data = {
                'id': password.id,
                'username': password.username,
                'website': password.website,
                'password': password.password,
                'note': password.note
            }
            return jsonify(password_data)
        else:
            return jsonify({'message': 'Password not found'}), 404

    def post(self):
         # 1. Request Data Handling
        data = request.get_json()

        if not data:
            return jsonify({"message": "No data provided in the request"}), 400

        # 2. Data Validation
        required_fields = ["title", "username", "password", "website"]
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"'{field}' is a required field"}), 400

        # 3. Database Interaction
        db = SessionLocal()
        new_password = Passwords(
            username=data["username"],
            title=data["title"],
            password=data["password"],
            website=data["website"]
        )
        db.add(new_password)
        db.commit()
        db.close()


    def put(self):
        # 1. Request Data Handling
        data = request.get_json()

        if not data:
            return jsonify({"message": "No data provided in the request"}), 400

        # 2. Data Validation
        required_fields = ["title", "username", "password", "website"]
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"'{field}' is a required field"}), 400

        # 3. Database Interaction
        db = SessionLocal()
        new_password = Passwords(
            username=data["username"],
            title=data["title"],
            password=data["password"],
            website=data["website"]
        )
        db.add(new_password)
        db.commit()
        db.close()

        # 4. Response
        return jsonify({"message": "Password created successfully"})

    def delete(self, password_id):
        # 1. URL Parameter Handling

        # 2. Database Interaction
        db = SessionLocal()
        password = db.query(Passwords).filter(Passwords.id == password_id).first()

        if not password:
            db.close()
            return jsonify({"message": "Password not found"}, 404)

        # Delete the password entry
        db.delete(password)
        db.commit()
        db.close()

        # 3. Response
        return jsonify({"message": "Password deleted successfully"})


api.add_resource(PasswordRes, '/passwords')

@app.route('/passwords')
def index():
    return "Welcome to your password manager!"

if __name__ == '__main__':
    app.run(debug=True)