import spacy

class healthsea:
    def __init__(self) -> None:
        # Selftrained NER for entity 'CONDITION'
        self.conditionIdentification = spacy.load("en_condition_identification_model") 

        # Selftrained Textcat on classes 'IMPROVED', 'WORSEN', and 'NEUTRAL'
        self.statementClassification = spacy.load("en_statement_classification_model")

        # Pretrained model provided by spaCy for Dependency Parsing
        self.nlp = spacy.load("en_core_web_trf")

    def classify_statement(self, text : str):
        doc = self.statementClassification(text)
        return max(doc.cats, key=doc.cats.get)

    def detect_extract_classify(self, text : str):
        returnList = []
        condition_Doc = self.conditionIdentification(text)
        doc = self.nlp(text)
        foundConditionList = []

        for i in range(0,len(doc)):

                # Condition Identification
                if(condition_Doc[i].ent_type_ == "CONDITION" and condition_Doc[i].ent_iob_ == "B"):
                    index = i
                    foundCondition = condition_Doc[i].text
                    foundConditionList.append(condition_Doc[i].text)

                    for k in range(i+1,len(doc)):
                        if condition_Doc[k].ent_iob_ == "I":
                            foundCondition += " "+condition_Doc[k].text
                            foundConditionList.append(condition_Doc[k].text)
                            foundConditionList.append(condition_Doc[i].text+" "+condition_Doc[k].text)

                            if doc[k].pos_ == "NOUN" and doc[index].pos_ != "NOUN":
                                index = k

                    # Statement Extraction        
                    statement = ""
                    ancestorList = []

                    for ancestor in doc[index].ancestors:
                        if ancestor.text not in foundConditionList:
                            ancestorList.append(ancestor.text)

                    for ancestor in reversed(ancestorList):
                        statement += ancestor+" "

                    if statement != "":
                        statement += "condition"
                        
                        # Statement Classification
                        statement_class = self.classify_statement(statement)
                        returnList.append((statement,foundCondition,statement_class))

        return returnList
