# Medical Dialogue Decision: Deidentity Tasks
* The top 25% for 2020 AI CUP Competition

* ### Introduction
  > The project is aim to detect some specific domains during a conversation in clinical. Due to the privacy issues, we can mask the private information to protect the patients after the detection. The contents are described in details on the website: https://aidea-web.tw/topic/d84fabf5-9adf-4e1d-808e-91fbd4e03e6d.

* ### Techniques
  * BERT-NER
    >The NER model was built with SimpleTransformer. The pre-trained model of tokenizer is bert-base-chinese. We figured out that the simplified Chinese has better performance than traditional Chinese. Therefore, we applied OpenCC to acheive the convertion. To generlize the predictions, we conducted twe kinds of NER tasks. One is to train the model in each entity, and the other is with all entities. Then, the results will be combined in the end.

  * BERT-MRC
    >The MRC model, which can solve the similar problems with NER model, was also applied in our project. Differently, The input format is as the form of (Q, A, context). It will return the answer span from the queries which are the domain we need to detect.

  * Regular Expression
    >Some entities are easier to detect with RE, such as the numbers with units, the family members and carriers. Hence, we adopted the methods on these fields.

  * Bagging
    >Different models have an advantage of themselves. Therefore, we set the priority of those model and combined the results of them.

* ### Supplement
  * Document
    >The document file contains the presentation and final report for NLP course. If wondering the project in details in Chinese, you can check the files there.
