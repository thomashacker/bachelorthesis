# Bachelorthesis :student:
## Title

Analysis of reviews in the field of complementary medicine for improvements of given attributes using machine learning

## Goal :dna:

This work aims to automatically analyze supplement reviews to classify which effects a product has on certain health conditions. The goal is to create a better access to supplementary medicine by recommend products based on personal health preferences.


## Content :clipboard:

**This repository contains the bachelor thesis, its algorithm, demos and datasets.**

- spaCy 3.0 or higher is required 
- spaCy model en_core_web_trf is required (```spacy download en_core_web_trf```)
- The trained models can be found on [OneDrive](https://1drv.ms/u/s!An0OhG3IMh2IjzI9skYrgznxs93J?e=1LrhGX) and installed via  (```pip install <package-name>/dist/<package-name>.tar```) 
- spacy_streamlit required for the demonstrations

## Usage :hammer_and_wrench:

```python
from healthsea import healthsea

algorithm = healthsea()
example_review = "This helped my migraine"
print(algorithm.detect_extract_classify(example_review))

> [('helped condition', 'migraine', 'IMPROVED')]

```

## Demo :clapper:
You can start the two streamlit-demonstration to explore the analyzed dataset and the workflow of the algorithm

```streamlit run ./code/healthsea-streamlit.py```

```streamlit run ./code/data-streamlit.py```

## Dataset :open_file_folder:

The dataset is an excerpt of the Iherb online-market with more than 180.000 english reviews to 1270 supplement products