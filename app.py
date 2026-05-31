from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-inquiry', methods=['POST'])
def submit_inquiry():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form.get('email', '')
        class_name = request.form.get('class', '')
        message = request.form.get('message', '')
        
        print(f"New inquiry received:")
        print(f"  Name: {name}")
        print(f"  Phone: {phone}")
        print(f"  Email: {email}")
        print(f"  Class: {class_name}")
        print(f"  Message: {message}")
        print(f"{'='*50}")

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
