import random, datetime
from flask import Flask, request, render_template, jsonify, session, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators
from flask_wtf import CSRFProtect
from pymongo import MongoClient

app = Flask(__name__)
app.config.from_pyfile('settings.cfg')
csrf = CSRFProtect(app)
#client = MongoClient('mongodb://localhost:27017')
client = MongoClient(host=app.config['MONGODB_HOST'], port=app.config['MONGODB_PORT'])
db = client[app.config['MONGODB_NAME']]

class RegistrationForm(FlaskForm):
    id_number = StringField('id_number', [validators.DataRequired(), validators.Length(min=1, max=4)])
    sex = SelectField('sex', choices = [('male', 'Moški'), ('female', 'Ženska')])
    age = StringField('age', [validators.DataRequired(), validators.Length(min=2, max=2)])

@app.route('/', methods=['GET', 'POST'])
def login():
    col = db[app.config['MONGODB_COLLECTION_1']]
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        session['log'] =  "andrej"
        if col.find({"data.id" : {'$eq' : int(form.id_number.data)}}).count() == 0:
            flash('Napačna ID šifra!')
            return redirect(url_for('login'))
        elif col.find({"data": {"$elemMatch": {"id":  int(form.id_number.data), "sex": {"$exists": "true"}}}}).count():
            flash('ID šifra že obstaja!')
            return redirect(url_for('login'))
        else:
            my_date = datetime.datetime.now().isoformat()
            session["date"] = my_date
            col.update({"data.id": int(form.id_number.data)},{"$set": {"data.$.sex": form.sex.data}}, upsert=False)
            col.update({"data.id": int(form.id_number.data)},{"$set": {"data.$.age": int(form.age.data)}}, upsert=False)
            col.update({"data.id": int(form.id_number.data)},{"$set": {"data.$.date": my_date}}, upsert=False)
            return render_template('stroopy.html', form=form)
    saved = session.pop('log', None)
    return render_template('login.html', form=form, log=saved)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/output', methods=['POST'])
def output():
    col = db[app.config['MONGODB_COLLECTION_2']]
    json = request.get_json()
    data = {'data': json}
    res = col.insert_one(data)
    return redirect(url_for('logout'))

# db.collection2.drop()
# curl -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/createdb
@app.route('/createdb', methods=['POST'])
@csrf.exempt
def createdb():
    id_list = list(range(1, 100))
    random.shuffle(id_list)
    json = [{'id': x, 'date': None} for x in id_list]
    data = {'data': json}
    col = db[app.config['MONGODB_COLLECTION_1']]
    res = col.insert_one(data)
    return redirect(url_for('logout'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
