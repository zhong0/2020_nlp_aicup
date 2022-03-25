import re
import pandas as pd
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
                if whole_split_sent[j] not in ['。','？','！', '，']:
                    if len(whole_split_sent[j])>0:
                        id_.append(i.split('\n')[0].split(' ')[1])
                        string_.append(''.join(whole_split_sent[j]))
                        num+=1
                else:
                    string_[num-1] += f'{whole_split_sent[j]}'
                    
    return id_, string_

id_, string_ = test_file_form(word_list)
test_df = pd.DataFrame({'sentence_id':id_, 'words':string_})
test_df_1 = test_df.copy()
print(test_df.head())
print(f'len test_df : {len(test_df)}')

sent_trans = []
id_trans = []
for i in list(set(test_df['sentence_id'].values)):
    id_trans.append(test_df[test_df['sentence_id']==i].iloc[0].sentence_id)
    sent_trans.append(''.join(test_df[test_df['sentence_id']==i]['words'].values))
df_for_test = pd.DataFrame({'id':id_trans, 'words':sent_trans})
df_for_test = df_for_test.sort_values(['id'])
df_for_test

regex = r'A\d{9,10}|B\d{9,10}|C\d{9,10}|D\d{9,10}|E\d{9,10}|F\d{9,10}|G\d{9,10}|H\d{9,10}|I\d{9,10}|J\d{9,10}|K\d{9,10}|L\d{9,10}|M\d{9,10}|N\d{9,10}|O\d{9,10}|P\d{9,10}|Q\d{9,10}|R\d{9,10}|S\d{9,10}|T\d{9,10}|U\d{9,10}|V\d{9,10}|W\d{9,10}|X\d{9,10}|Y\d{9,10}|Z\d{9,10}'
regex_phone = r'09\d{8}|line|LINE|Line|ＬＩＮＥ|EMAIL|MAIL|email|mail|FB|臉書|ＦＢ|Grindr|Hornet|Tinder|tinder|wootalk'
regex_time = r'去年\d+月\d+號|去年\d+月|去年\d+號|去年|明年|正午|清晨|明天|昨天|今天|一個月|兩個月|三個月|一個禮拜|一個星期|兩個禮拜|兩個星期|三個禮拜|三個星期|早上|中午|下午|晚上|一天|兩天|三天|四天|五天|六天|\d+天|\d+月\d+號|\d+月\d+日|\d+個月|\d+年|聖誕節|清明節|情人節|感恩節|端午節|[一二三四五六七八九十]月[一三四五六七八九][日號]'
regex_family = r'我姊姊|我姐姐|我妹妹|我老婆|我太太|我先生|我丈夫|我老公|你爺爺|你姊姊|你姐姐|你妹妹|你老婆|你太太|你先生|你丈夫|你老公|你奶奶|你爸爸|你叔叔|你嬸嬸|你舅舅|你阿姨|你姑姑|你大姑|你二姑|你外婆|你婆婆|你姊|你姐|你妹|你爺|你奶|你爸|你叔|你舅|你嬸|你姨|你姑|你婆|你大女兒|你二女兒|你三女兒|你小女兒|你小女|你大兒子|你二兒子|你三兒子|你小兒子|你兒子|你犬子|我爺爺|我奶奶|我爸爸|我叔叔|我嬸嬸|我舅舅|我阿姨|我姑姑|我大姑|我二姑|我外婆|我婆婆|我爺|我奶|我爸|你姊|你姐|你妹|我叔|我舅|我嬸|我姨|我姑|我婆|我大女兒|我二女兒|我三女兒|我小女兒|我小女|我女兒|我大兒子|我二兒子|我三兒子|我小兒子|我兒子|我犬子|爺爺|奶奶|爸爸|爸|叔叔|阿姨|嬸嬸|嬸|姑姑|大姑|二姑|姑|外婆|姊姊|姐姐|妹妹|老婆|太太|先生|丈夫|老公|婆|老大|老二|老三|大女兒|二女兒|三女兒|小女兒|小女|女兒|大兒子|二兒子|三兒子|小兒子|兒子|犬子'
regex_profession = r'Google'
regex_money = r'\d+塊|\d+元'

df_for_test['ID']=df_for_test['words'].apply(lambda x:re.findall(regex, x))
df_for_test['contact']=df_for_test['words'].apply(lambda x:re.findall(regex_phone, x))
df_for_test['time']=df_for_test['words'].apply(lambda x:re.findall(regex_time, x))
df_for_test['profession']=df_for_test['words'].apply(lambda x:re.findall(regex_profession, x))
df_for_test['money']=df_for_test['words'].apply(lambda x:re.findall(regex_money, x))
df_for_test['family']=df_for_test['words'].apply(lambda x:re.findall(regex_family, x))

