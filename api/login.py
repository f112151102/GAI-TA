from flask import Blueprint,request,session,render_template,redirect,url_for
from model import db,User,Login_in_out_time
from api.chat import chat_route


login_api = Blueprint('log_api',__name__,url_prefix="/login")
login_api.register_blueprint(chat_route)

@login_api.route("/",methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        pwd = request.form['password']
        
        user = User.query.filter_by(user_account=user_name).first()
        if user and (user.user_password == pwd):
            session['user_id'] = user.id
            session['username'] = user.user_account
            login_time=Login_in_out_time(
                user_id = user.id,
                user_account =user.user_account,
                user_staute ="login_in"
            )
            db.session.add(login_time)
            db.session.commit()
            return redirect('/chat')
    return render_template('login.html')
    