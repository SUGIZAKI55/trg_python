# org = [[1,"時事:雑学:歴史"],
# [2,"雑学:動物学:歴史"],
# [3,"雑学:スポーツ"],
# ]
# # ジャンルに当てはまるIDを抽出する

# genredic2 = {} #ジャンルに対して何個あるかを確認
# for o1 in org:
#     # print (o1[1]) 時事:雑学:歴史 ""囲まれた文字列
#     o2 = o1[1].split(":")
#     # print (o2) #['時事', '雑学', '歴史']　[]で囲まれた配列
#     for o3 in o2:
#         print(o3) #'時事', '雑学', '歴史'　文字列として抜き出したので改行もされる
#         #genredic2の中にo3があれば、カウント+1をする、なければo3をキーとしてカウントを1とする辞書を作る
#         if o3 in genredic2: #genredic2の中にo3があるかどうか　orgのカウントをする目的
#             genredic2[o3] += 1 #{"時事":2} {}辞書　、時事:2のキーが時事で、バリュー2がというバリューが更新される
#         else:
#             genredic2[o3] = 1 #{"時事":1} {}辞書　、時事:1のキーが時事で、バリューが1という辞書ができる
#         print(genredic2)

# genredic3 = {}
# for o4 in org:
#     o5 = o4[0]
#     print (o5) #ID番号の1,2,3を表示した
#     o2 = o4[1].split(":")
#     for o3 in o2:
#         print(o3) #'時事', '雑学', '歴史'　文字列として抜き出したので改行もされる
#         #genredic3の中にo3があれば、IDを追加する、なければo3をキーとしてカウントを1とする辞書を作る
#         if o3 in genredic3:
#             genredic3[o3].append(o5)
#         else:
#             genredic3[o3] = [o5] 
#         print(genredic3)
#     for o6 in o5:
#         print(o6) #'時事', '雑学', '歴史'　文字列として抜き出したので改行もされる
#         if o6 in genredic3:
#             genredic3[o6] += 1 #{"時事":2} {}辞書　、時事:2のキーが時事で、バリュー2がというバリューが更新される
#         else:
#             genredic3[o6] = 1 #{"時事":1} {}辞書　、時事:1のキーが時事で、バリューが1という辞書ができる
#         print(genredic3)


# genredic3 = {   #どのジャンルにID番号が入っているかを表示する
# "雑学":[1,2,3],
# "時事":[1],
# "歴史":[1,2],
# "動物学":[2],
# "スポーツ":[3],
# }

topics = [
    [1, "時事:雑学:歴史"],
    [2, "雑学:動物学:歴史"],
    [3, "雑学:スポーツ"],
]


# 各トピックのIDをジャンルごとに分類する辞書
genre_to_ids = {}

for topic in topics: #: pythonの基本でインデントの前に使われる#
    topic_id = topic[0]
    genre_list = topic[1].split(":")
    
    for genre in genre_list:
        # ジャンルに対応するIDリストを更新
        if genre in genre_to_ids:
            genre_to_ids[genre].append(topic_id) #配列に追加する場合にappendを使う
        else:
            genre_to_ids[genre] = [topic_id]

# 結果を表示
print("ジャンルごとのIDリスト:", genre_to_ids)

#答え
# ジャンルごとのIDリスト: {'時事': [1], '雑学': [1, 2, 3], '歴史': [1, 2], '動物学': [2], 'スポーツ': [3]}