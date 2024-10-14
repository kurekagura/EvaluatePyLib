# README

## 環境

```console
py -3.12 -m venv .py312
```

```console
pip install -r requirements.txt
```

## 出力画像のサイズ

出力画像の最大があるようで、自分の環境だと最大幅は下記であった。それを超えた画像を出力するとエラーは発生しないものの白黒のような画像が生成された。

```python
dpi=100
w_pix, h_pix = 327 * dpi, 1080  # 32700 OK
# w_pix, h_pix = 328 * dpi, 1080  # NG 327インチが最大のようだ
```

回避策として、BBoxを用いてクロップし、複数画像に分割して出力するとうまくいった。

```python
 bb_width = (w_pix - side_margin * 2) / 2
 # BBoxの作成 (左下の座標 (x_min, y_min), 幅 width, 高さ height)
 bbox1 = mtransforms.Bbox.from_bounds(side_margin / dpi, 0, bb_width / dpi, h_pix / dpi)
 print(bbox1, f"{bbox1.width}x{bbox1.height}")
 fig.savefig(".output/cropped1.png", bbox_inches=bbox1)
 bbox2 = mtransforms.Bbox.from_bounds(bbox1.x0 + bbox1.width, 0, bb_width / dpi, h_pix / dpi)
 print(bbox2, f"{bbox2.width}x{bbox2.height}")
 fig.savefig(".output/cropped2.png", bbox_inches=bbox2)
```

## 参考・謝辞

- [Pythonで株価をチャートに描画する ～Matplotlib編～](https://note.com/aoiam/n/n6a7b2cae0988)
