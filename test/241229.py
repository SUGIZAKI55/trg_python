import json

# NDJSONファイルを読み込む
log_data = []
with open('seiseki.ndjson', 'r', encoding='utf-8') as file:
    for line in file:
        log_data.append(json.loads(line.strip()))

# データの表示と解析
for entry in log_data:
    print(f"日付: {entry['date']}, ユーザー: {entry['name']}")
    print(f"ジャンル: {entry['genre'].strip()}")
    print(f"問題ID: {', '.join([q.strip() for q in entry['qmap']])}")
    print(f"開始時間: {entry['start_time']}, 終了時間: {entry['end_time']}")
    print(f"経過時間: {entry['elapsed_time']}")
    print(f"選択肢: {', '.join(entry['user_choice'])}")
    print(f"正解: {', '.join(entry['correct_answers'])}")
    print(f"結果: {entry['result']}")
    print("-" * 50)
