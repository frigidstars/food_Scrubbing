import sign_list
import re

"""-----------------------------------------------------------------------------

這程式負責做食物名稱、食材名稱的文字處理。

自訂套件：
    sign_list
        輸出一份專用標點符號清單
            >>> stripsign()
            >>> stripsign_origin():

※ 在各個過濾器當中常有去除首尾空白的狀況，做法上可能有點多餘，目的在於確保首尾空白部分完全消失。
   有可能發生因為上一個階段處理時的詞匯本身字元間具有空白，再除去多餘字元以後，原本區間內的空白就會變成首尾的空白。
   有時必須保留字元間的空白，所以也不能兼字元內所有空白一次去除，故用比較繁瑣的方式來做處理。 
   其他相關的過濾手段，被不斷重複使用的理由也同剛剛說明的情況。
   
   原始狀況：
        >>> {A.(Japan) 富士，蘋果 (3月產 🍎 )  } 
   過濾結果：     
        >>> 蘋果  
                        
-----------------------------------------------------------------------------"""

## 主要的清洗 function 接收到的資料從這開始
def filter_dept(row_food):
    clean_decorations1 = first_filter(row_food)             # 將 "原始_食材名稱" 先引入第一層過濾器
    clean_decorations2 = second_filter(clean_decorations1)  # 將第一層過濾器結果引入第二層過濾器
    return clean_decorations2                               # 輸出最終結果

## 第一層過濾器
def first_filter(sec_item):
    # 階段 1：將引入進來的詞彙做以下處理：1.去除首尾空白 2.呈1，去除去除首尾特殊符號 3.呈2，再去除前後空白
    newsec_item = sec_item.strip(" ").strip(sign_list.stripsign()).strip(" ")

    # 階段 2：呈上結果，去除詞彙中包含以下 "框對形式且框對中有任何字元" 的 "字元組"
    newsec_item2 = re.sub(r"[(【（{[《「﹝〈〔<].*[)】）}\]》」﹞〉〕>]", "", newsec_item)

    # 判斷上一階段中的處理狀況，是否把詞彙完全移除
    if newsec_item2 != "":      # 詞彙並非 "" 狀況
        # 階段 3-1：呈 階段2 結果，做以下處理：1.去除詞彙當中 "英文形式且後面包含區隔符號" 的 "字元組" 2.呈1，去除前後空白 3.呈2，去除去除首尾特殊符號 4.呈3，再去除前後空白
        newsec_item3 = re.sub(r"[a-zA-ZＡ-Ｚ][-:：./ )]", "", newsec_item2).strip(" ").strip(sign_list.stripsign()).strip(" ")
        return newsec_item3
    else:                       # 詞匯因 階段 2 成為 "" 狀況
        # 階段 3-2：呈 階段1 結果，做以下處理：1.去除詞彙當中 "英文形式且後面包含區隔符號" 的 "字元組" 2.呈1，去除前後空白 3.呈2，去除去除首尾特殊符號 4.呈3，再去除前後空白
        newfood_item3 = re.sub(r"[a-zA-ZＡ-Ｚ][-:：./ )]", "", newsec_item).strip(" ").strip(sign_list.stripsign()).strip(" ")
        return newfood_item3

## 第二層過濾器
def second_filter(trd_item):
    # 階段 1：將引入進來的第一層過濾後的資料做以下處理：1.去除首尾空白 2.去除首尾有以下羅列的符號
    newtrd_item = trd_item.strip(" ").strip("(【（{[《「﹝〈〔<)】）}]》」﹞〉〕>#,，、.:=※")
    # 判斷引入進來的第一層過濾後的資料是否具有 XO醬 這詞匯
    if "XO醬" not in trd_item:   # 詞匯中不具有 XO醬
        # 階段 2-1：呈 階段 1 結果，做以下處理：1.去除詞彙當中所有非中文字的字元
        newtrd_item2 = re.sub(r"[^\u4e00-\u9fa5]", "", newtrd_item)
        return newtrd_item2
    else:                        # 詞匯中具有 "XO醬"
        # 無論詞會有什麼字元，含有 XO醬 的詞匯直接轉換成 "XO醬"
        newtrd_item2 = "XO醬"
        return newtrd_item2


## 食譜名稱過濾器
def name_filter(recipe_name):
    # 階段 1：將引入進來的詞匯做以下處理：1.去除詞彙當中 2.去除首尾空白 3.去除 tab 空格型態字元 4. 去除換行型態字元
    c_name = re.sub(r"[\'\"]", "", recipe_name).strip().replace("\t", " ").replace("\n", "")

    # 階段 2：呈 階段1 結果，去除詞彙當中有自定義的特殊符號表中出現的字元
    c_name2 = re.sub(r"[{}]".format(sign_list.stripsign_origin()), "", c_name)

    # 階段 3：呈 階段2 結果，做以下處理：1.去除除了中文、英文及指定的框對符號以外的字元 2.去除首尾空白
    clean_name = re.sub(r"[^\u4e00-\u9fa5()\[\]{}\-a-zA-Z0-9]", " ", c_name2).strip()
    return clean_name


















