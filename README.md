# Plain Text Enrichment Using Tweets And Emojis
Team project for Text Analysis and Retrieval course at Faculty of Electrical Engineering and Computing, University of Zagreb, Croatia

## Description

Given the paramount importance of visual icons for providing an additional layer of meaning to social media messages, on one hand, and the indisputable role of Twitter as one of the most important social media platforms, on the other, the project **"Plain Text Enrichment Using Tweets And Emojis"** was created which is based on a competition task **"SemEval-2018 Task 2, Multilingual Emoji Prediction"**.

The task of this project is to make a system that would automatically fill the text with the appropriate emoticons. This can be done in two steps. First, for each position within the text a prediction is made whether an emoticon should be placed there. Second, an appropriate emoticon is chosen from a list of available emoticons. Both these tasks can be set up as supervised classification problems.

As a conclusion, model gives meaningful results even though problem proved to be very difficult due to the unstructured format and the diversity of the tweets. Even humans could have a hard time predicting emojis in tweets. The final results were computed using macro f1.

There are six subdirectories and three files:
- /train - used as source development folder from SemEval-2018 Task 2: Multilingual Emoji Prediction competition task
- /mapping - mapping each emoji to a number between 0 and 20
- /results - the results given using BLSTM and separately for each baseline
- /models - saved models for baselines, BLSTM and w2v model
- /embeddings - pretrained Glove embeddings for BLSTM which uses an embedding layer
- /demo - additional files used in Demo.ipynb
- Plain Text Enrichment Using Tweets And Emojis.ipynb - main jupyter notebook that shows the development of the whole project
- Demo.ipynb - demo jupyter notebook that shows final results
- EmojiPresentation.pptx - a brief presentation about the whole project and its results

## Authors and acknowledgment

Link to the white paper of this project:<br/>
**Marin Drabic, Dora Markovic, Luka Suman. Plain Text Enrichment Using Tweets And Emojis**<br/>
https://www.fer.unizg.hr/_download/repository/TAR-2018-ProjectReports.pdf#page=47

Competition website:<br/>
**Semeval 2018 Task 2 - Multilingual Emoji Prediction**<br/>
https://competitions.codalab.org/competitions/17344

Main reference paper:<br/>
**Francesco Barbieri, Miguel Ballesteros, Horacio Saggion. Are Emojis Predictable?**<br/>
https://arxiv.org/pdf/1702.07285.pdf

@InProceedings{semeval2018task2,
  title={{SemEval-2018 Task 2: Multilingual Emoji Prediction}},
  author={Barbieri, Francesco and Camacho-Collados, Jose and Ronzano, Francesco and Espinosa-Anke, Luis and Ballesteros, Miguel and Basile, Valerio and Patti, Viviana and Saggion, Horacio},
  booktitle={Proceedings of the 12th International Workshop on Semantic Evaluation (SemEval-2018)},
  year={2018}, 
  address={New Orleans, LA, United States},
  publisher = {Association for Computational Linguistics}
 }

## License

Copyright (c) 2018 Marin Drabic, Dora Markovic, Luka Suman

