import json

# ファイルを読み込み
filename = "seiseki.ndjson"

# 名前とジャンルごとに正解数と問題数を記録する辞書
result_data = {}

try:
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            # 各行を辞書型に変換
            #print(f"{type(line)=}  {line=} ")
            record = json.loads(line.strip())
            #print(f"{type(record)=} {record=}")
            name = record["name"]
            genre = record["genre"].strip()  # ジャンル名を取得
            result = record["result"]

            # 名前が辞書に存在しなければ初期化
            if name not in result_data:
                result_data[name] = {}

            # ジャンルが辞書に存在しなければ初期化
            if genre not in result_data[name]:
                result_data[name][genre] = {"correct": 0, "total": 0}

            # 総問題数を1増加
            result_data[name][genre]["total"] += 1

            # 正確に "正解" と一致する場合のみ正解数を増加
            if result.strip() == "正解":
                result_data[name][genre]["correct"] += 1
    print(f"{result_data=}")

    # 名前とジャンル別に正答率を計算
    for name, genres in result_data.items():
        print(f"名前: {name}")
        for genre, data in genres.items():
            total = data["total"]
            correct = data["correct"]
            
            # 正答率の計算
            if total > 0:
                accuracy = (correct / total) * 100
            else:
                accuracy = 0
            
            print(f"  ジャンル: {genre}, 正答率: {accuracy:.2f}% ({correct}/{total})")

except FileNotFoundError:
    print(f"ファイル '{filename}' が見つかりません。")
except json.JSONDecodeError:
    print("JSON データの解析中にエラーが発生しました。")
