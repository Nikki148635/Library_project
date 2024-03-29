from flask import Flask, render_template, request, jsonify
import mysql.connector
import json

app = Flask(__name__)

DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Abhishek@123',
    'database': 'nikki_db',
    'auth_plugin' : 'mysql_native_password'
}

@app.route('/data')
def get_data():
    try: