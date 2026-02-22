import os


def get_relative_path(folder, extensions=None):
    """
    スクリプトの配置されているディレクトリからの相対パスで
    指定したフォルダ内の画像ファイルのパスをすべて取得する

    Args:
        folder (str): フォルダのパス（スクリプトディレクトリからの相対パスまたは絶対パス）
        extensions (list): 対象とする拡張子のリスト (例: ['.jpg', '.png'])
                            Noneの場合、すべての画像拡張子が対象となる

    Returns:
        list: 画像ファイルの相対パスのリスト
    """

    # サポートされる拡張子のデフォルトリスト
    if extensions is None:
        extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']

    # このスクリプトのディレクトリ
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # フォルダの絶対パスを計算
    folder_abs = os.path.abspath(os.path.join(script_dir, folder))

    # 結果を格納するリスト
    image_paths = []

    # フォルダ内を再帰的に探索
    for root, _, files in os.walk(folder_abs):
        for file in files:
            # ファイルの拡張子をチェック
            if any(file.lower().endswith(ext) for ext in extensions):
                # スクリプトのディレクトリ基準で相対パスを取得
                absolute_path = os.path.join(root, file)
                relative_path = os.path.relpath(absolute_path, start=script_dir)
                image_paths.append(relative_path)

    return image_paths




def get_image_paths_with_output(input_dir, output_dir, extensions=None):
    """
    指定されたinput_dir内の画像ファイルのパスを取得し、
    output_dirに対応する出力パスを生成する。

    Args:
        input_dir (str): 入力ディレクトリのパス
        output_dir (str): 出力ディレクトリのパス
        extensions (list): 対象とする拡張子のリスト (例: ['.jpg', '.png'])
                            Noneの場合、すべての画像拡張子が対象となる

    Returns:
        list: (入力パス, 出力パス)のタプルのリスト
    """

    # サポートされる拡張子のデフォルトリスト
    if extensions is None:
        extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']

    # 入力ディレクトリの絶対パスを取得
    input_dir_abs = os.path.abspath(input_dir)
    output_dir_abs = os.path.abspath(output_dir)

    # 結果を格納するリスト
    input_output_paths = []

    # 入力ディレクトリ内を再帰的に探索
    for root, _, files in os.walk(input_dir_abs):
        for file in files:
            # ファイルの拡張子をチェック
            if any(file.lower().endswith(ext) for ext in extensions):
                # 入力ファイルの絶対パス
                input_path = os.path.join(root, file)

                # 入力ディレクトリからの相対パス
                relative_path = os.path.relpath(input_path, start=input_dir_abs)

                # 出力ディレクトリの対応する絶対パスを生成
                output_path = os.path.join(output_dir_abs, relative_path)

                # (入力パス, 出力パス)をリストに追加
                input_output_paths.append((input_path, output_path))

    return input_output_paths



# test
'''
if __name__ == "__main__":
    folder_path = "../image"  # スクリプトディレクトリからの相対パス
    image_paths = get_relative_path(folder_path)

    # 結果を表示
    print("画像ファイルの相対パス:")
    for path in image_paths:
        print(path)
'''
