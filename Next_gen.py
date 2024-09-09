from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:9652@localhost/Next_gen'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User model
class User(db.Model):
    __tablename__ = 'user' 
    name = db.Column(db.String(100), nullable=False)
    mobile_no = db.Column(db.String(15), primary_key=True)
    # otp = db.Column(db.String(6), nullable=False)
    vehicle = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

# POST API to store user data
@app.route('/callback-request', methods=['POST'])
def add_user():
    full_data = request.get_json(force=True)
    for data in full_data:
        new_user = User(
            name=data['name'],
            mobile_no=data['mobile_no'],
            # otp=data['otp'],
            vehicle=data['vehicle'],
            state=data['state'],
            city=data['city']
        )

        db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Callback requested successfully'}), 201

#GET API to fetch all user data
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.with_entities(User.name, User.mobile_no).all()
    users_list = [{'name': user.name, 'mobile_no': user.mobile_no} for user in users]
    return jsonify(users_list), 200
    

if __name__ == "__main__":
    app.run(debug=True)