article_id = []
start_position = []
end_position = []
entity_text = []
entity_type = []
for i in range(len(df_for_test)):
    # ID
    if len(df_for_test.iloc[i]['ID']) > 0 :
        for j in list(set(df_for_test.iloc[i]['ID'])):
            split_ = df_for_test.iloc[i]['words'].split(j)
            for k in range(len(split_)):
                if k == 0:
                    article_id.append(df_for_test.iloc[i]['id'])
                    start_position.append(len(split_[0]))
                    end_position.append(len(split_[0])+len(j))
                    entity_text.append(j)
                    entity_type.append('ID')
                elif k == (len(split_)-1):
                    pass
                else:
                    article_id.append(df_for_test.iloc[i]['id'])
                    start_position.append(len(''.join(split_[0:k+1]))+(len(j)*k))
                    end_position.append(len(''.join(split_[0:k+1]))+(len(j)*k)+len(j))
                    entity_text.append(j)
                    entity_type.append('ID')
                    

    if len(df_for_test.iloc[i]['contact']) > 0 :
        for j in list(set(df_for_test.iloc[i]['contact'])):
            split_ = df_for_test.iloc[i]['words'].split(j)
            for k in range(len(split_)):
                if k == 0:
                    article_id.append(df_for_test.iloc[i]['id'])
                    start_position.append(len(split_[0]))
                    end_position.append(len(split_[0])+len(j))
                    entity_text.append(j)
                    entity_type.append('contact')
                elif k == (len(split_)-1):
                    pass
                else:
                    article_id.append(df_for_test.iloc[i]['id'])
                    start_position.append(len(''.join(split_[0:k+1]))+(len(j)*k))
                    end_position.append(len(''.join(split_[0:k+1]))+(len(j)*k)+len(j))
                    entity_text.append(j)
                    entity_type.append('contact')
                    

    if len(df_for_test.iloc[i]['time']) > 0 :
        for j in list(set(df_for_test.iloc[i]['time'])):
            split_ = df_for_test.iloc[i]['words'].split(j)
            for k in range(len(split_)):
                if k == 0:
                    article_id.append(df_for_test.iloc[i]['id'])
                    start_position.append(len(split_[0]))
                    end_position.append(len(split_[0])+len(j))
                    entity_text.append(j)
                    entity_type.append('time')
                elif k == (len(split_)-1):
                    pass
                else:
                    article_id.append(df_for_test.iloc[i]['id'])
                    start_position.append(len(''.join(split_[0:k+1]))+(len(j)*k))
                    end_position.append(len(''.join(split_[0:k+1]))+(len(j)*k)+len(j))
                    entity_text.append(j)
                    entity_type.append('time')

                    
    if len(df_for_test.iloc[i]['profession']) > 0 :
        for j in list(set(df_for_test.iloc[i]['profession'])):
            split_ = df_for_test.iloc[i]['words'].split(j)
            for k in range(len(split_)):
                if k == 0:
                    article_id.append(df_for_test.iloc[i]['id'])
                    start_position.append(len(split_[0]))
                    end_position.append(len(split_[0])+len(j))
                    entity_text.append(j)
                    entity_type.append('profession')
                elif k == (len(split_)-1):
                    pass
                else:
                    article_id.append(df_for_test.iloc[i]['id'])
                    start_position.append(len(''.join(split_[0:k+1]))+(len(j)*k))
                    end_position.append(len(''.join(split_[0:k+1]))+(len(j)*k)+len(j))
                    entity_text.append(j)
                    entity_type.append('profession')
                    
    if len(df_for_test.iloc[i]['money']) > 0 :
        for j in list(set(df_for_test.iloc[i]['money'])):
            split_ = df_for_test.iloc[i]['words'].split(j)
            for k in range(len(split_)):
                if k == 0:
                    article_id.append(df_for_test.iloc[i]['id'])
                    start_position.append(len(split_[0]))
                    end_position.append(len(split_[0])+len(j))
                    entity_text.append(j)
                    entity_type.append('money')
                elif k == (len(split_)-1):
                    pass
                else:
                    article_id.append(df_for_test.iloc[i]['id'])
                    start_position.append(len(''.join(split_[0:k+1]))+(len(j)*k))
                    end_position.append(len(''.join(split_[0:k+1]))+(len(j)*k)+len(j))
                    entity_text.append(j)
                    entity_type.append('money')
                    

    if len(df_for_test.iloc[i]['family']) > 0 :
        for j in list(set(df_for_test.iloc[i]['family'])):
            split_ = df_for_test.iloc[i]['words'].split(j)
            for k in range(len(split_)):
                if k == 0:
                    article_id.append(df_for_test.iloc[i]['id'])
                    start_position.append(len(split_[0]))
                    end_position.append(len(split_[0])+len(j))
                    entity_text.append(j)
                    entity_type.append('family')
                elif k == (len(split_)-1):
                    pass
                else:
                    article_id.append(df_for_test.iloc[i]['id'])
                    start_position.append(len(''.join(split_[0:k+1]))+(len(j)*k))
                    end_position.append(len(''.join(split_[0:k+1]))+(len(j)*k)+len(j))
                    entity_text.append(j)
                    entity_type.append('family')

df = pd.DataFrame({'article_id':article_id,
        'start_position':start_position,
        'end_position':end_position,
        'entity_text':entity_text,
        'entity_type':entity_type})

df.article_id = df['article_id'].apply(lambda x : int(x))
df.start_position = df['start_position'].apply(lambda x : int(x))
df = df.sort_values(['article_id', 'start_position'])

df.to_csv('to_aidea/bert/rule_base.tsv', sep = '\t', index=None)