from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    place = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(50), nullable=False)

    items = db.relationship('QuotationItem', backref='customer', lazy=True)


class QuotationItem(db.Model):
    __tablename__ = 'quotation_items'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

    Product = db.Column(db.String(50), nullable=False)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    area = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    gst = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)

    glass_type = db.Column(db.String(100), nullable=False)
    handle = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(100), nullable=False)
    series = db.Column(db.String(100), nullable=False)
