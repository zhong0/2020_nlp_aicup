from simpletransformers.ner import NERModel
import pandas as pd
import logging
import re
import json
import os
from tqdm import tqdm
import random
from opencc import OpenCC


logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

f = open('train_2.txt', 'r')
words = f.read()
word_list = words.split('--------------------\n\n')

my_map = {'name':'名字', 'location':'地點', 'time':'時間', 'contact':'聯絡方式', 'id':'編號', 
    'profession':'職業', 'biomarker':'個人生物標誌', 'family':'家庭成員', 'clinical_event':'有名的臨床事件',
    'special_skills':'特殊專業或技能', 'unique_treatment':'獨家或聞名的治療方法', 'account':'帳號', 
    'organization':'所屬團體', 'education':'就學經歷或學歷', 'money':'金額', 'belonging_mark':'所屬品的特殊標誌',
    'med_exam':'報告數值', 'others':'其他'}
inv_map = {v: k for k, v in my_map.items()}



def split_conser_label(input_list):
    # input word_list
    convers = []
    label = []
    for i in input_list:
        j = i.split('\n', 1)
        if len(j[0]) > 0:
            convers.append(j[0])
        if len(j[1].split('\n\n')[0]):
            label.append(j[1].split('\n\n')[0])
    return convers, label


def label_to_dict(input_label_list):
    # input label
    dict_label = {}
    for i in range(len(input_label_list)):
        total_label = input_label_list[i].split('\n')
        dict_label.update({i : dict()})
        for j in range(len(total_label)-1):
            each_row = total_label[j+1].split('\t')
            duration = (int(each_row[2]) - int(each_row[1]))
            for q in range(duration):
                # origin_label = each_row[4].lower()
                # chinese_label = my_map[origin_label]
                dict_label[i].update({int(each_row[1])+q : each_row[4]})
    return dict_label




def fit_ner_form(input_con, input_label_dict):
    #input convers dict_label
    list_sentence_id = []
    list_words = []
    list_labels = []

    for i in range(len(input_con)):
        now = input_con[i]
        for j in range(len(now)):
            if j in input_label_dict[i].keys():
                list_sentence_id.append(i)
                list_words.append(now[j])
                list_labels.append(input_label_dict[i][j])
            else:
                list_sentence_id.append(i)
                list_words.append(now[j])
                list_labels.append('O')
    return list_sentence_id, list_words, list_labels



convers, label = split_conser_label(word_list)
print('done convers, label')
dict_label = label_to_dict(label)
print('done dict_label')
list_sentence_id, list_words, list_labels = fit_ner_form(convers, dict_label)
print('done list_sentence_id')

train_df = pd.DataFrame({'sentence_id':list_sentence_id, 'words':list_words, 'labels':list_labels})


count__ = 0
word_len = 0
list_warn = []
def split_sentence(row):
    global count__, word_len, list_warn
    word_len+=1
    if row.words in ['。', '？', '！', '，'] and word_len > 20:
        list_warn.append(word_len)
        if word_len > 128:
            print(count__)
        count__+=1
        word_len = 0
        return (count__ -1)
    else:
        return count__

train_df['sentence_id'] = train_df.apply(split_sentence, 1)
cc = OpenCC('t2s')
train_df['words'] = train_df['words'].apply(lambda x: cc.convert(x))

print(train_df.head())



label_list = list(set(train_df.labels.values))
print(label_list)



model = NERModel('bert', 'bert-base-chinese', 
    labels=label_list, args={'train_batch_size':16, 'overwrite_output_dir': True, 'output_dir':'output/ner/bert_Simplified', 'reprocess_input_data': True, 'num_train_epochs': 15})
# Train the model

#/home/jjlai/nas_home/aidea_med_context/RoBERTa/
model.train_model(train_df)
# Train the model


g = open('test.txt', 'r')
words = g.read()
word_list = words.split('--------------------\n\n')

def test_file_form(test_input):
    # word_list
    id_ = []
    string_ = []
    num = 0
    for i in test_input:
        #print(i)
        if len(i) > 0:
            #print('test',i)
            sequence = i.split('\n')[1]
            #print(sequence)
            whole_split_sent = re.split('(。|？|！|，)', sequence)
            for j in range(len(whole_split_sent)):
                if whole_split_sent[j] not in ['。','？','！','，']:
                    if len(whole_split_sent[j])>0:
                        id_.append(i.split('\n')[0].split(' ')[1])
                        string_.append(' '.join(whole_split_sent[j]))
                        num+=1
                else:
                    string_[num-1] += f' {whole_split_sent[j]}'
                    
    return id_, string_

