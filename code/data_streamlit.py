import streamlit as st
import numpy as np
import pandas as pd
import os
import json
import matplotlib.pyplot as plt

json_dir = 'data/analyzed_dataset.json'
json_dict = []

def getData():
    with open(json_dir,'rb') as f:
        return json.load(f)

json_dict = getData()

product_dict = json_dict["Product"]
condition_dict = json_dict["Condition"]
supplement_for_condition = json_dict["Best_Product_Supplement"]
top_improved_condition = json_dict["Improved_Condition"]
top_worsen_condition = json_dict["Worsen_Condition"]
best_products = json_dict["Best_Product"]
worst_products = json_dict["Worst_Product"]

# Count Reviews per Product
review_count = 0
for p_key in product_dict:
    review_count += len(product_dict[p_key]["reviews"])

st.write("# Discover the dataset analyzed by healthsea!")
st.write(f"### Products: {len(product_dict)} :pill: | Reviews: {review_count} :clipboard: | Unique Conditions: {len(condition_dict)} :mag_right:")

st.write(f'> All Conditions')
d_1 = {"Condition":[],"Improved":[],"Worsend":[],"Neutral":[]}
for entry in top_improved_condition:
    _condition = entry[0]
    d_1['Condition'].append(_condition)
    d_1['Improved'].append(entry[1])

    _stats = condition_dict[_condition]
    d_1['Worsend'].append(_stats['WORSEN'])
    d_1['Neutral'].append(_stats['NEUTRAL'])

df_1 = pd.DataFrame(data=d_1)
st.dataframe(df_1)

st.write("----")

st.write("## Search for conditions")
show_top = st.number_input('Show top',value=10)

look_for = st.text_input('Enter search query:')
found = []

d_3 = {"Condition":[],"Improved":[],"Worsend":[],"Neutral":[]}

for c in condition_dict:
    if look_for in c:
        found.append(c)
        _condition = condition_dict[c]
        d_3['Condition'].append(c)
        d_3['Improved'].append(_condition['IMPROVED'])
        d_3['Worsend'].append(_condition['WORSEN'])
        d_3['Neutral'].append(_condition['NEUTRAL'])

st.write(f'> {len(found)} Conditions found with **{look_for}**')       
df_3 = pd.DataFrame(data=d_3)
st.dataframe(df_3)

if look_for in supplement_for_condition:
    get_condition = look_for
elif len(found) > 0:
    get_condition = found[0]

d_4 = {"Product":[],"Score":[],"Improved":[],"Worsend":[],"Neutral":[],"ID":[]}

for _t in supplement_for_condition[get_condition][:show_top]:
    d_4["Product"].append(product_dict[_t[0]]['name'])
    d_4["Score"].append(_t[1])
    d_4["Improved"].append(product_dict[_t[0]]['condition'][get_condition]['IMPROVED'])
    d_4["Worsend"].append(product_dict[_t[0]]['condition'][get_condition]['WORSEN'])
    d_4["Neutral"].append(product_dict[_t[0]]['condition'][get_condition]['NEUTRAL'])
    d_4["ID"].append(_t[0])

st.write(f'> Showing **top {show_top}** most suitable Products for **{get_condition}**')  
df_4 = pd.DataFrame(data=d_4)
st.dataframe(df_4)

st.write("----")

st.write("## Search for reviews")

search_id = st.text_input('Enter product ID:')

for review in product_dict[search_id]["reviews"]:

    if len(review["condition"]) == 0:
        continue

    _text = review["text"]

    d_5 = {"Condition":[],"Improved":[],"Worsend":[],"Neutral":[]}

    for _c in review["condition"]:
        _text = _text.replace(_c,f"**{_c}**")
        condition = review["condition"][_c]
        d_5["Condition"].append(_c)
        d_5["Improved"].append(condition["IMPROVED"])
        d_5["Worsend"].append(condition["WORSEN"])
        d_5["Neutral"].append(condition["NEUTRAL"])
    
    st.write(f'> {_text}')
    df_5 = pd.DataFrame(data=d_5)
    st.dataframe(df_5)
