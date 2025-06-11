from flask import Blueprint,request,session,render_template,redirect,url_for
from model import db,User
from api.login import login_api



regsiter_route = Blueprint("regsiter_route",__name__,url_prefix="/register")
regsiter_route.register_blueprint(login_api)


@regsiter_route.route('/',methods=['GET','POST'])
def regsiter():
    if request.method =='POST':
        username = request.form['username']
        password = request.form["password"]
        if User.query.filter_by(user_account=username).first():
            return "帳號已存在，請回上一頁"
        user = User(user_account=username, user_password=password,role="normal")
        db.session.add(user)
        db.session.commit()
        db.session.close()
        return redirect('/login')
    return render_template('register.html')