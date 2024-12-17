# Main roots / endpoints
# CRUD: Create Run Update Delete

# Create:
# - first_name
# - last_name
# - email

# localhost:5000/home --> /home is the endpoint
# localhost:5000/create_contact

# Request types
# GET: access some kind of resource
# POST: create something new
# PUT/PATCH: updating something
# DELETE
#####################################################

# Request localhost:5000/delete_contact
# type: DELETE --> delete a contact
# json:{
# what contact to delete / data about the contact to delete
# }

# Response
# status: 200 --> OK / 404 --> not found
# json: {
#   contact data
# }

from flask import request, jsonify
from config import app, db
from models import Contact

# GET
@app.route("/contacts", methods = ["GET"])
def get_contacts():
    contacts = Contact.query.all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    return jsonify({"contacts": json_contacts})


# POST
@app.route("/create_contact", methods = ["POST"])
def create_contact():
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")

    if not first_name or not last_name or not email:
        return (
            jsonify({"message": "you must include a first name, last name and email"}), 400,
        )
    
    new_contact = Contact(first_name = first_name, last_name = last_name, email = email) # Create a python class
    try:
        db.session.add(new_contact) # added to db session / staged
        db.session.commit() # write to the db
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "User created!"}), 201

# Postman

# UPDATE
@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found!"}), 404
    
    data = request.json
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)

    db.session.commit()

    return jsonify({"message": "User updated!"}, 200)


# DELETE
@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found"}), 404
    
    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message": "User deleted!"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all() #create all db models

    app.run(debug = True)
