"""-----------------------------------------------------------------------------

從本地端的 自訂義特殊符號表txt 中將資料做成一個 list 型態，以讓之後資料清洗時使用

-----------------------------------------------------------------------------"""



def stripsign():
    f = open("filter\\special_sign2.txt", mode="r" ,encoding="utf-8")
    content = f.readlines()
    f.close()
    special_sign_list = ""
    for oneline in content:
        a_sp = oneline.split(" ")
        for oneitem in a_sp:
            # if oneitem != "":
            special_sign_list = special_sign_list + oneitem
    # print(special_sign_list)
    return special_sign_list

def stripsign_origin():
    f = open("filter\\special_sign.txt", mode="r", encoding="utf-8")
    content = f.readlines()
    f.close()
    special_sign_list = ""
    for oneline in content:
        a_sp = oneline.split(" ")
        for oneitem in a_sp:
            # if oneitem != "":
            special_sign_list = special_sign_list + oneitem
    # print(special_sign_list)
    return special_sign_list

# a = [{1: [['↑雞翅', '6', '隻']], 2: [['‧蜊', '200', '克']], 3: [[' ♓薑片⟢', '2', '片']]}]
# for item in a:
#     # print(item)
#     for item2 in item.values():
#         for item3 in item2[0]:
#             item4 = item3.strip(" ").strip(stripsign_origin()).strip(" ")
#             print(item4)






