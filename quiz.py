import random

#クイズと解答群、正解、解説のセット
sets=[
 #q, as,cors
["問題1 今月は何月ですか？","6月:7月:8月:9月:10月:11月:12月","10月","説明1"],
["q2","a:b:c:d" ,"b:c:d","説明2"]   ,
["q3","a:b:c:d:e" ,"a","説明3"]   ,
["q4","a:b:c:d" ,"b:a:d","説明4"],   
["q5","a:b:c:d:e:f:g" ,"a","説明5"],   
["q6","a:b:c" ,"d","説明6"]   ,
]


for q1 in sets:#背骨
    print(q1[0])#質問文の表示

    arr = q1[1].split(":")#解答群の作成　多数の中から４つをランダムで選択
    print("arr=",arr)
    if len(arr)<4:
        crs=len(arr)
    else:
        crs=4    
    result = random.sample(arr, crs) #7つの要素から4こを入れる
    print("result=",result)
    for i in range(crs):
        print(i+1,result[i])
    n=int(input("番号を入力してください"))

    cs=q1[2].split(":")
    # print("set result=",set(result))
    # print("set cs=",set(cs))
    print("set result&cs=",set(result) & set(cs))
    cors = list(set(result) & set(cs))#正解の作成
    print("cors[0]",cors[0])
    print("result[n-1]",result[n-1])
    
    if cors[0] == result[n-1]:
        print("正解")
    else:
        print("不正解")

#sets 4~12 問題、解答群、解答、説明が入っているものが6つある状態
#for in 
#split は()の中の引数を文字を分割する
#lenは要素の数を返す関数
#random.sampleは()の引数を入れる
#listはsetの集合型になっているものを配列に戻す関数
#集合型　rens　（再度確認）