from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL.ExifTags import TAGS
from fractions import Fraction

from EXIF import get_exif, select_exif


def create_image(image_path, output_path):
    """
    画像を白背景の正方形キャンバスの中心に配置

    Args:
        image_path (str): 入力画像のパス
        output_path (str): 出力画像のパス

    Returns:
        None

    Examples:
        >>> center_image_on_white_background("input.jpg", "output.jpg")
    """

    image = Image.open(image_path)

    # 画像の元の幅と高さを取得
    original_width, original_height = image.size

    # 正方形のキャンバスサイズを決定（元の画像の幅と高さのうち大きい方に合わせる）
    canvas_size = max(original_width, original_height)

    # 白背景の正方形キャンバスを作成
    canvas = Image.new("RGB", (canvas_size, canvas_size), "white")

    # 画像をキャンバスの中心に配置
    offset_x = (canvas_size - original_width) // 2
    offset_y = (canvas_size - original_height) // 2
    canvas.paste(image, (offset_x, offset_y))

    # 結果の画像を保存
    canvas.save(output_path)

    # print(f"画像が'{output_path}'に保存されました。")




def create_image_with_padding(input_path, output_path, padding=0.1):
    """
    画像を白背景の正方形キャンバスの中心に配置し、横に余白を追加

    Args:
        input_path (str): 入力画像のパス
        output_path (str): 出力画像のパス
        padding (float): 余白の割合（0.0～1.0）

    Returns:
        None

    Examples:
        >>> center_image_with_padding("input.jpg", "output.jpg", padding=0.1)
    """


    image = Image.open(input_path)

    # 元の幅と高さを取得
    original_width, original_height = image.size

    # 余白を追加した新しいキャンバスの幅を計算
    new_width = int(original_width * (1 + padding))
    new_height = max(new_width, original_height)  # 正方形になるように調整

    # 白背景の正方形キャンバスを作成
    canvas = Image.new("RGB", (new_width, new_width), "white")

    # 中心に画像を配置
    offset_x = (new_width - original_width) // 2
    offset_y = (new_width - original_height) // 2
    canvas.paste(image, (offset_x, offset_y))

    # 結果を保存
    canvas.save(output_path)

    # print(f"画像が'{output_path}'に保存されました。")





def create_image_with_padding_and_EXIF(image_path, output_path, fonts=None, font_sizes=None, line_spacing=None):
    """
    正方形白背景の中心に画像を配置し、画像下部の余白にEXIF情報を追加。

    Args:
        image_path (str): 入力画像のパス
        output_path (str): 出力画像のパス
        fonts (list): 各行のフォントパスを指定するリスト。
        font_sizes (list): 各行のフォントサイズを指定するリスト。
        line_spacing (list): 各行の行間を指定するリスト。

    Returns:
        None
    """
    # EXIF情報の取得と選択
    exif_data = get_exif(image_path)
    selected_exif = select_exif(exif_data)

    # 画像読み込み
    image = Image.open(image_path)
    original_width, original_height = image.size

    # 正方形キャンバスサイズを決定
    canvas_size = max(original_width, original_height) + 300  # 下部余白をさらに追加
    canvas = Image.new("RGB", (canvas_size, canvas_size), "white")

    # 画像をキャンバスの中央に配置
    offset_x = (canvas_size - original_width) // 2
    offset_y = (canvas_size - original_height - 300) // 2  # 下部余白を考慮
    canvas.paste(image, (offset_x, offset_y))

    # 描画用オブジェクト
    draw = ImageDraw.Draw(canvas)

    # デフォルトフォントパスを設定
    if fonts is None:
        fonts = ["/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"] * 4

    # デフォルトフォントサイズと行間を設定
    if font_sizes is None:
        font_sizes = [50, 50, 50, 50]  # デフォルトフォントサイズ
    if line_spacing is None:
        line_spacing = [30, 30, 30, 30]  # デフォルト行間

    # テキスト情報のリスト
    texts = [
        selected_exif.get("Date", "N/A"),
        selected_exif.get("Camera Model", "N/A"),
        f"Focal Length: {selected_exif.get('Focal Length (mm)', 'N/A')} mm",
        f"ISO: {selected_exif.get('ISO', 'N/A')} | F: {selected_exif.get('F-Number', 'N/A')} | S: {selected_exif.get('Shutter Speed (s)', 'N/A')}",
    ]

    # 各行のテキストを描画
    text_y_start = original_height + (canvas_size - original_height) // 2  # 余白部分の中央
    center_x = canvas_size // 2  # キャンバスの中心

    current_y = text_y_start  # 描画開始位置

    for idx, (text, font_path, font_size, spacing) in enumerate(zip(texts, fonts, font_sizes, line_spacing)):
        # 使用するフォントを設定
        try:
            font = ImageFont.truetype(font_path, font_size)
        except IOError as e:
            print(f"Error loading font: {font_path}. Please check the font path.")
            raise e

        # テキストの描画位置を計算
        text_bbox = draw.textbbox((0, 0), text, font=font)  # テキストのバウンディングボックス
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = center_x - text_width // 2  # 中央揃え

        # テキストを描画
        draw.text((text_x, current_y), text, fill="black", font=font)

        # 次の行のY座標を計算（行ごとの行間を適用）
        current_y += text_height + spacing

    # 結果を保存
    canvas.save(output_path)



# test

