
# import json
# import io

# # 数据来源：
# # 从github下载rasa_nlu项目的repo， 使用`rasa_nlu/test_models/test_model_mitie/training_data.json`

# # 1. 从json文件读入数据
# name = 'data/testing_dataset_1547394831.json'
# with io.open(name, encoding="utf-8-sig") as f:
#     data = json.loads(f.read())

# labels, texts = [], []

# # 2. 从json格式的数据提取intent和text
# for eg in data['rasa_nlu_data']['common_examples']:
#     texts.append(eg['text'])
#     labels.append('__label__'  + eg['intent'])

# # 3. 将数据分割成 training数据 和 heldout(又名validation)数据
# with open('data/intent_small_train.txt', 'w') as f_tr:
#     with open('data/intent_small_valid.txt', 'w') as f_val:
#         for i in range(len(labels)):
#             if i==0 or labels[i]!=labels[i-1]:
#                 f_val.write(labels[i] + ' ' + texts[i]+'\n')
#             else:
#                 f_tr.write(labels[i] + ' ' + texts[i]+'\n')

# # 4. 打印数据，直观了解

# print('所有的 intent:')
# print(set([x[9:] for x in labels]))
# print('\n')

# print('所有的 (intent, text) 样本:')
# xs = sorted([(labels[i], texts[i]) for i in range(len(labels))])

# for i in range(len(labels)):
#     print('\t%s : %s' % (xs[i][0][9:], xs[i][1]))



import fastText.FastText as ff
# lr = 0.05
# dim = 10
# classifier = ff.train_supervised(input= 'data/intent_small_train.txt',
#                                  dim = dim,
#                                  lr = lr,
#                                  epoch = 50,
#                                 label='__label__')
                               
# classifier.save_model('model.m')
classifier = ff.load_model('model.m')
# test = classifier.test('data\intent_small_valid.txt',1)   
pre = classifier.predict('i want to get some suggestion about the blockage between station and station2',1) 
pre2 = classifier.predict('what is the matter with the london and Norwich',1)
pre3 = classifier.predict('i want to know the new arrival time between London and Norwich from Morgate',1)
pre4=classifier.predict('how delayed is the train between London and Norwich form york',1) 
pre5 =classifier.predict('delay between London and Norwich form york ',1)  
print(pre[0][0])
print(pre2[0][0])
print(pre3[0][0])
print(pre4[0][0])
print(pre5[0][0])
# # classifier = ft.train_supervised('data/intent__train.txt')
# # result_tr = classifier.test('data/intent__train.txt')[1]
# # result_val = classifier.test('data/intent__valid.txt')[1]
# # print(result_tr)
# # print(result_val)
# # print(classifier.predict(["when will my train arrive"], k=3))
