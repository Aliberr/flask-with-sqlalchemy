# wsgi.py
import os
import logging
from flask import Flask, request, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Product
from schemas import product_schema, products_schema

admin = Admin(app, name='Back-office', template_mode='bootstrap3')
admin.add_view(ModelView(Product, db.session)) # `Product` needs to be imported before

@app.route('/')
def home():
    products = db.session.query(Product).all()
    return render_template('home.html', products=products)


@app.route('/hello')
def hello():
    return "Hello World"

@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'GET':
        products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
        return products_schema.jsonify(products)
    elif request.method == 'POST':
        product = Product()
        product.name = request.get_json()['name']
        db.session.add(product)
        db.session.commit()
        return f'{product.name} successfully added to database', 201



@app.route('/products/<int:id>', methods=['GET', 'DELETE', 'PATCH'])
def products_id(id):
    if request.method == 'GET':
        products_id = db.session.query(Product).get(id)
        if products_id:
            return product_schema.jsonify(products_id)
        else:
            return "Id not found", 404
    elif request.method == 'DELETE':
        products_id = db.session.query(Product).get(id)
        db.session.delete(products_id)
        db.session.commit()
        return f'product with id: {id} successflully deleted', 200
    elif request.method == 'PATCH':
        products_id = db.session.query(Product).get(id)
        products_id.name = request.get_json()['name']
        db.session.commit()
        return f'product with id: {id} successflully updated', 200
    else:
        return "Read the API documentation", 403




