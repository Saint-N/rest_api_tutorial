from flask import Flask, request
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db  = SQLAlchemy(app)

class Phones(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable = False)
    description = db.Column(db.String(150))

    def __repr__(self):
        return f"{self.name} - {self.description}"

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/phones')
def get_phones():
    phones = Phones.query.all()
    output = []

    for phone in phones:
        phone_data = {'name': phone.name, 'description' : phone.description}
        output.append(phone_data)

    return {"phone" : output}

@app.route('/phones/<id>')
def get_phone(id):
    phone = Phones.query.get_or_404(id)
    return {"name": phone.name, "description": phone.description}

@app.route("/phones", methods = ['POST'])
def add_phone():
    phone = Phones(name = request.json['name'], description = request.json['description'])
    db.session.add(phone)
    db.session.commit()
    return {'id' : phone.id}

@app.route('phones/<id>', methods = ['DELETE'])
def delete_phone(id):
    phone = Phones.query.get(id)
    if phone is None:
        return {"Error": "Phone not found"}
    db.session.delte(phone)
    db.session.commit()
    return {"Success": "Phone deleted"}

if __name__ == '__main__':
    app.run(debug=True)