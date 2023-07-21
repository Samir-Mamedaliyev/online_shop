import mysql.connector
import os
import json
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/internet_store'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with app.app_context():
    try:
        # db.session.execute('SELECT 1')
        db.session.execute(text('SELECT 1'))
        print('\n\n----------- Connection successful !')
    except Exception as e:
        print('\n\n----------- Connection failed ! ERROR : ', e)

# Product Table


class Product(db.Model):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    price = Column(Integer)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# Home page


@app.route('/')
def all_products():
    products = Product.query.all()
    product_list = []

    for product in products:
        product_data = {
            'id': product.id,
            'name': product.name,
        }
        product_list.append(product_data)

    return jsonify(product_list)


@app.route('/product/<int:id>')
def get_one(id):
    if id:
        product = Product.query.filter_by(id=id).first()
        if not product:
            return 'Product not found'
        return jsonify({'id': product.id, 'name': product.name})

# Add new products


# class Product(db.Model):
#     __tablename__ = 'product'
#     __table_args__ = {'extend_existing': True}

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))


@app.route('/product', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')

    if not name or not price:
        return jsonify({'message': 'Invalid product data'}), 400

    new_product = Product(name=name, price=price)
    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': 'Product added successfully'}), 201

# Маршрут для удаления продукта по его id


@app.route('/delete_product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({'message': 'Product not found'}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({'message': 'Product deleted successfully'}), 200

# Маршрут для редактирования продукта по его id


@app.route('/edit_product/<int:id>', methods=['PUT'])
def edit_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({'message': 'Product not found'}), 404

    data = request.get_json()
    name = data.get('name')
    price = data.get('price')

    if not name or not price:
        return jsonify({'message': 'Invalid product data'}), 400

    product.name = name
    product.price = price
    db.session.commit()


# Открываем файл products.json и добавляем продукты в базу данных
with open('../backend/products.json', 'r') as file:
    products_data = json.load(file)

for product_data in products_data:
    name = product_data.get('name')
    price = product_data.get('price')

    if name and price:
        new_product = Product(name=name, price=price)
        db.session.add(new_product)

db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)
