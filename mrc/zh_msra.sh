#export PYTHONPATH="$PWD"
#export TOKENIZERS_PARALLELISM=false
DATA_DIR="ner2mrc/zh_mrc/reformat80/mrc_format"
BERT_DIR="chinese_roberta_wwm_large_ext_pytorch/"
SPAN_WEIGHT=0.1
DROPOUT=0.2
LR=6e-6
MAXLEN=128
MAXNORM=1.0
#WARMUP=5000
OUTPUT_DIR="ner2mrc/zh_mrc/zh_mrc_bertlarge_lr${LR}20201215_dropout${DROPOUT}_bsz16_maxlen${MAXLEN}"

mkdir -p $OUTPUT_DIR

python trainer.py \
--chinese \
--data_dir $DATA_DIR \
--bert_config_dir $BERT_DIR \
--max_length $MAXLEN \
--batch_size 4 \
--precision=16 \
--gpus='1' \
--progress_bar_refresh_rate 1 \
--lr ${LR} \
--val_check_interval 0.5 \
--accumulate_grad_batches 1 \
--default_root_dir $OUTPUT_DIR \
--mrc_dropout $DROPOUT \
--max_epochs 20 \
--weight_span $SPAN_WEIGHT \
--span_loss_candidates "pred_and_gold"
--gradient_clip_val $MAXNORM
--final_div_factor 20
#--warmup_steps $WARMUP
