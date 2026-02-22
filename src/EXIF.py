from PIL import Image
from PIL.ExifTags import TAGS
from math import gcd


def format_date(date_string):
    """
    日付フォーマットを変更し、時間部分を削除

    Args:
        date_string (str): 元のEXIF日付文字列 (例: "2024:08:03 11:38:44")

    Returns:
        str: フォーマット変更後の日付文字列 (例: "2024.08.03")
    """
    if not date_string or " " not in date_string:
        return "N/A"
    date_part = date_string.split(" ")[0]  # 時間部分を削除
    return date_part.replace(":", ".")




def convert_to_fraction(decimal_value):
    """
    小数を分数形式に変換

    Args:
        decimal_value (float): 小数値 (例: 0.000625)

    Returns:
        str: 分数形式の文字列 (例: "1/1600")
    """
    if not isinstance(decimal_value, (float, int)):
        return "N/A"

    denominator = 1
    while (decimal_value * denominator) % 1 != 0:  # 小数点以下が消えるまで分母を増やす
        denominator *= 10
    numerator = int(decimal_value * denominator)
    common_divisor = gcd(numerator, denominator)  # 最大公約数で約分
    numerator //= common_divisor
    denominator //= common_divisor
    return f"{numerator}/{denominator}"



def get_exif(image_path):
    """
    画像のEXIF情報を取得

    Args:
        image_path (str): 画像のパス

    Returns:
        dict: 画像のEXIF情報

    Examples:
        >>> exif = get_exif("image.jpg")
    """

    exif_data = Image.open(image_path)._getexif()
    if exif_data:
        exif = {
            TAGS.get(tag, tag): value
                for tag, value in exif_data.items()
        }

        return exif




def select_exif(exif_data):
    """
    指定されたEXIFデータから特定の情報を抽出して返す

    Args:
        exif_data (dict): EXIFデータを含む辞書

    Returns:
        dict: 抽出したEXIF情報を含む辞書
            対象情報:
                - 日付 (DateTimeOriginal)
                - カメラモデル (Model)
                - ISO感度 (ISOSpeedRatings)
                - 焦点距離 (FocalLength)
                - F値 (FNumber)
                - シャッタースピード (ExposureTime)
    """
    # 抽出するキーをリストで指定
    target_keys = {
        "DateTimeOriginal": "Date",
        "Model": "Camera Model",
        "ISOSpeedRatings": "ISO",
        "FocalLength": "Focal Length (mm)",
        "FNumber": "F-Number",
        "ExposureTime": "Shutter Speed (s)"
    }

    # 必要なキーを抽出
    selected = {label: exif_data.get(key, "N/A") for key, label in target_keys.items()}

    # 日付フォーマットを修正
    if "Date" in selected and selected["Date"] != "N/A":
        selected["Date"] = format_date(selected["Date"])

    # シャッタースピードを分数形式に変換
    if "Shutter Speed (s)" in selected and selected["Shutter Speed (s)"] != "N/A":
        try:
            selected["Shutter Speed (s)"] = convert_to_fraction(float(selected["Shutter Speed (s)"]))
        except ValueError:
            selected["Shutter Speed (s)"] = "N/A"

    return selected





# Test
'''
if __name__ == "__main__":
    path = "../image/image.jpg"
    exif = get_exif(path)
    for tag, value in exif.items():
        print(f"{tag}: {value}")
'''
