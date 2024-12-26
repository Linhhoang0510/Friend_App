from app import app, db
from flask import request, jsonify
from models import Friend

# CRUD operations

# Get all friends
@app.route('/api/friends', methods=['GET']) # import back to the app.py file
def get_friends():
    friends = Friend.query.all() # get all friends from the database using Python code instead of SQL queries
    result = [friend.to_json() for friend in friends] # convert the friends to JSON format
    return jsonify(result) # return the JSON response

# Create a friend
@app.route('/api/friends', methods=['POST']) # POST is used to send data to the server from the client side in a request body to create a new friend
def create_friend():
    try:
        data = request.json # get the JSON data from the request
        
        required_fields = ['name', 'role', 'description', 'gender']
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing {field} required field in request'}), 400
                 
        name = data.get('name') # get the name from the JSON data
        role = data.get('role') # get the role from the JSON data
        description = data.get('description') # get the description from the JSON data
        gender = data.get('gender') # get the gender from the JSON data
        
        # fetch avatar image based on gender
        if gender == "male":
            img_url = f"https://avatar.iran.liara.run/public/boy?username={name}"
        elif gender == "female":
            img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
        else:
            img_url = None

        new_friend = Friend(name=name, role=role, description=description, gender=gender, img_url=img_url) # create a new friend object
        db.session.add(new_friend) # add the new friend to the database session
        db.session.commit() # commit the session to the database
        
        return jsonify({'message': 'Friend created successfully'}), 201 # return a success message
    
    except Exception as e:
        db.session.rollback() # rollback the previous session if an error occurs
        return jsonify({'error': str(e)}), 500
    
# Delete a friend
@app.route('/api/friends/<int:id>', methods=['DELETE']) # DELETE is used to delete a friend based on the ID
def delete_friend(id):
    try:
        friend = Friend.query.get(id) # get the friend based on the ID
        if friend is None:
            return jsonify({'error': 'Friend not found'}), 404 # return a 404 error which means the resource is not found
        db.session.delete(friend) # delete the friend from the session
        db.session.commit() # commit the session to the database
        return jsonify({'message': 'Friend deleted successfully'}), 200 # return a success message
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 # internal error

# Update a friend
@app.route('/api/friends/<int:id>', methods=['PATCH']) # PUT is used to update a friend based on the ID
def update_friend(id):
    try:
        friend = Friend.query.get(id) # get the friend based on the ID
        if friend is None:
            return jsonify({'error': 'Friend not found'}), 404
        
        data = request.json # get the JSON data from the request
        
        friend.name = data.get('name', friend.name) # update the name of the friend if it exists in the JSON data, or keep the existing name
        friend.role = data.get('role', friend.role) # update the role of the friend if it exists in the JSON data, or keep the existing role
        friend.description = data.get('description', friend.description) # update the description of the friend if it exists in the JSON data, or keep the existing description 
        friend.gender = data.get('gender', friend.gender) # update the gender
        
        db.session.commit() # commit the session to the database
        return jsonify(friend.to_json()), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500