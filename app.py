from flask import Flask, url_for, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

import os

_basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(_basedir, 'app.db')
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    description = db.Column(db.Text)
    price = db.Column(db.Float)

    def __init__(self, name=None, description=None, price=None):
        self.name = name
        self.description = description
        self.price = price


@app.route('/', methods=['GET', 'POST'])
def product_list():
    if request.method == 'GET':
        return render_template('product_list.html', products=Product.query.all())
    else:
        form = request.form
        db.session.add(Product(form['name'], form['description'], form['price']))
        db.session.commit()
        return redirect(url_for('product_list'))


@app.route('/detail/<int:product_id>')
def product_detail(product_id):
    product = db.session.query(Product).get(product_id)
    return render_template('product_detail.html', product=product)


if __name__ == '__main__':
    manager.run()
