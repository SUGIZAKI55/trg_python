import time
import datetime

# 現在の日付と時刻を取得
start_datetime = datetime.datetime.now()
print(f"開始時刻: {start_datetime}")

# ここで時間を計測したい処理を実行する
time.sleep(2)  # 例として2秒間待つ

end_datetime = datetime.datetime.now()
print(f"終了時刻: {end_datetime}")

elapsed_time = end_datetime - start_datetime
print(f"高精度な実行時間: {elapsed_time} 秒")
