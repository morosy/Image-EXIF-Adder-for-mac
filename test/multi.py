import create_image as ci

import path


# 使用例
if __name__ == "__main__":
    input_dir = "../image"  # 画像ディレクトリ
    output_dir = "../output" # 出力ディレクトリ

    dir_list = path.get_relative_path(input_dir)

    # 行ごとのフォントとフォントサイズを指定
    fonts = [
        "/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc",  # 日付用フォント
        "/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc",  # カメラモデル用フォント
        "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",  # 焦点距離用フォント
        "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",  # 設定値用フォント
    ]
    font_sizes = [250, 200, 150, 150]  # 各行のフォントサイズ
    line_spacing = [100, 100, 50, 50]  # 各行の行間

    img_counter = 0
    for image_path in dir_list:
        output_path = output_dir + "/" + image_path.split("/")[-1]
        ci.create_image_with_padding_and_EXIF(image_path, output_path, fonts=fonts, font_sizes=font_sizes, line_spacing=line_spacing)
        img_counter += 1

    print(f"done. {img_counter} images processed.")
