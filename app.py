from enum import unique
from unittest import result
from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

import jwt
import os
import datetime

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
CORS(app)

filename = os.path.dirname(os.path.abspath(__file__))
database = 'sqlite:///' + os.path.join(filename, 'db.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = database 
app.config['SECRET_KEY'] = "cretivoxtechnology22"

class Owner(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    email = db.Column(db.String(200))
    status = db.relationship('Status', back_populates="owner")
    datateknik = db.relationship('DataTeknik', back_populates="owner")
    dataasset = db.relationship('DataAsset', back_populates="owner")
    consumable = db.relationship('Consumable', backref="owner")
    assesment = db.relationship('Assesment', back_populates="owner")
    
    
class Status(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    prodi = db.Column(db.String(50))
    nama_lab = db.Column(db.String(50))
    klarifikasi = db.Column(db.String(50))
    kelas =  db.Column(db.String(100))
    ka_lab = db.Column(db.String(100))
    kapasitas = (db.Integer)
    tahun_berdiri = (db.Integer)
    ukuran = db.Column(db.String(100))
    lokasi = db.Column(db.String(100))
    layout = db.Column(db.String(100))
    utility_listrik = db.Column(db.String(100))
    utility_internet = db.Column(db.String(100))
    utility_gas = db.Column(db.String(100))
    status = db.Column(db.String(50))
    rab = db.Column(db.String(100))
    animasi = db.Column(db.String(200))
    Owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'))
    owner = db.relationship("Owner", back_populates='status')
    
class DataTeknik(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data_teknik = db.Column(db.String(200))
    detil = db.Column(db.String(200))
    status = db.Column(db.String(200))
    Owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'))
    owner = db.relationship("Owner", back_populates='datateknik')

class DataAsset(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data_asset = db.Column(db.String(200))
    wdtcolumn = db.Column(db.String(200))
    status = db.Column(db.String(200))
    Owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'))
    owner = db.relationship("Owner", back_populates='dataasset')

class Consumable(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    chemical = db.Column(db.String(200))
    pcs = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'))
    # owner = db.relationship("Owner", back_populates='consumable')
    

class Assesment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    testing_parameter = db.Column(db.String(200))
    result = db.Column(db.String(200))
    unit = db.Column(db.String(200))
    methods = db.Column(db.String(200))
    recomendation = db.Column(db.String(200))
    Owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'))
    owner = db.relationship("Owner", back_populates='assesment')
db.drop_all()    
db.create_all()

def token_api(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.args.get('token') 
        if not token:
            return make_response(jsonify({"msg":"there is no token"}), 401)
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return make_response(jsonify({"msg":"invalid token"}), 401)
        return f(*args, **kwargs)
    return decorator

class Register(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')
        dataEmail = request.form.get('email')
        
        if dataUsername and dataPassword:
            dataModel = Owner(username=dataUsername, password=dataPassword, email=dataEmail)
            db.session.add(dataModel)
            db.session.commit()
            return make_response(jsonify({"msg":"success"}), 200)
        return jsonify({"msg":"Username / password is empty"})

    def get(self):
        dataQuery = Owner.query.all()
        output = [
            {
                "id" : data.id,
                "username" : data.username,
                "password" : data.password, 
                "email" : data.email 
            }    for data in dataQuery 
        ]
        return make_response(jsonify(output), 200)
    
class LoginUser(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')
        
        queryUsername = [data.username for data in Owner.query.all()]
        queryPassword = [data.password for data in Owner.query.all()]
        if dataUsername in queryUsername and dataPassword in queryPassword:
            token = jwt.encode(
                {
                    "username":queryUsername, "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
                }, app.config['SECRET_KEY'],  algorithm="HS256"
            )
            return make_response(jsonify({"msg":"Welcome", "token":token}), 200)
        return jsonify({"msg":"failed"})
    
class Consum(Resource):
    def post(self):
        dataChemical = request.form.get('chemical')
        dataPcs = request.form.get('pcs')
        own = Owner(username="admin" , password="admin", email="test@mail")
        dataModel = Consumable(chemical = dataChemical, pcs = dataPcs, owner = own)
        db.session.add(own)
        db.session.add(dataModel)
        # own.consumable.append(dataModel)
        db.session.commit()
        return make_response(jsonify({'msg':'success'}), 200)
    
    
        

    
api.add_resource(Consum, "/api/consumable", methods=["POST"])    
api.add_resource(Register, "/api/register", methods=["POST","GET"])
api.add_resource(LoginUser, "/api/login", methods=["POST"])

if __name__ ==  '__main__':
    app.run(debug=True, port=2022, host= "0.0.0.0")
