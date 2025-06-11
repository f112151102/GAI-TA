# -*- coding: utf-8 -*-
"""
Created on Sun Jun  8 14:05:53 2025

@author: User
"""

text ="時間複雜度"





def Class_Quiz(text):
    key_dict = {
        "單元一" : ["演算法","時間複雜度","bigO"],
        "單元二" : ["陣列","陣列表示方法","矩陣","多項式表示法","三角形表示法"],
        "單元三" : ["堆疊","佇列","stack","queue","後序表示式","前序表示式"],
        "單元四" : ['樹', 'BST', '遍歷', '節點',"Heap"]
        }
    for category,words in key_dict.items():
        if any(word in text for word in words):
            return category
    return "未確定單元"


class_name = Class_Quiz(text)
#print(class_name)
            

