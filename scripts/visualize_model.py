import spacy
from spacy.language import Language
import streamlit as st
import spacy_streamlit
import typer


def init_model(ner: str, textcat: str) -> Language:
    nlp = spacy.load("en_core_web_trf")
    nlp.remove_pipe("ner")

    nlp.add_pipe("ner", source=spacy.load(ner))
    nlp.add_pipe("textcat", source=spacy.load(textcat))
    return nlp


def process_review(text: str, nlp: Language):
    doc = nlp(text)
    returnList = []
    exclude_conditions = []

    for i in range(0, len(doc)):
        # Condition Identification
        if doc[i].ent_type_ == "CONDITION" and doc[i].ent_iob_ == "B":

            index = i
            current_condition = doc[i].text
            exclude_conditions.append(doc[i].text)

            for k in range(i + 1, len(doc)):
                if doc[k].ent_type_ == "CONDITION" and doc[k].ent_iob_ == "I":
                    exclude_conditions.append(doc[k].text)
                    exclude_conditions.append(doc[i].text + " " + doc[k].text)
                    current_condition += "_" + doc[k].text

                    if doc[k].pos_ == "NOUN" and doc[index].pos_ != "NOUN":
                        index = k
            # --------------------------
            # Statement Extraction
            statement = ""
            ancestors = []

            for ancestor in doc[index].ancestors:
                if ancestor.text not in exclude_conditions:
                    ancestors.append(ancestor.text)

            for ancestor in reversed(ancestors):
                statement += ancestor + " "

            if statement != "":
                statement += "condition"
            # --------------------------
            # Statement Classification
            doc_textcat = nlp(statement)
            classfication = max(doc_textcat.cats, key=doc_textcat.cats.get)
            returnList.append((current_condition, statement, classfication))
            # --------------------------

    return returnList


def main(ner: str, textcat: str) -> None:

    nlp = init_model(ner, textcat)

    # Title
    st.write("# Welcome to the spaCy project Healthsea!")
    st.subheader(
        "Detecting conditions, extracting their statements, and classifying their described effect."
    )

    input_text = st.text_input("Enter an example review:")

    results = process_review(input_text, nlp)

    st.write(results)

    doc = nlp(input_text)

    spacy_streamlit.visualize_ner(
        doc,
        labels=["CONDITION"],
        show_table=False,
        title="Found conditions",
        colors={"CONDITION": "#8D66FD"},
    )

    spacy_streamlit.visualize_parser(doc)

    for result in results:
        spacy_streamlit.visualize_textcat(nlp(result[1]))


# --- Main ---
if __name__ == "__main__":
    try:
        typer.run(main)
    except SystemExit:
        pass
