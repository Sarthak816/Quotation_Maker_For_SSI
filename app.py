from flask import Flask, render_template, request, send_file, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from pdf_generator import generate_pdf
from dashboard import get_all_quotations

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quotations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)

# Models (Could be moved to models.py)
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    contact = db.Column(db.String(20))
    place = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class QuotationItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    product = db.Column(db.String(100))
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    area = db.Column(db.Float)
    price = db.Column(db.Float)
    gst = db.Column(db.Float)
    total = db.Column(db.Float)
    glass_type = db.Column(db.String(50))
    handle = db.Column(db.String(50))
    color = db.Column(db.String(50))
    series = db.Column(db.String(50))

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
def generate():
    name = request.form['name']
    contact = request.form['contact']
    place = request.form['place']
    notes = request.form.get('notes', '')

    customer = Customer(name=name, contact=contact, place=place)
    db.session.add(customer)
    db.session.commit()

    # Fetch dynamic table data
    fields = ['product', 'width', 'height', 'quantity', 'area', 'price', 'gst', 'total', 'glass_type', 'handle', 'color', 'series']
    data = {field: request.form.getlist(f"{field}[]") for field in fields}

    items = []
    for i in range(len(data['product'])):
        item = QuotationItem(
            customer_id=customer.id,
            product=data['product'][i],
            width=int(data['width'][i]),
            height=int(data['height'][i]),
            quantity=int(data['quantity'][i]),
            area=float(data['area'][i]),
            price=float(data['price'][i]),
            gst=float(data['gst'][i]),
            total=float(data['total'][i]),
            glass_type=data['glass_type'][i],
            handle=data['handle'][i],
            color=data['color'][i],
            series=data['series'][i],
        )
        db.session.add(item)
        items.append(item)
    db.session.commit()

    filename = f"{customer.name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join("quotations", filename)
    generate_pdf(customer, items, filepath, notes=notes)

    return send_file(filepath, as_attachment=True)

@app.route('/dashboard')
def dashboard():
    quotations = get_all_quotations()
    return render_template('dashboard.html', quotations=quotations)

@app.route('/delete/<filename>')
def delete_file(filename):
    filepath = os.path.join("quotations", filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
