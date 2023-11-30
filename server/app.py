#!/usr/bin/env python3

# Remote library imports
from flask import Flask, jsonify, make_response, request, session, json
from flask_restful import Resource
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from sqlalchemy import desc
from datetime import datetime

# Local imports
from config import app, db, api
from models import db, Board, Guru, User, Qna 
# Deck, Wheel, Truck, Motor, Battery, Controller, Remote, Max_speed, Range
# from guru_assistant import guru_assistant
import os

# API imports
from openai import OpenAI


### This puts app.db in server directory???
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DATABASE = os.environ.get(
#     "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


# Instantiate app, set attributes
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.json.compact = False

# Instantiate db
db.init_app(app)
migrate = Migrate()
migrate.init_app(app, db)


# API Secret Key
load_dotenv()
openai_api_key = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)
# openai.api_key = openai_api_key


# another way of getting the secret key using os.getenv??
# os.getenv('OPENAI_API_KEY')


# Instantiate CORS
CORS(app)
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})



### ------------------ OPENAI API REQUESTS ------------------ ###
guru_instructions = "You are an expert in electric skateboards who will be answering questions from prospective builders, aka users. Please follow the instructions below: 1. You will come up with the most appropriate response that suits best for the builder's question. If you are unable to provide an appropriate response to the builder, then please refer them to the following websites: https://electric-skateboard.builders/ , https://forum.esk8.news/ 2. Please refrain from engaing in any other conversation that isn't related to the field of electric skateboards, and in the case that the builder asks a question that is unrelated to and/or outside the scope of electric skateboards, please respond with: 'I apologize but I can only answer questions that are related to electric skateboards.' and end with an appropriate response."

### Not using guru_assistant.py

@app.post('/guru_assistant')
def guru_assistant():
    data = request.get_json()
    user_input = data.get('user_input')

    if not user_input:
        return make_response(
            jsonify({"error": "User input cannot be empty."}), 400
        )
    
    try:
        messages = [
            {"role": "system", "content": guru_instructions},
            {"role": "user", "content": f'I have a question about: {user_input}.'}
            ]
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500
        )

        answer = completion.choices[0].message.content

        #Save user input and the generated response into the database
        guru_entry = Guru(user_input=user_input, answer=answer)
        db.session.add(guru_entry)
        db.session.commit()

        return make_response(
            jsonify({"content": answer}), 200
        )
    except Exception as e:
        print(e)
        
        return make_response(
            jsonify({"error": "Cannot formulate a response."}), 500
        )




### ------------------ USER SIGNUP ------------------ ###


# @app.route('/signup', methods=['POST'])
# def signup():
#     data = request.get_json()
#     new_user = User(email=data['email'])
#     new_user.password_hash = data['password']

#     db.session.add(new_user)
#     db.session.commit()

#     return {'message': 'Registration Successful!'}, 201



### ------------------ CHECK SESSION, LOGIN-LOGOUT ------------------ ###



# @app.route('/check_session')
# def check_session():
#     user_id = session.get('user_id')
#     user = User.query.filter(User.id == user_id).first()

#     if not user:
#         return {'error': 'Invalid Session.'}, 401
    
#     return {'message': 'Session Valid, Access Granted'}, 200


# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()

#     # check if user exists
#     user = User.query.filter(User.email == data['email']).first()

#     if not user:
#         return make_response(jsonify({'error': 'User not found.'}), 404)
    
#     if user.authenticate(data['password']):  # check if pwd match
#         session['user_id'] = user.id
#         user_data = {
#             'id': user.id,
#             'email': user.email
#         }
#         return make_response(jsonify({'message': 'Login successful!', 'user': user_data}), 200)
#     else:
#         # password did not match, send error resp
#         return make_response(jsonify({'error': 'Invalid email or password.'}), 401)


# @app.delete('/logout')
# def logout():
#     session.pop('user_id')

#     return {'message': 'Successfully logged out.'}, 200



