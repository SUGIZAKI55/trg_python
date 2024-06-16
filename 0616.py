# arr = ["ライオン","象","ペンギン","ムカデ","サル","ハチ"] 

# if len(arr) < 4: #llenは要素の数　len arrが6 これは成り立たないケース6<4
#     crs = len(arr) #成り立たないので実行されなし
# else:
#     crs = 4  # 解答群の中から4つ選ぶための数を設定

# import random
# result = random.sample(arr, crs)

# print(result)

import random
q1 = ["問題2 以下の動物の中で鳥はどれ？","ライオン:象:ペンギン:カンガルー:カモメ:スズメ","ペンギン:カモメ:スズメ","ペンギンは鳥の一種ですが、飛べません。"] 

arr = q1[1].split(":")  # 解答群の作成　多数の中から４つをランダムで選択
print("arr=",arr)
if len(arr) < 4:
    crs = len(arr)
else:
    crs = 4
print("crs=",crs)
result = random.sample(arr, crs)      
print("result=",result)

cs_temp = set(q1[2].split(":")) #正解をここで作っておく　["ペンギン","カモメ","スズメ"]
print("cs_temp=",cs_temp)
correct_choices = set(result) & cs_temp #積集合
print("correct_choices=",correct_choices)

# for i, choice in enumerate(result, 1):
#     print(i, choice)