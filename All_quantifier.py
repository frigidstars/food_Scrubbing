import re

"""-----------------------------------------------------------------------------

這程式負責將引入的資料分成食材用量及食材單位，再針對食材用量會出現的書寫形式做標準化處理。
透過大量的正規表示法判斷一筆資料當中什麼是用量什麼是單位。

-----------------------------------------------------------------------------"""

## 建立數字及用量單位的自訂義字典
NumTable = {'零': '0', '一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9',
            '〇': '0', '○': '0', '０': '0', '１': '1', '２': '2', '３': '3', '４': '4', '５': '5', '６': '6',
            '７': '7', '８': '8', '９': '9', '壹': '1', '乙': '1', '貳': '2', '參': '3', '肆': '4', '伍': '5', '陆': '6',
            '柒': '7', '捌': '8', '玖': '9', '半': '0.5', '㏄': "ml", ' ': '', '公克': 'g', '克': 'g', 'cc': "ml",
            'c.c.': "ml", '各': '', 'c,c': "ml", '十': '10', 'c.c': "ml"}

## 預備項目 (狀態：廢案)
'''
'½': "1/2", '⅓': "1/3", '⅔': "2/3", '¼': "1/4", '¾': "3/4", '⅕': "1/5", '⅖': "2/5", '⅗': '3/5', '⅘': '4/6',
'⅙': "1/6", '⅚': "5/6", '⅐': "1/7", '⅛': "1/8", '⅜': "3/8", '⅝': "5/8", '⅞': "7/8", '⅑': '1/9', '⅒': '1/10'
'''

