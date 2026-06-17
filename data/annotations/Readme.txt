# CONLL 2018 Anonymous Submission
Challenge or Empower: Revisiting Argumentation Quality in a News Editorial Corpus
####################################################
##    OVERVIEW
####################################################
The conll2018-news-editorial-quality_partial.json file contains the annotations of 250 news editorials annotated by three liberals and three conservatives. Therefore, it contains a total of 1500 annotations. The full data (1000 news editorials, 6000 annotations) will be shared publicaly after the paper is published.

Each single annotation (1 annotator annotating 1 news editorial) is save in one json object. The JSON file contains a JSON array of 1500 JSON objects.

Please note that we do not have the right to publish the content of the annotated news editorials. We provide the file name of each news editorial which serves as an identification.  [1]

[1] Sandhaus, Evan. The New York Times Annotated Corpus LDC2008T19. DVD. Philadelphia: Linguistic Data Consortium, 2008.

####################################################
##    FIELDS
####################################################
In this readme file, we present an explanation for each field  showed in our corpus:

- annotator_id: unique identification of the annotator.  the ID of annotators with liberal political ideology starts with L and C otherwise.

- article_id: article id is a unique identification of the article and is the same file name as assigned in the New York Times Corpus.

- article_index: article index has a value from 0 to 249. It is the article number annotated. For example, the article_id '4' means that the annotated article is the 5th article annotated by a specific annotator.

- batch: batch has a value from batch1 to batch4. As mentioned in our paper, we have four batches of data. Each batch contains 250 news editorials and there are no overap between the batches.

- date_created: Date and time the news editorial was annotated.

- effect: The effect of an editorial on the reader as reported by the reader. It has a value from 1 to 5: 
             1: Strongly Challenging
             2: Somewhat Challenging
             3: No Effect
             4: Somewhat Reinforcing
             5: Strongly Reinforcing
- effect_abstracted: This value is calculted from the effect value to reflect if the editorial is 'Reinforcing', 'Challenging' or has 'No Effect':
             1: Challenging
             2: No Effect
             3: Reinforcing
- explanation: The free text explanation of the annotator.

- intensity: The intensity of the effect of the editorial:
            - strong: Strongly Challenging, Strongly Reinforcing
            - moderate: Somewhat Challenging, Somewhat Reinforcing
            - none: No Effect

- political_ideology: The political ideology of the annotator based on PEW political typology test. It can be 'liberal' or 'conservative'.
- political_typology: The political ideology based on PEW  typology. The values are  
        'Solid Liberals'
        'Opportunity Democrats'
        'Disaffected Democrats'
        'Devout and Diverse'
        'New Era Enterprisers'
        'Market Skeptic Republicans'
        'Country First Conservatives'
        'Core Conservatives'
        'Bystanders'

- empower: In case the annotator answers that the news editorial 'Strongly Reinforced' his or her stance, we ask if the news editorial 'empowered' him or her to better argue about the presented topic. This value holds the answer to this question ('YES' or 'NO'). In case the effect is not 'Strongly Reinforcing', the value is null.

- change: In case the annotator answers that the news editorial 'Strongly Challenged' his/her, we ask if the news editorial 'changed' him or her  stance about the presented topic. This value holds the answer to this question ('YES' or 'NO'). In case the effect is not 'Strongly Challenging', the value is null.
    
####################################################
##    END
####################################################
