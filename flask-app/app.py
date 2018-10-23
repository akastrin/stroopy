from flask import Flask, request, render_template, jsonify, session, redirect, url_for, flash
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017')
db = client['test1']
col = db['collection1']

app.secret_key = 'abc'

@app.after_request
def remove_if_invalid(response):
    if "__invalidate__" in session:
        response.delete_cookie(app.session_cookie_name)
    return response

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id_number = request.form['id_number']
        sex = request.form['sex']
        age = request.form['age']
        return render_template('index3.html', id_number = id_number, sex = sex, age = age)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
    
#@app.route('/test')
#def test():
#    if session.get('logged_in') is not None:
#        if session['logged_in'] == True:
#            return render_template('index3.html')
#    return redirect(url_for('login'))
    

@app.route('/output', methods=['POST'])
def output():
    json = request.get_json()
    #data = {'logged_in': session['logged_in'], 'id_number': session['id_number'], 'sex': session['sex'], 'age': session['age'], 'data': json}
    data = {'data': json}
    res = col.insert_one(data)
    return redirect(url_for('logout'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
