from flask import Flask, jsonify, render_template, request, redirect, url_for
import pyodbc
from decimal import Decimal

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# SQL Server Configuration
server = 'localhost'  # Replace with your server name or IP address
database = 'MyModelsCars'  # Replace with your database name
driver = '{ODBC Driver 17 for SQL Server}'

# Connect to the database
cnxn = pyodbc.connect(
    DRIVER=driver,
    SERVER=server,
    DATABASE=database,
    Trusted_Connection="yes"
)
cursor = cnxn.cursor()

@app.route('/api/data')
def get_data():
    data = {'message': 'This data is from the backend!'}
    return jsonify(data)

# Routes
@app.route('/')
def index():
    # Fetch records from the database
    cursor.execute('SELECT * FROM dbo.MyCars')
    records = cursor.fetchall()
    return render_template('index.html', records=records)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        # Get form data
        model = request.form['model']
        color = request.form['color']
        name = request.form['name']
        manufacture_year = request.form['manufacture_year']
        price = Decimal(request.form['price'])  # Convert to Decimal
        # Call stored procedure to insert data
        cursor.execute('EXECUTE InsertRecord ?, ?, ?, ?, ?', (model, color, name, int(manufacture_year), price))
        cnxn.commit()
        return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    # Delete record from the database
    cursor.execute('DELETE FROM dbo.MyCars WHERE CarID = ?', (id,))
    cnxn.commit()
    return redirect(url_for('index'))


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        # Get form data
        model = request.form['model']
        color = request.form['color']
        name = request.form['name']
        manufacture_year = request.form['manufacture_year']
        price = request.form['price']
        # Update record in the database
        cursor.execute('UPDATE dbo.MyCars SET Model=?, Color=?, Name=?, ManufactureYear=?, Price=? WHERE CarID=?',
                       (model, color, name, manufacture_year, price, id))
        cnxn.commit()
        return redirect(url_for('index'))
    else:
        # Fetch the record to be updated
        cursor.execute('SELECT * FROM dbo.MyCars WHERE CarID = ?', (id,))
        record = cursor.fetchone()
        return render_template('update.html', record=record)



if __name__ == '__main__':
    app.run(debug=True)
