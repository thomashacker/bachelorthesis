import pandas as pd
import json
from .healthsea import healthsea

iherb_data = pd.read_csv("../data/iherb_dataset.csv")
algorithm = healthsea()
product_dict = []

# Configuration
start_index = 0

for index, row in iherb_data.loc[start_index:].iterrows():
    review_json = {}
    review_json["pId"] = row["ProductID"]
    review_json["text"] = row["Body"]
    review_json["rating"] = row["Rating"]
    review_json["id"] = row["ReviewID"]
    review_json["condition"] = {}
    
    review_analysis =  algorithm.detect_extract_classify(row["Body"])
    
    for condition in review_analysis:
        if condition[1] not in review_json["condition"]:
            review_json["condition"][condition[1]] = {}
            review_json["condition"][condition[1]]["IMPROVED"] = 0
            review_json["condition"][condition[1]]["WORSEN"] = 0
            review_json["condition"][condition[1]]["NEUTRAL"] = 0
        review_json["condition"][condition[1]][condition[2]] += 1
        
    if row["ProductID"] not in product_dict:
        product_dict[row["ProductID"]] = {}
        product_dict[row["ProductID"]]["name"] = row["ProductName"]
        product_dict[row["ProductID"]]["brand"] = row["ProductBrand"]
        product_dict[row["ProductID"]]["reviews"] = []
    
    product_dict[row["ProductID"]]["reviews"].append(review_json)
    
with open('./data/iherb_analyzed_2.json', 'w') as f:
    json.dump(product_dict, f)