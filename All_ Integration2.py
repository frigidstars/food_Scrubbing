import pandas as pd
import json
import time
import All_filter as clean
import All_quantifier as qer
import All_relation as rel
import All_transunit as uni

"""-----------------------------------------------------------------------------

這個是主要運作的程式，我們會將其他自己寫的 function 引入這個主頁當中完成資料清洗的作業。

自訂套件：
    All_filter
        清洗食譜名稱
            >>> filter_dept(row_food)
                >>> first_filter(sec_item)
                >>> second_filter(trd_item)
        清洗食材名稱
            >>> name_filter(recipe_name)
            
    All_quantifier
        分離食材用量、食材單位
        清洗食材用量
        清洗食材單位
            >>> quantifier(input)
            
    All_relation
        判斷食譜當中的食材是否存在於自訂義食材字典當中
            >>> metch(food)
        導入不可食字典
            >>> load_stopwords()
            
    All_transunit
        將導入的食材單位針對自訂義單位字典進行轉換
            >>> unitclean(it_unit)
                >>> matchscore(it_unit)

-----------------------------------------------------------------------------"""

## 從本地端打開檔案
def openfile():
    # df = pd.read_excel("E:\\recipe\\icook_clean0529.xlsx")
    # df = pd.read_excel("E:\\recipe\\台灣好食材.xlsx")
    # df = pd.read_excel("E:\\recipe\\cook1cook_recipe.xlsx")

    df = pd.read_excel("E:\\recipe\\楊桃.xlsx")   # 選擇要開啟的檔案並作成 DataFrame 形式
    df0 = df["食譜名稱"]        # 開啟的檔案中某個欄位 "食譜名稱"
    df1 = df["食譜連結"]        # 開啟的檔案中某個欄位 "食譜連結"
    df2 = df["食材"]            # 開啟的檔案中某個欄位 "食材"
    df3 = df["圖片連結"]        # 開啟的檔案中某個欄位 "圖片連結"
    return df0, df1, df2, df3

## 將檔案輸出成一個 json 檔案
def writefile(food_data):
    with open("recipe8.json", mode="w", encoding='utf-8') as f:
        json.dump(food_data, f, separators=(",\n", ": "))

