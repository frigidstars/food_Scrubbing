import json
import pandas as pd
import All_syncword as sync

sync_dict = sync.create_dict("人工處理分類/syncword_1by1.xlsx")
# print(sync_dict)
df_json = pd.read_json("[200619_2]recipe.json")["Recipe"]
df = pd.read_excel("人工處理分類/衛服部營養素資料庫0613.xlsx")["Ingredient Name"]
df_list = list(x for x in df)
x = 0
for item in df_json:
    # print(item)
    if item["RecipeName"] == "" or item["RecipeName"] == None:
        print(item)
    if item["RecipeURL"] == "" or item["RecipeURL"] == None:
        print(item)
    if item["Ingredients"] == [] or item["Ingredients"] == None:
        print(item)
    for it in item["Ingredients"]:
        if (it["It_name"] == "") or (it["It_name"] == None):
            print(it)
        # if (it["It_quantity"] == "") or (it["It_quantity"] == None) or (it["It_quantity"] == 0):
        #     print(it)
        # if (it["It_unit"] == "") or (it["It_unit"] == None):
        #     print(it)

        new_itname = sync.trans_word(it["It_name"], sync_dict)
        if new_itname not in df_list:
            print(it)
    print(x)
    x = x + 1
print("完成")