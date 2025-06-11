import os
import openai
import time
from dotenv import load_dotenv


from api.classquiz import Class_Quiz
from flask import session
from model import db,Quiz,QuizClass
from sqlalchemy import func


api_key = os.getenv("openai_api_key")

openai.api_key = api_key


def GAI_Answer(text):
    input_text = f"請告訴我{text}的答案"
    for attempt in range(3):
        try:
            response = openai.ChatCompletion.create(
                model="ft:gpt-3.5-turbo-1106:personal:dsv2:AxcAkv9L",  # 此為微調後的模型
                messages=[
                    {"role": "user", "content": input_text}  # content 內輸入要問的問題
                    ],
                max_tokens=2000,   # GPT-3.5 turbo 最高 token 為 4096
                temperature=0.7,   # 控制輸出的隨機性:0~1, 數字越低，輸出結果會越保守、越直接
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )   
            return response["choices"][0]["message"]["content"]
            break
        except openai.error.APIError as e:
            print(f"⚠️ API Error: {e}")
            time.sleep(2)

def GAI_QUIZ(text):
    p=5
    input_text = f"請以「{text}」為主，產生 {p}個不同衍生問法比如說「堆疊pop的作法」生成「堆疊pop的建立方式」…等答案相同但題目敘述不同的題目 。並避免重復"
    system_prompt =''' 你是一位問答設計專家，根據指定主題設計多個問題。

請嚴格遵守以下規則：
1. 所有問題必須與主題密切相關，並且具有正確且明確的答案。
2. 僅需產出問題本身，**不要加入任何編號（如 Q1、Q2）、標點提示、說明或對話語氣**。
3. 不得出現「Quiz」、「你知道嗎」、「是否了解」等語句。
4. 每題獨立一行，每題需涵蓋不同的觀點或層面。
5. 開頭不要出現 1.,2.…等

--- 僅輸出問題文字，範例如下 ---
在堆疊中執行 push 操作會將元素放在哪裡？
什麼情況下 push 操作會導致堆疊溢出？
堆疊的 push 操作與 pop 操作在方向上有何不同？
'''
    for attempt in range(3):
    # 呼叫微調後的模型進行對話生成
        try:
            response = openai.ChatCompletion.create(
            model="ft:gpt-3.5-turbo-1106:personal:dsv2:AxcAkv9L",  # 此為微調後的模型
                messages=[
                {"role" :"system","content":system_prompt},
                {"role": "user", "content": input_text}  # content 內輸入要問的問題
                ],
                max_tokens=4000,   # GPT-3.5 turbo 最高 token 為 4096
                temperature=0.7,   # 控制輸出的隨機性:0~1, 數字越低，輸出結果會越保守、越直接
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            return response["choices"][0]["message"]["content"]
            break
        except openai.error.APIError as e:
            print(f"⚠️ API Error: {e}")
            time.sleep(2)


def Add_New_Quiz():
    quiz_title_list = db.session.query(Quiz.Quiz_title).all()
    for quizs in quiz_title_list:
        quiz = quizs[0]
        quiz_query  = Quiz.query.filter_by(Quiz_title=quiz).first()
        count = db.session.query(func.count()).select_from(Quiz).filter_by(answer=quiz_query.answer).scalar()
        if count>3:
            pass
        else:
            new_quiz_text = GAI_QUIZ(quiz)
            if new_quiz_text ==None:
                print("api error",flush=True )
                return "api error"
            split_text = new_quiz_text.split('\n')
            
            for line in split_text:
                if(len(line)==0):
                    pass
                else:
                    new_quiz=Quiz(Quiz_class =quiz_query.Quiz_class ,Quiz_title=line,answer=quiz_query.answer)
                    db.session.add(new_quiz)

    db.session.commit()

    
def GPT_AI(text):
    quiz = Quiz.query.filter_by(Quiz_title = text).first()
   
    if quiz :
        if quiz.error_check ==0:
            answer = "以儲存錯誤訊息，感謝您的回報，經過下次更新後再給予您新的答案"
        else:
            answer = quiz.answer 
    else:
        quiz_class=Class_Quiz(text)
        class_id = QuizClass.query.filter_by(class_name =quiz_class).first()
        print(text,flush=True)
        answer = GAI_Answer(text)
        if answer ==None:
            answer = "API 錯誤，請稍等在試一次"
        if class_id:
            new_quiz=Quiz(Quiz_class =class_id.id,Quiz_title =text,answer = answer)
        else :
             class_name = QuizClass(class_name = quiz_class)
             db.session.add(class_name)
             db.session.commit()
             class_id = QuizClass.query.filter_by(class_name =quiz_class).first()
             new_quiz=Quiz(Quiz_class =class_id.id,Quiz_title =text,answer = answer, error_check = 1)
        
        Add_New_Quiz()
        db.session.add(new_quiz) 
        db.session.commit()
    
    db.session.close()
    return answer


    #GPT_AI(text)
#Add_New_Quiz()