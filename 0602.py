# english:英語
# japanese:日本語

dic = {"english": "英語", "japanese": "日本語"}  # 辞書型の変数名
print(dic["japanese"])

dic2 = {"chinese": "中国語","freanch": "フランス語"}  # 辞書型の変数名

dics =[dic,dic2]
print(dics[1])
print(dics[1]["freanch"])

dic3 = {"german": "ドイツ語", "polish": "ポーランド語"}

dics.append(dic3) #配列に追加をする

print(dics)

print(dics[2])
