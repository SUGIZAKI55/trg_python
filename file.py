# ファイルからデータを読み込む関数
def load_quiz_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read().strip()  # ファイル全体を読み込み、前後の空白を除去

    # 問題ごとにデータを分割する（空行で分割）
    questions = content.split('\n\n')
    sets = []

    # 各問題のデータをリストに変換
    for question in questions:
        parts = question.split('\n')
        if len(parts) == 4:  # 問題文、選択肢、正解、説明の4部分からなることを確認
            sets.append(parts)

    return sets

# ファイル名を指定して関数を呼び出し
filename = 'quiz_questions.txt'
quiz_sets = load_quiz_from_file(filename)

# 結果を表示
for q in quiz_sets:
    print(q)