id_, string_ = test_file_form(word_list)
test_df = pd.DataFrame({'sentence_id':id_, 'words':string_})

print(test_df.head())
print(f'len test_df : {len(test_df)}')


temp_id = []
temp_sent = []
trans_id = []
trans_sent = []

for i in range(len(test_df)):
    if len(temp_id)==0 and len(temp_sent)==0:
        if len(test_df.iloc[i]['words']) > 20:
            trans_id.append(test_df.iloc[i]['sentence_id'])
            trans_sent.append(test_df.iloc[i]['words'])
        else:
            temp_id.append(test_df.iloc[i]['sentence_id'])
            temp_sent.append(test_df.iloc[i]['words'])
    else:
        if temp_id[0] == test_df.iloc[i]['sentence_id']:
            now_sent = temp_sent[0] +' '+ test_df.iloc[i]['words']
            if len(now_sent) > 20:
                trans_id.append(test_df.iloc[i]['sentence_id'])
                trans_sent.append(now_sent)
                temp_id = []
                temp_sent = [] 
                now_sent = ''
            else:
                temp_sent = [now_sent]
        else:
            trans_id.append(temp_id[0])
            trans_sent.append(temp_sent[0])
            temp_id = [test_df.iloc[i]['sentence_id']]
            temp_sent = [test_df.iloc[i]['words']]


if len(temp_id)>0 and len(temp_sent)>0:
    trans_id.append(temp_id[0])
    trans_sent.append(temp_sent[0])

test_df = pd.DataFrame({'sentence_id':trans_id, 'words':trans_sent})
test_df['words'] = test_df['words'].apply(lambda x: cc.convert(x))


print(test_df.head())
print(f'len test_df : {len(test_df)}')

# Predictions on arbitary text strings
predictions, raw_outputs = model.predict(test_df.words.values)
#print(predictions)

test_df['predict'] = predictions
test_df['raw_outputs'] = raw_outputs

df = test_df

num = 0
sentence_id = []
words = []
predictions = []

for i in range(len(df)):
    if i==0:
        sentence_id.append(df.iloc[i]['sentence_id'])
        words.append(df.iloc[i]['words'])
        predictions.append(eval(df.iloc[i]['predict']))
    else:
        if df.iloc[i]['sentence_id'] == sentence_id[num]:
            words[num]+= ' '+ df.iloc[i]['words']
                #print(words[num])
                #print(predictions[num])
            predictions[num].extend((eval(df.iloc[i]['predict'])))
        else:
            sentence_id.append(df.iloc[i]['sentence_id'])
            words.append(df.iloc[i]['words'])
            predictions.append(eval(df.iloc[i]['predict']))
            num+=1
df = pd.DataFrame({'sentence_id':sentence_id, 'words':words, 'predictions':predictions})
print(len(df))

art_id = []
order_ = []
word_ = []
label_ = []

for i in range(len(df)):
    now = df.iloc[i]['predictions']
    for j in range(len(now)):
        if 'O' not in now[j].values():
            art_id.append(i)
            order_.append(j)
            for k, v in now[j].items():
                word_.append(k)
                label_.append(v)
                #label_.append(v.split('-')[1])

print(len(pd.DataFrame({'art_id':art_id, 'order_':order_, 'word_':word_, 'label_':label_})))


total = len(art_id)
i = 0
j = 0

article_id = []
start_position = []
end_position = []
entity_text = []
entity_type = []

# 'art_id':art_id, 'order_':order_, 'word_':word_, 'label_':label_
while i<total:
    if i == 0:
        article_id.append(art_id[i])
        start_position.append(int(order_[i]))
        end_position.append(int(order_[i])+1)
        entity_text.append(word_[i])
        entity_type.append(label_[i])
        i+=1
    else:
        if article_id[j] == art_id[i] and end_position[j] == int(order_[i]) and entity_type[j] == label_[i]:
            end_position[j] = int(order_[i])+1
            entity_text[j] += word_[i]
            i+=1
        else:
            article_id.append(art_id[i])
            start_position.append(int(order_[i]))
            end_position.append(int(order_[i])+1)
            entity_text.append(word_[i])
            entity_type.append(label_[i])
            i+=1
            j+=1
df = pd.DataFrame({'article_id':article_id, 'start_position':start_position, 'end_position':end_position,
                  'entity_text':entity_text, 'entity_type':entity_type})
df.to_csv('to_aidea/simplified_bert/bert_Simplified_{only_label}.tsv', sep = '\t', index=None)