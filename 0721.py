# # ランダムな解答群と正解を設定
# cho = ["b", "d", "e", "f"]  # ランダム解答群
# sei = ["c", "e"]  # 正解

# # 各選択肢に対して○×判定を行う
# result = {choice: '○' if choice in sei else '×' for choice in cho}
# print(result)

# # 結果を表示
# for choice, mark in result.items():
#     print(f"{choice}: {mark}")


# ランダムな解答群と正解を設定
cho = ["b", "d", "e", "f"]  # ランダム解答群
sei = ["c", "e"]  # 正解

# # 各選択肢に対して○×判定を行う
# result = {}
# for choice in cho:
#     if choice in sei:
#         result[choice] = '○'
#     else:
#         result[choice] = '×'

# # 結果を表示
# for choice, mark in result.items():
#     print(f"{choice}: {mark}")


for c1 in cho:
    if c1 in sei:
        print(c1,"o")
    else:
        print(c1,"x")