### ------------------ USERS ------------------ ###



### ------------------ BOARDS ------------------ ###

@app.route('/boards', methods=['GET'])
def get_boards():
    boards = Board.query.all()
    return make_response(jsonify([board.to_dict() for board in boards]), 200)



@app.route('/latest_boards')
def get_latest_board():
    # Query the boards, order by timestamp in descending order, and retrieve the first one
    latest_board = Board.query.order_by(desc(Board.timestamp)).first()

    if latest_board:
        return make_response(jsonify(latest_board.to_dict()), 200)
    else:
        return make_response(jsonify({}), 404)



@app.route('/boards/<int:board_id>', methods=['DELETE'])
def delete_board_by_id(board_id):
    board = Board.query.filter(Board.id == board_id).first()

    if board:
        db.session.delete(board)
        db.session.commit()
        return {"message": "Board deleted successfully."}, 200
    else:
        return {"error": "Board not found."}, 404



# appending data directly onto Board:
@app.post('/update_board')
def update_board():
    data = request.json

    # print(data)

    deck_type = data.get('deckType', '')
    deck_length = data.get('deckLength', '')
    deck_material = data.get('deckMaterial', '')
    truck_type = data.get('truckType', '')
    truck_width = data.get('truckWidth', '')
    controller_feature = data.get('controllerFeature', '')
    controller_type = data.get('controllerType', '')
    remote_feature = data.get('remoteFeature', '')
    remote_type = data.get('remoteType', '')
    motor_size = data.get('motorSize', '')
    motor_kv = data.get('motorKv', '')
    wheel_size = data.get('wheelSize', '')
    wheel_type = data.get('wheelType', '')
    battery_voltage = data.get('batteryVoltage', '')
    battery_type = data.get('batteryType', '')
    battery_capacity = data.get('batteryCapacity', '')
    battery_configuration = data.get('batteryConfiguration', '')
    range_mileage = data.get('mileage', '')
    image_url = data.get('imageURL', '')

    # Update the Wheel database with the new values
    sample_board_entry = Board(deck_type=deck_type, deck_length=deck_length, deck_material=deck_material, truck_type=truck_type, truck_width=truck_width, controller_feature=controller_feature, controller_type=controller_type, remote_feature=remote_feature, remote_type=remote_type, motor_size=motor_size, motor_kv=motor_kv, wheel_size=wheel_size, wheel_type=wheel_type, battery_voltage=battery_voltage, battery_type=battery_type, battery_capacity=battery_capacity, battery_configuration=battery_configuration, range_mileage=range_mileage, image_url=image_url)
    # Board.query.delete()
    db.session.add(sample_board_entry)
    db.session.commit()

    return {"message": "Wheel updated successfully."}, 200


### ------------------ QNA ------------------ ###


@app.route('/qna', methods=['GET'])
def get_qna():
    # Fetch all Qna entries from the database
    qna_entries = Qna.query.all()

    # Convert Qna entries to a list of dictionaries
    qna_data = [{'id': entry.id, 'post': entry.post, 'reply': entry.reply, 'timestamp': entry.timestamp} for entry in qna_entries]

    # Return the Qna data as JSON
    return jsonify(qna_data)



@app.route('/qna', methods=['POST'])
def add_qna():
    try:
        # Get data from the request
        data = request.get_json()

        # Extract post and reply from the request data
        post = data.get('post', '')
        reply = data.get('reply', '')

        # Check if both post and reply are provided
        if not post and not reply:
            return jsonify({'error': 'Both post and reply are required'}), 400

        # Create a new Qna entry
        new_qna = Qna(post=post, reply=reply, timestamp=datetime.utcnow())

        # Add the new Qna entry to the database
        db.session.add(new_qna)
        db.session.commit()

        # Return the newly created Qna entry as JSON
        return jsonify({'id': new_qna.id, 'post': new_qna.post, 'reply': new_qna.reply, 'timestamp': new_qna.timestamp}), 201

    except Exception as e:
        # Handle exceptions and return a JSON response
        return jsonify({'error': str(e)}), 500

