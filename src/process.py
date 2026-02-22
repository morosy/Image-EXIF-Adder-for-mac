import sys
import create_image as ci
import path as pt

def process(input_image_path: str, output_image_path: str):
    # input_image_path = sys.argv[1]   # 入力画像パス
    # output_image_path = sys.argv[2]  # 出力画像パス

    # 行ごとのフォントとフォントサイズを指定
    fonts = [
        "/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc",  # 日付用フォント
        "/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc",  # カメラモデル用フォント
        "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",  # 焦点距離用フォント
        "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",  # 設定値用フォント
    ]
    font_sizes = [250, 200, 150, 150]  # 各行のフォントサイズ
    line_spacing = [100, 100, 50, 50]  # 各行の行間

    pathes = pt.get_image_paths_with_output(input_image_path, output_image_path)
    for path in pathes:
        ci.create_image_with_padding_and_EXIF(path[0], path[1], fonts=fonts, font_sizes=font_sizes, line_spacing=line_spacing)
