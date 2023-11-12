# ar = [5, 8, 2, 7]
# total = 0

# # # 配列の値を足している
# # for num in ar:
# #     total = total + num

# # #　iはindex番号、 rangeは0から4未満の整数
# # for i in range(4): 　　　0,1,2,3, 
# #     total = total + ar[i]

# i ar[i] total(右側) total（左側）
# 0 5     0           5
# 1 8     5           13
# 2 2     13          15
# 3 7     15          22


# # print(total)

# 4+3=7
# 5
# 6
# 7+3=10
# 8
# 9
# 10+3=13
# 11
# 12

# #range(4,13)＝range(4,13,1)と同じ
# # for i in range(4,13):
# 4+1
# 5+1
# 6+1
# 7+1
# 8+1
# 9+1
# 10+1
# 11+1
# 12+1

# #range(4)＝range(0,4,1)と同じ
# # for i in range(4):
# 0 
# 0+1
# 1+1
# 2+1
# 3+1

#listは本物の配列にしたいとき元々が仮装配列
# a=range(4,13,3)
# b=list(a)
# print(b)
# 4
# 4+3
# 7+3

# i = [0]
# for i in range(10):
#     total = i + 1
#     print(total)

#rangeはパラメーター 1~11未満の整数の範囲を指定
# for i in range(0,11,1):
#     print(i)

#-3~5 2ずつ
# for i in [-3,-1,1,3,5]:
#     print(i)

# for i in range(-3,6,2):
#     print(i)

#[]の部分がイテラブル（繰り返し）
for i in ["アップル","マンゴー","イチゴ","スイカ","メロン"]:
    print(i)