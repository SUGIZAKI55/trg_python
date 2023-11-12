import random

sets = [
    ["問題1 今月は何月ですか？", "6月:7月:8月:9月:10月:11月:12月", "10月", "説明1"],
    ["問題2 以下の動物の中で鳥はどれ？", "ライオン:象:ペンギン:カンガルー:カモメ:スズメ", "ペンギン:カモメ:スズメ", "ペンギンは鳥の一種ですが、飛べません。"],
    ["問題3 最も大きな惑星は？", "地球:火星:木星:金星", "木星", "木星は太陽系で最も大きな惑星です。"],
    ["問題4 日本の首都は？", "大阪:東京:福岡:仙台", "東京", "日本の首都は東京です。"],
    ["問題5 以下の中で果物はどれ？", "ピーマン:キャベツ:ブロッコリー:メロン:パイナップル:バナナ", "メロン:パイナップル:バナナ", "メロン:パイナップル:バナナは果物の一種ですが、野菜としても扱われることが多いです。"],
    ["問題6 以下の言語の中でスペイン語で「こんにちは」は？", "Hello:Bonjour:Halo:Hola", "Hola", "スペイン語で「こんにちは」は「Hola」と言います。"],
]

for q1 in sets: #13~23 １セット
    print(q1[0])  # 質問文の表示

    arr = q1[1].split(":")  # 解答群の作成　多数の中から４つをランダムで選択
    if len(arr) < 4:
        crs = len(arr)
    else:
        crs = 4    
    result = random.sample(arr, crs)
    
    for i, choice in enumerate(result, 1):
        print(i, choice)
    
    n = input("番号を入力してください: ")
    user = n.split(":")
    usern = list(map(int,user))
    print("usern=",list(usern))
    a =[]
    for u1 in usern:
        a.append(result[u1-1])
        print("u1=",u1,"result[u1-1]=",result[u1-1])
    
    cs = set(q1[2].split(":"))
    correct_choices = set(result) & cs
    print("correct_choices=",correct_choices)

    a_set = set(a)
    target_set = correct_choices
    if a_set == target_set:
        print("配列aは目的の集合と一致します。")
    else:
        print("配列aは目的の集合と一致しません。")

#setは照合で使うことが便利