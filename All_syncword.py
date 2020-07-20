import pandas as pd

"""-----------------------------------------------------------------------------
這是製作同義詞1對1表的程式。

在本次清洗當中會用到兩種 1對1表：
    1. 食材名稱1對1表 syncword_1by1.xlsx  (素材：同義詞.txt)
    2. 單位名稱1對1表 unit_1by1.xlsx      (素材：unit.txt)

-----------------------------------------------------------------------------"""

## 將結果以 excel 形式儲存進本地端
def outputexcell(sync, outputdata):
    writer = pd.ExcelWriter("{}.xlsx".format(outputdata))   # 將 DataFrame 製作成 excel 檔案的格式
    sync.to_excel(writer, sheet_name="sync")                # 寫入 excel 格式，將工作表命名為 "sync" (此時為暫存狀態)
    writer.save()                                           # 完成 excel 儲存進本地端的命令
    writer.close()                                          # 結束 寫入excel 這個動作
    print("輸出成功")

## 將本地端的 同義詞1對1表 (excel) 做成字典檔
def create_dict(xlsxdata):
    df = pd.read_excel(xlsxdata)                # 將 excel 檔案製作成 DataFrame
    df2 = df[df.columns[1]]                     # 將 DataFrame 第二個欄位暫存進一個 list (ex, syncword)
    df3 = df[df.columns[2]]                     # 將 DataFrame 第三個欄位暫存進一個 list (ex, Word)
    sync_dict = {}                              # 暫存以同義詞與代換詞為 key, value 的字典檔
    for df2_item, df3_item in zip(df2, df3):    # 逐一取出二、三欄位內的所有東西
        sync_dict[df2_item] = df3_item          # 將欄位二的項目作為 key、欄位三作為 value 暫存進 sync_dict
    return sync_dict                            # 輸出字典檔 sync_dict

## 同義詞轉換器
def trans_word(name, sync_dict):
    # 判斷引入的詞彙是否出現在字典中所有的 key 值項目
    if name in sync_dict.keys():
        name = sync_dict[name]      # 判定存在情況時，將引入詞匯轉換為字典當中相對應 key 中記述的 value 值
        return name
    else:
        return name                 # 判定不存在時，則返回原引入詞匯

## 製作本地端檔案
def create_local_dict(txtdata, outputdata):
    """
    引入資料 txtdata 的預設狀態：
        干貝醬	XO醬	香菇昆布黑菇醬
        五香粉	丁香粉
        日本銀帶鯡	丁香魚
        加工日本銀帶鯡	丁香魚乾

    ※ 每一列第一個項目皆為比對詞，第二項目之後皆為同義詞
    """

    with open(txtdata, mode="r", encoding="utf-8") as s:            # 將尚未詞匯1對1化的原始檔案打開流程
        food = s.readlines()
        sync_key = []                                               # 製作 DataFrame 時需要的暫存桶子 (ex, 存放同義詞)
        sync_value = []                                             # 製作 DataFrame 時需要的暫存桶子 (ex, 存放比對詞)

        # 逐列取出所有同義詞
        for item in food:
            item2 = item.strip("\t\n").split("\t")    # 食材專用形式
            # item2 = item.strip("\t\n").split(" ")   # 單位專用形式

            # 判斷每筆同義詞的長度是否為 1 (判斷是不是只有比對詞)
            if len(item2) != 1:
                # 將該列所有項目逐一從 index[1] 開始取出 (從 index[1] 開始都是同義詞，而 index[0] 為比對詞)
                for sync_item in item2[1:]:
                    sync_key.append(sync_item)          # 將一個同義詞塞入 sync_key 的暫存桶子中
                    sync_value.append(item2[0])         # 將一個比對詞塞入 sync_value 的暫存桶子中
            else:                                       # 每列長度只有 1 (只有比對詞的狀況)
                sync_key.append(item2[0])               # 將一個比對詞塞入 sync_key 的暫存桶子中
                sync_value.append(item2[0])             # 將一個比對詞塞入 sync_value 的暫存桶子中

    sync_dict = {"syncword":sync_key, "Word":sync_value}    # 製作 DataFrame 需要的字典格式
    sync_df = pd.DataFrame(sync_dict)                       # 產生 DataFrame
    sync_df.index = sync_df.index + 1                       # 指定 DataFrame 的 index 值從 1 開始
    outputexcell(sync_df, outputdata)                       # 將製作好的 DataFrame 在本地端以 excel 檔儲存
    print(sync_df)                                          # 印出 DataFrame 狀況



# create_local_dict("人工處理分類/同義詞.txt","syncword_1by1")
