import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mplotticker
import matplotlib.transforms as mtransforms


def read_csv(csv_file_path):
    """
    CSVからpandasのDataFrameにロードする関数。
    必須の列とオプション列があるので、オプション列のリストも戻す。
    """
    df = pd.read_csv(csv_file_path, encoding="utf-8", engine="python")

    # 可変の列を抽出
    fixed_columns = {"取引日", "始値", "終値", "安値", "高値", "出来高"}
    optional_columns = [col for col in df.columns if col not in fixed_columns]
    # 固定列の処理
    df["date"] = df["取引日"]
    df["open"] = df["始値"]
    df["close"] = df["終値"]
    df["low"] = df["安値"]
    df["high"] = df["高値"]
    df["volume"] = df["出来高"]
    df.set_index("date", inplace=True)  # 文字列としてインデックス
    return df, optional_columns


def plot_price_of_column(axis, df, plot_column):
    """
    指定されたカラムのデータをaxisにプロットする関数。
    NaNの値は無視してプロットする。
    """
    # NaNを無視したデータを抽出
    valid_data = df[[plot_column]].dropna()
    axis.plot(valid_data.index, valid_data[plot_column], label=plot_column)


if __name__ == "__main__":
    plt.rcParams["font.family"] = "MS Gothic"
    # matplotlib.use("Qt5Agg")  # 'TkAgg' 'Qt5Agg' を試す
    # plt.ion()  # インタラクティブモードを有効にする
    # matplotlib.interactive(False)

    # parser = argparse.ArgumentParser(description="チャート生成検証コード")
    # parser.add_argument("datestart", help="開始日")  # 必須の引数
    # parser.add_argument("dateend", help="開始日")  # 必須の引数
    # args = parser.parse_args()
    # start = args.datestart
    # end = args.dateend

    csv_file_path = "../../../PrivateJunkData/20241013_StockChartData2.csv"
    abs_csv_file_path = os.path.abspath(csv_file_path)
    df, variable_columns = read_csv(abs_csv_file_path)
    date_count = len(df) - 1  # ヘッダを除いた行数

    label_date_size = 9
    label_price_size = 12
    label_ratio_size = 9
    dpi = 100

    # ピクセル単位で指定した幅と高さ
    # w_pix, h_pix = 326 * dpi, 1080  # OK
    w_pix, h_pix = 327 * dpi, 1080  # 32700 OK
    # w_pix, h_pix = 328 * dpi, 1080  # NG 327インチが最大のようだ
    # w_pix, h_pix = date_count * 18, 1080
    # w_pix, h_pix = 34000, 1080
    # w_pix, h_pix = 32700 * 2, 1080

    inchfigsize = (w_pix / dpi, h_pix / dpi)

    price_axis_height = h_pix * 0.7  # チャートエリアの高さ
    tick_area_height = 100  # x軸目盛りエリアの高さ
    ratio_axis_height = h_pix - price_axis_height - tick_area_height  # 騰落レシオエリアの高さ
    side_margin = 60  # 縦軸ラベルの幅

    # # インチ指定が必須のためインチに変換
    fig = plt.figure(figsize=inchfigsize, dpi=dpi)
    print(inchfigsize)
    print(w_pix, h_pix)

    left_margin_ratio = side_margin / w_pix
    ww_ratio = (w_pix - side_margin * 2) / w_pix

    ax_price = fig.add_axes([left_margin_ratio, ((tick_area_height + ratio_axis_height) / h_pix), ww_ratio, (price_axis_height / h_pix)])
    ax_ratio = fig.add_axes([left_margin_ratio, (tick_area_height / h_pix), ww_ratio, (ratio_axis_height / h_pix)])

    ax_price.plot(df.index, df["close"], color="blue", marker=".")
    # ax_price.set_ylabel("Price", fontsize=label_price_size)
    ax_price.set_xticks(range(len(df)))  # データポイントの数だけX軸の目盛を設定
    ax_price.set_xlim(0, len(df) - 1)  # 余白なしの設定
    ax_price.set_xticklabels([""] * len(df))  # ラベルを空に設定
    ax_price.tick_params(labelright=True, labelsize=label_price_size)
    ax_price.grid(True)

    ratio = ((df["close"] - df["close"].shift(1)) / df["close"].shift(1)) * 100
    # X軸のマスの数
    x_tick_num = len(df) - 1
    # X座標方向へ1枠分ずらしてバーを描画
    x_tick_val = 1 / x_tick_num
    bar_pos_x = range(0, len(df))  # 最初のNaNを避けるため1から開始
    # ax_ratio.bar(df.index[1:], ratio[1:], color="blue", width=0.05)  # 最初のNaNを避けるためにindex[1:]を使用
    ax_ratio.bar([x - 0.5 for x in bar_pos_x], ratio, color="gray", width=0.8)  # widthを適切に設定

    ax_ratio.yaxis.set_major_formatter(mplotticker.FuncFormatter(lambda x, _: f"{x:.2f}%"))
    ax_ratio.tick_params(labelright=True, labelsize=label_ratio_size)
    # ax_ratio.set_ylabel("ratio", fontsize=label_ratio_size)

    ax_ratio.set_xticks(range(len(df)))  # データポイントの数だけX軸の目盛を設定
    ax_ratio.set_xlim(0, len(df) - 1)  # 余白なしの設定
    ax_ratio.set_xticklabels(df.index, rotation=90, horizontalalignment="center", fontsize=9)
    ax_ratio.grid(True)

    # 可変列をループでプロット
    for column in variable_columns:
        plot_price_of_column(ax_price, df, column)

    ax_price.legend(fontsize=label_price_size)  # 凡例

    # plt.show(block=True)

    base_name = os.path.splitext(os.path.basename(abs_csv_file_path))[0]  # ファイル名の取得と拡張子を.pngに変更
    img_output_path = f".output/{base_name}_{w_pix}x{h_pix}-dpi{dpi}.png"
    if not os.path.exists(".output"):
        os.makedirs(".output")

    # extent = ax_price.get_window_extent()
    # print(extent)
    # bbox = extent.transformed(fig.dpi_scale_trans.inverted())
    # print(bbox)

    # bb_width = (w_pix - side_margin * 2) / 2
    # # BBoxの作成 (左下の座標 (x_min, y_min), 幅 width, 高さ height)
    # bbox1 = mtransforms.Bbox.from_bounds(side_margin / dpi, 0, bb_width / dpi, h_pix / dpi)
    # print(bbox1, f"{bbox1.width}x{bbox1.height}")
    # fig.savefig(".output/cropped1.png", bbox_inches=bbox1)
    # bbox2 = mtransforms.Bbox.from_bounds(bbox1.x0 + bbox1.width, 0, bb_width / dpi, h_pix / dpi)
    # print(bbox2, f"{bbox2.width}x{bbox2.height}")
    # fig.savefig(".output/cropped2.png", bbox_inches=bbox2)

    fig.savefig(img_output_path, dpi=dpi)  # 解像度(dpi)を指定することもできる

    print("finished.")
