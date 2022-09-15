import json
import time
from pprint import pprint

import naverMapCrawler
import testplace2
import pandas as pd

if __name__ == '__main__':
    rawDataList = pd.read_csv("text.csv")
    rawDataList = rawDataList.drop("Unnamed: 0", axis = 1)

    print(rawDataList.columns)
    print(rawDataList.shape)

    reviewData = {"reviewData" : []}
    startIdx = 0
    endIdx = len(rawDataList)
    nowIdx = startIdx
    try:
        with open('result.json', 'r', encoding='utf-8') as f:
            reviewData = json.load(f)
        lastStoreIdx = reviewData['reviewData'][-1]["storeIdx"]
        print(type(str(rawDataList.loc[0, ["상가업소번호"]][0])), type(lastStoreIdx))
        # print(rawDataList.loc[:,["상가업소번호"]].head())
        for idx in range(len(rawDataList.loc[:, ["상가업소번호"]])):
            tempIdx = str(rawDataList.loc[idx, ["상가업소번호"]][0])
            if tempIdx == lastStoreIdx:
                print("last idx", idx)
                startIdx = idx + 1
                break
        print("start idx", startIdx)
    except:
        print("결과 데이터 없음. 새로 생성")
    sumTime = 0

    for idx in range(startIdx,10):
        startTime = time.time()
        searchWord = ""
        rawData = rawDataList.loc[idx, ["상가업소번호", "상호명", "도로명주소"]]
        searchIdx = rawData[0]
        searchName = rawData[1]
        searchAdress = rawData[2]
        print(str(searchIdx) + " " + searchName + " " + searchAdress)
        result = []
        try:
            result = testplace2.crawler(str(searchIdx),searchName,searchAdress)
            with open('result.json', 'w', encoding='utf-8') as f:
                json.dump(reviewData, f, indent=4, ensure_ascii=False)
            nowIdx = idx
            reviewData['reviewData'].append(result)
        except:
            print(searchWord,"크롤링 실패")
        sumTime += time.time() - startTime
        print("총 소요시간 : {}, 처리 개수 : {}, 1개당 걸린 평균시간 : {}".format(sumTime, idx-startIdx+1, sumTime /(idx-startIdx+1)))
        print(idx,"="*70)

    pprint(reviewData['reviewData'])


