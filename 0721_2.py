fish=["マグロ","イカ","タコ","ウナギ"]
seikai=["タコ","ウナギ"]
dic = {}
# sentaku2="アナゴ"
# dic[sentaku2]="○"
for sentaku in fish:
    # print(sentaku)
    if sentaku in seikai: 
        dic[sentaku]="○"
        # print(sentaku,"○")
    else:
        dic[sentaku]="×"
        # print(sentaku,"×")

# dic3[sentaku]
print(dic.items())
for k,v in dic.items(): 
    print(k,v)
# dic2 = {"マグロ": "×", "イカ": "×","タコ": "○","ウナギ": "○",}  # 辞書型
# print(dic2)

