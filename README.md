# Bachelorthesis
### Analysis of reviews in the field of complementary medicine for improvements of given attributes using machine learning

---

**Author: Edward Schmuhl**

This repository contains the Iherb dataset, the training/ -evaluation dataset and the trained model of the Condition Identification and Statment Classification, and multiple Jupyter Notebooks.

```text
bachelorthesis/
├── Algorithm.ipynb/
├── ConditionIdentification.ipynb/
├── StatementExtraction.ipynb/
├── StatementClassification.ipynb/
├── Results.ipynb/
├── models/
|    ├── condition_identification_model/
|    ├── statment_classification_model/
|    └── packages/
|        ├── en_condition_identification_model-0.0.0
|        └── en_statement_classification_model-0.0.0
└── data/
    ├── iherb_data/
    |    ├── analyzed_dataset.json
    |    └── iherb_dataset.csv
    ├── Conditionidentification_TrainingEvaluation/
    |    ├── train.json
    |    └── eval.json
    └── Statementclassification_TrainingEvaluation/
         ├── train.json
         └── eval.json
```

It is required to have spacy and the english model installed.
The english model can be installed via ```spacy download en_core_web_trf```

It can occur that spacy cannot resolve the path of the self-trained models ```"./models/condition_identification_model"``` and ```"./models/statment_classification_model"```

In this case, you need to install the models that are contained in the package folder. After installation, use ```spacy.load(<package-name>)``` to import the model. For more information visit spacy.


