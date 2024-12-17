#All database models for application

from config import db

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(80), unique = False, nullable = False) #cannot pass a null value
    last_name = db.Column(db.String(80), unique = False, nullable = False) #cannot pass a null value
    email = db.Column(db.String(120), unique = True, nullable = False) #cannot pass a null value

    def to_json(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
        }