@app.route('/qna/<int:post_id>/reply', methods=['POST'])
def add_reply(post_id):
    try:
        # Get data from the request
        data = request.get_json()

        # Extract reply from the request data
        reply = data.get('reply', '')

        # Check if reply is provided
        if not reply:
            return jsonify({'error': 'Reply is required'}), 400

        # Find the post in the database
        post = Qna.query.get(post_id)

        if not post:
            return jsonify({'error': 'Post not found'}), 404

        # Create a new Reply entry
        new_reply = Reply(reply=reply, timestamp=datetime.utcnow(), post=post)

        # Add the new Reply entry to the database
        db.session.add(new_reply)
        db.session.commit()

        # Return the newly created Reply entry as JSON
        return jsonify({'id': new_reply.id, 'reply': new_reply.reply, 'timestamp': new_reply.timestamp}), 201

    except Exception as e:
        # Handle exceptions and return a JSON response
        return jsonify({'error': str(e)}), 500

















#####working but only for post

# @app.route('/qna', methods=['POST'])
# def add_qna():
#     try:
#         # Get data from the request
#         data = request.get_json()

#         # Extract post and reply from the request data
#         post = data.get('post', '')
#         reply = data.get('reply', '')

#         # Check if both post and reply are provided
#         if not post:
#             return jsonify({'error': 'Post cannot be empty.'}), 400
        
#         # if not reply:
#         #     return jsonify({'error': 'Reply cannot be empty.'}), 400

#         # Create a new Qna entry
#         new_qna = Qna(post=post, reply=reply, timestamp=datetime.utcnow())

#         # Add the new Qna entry to the database
#         db.session.add(new_qna)
#         db.session.commit()

#         # Return the newly created Qna entry as JSON
#         return jsonify({'id': new_qna.id, 'post': new_qna.post, 'reply': new_qna.reply, 'timestamp': new_qna.timestamp}), 201

#     except Exception as e:
#         # Handle exceptions and return a JSON response
#         return jsonify({'error': str(e)}), 500
















#####simplified

# @app.route('/qna', methods=['GET'])
# def get_qna():
#     # Fetch all Q&A posts from the database
#     qna_posts = Qna.query.all()
#     # Convert posts to a list of dictionaries
#     qna_list = [{'id': post.id, 'post': post.post, 'reply': post.reply, 'timestamp': post.timestamp} for post in qna_posts]
#     return jsonify(qna_list)

# @app.route('/qna', methods=['POST'])
# def add_qna():
#     # Get post and reply from the request JSON
#     post_content = request.json.get('post')
#     reply_content = request.json.get('reply')

#     # Create a new Qna instance
#     new_qna = Qna(post=post_content, reply=reply_content)

#     # Add and commit to the database
#     db.session.add(new_qna)
#     db.session.commit()

#     # Return the new Q&A post as JSON
#     return jsonify({'id': new_qna.id, 'post': new_qna.post, 'reply': new_qna.reply, 'timestamp': new_qna.timestamp})










####old

# app.get('/qna')
# def get_posts():
#     posts = Qna.query.all()
#     return make_response(jsonify([post.to_dict() for post in posts]), 200)


# app.patch('/qna/<int:id>')
# def edit_post_by_id(id):
#     data = request.json

#     Qna.query.filter(Qna.id == id).update(data)
#     db.session.commit()
    
#     post = Qna.query.filter(Qna.id == id).first()
    
#     return make_response(jsonify(post.to_dict()), 200)


# app.delete('/qna/<int:id>')
# def delete_post_by_id():
#     post = Qna.query.filter(Qna.id == id).first()

#     if post:
#         db.session.delete(post)
#         db.session.commit()
#         return {"message": "Post deleted successfully."}, 200
#     else:
#         return {"error": "Post not found."}, 404





if __name__ == '__main__':
    app.run(port=5555, debug=True)
