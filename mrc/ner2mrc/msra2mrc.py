# encoding: utf-8

import os
#from ..utils import Tag
import json
import re

class Tag(object):
    def __init__(self, term, tag, begin, end):
        self.term = term
        self.tag = tag
        self.begin = begin
        self.end = end

    def to_tuple(self):
        return tuple([self.term, self.begin, self.end])

    def __str__(self):
        return str({key: value for key, value in self.__dict__.items()})

    def __repr__(self):
        return str({key: value for key, value in self.__dict__.items()})


def trans_tag(term):
    if term == "name":
        return "名字"
    elif term == "location":
        return "地點"
    elif term == "time":
        return "時間"
    elif term == "contact":
        return "聯絡方式"
    elif term == "ID":
        return "編號"
    elif term == "profession":
        return "職業"
    elif term == "biomarker":
        return "個人生物標誌"
    elif term == "family":
        return "家庭成員"
    elif term == "clinical_event":
        return "有名的臨床事件"
    elif term == "special_skills":
        return "特殊專業或技能"
    elif term == "unique_treatment":
        return "獨家或聞名的治療方法"
    elif term == "account":
        return "帳號"
    elif term == "organization":
        return "所屬團體"
    elif term == "education":
        return "就學經歷或學歷"
    elif term == "money":
        return "金額"
    elif term == "belonging_mark":
        return "所屬品的特殊標誌"
    elif term == "med_exam":
        return "報告數值"
    elif term == "others":
        return "其他"

def getdocID(tag_idx,origin_count,qid):
    if qid == None:
        return f"{origin_count}.{tag_idx}"
    else:
        return f"{qid}.{tag_idx}"

def convert_file(input_file, output_file, tag2query_file):
    """
    Convert MSRA raw data to MRC format
    """
    origin_count = 0
    new_count = 0
    tag2query = json.load(open(tag2query_file))
    mrc_samples = []
    
    f = open(input_file,encoding='utf-8')
    whole_text = f.read()
    texts_list = whole_text.split('--------------------\n')
    
    for text in texts_list[:-1]:
        
        origin_count += 1
        
        if 'test' not in input_file:
            seg = text.split('article_id\tstart_position\tend_position\tentity_text\tentity_type\n')
            src = ' '.join(seg[0]).strip()
            tags = seg[1].split('\n')
            qid = None
        else:
            text = text.strip()
            t = re.split('article_id: (\d+)\n',text)
            src = ' '.join(t[2])
            tags = []
            qid = t[1]

        all_tags = list(tag2query.keys())
        is_Tags = []
        for t in tags:
            t = t.split('\t')
            if t[0] == '':
                continue
            start_pos = int(t[1])
            end_pos = int(t[2])-1
            tag = t[4]
            tag = trans_tag(tag) 
            is_Tags.append(Tag(src,tag,start_pos,end_pos))
        
        tag_idx = 0
        
        for label, query in tag2query.items():
            mrc_samples.append(
                {
                    "context": ' '.join(src),
                    "start_position": [tag.begin for tag in is_Tags if tag.tag == label],
                    "end_position": [tag.end for tag in is_Tags if tag.tag == label],
                    "query": query,
                    "qas_id": getdocID(tag_idx=tag_idx,origin_count=origin_count,qid=qid)
                }
            )
            new_count += 1
            tag_idx += 1

    json.dump(mrc_samples, open(output_file, "w"), ensure_ascii=False, sort_keys=True, indent=2)
    print(f"Convert {origin_count} samples to {new_count} samples and save to {output_file}")


def main():
    msra_raw_dir = "zh_mrc/reformat80/"
    msra_mrc_dir = "zh_mrc/reformat80/mrc_format"
    tag2query_file = "queries/zh_mrc.json"
    os.makedirs(msra_mrc_dir, exist_ok=True)
    #for phase in ["train", "dev", "test"]:
    for phase in ["test"]:
    #for phase in ["test_sample"]:
        old_file = os.path.join(msra_raw_dir, f"{phase}.txt")
        new_file = os.path.join(msra_mrc_dir, f"mrc-ner.{phase}")
        convert_file(old_file, new_file, tag2query_file)


if __name__ == '__main__':
    main()
