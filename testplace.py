import json
import time
from pprint import pprint

import naverMapCrawler
import pandas as pd

rawDataList = pd.read_csv("text.csv")
rawDataList = rawDataList.drop("Unnamed: 0", axis = 1)

print(rawDataList.columns)
print(rawDataList.shape)

reviewData = {"reviewData" : []}
startIdx = 0
endIdx = len(rawDataList)

with open('result.json', 'r', encoding='utf-8') as f:
    reviewData = json.load(f)
pprint(reviewData)
print(reviewData['reviewData'][-1])
lastStoreIdx = reviewData['reviewData'][-1]["storeIdx"]
print(type(str(rawDataList.loc[0,["상가업소번호"]][0])),type(lastStoreIdx))
# print(rawDataList.loc[:,["상가업소번호"]].head())
for idx in range(len(rawDataList.loc[:,["상가업소번호"]])):
    print(rawDataList.loc[idx,["상가업소번호"]][0],lastStoreIdx)
    tempIdx = str(rawDataList.loc[idx,["상가업소번호"]][0])
    if tempIdx == lastStoreIdx:
        print("last idx",idx)
        startIdx = idx + 1
        break
print("start idx",startIdx)