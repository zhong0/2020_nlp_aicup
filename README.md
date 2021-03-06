# Medical Dialogue Decision: Deidentity Tasks
* The top 25% for 2020 AI CUP Competition

Introduction
----
  > The project is aim to detect specific entities during a conversation in clinical. Then, we can mask the sensitive information to protect the patients' privacy after the detection. The contents are described in details on the website: https://aidea-web.tw/topic/d84fabf5-9adf-4e1d-808e-91fbd4e03e6d. BERT-NER model and BERT-MRC model were constructed for the tasks in our project. However, some entities are easier to detect with regular expression. The results of the models and RegEx would be combined in the bagging process, and the final result would be obtained.

Techniques
----
* ### BERT-NER
  >The NER model was built with Simple Transformers. The pre-trained model of tokenizer is bert-base-chinese. We figured out that the simplified Chinese performs better than the traditional one. Therefore, we applied OpenCC to acheive the translation. To generalize the predictions, we conducted two kinds of NER tasks. One is to train the model for each entity, and the other is for all entities. The results would be combined in the end.

* ### BERT-MRC
  >The MRC model, which can solve the similar problems with NER model, was also applied in our project. Differently, the input format is as the form of (Q, A, context). It will return the answer span from the queries which are the entities we need to detect.

* ### Regular Expression
  >Some entities are easier to detect with RegEx, such as the numbers with units, the family members and occupations. Hence, we adopted the methods to these fields.

* ### Bagging
  >Each method has an advantage of itself. Therefore, we set the priority of those methods and combined the results of them.

Result
----
* ### Public Leaderboard
  * F1-Score: 76.60 %
  * Recall: 82.30 %
  * Precision: 71.63%
* ### Private Leaderboard
  * F1-Score: 78.11 %

Supplement
----
* ### Document
  >The document file contains the presentation and final report for NLP course. If wondering the project in details in Chinese, you can check the files there.
