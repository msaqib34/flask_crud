from flask import Flask , request , jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
            return {"id": self.id, "name": self.name, "email": self.email}    

@app.before_request
def createall():  
    db.create_all()  

@app.route('/create-item', methods=['POST'])
def create():
    data = request.json
    if not data or not data.get('name'):
        return jsonify({"error": "Name is required"}), 400
    if not data or not data.get('email'):
        return jsonify({"error": "Email is required"}), 400
    Item=item(name=data['name'], email=data['email'])
    db.session.add(Item)
    db.session.commit()

    return jsonify(Item.to_dict())

@app.route('/show' , methods=['GET'])
def showall():
    Items= item.query.all()
    return jsonify([item.to_dict() for item in Items]) , 200


@app.route('/one-detail/<int:id>', methods=['GET'])
def showone(id):
     Items=item.query.get(id)
     return jsonify(Items.to_dict()), 200


@app.route('/update/<int:id>',methods=['POST'])
def update(id):
    data = request.json
    Items=item.query.get(id)
    Items.name= data['name']
    Items.email=data['email']
    db.session.commit()
    return jsonify(Items.to_dict(),{"message" : "details updated"}) , 200


@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    Item = item.query.get(id)
    db.session.delete(Item)
    db.session.commit()
    return jsonify({"Message" : "Data Removed Sucessfully!"}) , 200

if __name__ == '__main__':
    app.run(debug=True)