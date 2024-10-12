import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

# CSVデータを読み込む
data = """取引日,始値,終値,安値,高値
"1970/01/01","20000","20000","20000","20000"
"2021/01/04","25000","25000","25000","25000"
"9999/12/31","23000","23000","23000","23000"
"""

df = pd.read_csv(StringIO(data))

fig, ax_price = plt.subplots(figsize=(10, 6))

# 存在する終値をプロット
ax_price.plot(df["取引日"], df["終値"], color="black", marker=".")

# X軸の目盛を等間隔にするためにインデックスを設定
ax_price.set_xticks(range(len(df)))  # データポイントの数だけX軸の目盛を設定

# X軸のラベル設定（文字列形式）
ax_price.set_xticklabels(df["取引日"], rotation=90)  # ダブルクオーテーションを除去

ax_price.tick_params(labelright=True, labelsize=8)
ax_price.grid(True)
ax_price.set_ylabel("Price", fontsize=12)

plt.title("Stock Chart")
plt.tight_layout()
plt.show(block=True)
