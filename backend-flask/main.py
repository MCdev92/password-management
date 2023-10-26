from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from database import SessionLocal
from models import Passwords
from flask_bcrypt import Bcrypt

app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)


class PasswordRes(Resource):
    def get(self, password_id):
   # Retrieve a password by its ID
        with SessionLocal() as db:
            password = db.query(Passwords).filter(Passwords.id == password_id).first()
            if password:
                password_data = {
                    'id': password.id,
                    'username': password.username,
                    'website': password.website,
                    'note': password.note
                }
                return jsonify(password_data)
            else:
                return jsonify({'message': 'Password not found'}), 404

    def post(self):
        # Request Data Handling
        data = request.get_json()

        if not data:
            return jsonify({"message": "No data provided in the request"}), 400

        # Data Validation
        required_fields = ["username", "password", "website"]
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"'{field}' is a required field"}), 400

        # Hash the password using flask_bcrypt
        hashed_password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')

        # Database Interaction
        with SessionLocal() as db:
            new_password = Passwords(
                username=data["username"],
                password=hashed_password,  # Store the hashed password
                website=data["website"],
                note=data.get("note")
            )
            db.add(new_password)
            db.commit()

        return jsonify({"message": "Password created successfully"})

    def put(self):
        # Request Data Handling
        data = request.get_json()

        if not data:
            return jsonify({"message": "No data provided in the request"}), 400

        # Data Validation
        required_fields = ["username", "password", "website"]
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"'{field}' is a required field"}), 400

        # Database Interaction
        with SessionLocal() as db:
            password_id = data.get('id')
            password = db.query(Passwords).filter(Passwords.id == password_id).first()
            if not password:
                return jsonify({"message": "Password not found"}, 404)
            # Update the password entry
            for field in data:
                setattr(password, field, data[field])
            db.commit()

        return jsonify({"message": "Password updated successfully"})

    def delete(self, password_id):
        # Database Interaction
        with SessionLocal() as db:
            password = db.query(Passwords).filter(Passwords.id == password_id).first()

            if not password:
                return jsonify({"message": "Password not found"}, 404)

            # Delete the password entry
            db.delete(password)
            db.commit()

        return jsonify({"message": "Password deleted successfully"})

api.add_resource(PasswordRes, '/passwords/')
@app.route('/passwords/', methods=['POST'])
def index():
    return "Welcome to your password manager!"

if __name__ == '__main__':
    app.run(debug=True)
