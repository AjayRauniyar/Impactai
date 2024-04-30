import os
from flask import Flask, request, redirect, url_for, render_template, flash, send_file, jsonify
from werkzeug.utils import secure_filename
import pandas as pd
import pdfplumber
from io import BytesIO
import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'xls', 'xlsx', 'pdf'}  # Allowed file types

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            if filename.endswith('.pdf'):
                return convert_to_excel(file_path)
            elif filename.endswith(('.xls', '.xlsx')):
                return redirect(url_for('column_select', filename=filename))
    return render_template('index.html')

@app.route('/select_column/<filename>', methods=['GET', 'POST'])
def column_select(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_excel(file_path, header=1)
    column_data = None
    search_value = None
    if request.method == 'POST':
        search_value = request.form['column_name'].upper()
        if search_value in df.columns:
            column_data = df[[search_value]].to_html(classes='table table-striped', border=0, index=False)
        else:
            flash('Column not found.', 'error')
    return render_template('excel.html', columns=df.columns, column_data=column_data, column_name=search_value)

def convert_to_excel(filepath):
    excel_filename = os.path.splitext(os.path.basename(filepath))[0] + '.xlsx'
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], excel_filename)
    with pdfplumber.open(filepath) as pdf:
        all_text = []
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text.append(text.split('\n'))
        df = pd.DataFrame(all_text)
        df.to_excel(output_path, index=False)
    return send_file(output_path, as_attachment=True)

@app.route('/iliteracy')
def iliteracy():
    return render_template('iliteracy.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/excel')
def excel():
    return render_template('excel.html')

@app.route('/getstory', methods=['POST'])
def get_story():
    data = {
        "contents": [
            {"parts": [{"text": request.json['story_prompt']}]}
        ]
    }
    headers = {
        'Content-Type': 'application/json'
    }
    api_key = 'AIzaSyBz2-4AHBls9DqmuZZ6qpHoFyZ0S16BxIk'  # Replace with your actual API key
    response = requests.post(
        'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + api_key,
        headers=headers,
        json=data
    )
    return jsonify(response.json())

@app.route('/getstory2', methods=['POST'])
def get_story2():
    data = {
        "contents": [
            {"parts": [{"text": request.json['story_prompt']}]}
        ]
    }
    headers = {
        'Content-Type': 'application/json'
    }
    api_key = 'AIzaSyBz2-4AHBls9DqmuZZ6qpHoFyZ0S16BxIk'  # Replace with your actual API key
    response = requests.post(
        'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + api_key,
        headers=headers,
        json=data
    )
    return jsonify(response.json())

@app.route('/getstory3', methods=['POST'])
def get_story3():
    data = {
        "contents": [
            {"parts": [{"text": request.json['story_prompt']}]}
        ]
    }
    headers = {
        'Content-Type': 'application/json'
    }
    api_key = 'AIzaSyBz2-4AHBls9DqmuZZ6qpHoFyZ0S16BxIk'  # Replace with your actual API key
    response = requests.post(
        'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + api_key,
        headers=headers,
        json=data
    )
    return jsonify(response.json())


if __name__ == "__main__":
    app.run(debug=True)
