from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

from api.classquiz import Class_Quiz


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True,index=True)
    user_account = Column(String(50),unique=True,nullable=False)
    user_password = Column(String(225),nullable=False)
    role = Column(String(10),nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    chats = relationship("ChatHistory",back_populates="user")

class ChatHistory(db.Model): 
    __tablename__ = "chathistory"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user_message = Column(Text)
    assistant_message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chats")

class QuizClass(db.Model):
    __tablename__ = "quiz_class"
    id =Column(Integer,primary_key=True,index=True)
    class_name = Column(String(20),nullable=False)
    
    quiz = relationship("Quiz",back_populates = "quiz_class" )

class Quiz(db.Model):
    __tablename__ = "quiz"
    id = Column(Integer,primary_key=True,index=True)
    Quiz_class = Column(Integer,ForeignKey("quiz_class.id"))
    Quiz_title =Column(Text,nullable=False)
    answer = Column(Text,nullable=False)
    error_check = Column(Integer)

    quiz_class = relationship("QuizClass",back_populates = "quiz" )

class ErrorLog(db.Model):
    __tablename__ = 'error_log'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Login_in_out_time(db.Model):
    __tablename__ = "login_in_out_time"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    user_account = Column(String(50))
    user_staute = Column(String(10))
    timestamp = Column(DateTime, default=datetime.utcnow) 


def init_db():

    if not User.query.filter_by(user_account="LAB1112").first():
        admin = User(
            user_account="LAB1112",
            user_password="admin", 
            role="admin"
        )
        db.session.add(admin)
    if QuizClass.query.first() is None:
        db.session.add_all(
            [QuizClass(class_name = "單元一"),
            QuizClass(class_name = "單元二"),
            QuizClass(class_name = "單元三"),
            QuizClass(class_name = "單元四")]
            )
    if Quiz.query.first() is None:
        stack_class = QuizClass.query.filter_by(class_name = "單元三").first()
        tree_class = QuizClass.query.filter_by(class_name = "單元四").first()

        db.session.add_all(
            [
                Quiz(Quiz_class = stack_class.id,
                  Quiz_title = "請說明堆疊的基本操作有哪些？",
                  answer = "堆疊的基本操作包括 push (壓入)、pop (彈出) 和 top (取頂)，push 將元素壓入堆疊頂部，pop 將頂部元素彈出，top 則是取得頂部元素但不移除",
                  error_check =1
                  ),
                Quiz(Quiz_class =stack_class.id,
                  Quiz_title = "堆疊在電腦科學中有哪些常見的應用？請舉例說明",
                  answer = "堆疊常用於記憶體管理 (memory management)、遞迴函數 (recursive functions)、編譯器的語法分析 (syntax analysis) 等場合。例如，在遞迴函數中，函數呼叫會產生一個新的堆疊幀 (stack frame)，當函數結束時會將該堆疊幀彈出。",
                  error_check =1
                  ),
                Quiz(Quiz_class = tree_class.id,
                  Quiz_title = "什麼是二元樹，它有哪些特性",
                  answer = "二元樹是一種樹狀結構，每個節點最多有兩個子節點，分別為左子節點和右子節點",
                  error_check =1
                  ),
            ]

        )
    db.session.commit()
    db.session.close()