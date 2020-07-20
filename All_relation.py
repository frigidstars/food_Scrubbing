import time

"""
這程式負責做食材名稱的比對。

"""


## 同義詞比對器
def metch(food):
    my_food_list = []   # 暫存自訂義食材辭典的桶子
    with open("人工處理分類\\food_dict.txt", mode="r", encoding="utf-8") as f:    # 將自訂義食材的辭典打開流程
        for item2 in f.readlines():         # 逐一取出其中食材名稱
            new_item2 = item2.strip(" \n")
            my_food_list.append(new_item2)  # 將食材名稱存進 my_food_list 暫存的桶子

    # print(my_food_list)

    # 判斷引入的食材名稱是否存在於食材自訂義辭典中
    if food in my_food_list:    # 如果有存在，輸出原樣的名稱
        return food
    else:                       # 如果不存在，則將食材名稱轉為 None 輸出
        food = None
        return food

# 自訂義停用詞辭典 (不能吃的東西清單)
def load_stopwords():
    stopwords = []      # 暫存不可食食材辭典的桶子
    with open("人工處理分類\\stopwords.txt", mode="r", encoding="utf-8") as f:    # 將自訂義食材的辭典打開流程
        for item in f.readlines()[:]:       # 逐一取出其中停用詞名稱
            stopwords.append(item.strip("\n \t"))   # 將停用食材名稱存進 stopwords 暫存的桶子
    return stopwords    # 輸出不可食的暫存桶子 stopwords

