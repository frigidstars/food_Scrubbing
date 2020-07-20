import jieba
import All_syncword as sync

"""-----------------------------------------------------------------------------
這程式負責將單位進行標準化的動作。
由於爬蟲下來的資料過於混亂，許多食材單位在填寫上頗具創意，必須要將單位名稱進行統一化處理。

自訂套件：
    All_syncword:
        將本地端的 同義詞1對1表 (excel) 做成字典檔
            >>> create_dict(xlsxdata) 
        同義詞轉換
            >>> trans_word(name, sync_dict)
    
-----------------------------------------------------------------------------"""
# 將單位1對1表，在代入另一個自訂套件 All_syncword 產生一個暫存的字典
unit_dict = sync.create_dict("人工處理分類\\unit_1by1.xlsx")

# 使用 jieba 套件以 unit_dict 的所有 key 值 (所有自建的同義詞) 為自訂義辭典
jieba.load_userdict(unit_dict.keys())


## 分數比對器
def matchscore(it_unit):
    """
    將引入的食材單位名稱 it_unit 進行評分，在依照朝分數狀況做不同的代換處理。
    每次近來一種測試的食材單位名稱，會與所有的自訂義詞逐一的做分數比對，優先取出筆對較高者做輸出。

    預計輸出結果：
        個 > 個
        超級大碗公 >　碗公
        一些些 > 一些
        依各人喜好　> Moderation

    """

    # 輸入進來的值先依照自訂義字典進行斷詞 / >>> {超級, 碗公}
    u_item = set(jieba.cut(str(it_unit), cut_all=False, HMM=True))

    unit_d_key = unit_dict.keys()  # 取出單位字典當中的key值 / >>> [斤, g, 公斤,...]

    # 製作 jieba 後的量詞字典，裡面的值為 set 型態，以便之後做交集聯集比對
    """
    運作狀況：
        ud_key, 同義詞 ex, 公斤 
            > 經過 jieba > type 轉換 set > (公斤)
        u_item, 引入近來的詞彙進行 jieba 斷詞後，以 set 形式儲存
        udk_item, 自訂義同義詞當中某一個詞彙 jieba 斷詞後，以 set 形式儲存 
        
        ※ set 的目的在於可以在不重複字元集情況下，進行交聯及比對
        
        ex, u_item = ("超級","碗公") / udk_itm = ("碗公")
            透過 u_item 及 udk_item 各集合中的筆數產生分數
            在這例子當中，u_item | udk_item len() 為 2 (兩集合做聯集，結果：("超級", "碗公"))
                         u_item & udk_item len() 為 1 (兩集合做交集，結果：("碗公"))
            透過 聯集除以交集 得到分數為 0.5 
            ※ 分母(聯集)的筆數越多則分數就會越小，在這公式的設計中交集的筆數結果只會有 0 或 1
    """


    try:
        ud_list = []                        # 暫儲 set化 同義詞字典當中詞彙的桶子
        for ud_key in unit_d_key:
            result = jieba.cut(ud_key, cut_all=False, HMM=True)
            ud_list.append(set(result))
        # 逐一取出 set化的同義詞字典 及 本來的同義詞字典
        for ud_item, udk_item in zip(ud_list, unit_d_key):
            # 判斷 set化引入詞 是否完全等於 set化同義詞字典中的某詞彙
            if u_item == ud_item:
                u_item = u_item             # 保持原樣
                return list(u_item)[0]      # 輸出 str 型態的量詞

            # 判斷 set化引入詞其筆數是否大於 1 且小於等於 3
            elif len(u_item) > 1 and len(u_item) <= 3:
                score = len(u_item & ud_item) / len(u_item | ud_item)   # 取 交集 / 聯集 分數
                if score >= 0.5:
                    u_item = ud_item        # 分數為 0.5 時，set化引入詞 會轉變成 同義詞當中的詞彙
                    return list(u_item)[0]  # 輸出 str 型態的量詞

                elif score >= 0.3 and "cup" in u_item:  # 分數為 0.3 時，且 "cup" 詞彙有出現在 set化引入詞 中
                    u_item = {"cup"}        # set化引入詞 轉變成 {"cup"}
                    return list(u_item)[0]  # 輸出 str 型態的量詞

                elif score >= 0.3 and "杯" in it_unit:   # 分數為 0.3 時，且 "杯" 詞彙有出現在 set化引入詞 中
                    u_item = {"cup"}        # set化引入詞 轉變成 {"cup"}
                    return list(u_item)[0]  # 輸出 str 型態的量詞

            elif u_item == {"None"}:        # set化引入詞 為 {"None"}
                u_item = {"Moderation"}     # set化引入詞 轉變成 {"Moderation"}
                return list(u_item)[0]      # 輸出 str 型態的量詞

            # 將剩下沒做到匹配的東西變成適量
            elif len(u_item) > 1:
                u_item = {"Moderation"}     # set化引入詞 筆數超過 1 時，直接將 set化引入詞 轉變成 {"Moderation"}
                return list(u_item)[0]      # 輸出 str 型態的量詞
    except:
        # 不可預期的例外狀況也直接變成適量
        u_item = "Moderation"
        return u_item



## 本程式主要運作的 function
def unitclean(it_unit):
    clean_unit = matchscore(it_unit)        # 將引入的食物單位詞彙代入分數比對器 matchscore

    # 將比對分數器的結果，再代入另一個自訂套件 All_syncword 進行詞彙轉換
    """
    預期結果：
        公斤 > kilogram
        個 > EA        
        適量 > Moderation
    """
    it_unit = sync.trans_word(clean_unit, unit_dict)

    # 保險機制，若代換完是 None 轉變為 "Moderation" 輸出
    if it_unit == None:
        it_unit = "Moderation"
    return it_unit


# count=[]
# x = 0
# df_json = pd.read_json("[200614]recipe.json")["Recipe"]
# for it in df_json[:]:
#     it_ing = it["Ingredients"]
#     for it_item in it_ing:
#         it_unit = it_item["It_unit"]
#         it_unit2 = unitclean(it_unit)
        # print(x, it_unit2)
        # count.append(it_unit2)
        # x = x + 1

# print("計數", len(count))
# wf.wf(count)




