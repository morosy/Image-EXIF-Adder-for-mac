import create_image as ci


# 使用例
if __name__ == "__main__":
    input_image_path = "../image/image1.jpg"   # 入力画像パス
    output_image_path = "../output/image.jpg"  # 出力画像パス

    # 行ごとのフォントとフォントサイズを指定
    fonts = [
        "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",  # 日付用フォント
        "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",  # カメラモデル用フォント
        "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",  # 焦点距離用フォント
        "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",  # 設定値用フォント
    ]
    font_sizes = [250, 200, 150, 150]  # 各行のフォントサイズ
    line_spacing = [100, 100, 50, 50]  # 各行の行間

    ci.create_image_with_padding_and_EXIF(input_image_path, output_image_path, fonts=fonts, font_sizes=font_sizes, line_spacing=line_spacing)
    print("done")
