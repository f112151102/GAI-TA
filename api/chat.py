from flask import Blueprint,request,session,render_template,redirect,url_for,request
from model import db,ChatHistory,User,ErrorLog,Quiz
from api.ta import GPT_AI,Add_New_Quiz
from flask import jsonify

chat_route = Blueprint("chat_route",__name__)


def Change_Data(quiz_id):
    query = Quiz.query.get(quiz_id)
    if query !=None:
        query.error_check = 0
        db.session.commit()
    

@chat_route.route("/chat",methods=["GET",'POST'])
def Chat_Page():
    if "user_id" not in session:
        return redirect("/login")
    else:
        return render_template("index.html")

@chat_route.route("/chat_api",methods=['POST'])
def Chat_api():
    user_input = request.json.get('message', '').strip()
    current_user_id = session["user_id"]
    bot_reply = GPT_AI(user_input)
    user_history = ChatHistory(user_id = current_user_id ,user_message = user_input,assistant_message = bot_reply)
    db.session.add(user_history)
    db.session.commit()
    

    return jsonify({'reply': bot_reply})

@chat_route.route("/report-error",methods =["POST"])
def report_error():
    print("test",flush=True)
    data = request.json
    question = data.get('question')
    answer = data.get("answer")
    if not question or not answer:
        return jsonify({"error": "缺少欄位"}), 400
    new_log = ErrorLog(question=question, answer=answer)
    quiz_query = Quiz.query.filter_by(Quiz_title = question).first()
    Change_Data(quiz_query.id)
    try:
        db.session.add(new_log)
        db.session.commit()
        return jsonify({"message": "錯誤已儲存"}), 200
    except Exception as e:
        return jsonify({"error": "資料庫儲存失敗", "detail": str(e)}), 500
