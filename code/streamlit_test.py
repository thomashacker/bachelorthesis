import streamlit as st
import spacy_streamlit
import spacy

conditionidentification = spacy.load("en_condition_identification_model")
nlp = spacy.load("en_core_web_trf")
statement_classifier = spacy.load("en_statement_classification_model")


def classify_statement(text: str):
    doc = statement_classifier(text)
    return max(doc.cats, key=doc.cats.get)


def detect_extract_classify(text: str):
    returnList = []
    condition_Doc = conditionidentification(text)
    doc = nlp(text)
    foundConditionList = []

    for i in range(0, len(doc)):

        # Condition Identification
        if (
            condition_Doc[i].ent_type_ == "CONDITION"
            and condition_Doc[i].ent_iob_ == "B"
        ):
            index = i
            foundCondition = condition_Doc[i].text
            foundConditionList.append(condition_Doc[i].text)

            for k in range(i + 1, len(doc)):
                if condition_Doc[k].ent_iob_ == "I":
                    foundCondition += " " + condition_Doc[k].text
                    foundConditionList.append(condition_Doc[k].text)
                    foundConditionList.append(
                        condition_Doc[i].text + " " + condition_Doc[k].text
                    )

                    if doc[k].pos_ == "NOUN" and doc[index].pos_ != "NOUN":
                        index = k

            # Statement Extraction
            statement = ""
            ancestorList = []

            for ancestor in doc[index].ancestors:
                if ancestor.text not in foundConditionList:
                    ancestorList.append(ancestor.text)

            for ancestor in reversed(ancestorList):
                statement += ancestor + " "

            if statement != "":
                statement += "condition"

                # Statement Classification
                statement_class = classify_statement(statement)
                returnList.append((foundCondition, statement, statement_class))

    return returnList


color_dict = {
    "IMPROVED": "0BB463",
    "WORSEN": "F12020",
    "NEUTRAL": "dadada",
}

style_string = """
<style>
    .container{
        text-align: center;
    }
    .review{
        padding: 20px;
    }
    .condition{
        background-color:#E83AD6;
        color: white;
        border-radius: 10px;
        padding: 10px;  
    }
    .label{
        font-size: 10px;
    }
    .statement{
        color: white;
        border-radius: 5px;
        padding: 7px;  
    }
    .classification{
        font-size: 20px;
    }
</style>
"""

layout = """
<div class ="container">
<div class="review" style="border: 2px solid #{color};">
    <span>
        <span>{content}</span>
    </span>
</div>
    <div>
        <span class="classification" style="color: #{color};"><b>{classification}</b></span>
    </div>
</div>
"""

statement_layout = """
<span class ="statement" style="background-color: #{color};"> <b>{statement}</b> </span>
"""

condition_layout = """
<span class ="condition"><b>{condition}</b> <span class ="label">Condition</span></span>
"""

# Title
st.write("# Welcome to healthsea! :purple_heart:")
st.subheader(
    "Find the most suitable supplement for your personal health goals based on reviews"
)

default_text = st.text_input("Enter an example review:")
results = detect_extract_classify(default_text)

st.markdown(style_string, unsafe_allow_html=True)

for result in results:
    review = str(default_text)
    statement_tokens = result[1].split()

    for token in statement_tokens:
        review = review.replace(
            token,
            statement_layout.format(color=color_dict[result[2]], statement=token),
        )

    review = review.replace(result[0], condition_layout.format(condition=result[0]))

    main = layout.format(
        color=color_dict[result[2]], content=review, classification=result[2]
    )

    st.markdown(main, unsafe_allow_html=True)

st.write(results)
