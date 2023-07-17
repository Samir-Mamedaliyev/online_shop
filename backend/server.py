import mysql.connector
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/internet_store'
db = SQLAlchemy(app)

with app.app_context():
    try:
        # db.session.execute('SELECT 1')
        db.session.execute(text('SELECT 1'))
        print('\n\n----------- Connection successful !')
    except Exception as e:
        print('\n\n----------- Connection failed ! ERROR : ', e)


class Product(db.Model):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    price = Column(Integer)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


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


if __name__ == "__main__":
    app.run(debug=True)
