"""
reasoning.py

Reasoning Engine component
"""

import random
import fastText.FastText as ff

# greetings=["hello", "hi", "hey"]
# bookings=["book", "purchase", "buy", "ticket", "booking"]
# delays=["delay", "late", "missing", "waiting", "predict", "prediction"]
# helper=["help", "how"]
# staff=["staff"]

acceptances=["yes", "y", "continue"]
rejections=["no", "n", "stop", "bye", "quit", "exit"]

def reason_standard(sentence):  

    # classifier.save_model('model.m') # 保存模型  
    classifier = ff.load_model('data\model.m') # 载入已经训练好的模型
    # test = classifier.test('data\intent_small_valid.txt',1) # 输出测试结果  
    pre = classifier.predict(sentence,1)[0] #输出改文本的预测结果 
    intent = pre[0]

    #if not set (tokens).isdisjoint(greetings):
     #   return "greeting"
    #elif not set (tokens).isdisjoint(bookings):
    #    return "booking"
    #elif not set (tokens).isdisjoint(delays):
    #    return "delay"
    #elif not set (tokens).isdisjoint(staff):
    #    return "staff"
    #elif not set (tokens).isdisjoint(helper):
    #    return "help"

    return intent

def reason_should_quit(tokens):
    if not set (tokens).isdisjoint(acceptances):
        return False
    elif not set (tokens).isdisjoint(rejections):
        return True
    
    print("Chatbot: I'm sorry, I can't understand you. Quitting.")
    return True