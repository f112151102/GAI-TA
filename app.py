import os
from dotenv import load_dotenv

from flask import Flask, render_template, request, redirect, url_for, session, flash
from sqlalchemy import inspect

from model import db,User,QuizClass,Quiz, init_db,Login_in_out_time
from api.login import login_api
from api.register import regsiter_route
from api.chat import chat_route


load_dotenv()

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


app = Flask(__name__)
app.secret_key = "LAB-1112"

app.register_blueprint(login_api)
app.register_blueprint(regsiter_route)
app.register_blueprint(chat_route)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

with app.app_context():
    #db.drop_all()
    db.create_all()
    init_db()
    '''
    inspector = inspect(db.engine)
    print("Tables in DB:", inspector.get_table_names())'''


@app.route('/')
def index():
    return redirect("/login")


@app.route("/logout")
def logout():
    current_user_id = session["user_id"]
    current_user_name = session['username']
    login_out_time=Login_in_out_time(
                user_id = current_user_id ,
                user_account =current_user_name,
                user_staute ="login_out"
            )
    db.session.add(login_out_time)
    db.session.commit()
    return redirect('/login')

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1000,debug=True)