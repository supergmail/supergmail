from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request
from threading import Lock

app = Flask(__name__)
app.config['SECRET_KEY'] = 'devilzbotsecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cmfa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db = SQLAlchemy(app)
lock = Lock()
class logins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(800), unique=True)
    password = db.Column(db.String(800))

    def __repr__(self):
        return f'<logins {self.phone}>'

@app.before_first_request
def create_tables():
    db.create_all()



@app.route('/api/addlogins', methods=['POST'])
def addlogins():
    if request.method == 'POST':
        try:
            json = request.get_json()
            phone = json['phone']
            password = json['password']

            addlogins = logins(phone=phone, password=password)
            db.session.add(addlogins)
            db.session.commit()
            return "True"
        except:
            return "False"



@app.route('/api/get', methods=['GET', 'POST'])
def api_get():
    with lock:
        all_data = logins.query.limit(1).all()
        data_list = ''
        for a in all_data:
            data_list = f'{data_list}{a.phone},{a.password}|'
            logins.query.filter_by(phone=a.phone).delete()
        db.session.commit()
        return data_list



if __name__ == '__main__':
    app.run(host="0.0.0.0")
