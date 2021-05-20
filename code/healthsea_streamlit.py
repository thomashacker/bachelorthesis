import streamlit as st
import spacy_streamlit
import spacy

conditionidentification = spacy.load("en_condition_identification_model")
nlp = spacy.load("en_core_web_trf")
statement_classifier = spacy.load("en_statement_classification_model")

# Title
st.write("# Welcome to healthsea! :purple_heart:")
st.subheader("Find the most suitable supplement for your personal health goals based on reviews")

default_text = st.text_input('Enter an example review:')

# Condition Identification
st.write('## Condition Identification')
st.write('> Detecting health conditions in text. Diseases, symptoms (classified by the [ICD 10](https://www.icd-code.de/)) and health issues regarding body functions, organs, and regions')
st.code("""Condition_Identification = spacy.load(en_condition_identification_model)""")

doc = conditionidentification(default_text)

spacy_streamlit.visualize_ner(
    doc,
    labels=["CONDITION"],
    show_table=False,
    title="Found conditions",
    colors={'CONDITION':"#8D66FD"},
)

st.write('---')

# Statement Extraction
def extract_Statement(text):
    returnList = []
    condition_Doc = conditionidentification(text)
    doc = nlp(text)
    
    conditionList = []
    for i in range(0,len(doc)):
        try:
            if(condition_Doc[i].ent_type_ == "CONDITION" and condition_Doc[i].ent_iob_ == "B"):
                index = i
                
                condition = condition_Doc[i].text
                conditionList.append(condition)
                for k in range(i,len(doc)):
                    if condition_Doc[k].ent_iob_ == "I":
                        condition += " "+condition_Doc[k].text
                        conditionList.append(condition_Doc[k].text)
                        conditionList.append(condition)
                        if doc[k].pos_ == "NOUN" and doc[i].pos_ != "NOUN":
                            index = k
     
                statement = ""
                ancestorList = []
                for ancestor in doc[index].ancestors:
                    if ancestor.text not in conditionList:
                        ancestorList.append(ancestor.text)
                for ancestor in reversed(ancestorList):
                    statement += ancestor+" "
                if statement != "":
                    statement += "condition"
                    returnList.append((statement,condition))
        except IndexError:
            print(i,doc.text)
            continue
    return returnList

st.write('## Statement Extraction')
st.write('> Extract the statement made about a condition by recursively extracting the head starting from the condition token. Replace the conditionname with a placeholder to increase the performance of the Statement Classification.')
st.code("""def extract_Statement(text):
    returnList = []
    condition_Doc = conditionidentification(text)
    doc = nlp(text)
    
    # Conditionidentification
    conditionList = []
    for i in range(0,len(doc)):
        try:
            if(condition_Doc[i].ent_type_ == "CONDITION" and condition_Doc[i].ent_iob_ == "B"):
                index = i
                
                # Conditionidentification
                condition = condition_Doc[i].text
                conditionList.append(condition)
                for k in range(i,len(doc)):
                    if condition_Doc[k].ent_iob_ == "I":
                        condition += " "+condition_Doc[k].text
                        conditionList.append(condition_Doc[k].text)
                        conditionList.append(condition)
                        if doc[k].pos_ == "NOUN" and doc[i].pos_ != "NOUN":
                            index = k

                # Statementextraction        
                statement = ""
                ancestorList = []
                for ancestor in doc[index].ancestors:
                    if ancestor.text not in conditionList:
                        ancestorList.append(ancestor.text)
                for ancestor in reversed(ancestorList):
                    statement += ancestor+" "
                if statement != "":
                    statement += "condition"
                    returnList.append((statement,condition))
        except IndexError:
            print(i,doc.text)
            continue
    return returnList
""")

doc2 = nlp(default_text)

spacy_streamlit.visualize_parser(doc2)

statements = extract_Statement(default_text)
return_Statements = ""
for statement in statements:
    return_Statements += f"> - Extracted statement for condition **{statement[1]}** -> {statement[0]} \n"

st.write(return_Statements)

# Statement Classification

st.write('## Statement Classification')
st.write('> Classify the extracted statements to three defined classes: **IMPROVED**, **WORSEND**, and **NEUTRAL**')
st.code('Statement_Classifier = spacy.load("en_statement_classification_model")')

for statement in statements:
    doc3 = statement_classifier(statement[0])
    spacy_streamlit.visualize_textcat(doc3)