## 單位及用量分離器
def quantifier(input):
    input = input.lower()                     # 將引入的原始資料(含英文字時)做小寫化處理
    input = re.sub('2兩', '兩兩', input)       # 呈上，將詞彙當中出現 "兩兩" 的狀況轉換為 "2兩" ("兩" 本身為一個單位時的狀況)
    input = re.sub(r'\(.+\)', '', input)        # 呈上，將詞彙當中具有 ("任一字元") 的 "字元集" 轉換為 ""

    # 判斷 "兩"後面接任意中文或英文字元的狀況
    if re.search(r'[兩][\u4e00-\u9fa5a-zA-Z]+', input):
        input = input.replace("兩", "2", 1)      # 代換 "兩" > 2 (ex, 兩個 > 2個)
    input = input.replace('個人', '各人')       # 代換 "個人" > "個人" (ex, 依個人喜好 > 依各人喜好)

    tempstr = input

    # 逐一取出自訂義字典中的 key 值，作為判斷依據及代換使用
    for ChangeWord in NumTable.keys():
        # 判斷某 key 值 是否存在於引入的原始資料中
        if ChangeWord in input:
            # 將詞彙中符合的項目以該 key 值對應的 value 值代換
            tempstr = re.sub(ChangeWord, NumTable[ChangeWord], tempstr)
        input = tempstr

    # 如果有任何形式的冒號字元出現在詞彙當中，其 "食物用量" 及 "食物單位" 皆以 None 輸出 (ex, 1:3:5)
    if ':' in input or ':' in input or '：' in input:
        num = None
        unit = None

    # 處理 1/2~3/2; 1/2~2; 2~1/3
    elif re.search(r'((([1-9]+[0-9]*\/[1-9]+[0-9]*)|([1-9]+))[-|—|~|～|_|到|至](([1-9]+[0-9]*\/[1-9]+[0-9]*)))|((([1-9]+[0-9]*\/[1-9]+[0-9]*))[-|—|~|～|_|到|至](([1-9]+[0-9]*\/[1-9]+[0-9]*)|([1-9]+)))', input):
        tempNumList = re.search(r'((([1-9]+[0-9]*\/[1-9]+[0-9]*)|([1-9]+))[-|—|~|～|_|到|至](([1-9]+[0-9]*\/[1-9]+[0-9]*)))|((([1-9]+[0-9]*\/[1-9]+[0-9]*))[-|—|~|～|_|到|至](([1-9]+[0-9]*\/[1-9]+[0-9]*)|([1-9]+)))', input).group()
        tempNum0 = re.search(r'(.*)[-|—|~|～|_|到|至]', tempNumList).group()
        tempNum1 = re.findall(r"[0-9]+", tempNum0)
        if len(tempNum1) == 2:
            num = round(eval(tempNum1[0]) / eval(tempNum1[1]), 2)
            try:
                unit = re.search(r"[\u4e00-\u9fa5a-zA-Z]+$", input).group()
            except:
                unit = None
        else:
            num = eval(tempNum1[0])
            try:
                unit = re.search(r"[\u4e00-\u9fa5a-zA-Z]+$", input).group()
            except:
                unit = None

    # 處理 1.5~2.0; 2~3
    elif re.search(r'(([0-9]+[\.]{1}[0-9]+)|([0-9]+))[-|—|~|～|_|到|至]{1}(([0-9]+[\.]{1}[0-9]+)|([0-9]+))|(([0-9]+)[-|—|~|～|_|到|至]{1}([0-9]+))', input):
        tempNumList = re.search(r'(([0-9]+[\.]{1}[0-9]+)|([0-9]+))[-|—|~|～|_|到|至]{1}(([0-9]+[\.]{1}[0-9]+)|([0-9]+))|(([0-9]+)[-|—|~|～|_|到|至]{1}([0-9]+))', input).group()
        tempNum0 = re.findall(r"([0-9]+\.[0-9]+)|([0-9]+)", tempNumList)[0][0]
        num = tempNum0
        try:
            unit = re.search(r"[\u4e00-\u9fa5a-zA-Z]+$", input).group()
        except:
            unit = None

    # 處理 ex, 1又1/2
    elif re.search(r'[0-9]+又{1}[1-9]+[\/]{1}[1-9]+[0-9]*', input):
        tempNumList = re.search(r'[0-9]+又{1}[1-9]+[\/]{1}[1-9]+[0-9]*', input).group()
        tempNum0 = re.findall(r"[0-9]+", tempNumList)
        tempNum1 = eval(tempNum0[0]) + round(eval(tempNum0[1]) / eval(tempNum0[2]), 2)
        num = tempNum1
        try:
            unit = re.search(r"[\u4e00-\u9fa5a-zA-Z]+$", input).group()
        except:
            unit = None

    # 處理 1又2分之1
    elif re.search(r'[0-9]+又{1}[1-9]+([分][之]){1}[1-9]+[0-9]*', input):
        tempNumList = re.search(r'[0-9]+又{1}[1-9]+([分][之]){1}[1-9]+[0-9]*', input).group()
        tempNum0 = re.findall(r"[0-9]+", tempNumList)
        tempNum1 = eval(tempNum0[0]) + round(eval(tempNum0[2]) / eval(tempNum0[1]), 2)
        num = tempNum1
        try:
            unit = re.search(r"[\u4e00-\u9fa5a-zA-Z]+$", input).group()
        except:
            unit = None

    # 處理 1/2
    elif re.search(r'[0-9]+[\/]{1}[1-9]+[0-9]*', input):
        tempNumList = re.search(r'[0-9]+[\/]{1}[1-9]+[0-9]*', input).group()
        tempNum0 = re.findall(r"[0-9]+", tempNumList)
        tempNum1 = round(eval(tempNum0[0]) / eval(tempNum0[1]), 2)
        num = tempNum1
        try:
            unit = re.search(r"[\u4e00-\u9fa5a-zA-Z]+$", input).group()
        except:
            unit = None

    # 處理 2分之1
    elif re.search(r'[0-9]+([分][之]){1}[1-9]+[0-9]*', input):
        tempNumList = re.search(r'[0-9]+([分][之]){1}[1-9]+[0-9]*', input).group()
        tempNum0 = re.findall(r"[0-9]+", tempNumList)
        tempNum1 = round(eval(tempNum0[1]) / eval(tempNum0[0]), 2)
        num = tempNum1
        try:
            unit = re.search(r"[\u4e00-\u9fa5a-zA-Z]+$", input).group()
        except:
            unit = None

    # 處理小數點 ex, 1.2
    elif re.search(r'[0-9]+\.[0-9]+', input):
        num = re.search(r'[0-9]+\.[0-9]+', input).group()
        try:
            unit = re.search(r"[\u4e00-\u9fa5a-zA-Z]+$", input).group()
        except:
            unit = None

    # 處理只有數字 ex, 5; 1.5; 1/5
    elif re.search(r'^([0-9]+[\/]{1}([1-9]+[0-9]*))$|^([0-9]+[\.]{1}[0-9]+)$|^([0-9]+)$', input):
        num = re.search(r'^([0-9]+[\/]{1}([1-9]+[0-9]*))$|^([0-9]+[\.]{1}[0-9]+)$|^([0-9]+)$', input).group()
        unit = None

    # 只有量詞 ex, 適量
    elif re.search(r'[0-9]+', input) is None and re.search(r'[\u4e00-\u9fa5a-zA-Z]+', input):
        num = None
        try:
            unit = re.search(r"[\u4e00-\u9fa5a-zA-Z]+", input).group()
        except:
            unit = None

    # 正常情況 ex, 15公克; 15g
    elif re.search(r'[0-9]+', input) and re.search(r'[\u4e00-\u9fa5a-zA-Z]+$', input):
        num = re.search(r'[0-9]+', input).group()
        try:
            unit = re.search(r"[\u4e00-\u9fa5a-zA-Z]+$", input).group()
        except:
            unit = None

    else:
        num = 0
        unit = None

    if num == '':
        num = None

    if num != None and isinstance(num, str) == True:
        num = eval(num)

    # print('-------------')
    # print(input)
    # print('數量:', num)
    # print('量詞:', unit)

    return num, unit



# if __name__ == '__main__':
    # start = time.clock()
    #
    # end = time.clock()
    # print("CPU Time: ", end - start)
