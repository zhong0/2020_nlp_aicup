
from pytorch_lightning import Trainer
import torch
from tokenizers import BertWordPieceTokenizer
import os
from trainer import BertLabeling
from metrics.functional.query_span_f1 import extract_flat_spans
import json

f = open("result1222.tsv",'w',encoding='utf-8')
lookup = json.load(open("ner2mrc/queries/zh_mrc_idx18.json"))
#test_data = json.load(open("convert_testid.json"))
test_data = json.load(open("convert_testid.json"))
#test_data = json.load(open("debug_use/convert_sample_testid.json"))

def find_str(s, char, i=0):
    index = i
    if char in s:
        for ch in range(index,len(s)):
            if s[ch:ch+len(char)] == char:
                return ch

def inference(ckpt, hparams_file, file=None):
    """main"""
    model = BertLabeling.load_from_checkpoint(
        checkpoint_path=ckpt,
        hparams_file=hparams_file,
        map_location=None,
        batch_size=1,
        max_length=128,
        workers=0
    )
    loader = model.get_dataloader("test")#, limit=1000)
    tokenizer = BertWordPieceTokenizer(os.path.join(model.bert_dir, "vocab.txt"))
    seg_num = 0 # alignment for origin segmented sentnce/ lookup list of same sample_id
    sample_num = 0 
    before = 0
    i = 0 # num of type 
    for batch in loader:
        tokens, token_type_ids, start_labels, end_labels, start_label_mask, end_label_mask, match_labels, sample_idx, label_idx = batch
        #f.write(str(int(sample_idx))+str(int(label_idx))+'\n')
        #if int(sample_idx) < 38:
        #    continue
        attention_mask = (tokens != 0).long()
        start_logits, end_logits, span_logits = model(tokens, attention_mask, token_type_ids)
        start_preds, end_preds = (start_logits > 0).squeeze(), (end_logits > 0).squeeze()

        match_preds = (span_logits > 0).squeeze()
        token_type_ids = token_type_ids[0].tolist()
        output = extract_flat_spans(start_preds, end_preds, match_preds, token_type_ids)
        tokens = tokens[0].tolist()
        #f.write(tokenizer.decode(tokens, skip_special_tokens=False))
        
        sent_tokens = []
        pivot = 0 # for minus length of question
        
        if int(i/18) == 1:
            seg_num += 1
            before += len(original_text)
            i = 0

        if int(sample_idx) != sample_num:
            sample_num += 1
            print(sample_num)
            before = 0
            seg_num = 0

        for ts in range(len(tokens)):
            if token_type_ids[ts] != 0:
                sent_tokens.append(tokens[ts])
                #break
            else:
                pivot += 1
        #f.write(tokenizer.decode(sent_tokens,skip_special_tokens=False)+'\n') 
        #print(str(int(sample_idx)),file=file)
        original_text = test_data[str(int(sample_idx))][seg_num] 
        #f.write(original_text)
        off = tokenizer.encode(original_text).offsets
        #f.write(original_text)
        #tt = tokenizer.decode(sent_tokens,skip_special_tokens=True).replace(' ','')
        #print(tt)
        #line = str(sample_idx) + ' ' + str(label_idx) + ' ' + str(seg_num)
        
        #f.write(line+'\n')
        #f.write(original_text+'\n')
        
        for start, end in output:
            s = start - pivot + 1
            #ss = s + before
            e = end - pivot + 1
            #ee = e + before
            #tt = tokenizer.decode(sent_tokens[s:e],skip_special_tokens=True).replace(' ','')
            #f.write("word: "+tt+'\n')
            wbs,wes = off[s][0], off[e-1][1]
            ss = wbs + before
            ee = wes + before
            #print("tokenizer: ",tt)
            #print("original text: ",)
            #t = test_data[str(sample_idx)][seg_num]
            line = str(int(sample_idx)) + '\t' + str(ss) + '\t' + str(ee) + '\t' + original_text[wbs:wes]  + '\t' + lookup[str(int(label_idx))] + '\n'
            #print(line)
            f.write(line)
            #f.write(str(i) + ' ' + str(ss) + ' '+str(ee))
        #before += len(original_text)
        i += 1
        #f.write(str(i)+'\n')
if __name__ == '__main__':
    # zh_msra
    CHECKPOINTS = "ner2mrc/zh_mrc/zh_mrc_bertlarge_lr8e-620201209_dropout0.2_bsz16_maxlen128/epoch=19_v0.ckpt"
    HPARAMS = "ner2mrc/zh_mrc/zh_mrc_bertlarge_lr8e-620201209_dropout0.2_bsz16_maxlen128/lightning_logs/version_0/hparams.yaml"

    inference(ckpt=CHECKPOINTS, hparams_file=HPARAMS, file=f)