## 清洗工廠，執行所有清洗作業
def factory(data):
    recipe_list = []    # 儲存所有可用食譜的資訊用的桶子
    x = 0               # 處理食譜計數器
    y = 0               # 有效食譜計數器

    # 透過迴圈將一份食譜清單逐一取出後，再進入對應的自訂套件當中做清洗
    for df0_item, df1_item, df2_item, df3_item in zip(data[0], data[1], data[2], data[3]):
        if x < 200000:
            try:
                newdf0_item = clean.name_filter(df0_item)               # 將 "食譜名稱" 代入自訂套件 All_filter
                newdf2_item = json.loads(df2_item.replace("\'","\""))   # ex, 將食材 {'蘋果':'1顆'} > {"蘋果":"1顆"} / json 的格式在 python 只能識別雙引號
                df2_item_keys = newdf2_item.keys()                      # 取出食材當中 key 值 (預計輸出 "食材名稱")
                df2_item_values = newdf2_item.values()                  # 取出食材當中 value 值 (預計輸出 "食材用量" 及 "食材單位")

                Ingredients = []    # 存放一份食譜當中所有的食材名稱、食材單位、食材用量的桶子

                # 透過迴圈將一份食譜當中所有的食材逐一取出後，分別針對 key, value 值在對應的自訂套件做清洗
                for row_it, row_nu in zip(df2_item_keys, df2_item_values):
                    row_it2 = clean.filter_dept(row_it)         # 將 key 值代入自訂套件 All_filter

                    it_name = rel.metch(row_it2)                # 將 key 初步清洗完成後的值，在代入另一個自訂套件 All_relation 作比對處理，通過比對出來的值即是我們要的 "食材名稱"
                    it_quantity = qer.quantifier(row_nu)[0]     # 將 value 值代入自訂套件 All_quantifier 輸出是個 tuple 其 index[0]即是我們要的 "食材用量"
                    it_unit = qer.quantifier(row_nu)[1]         # 將 value 值代入自訂套件 All_quantifier 輸出是個 tuple 其 index[1]即是我們 "初步_食材單位"
                    new_it_unit = uni.unitclean(it_unit)        # 將 "初步_食材單位" 結果再代入自訂套件 All_transunit 產出的新值即是我們要的 "食材單位"

                    # 將每一種食材的三種需求值 ("食材名稱", "食材用量", "食材單位") 放入一個字典檔
                    ingredient = {"It_name":it_name, "It_quantity":it_quantity , "It_unit": new_it_unit}

                    # 再塞入 Ingredients 這桶子前，會先做一個判斷，判斷初步清洗完的 key 是存在於不可食名單當中
                    if row_it2 not in rel.load_stopwords():
                        Ingredients.append(ingredient)          # 只放入通過不可食測驗的單一食材(3狀態)進 Ingredients

                j_num = 0   # 判斷食材名稱是否 None 的計數器 / (這個步驟可以在食材加入 Ingredients 前做處理，效率會更好)
                # 逐一取出每個食譜中剛剛清洗完的食材字典，判斷 "食材名稱" 是否出現 None 狀態
                for its_item in Ingredients:
                    if its_item["It_name"] == None:     # 判斷 "食材名稱" 是否 None
                        j_num = j_num + 1               # 如果有 None 則在計數器上 + 1

                # 根據計數器的結果在做判斷式處理，判斷 計數值 = 0 且 Ingredients 不能是空桶子
                if j_num == 0 and Ingredients != []:
                    # 通過測試的項目才會將這食譜加入可用食譜的桶子 (recipe_list) 當中
                    recipe_list.append({"RecipeName":newdf0_item, "RecipeURL":df1_item, "RecipeImageURL":df3_item, "Ingredients":Ingredients})
                    print({"RecipeName":newdf0_item, "RecipeURL":df1_item, "RecipeImageURL":df3_item, "Ingredients":Ingredients})   # 印出一個可用食譜的所有資訊
                    print("目前:{}, 有效:{} / {}".format(x, y, newdf0_item))    # 印出目前程式處裡的筆數狀況
                    y = y + 1   # 在有效食譜計數器上 + 1

                x = x + 1       # 在 處理食譜計數器上 + 1

            except:
                x = x + 1   # 發生格式錯誤無法讀取某一個食譜狀況時，依然也會在處理食譜計數器上 + 1
                pass        # 無法讀取狀況總筆數不到200筆這邊就不多做處理

    output = {"Recipe":recipe_list}     # 將最後全有效食譜資訊的桶子做成一個字典檔
    return output                       # 輸出上列該字典檔到外部準備做寫入處理

def main():
    """
    預期輸出結果:
        data = {
            "Recipe":[
                {
                    "RecipeName":"xxx",
                    "RecipeURL":"https://icook.com/xxxxxx",
                    "RecipeImageURL":"https://icook.com/xxxxxx.jpg",
                    "Ingredients":
                        [
                            {"It_name":"aaa1", "It_quantity":20, "it_unit":"c"},
                            {"It_name":"aaa2", "It_quantity":200, "it_unit":"c"},
                            {"It_name":"aaa3", "It_quantity":5, "it_unit":"c"}
                        ]
                }
            ]
        }
    """
    open = openfile()           # 開啟本地端的某個食譜檔
    food_data = factory(open)   # 將方才開檔的資料倒入資料清洗的 function
    writefile(food_data)        # 將清洗完的字典檔導入輸出 json 的 function

if __name__ == "__main__":
    start = time.clock()
    main()
    end = time.clock()
    print("花費時間: {} 秒".format(end - start))