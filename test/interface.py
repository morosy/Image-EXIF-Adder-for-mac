import flet as ft
import os
import path

import create_image as ci



def main(page: ft.Page):
    # ページの設定
    page.title = "画像処理ツール"
    page.window_height = 600
    page.window_width = 400
    page.theme = ft.Theme(color_scheme_seed="blue")

    selected_files = ft.Text()


    def number_of_images_in_dir(dir_path):
        dir_list = os.listdir(dir_path)
        return len([f for f in dir_list if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".jpeg")])


    def visible_number_of_files_in_dir(dir_path):
        message = f"{number_of_images_in_dir(dir_path)}個の画像ファイルが見つかりました。"
        message = message if number_of_images_in_dir(dir_path) > 0 else "入力フォルダに画像が見つかりません"



    global input_TorF, output_TorF
    input_TorF = False
    output_TorF = False

    def visible_running_button():
        if input_TorF and output_TorF:
            running_button.visible = True
        else:
            running_button.visible = False
        running_button.update()
        page.update()


    global input_path, output_path

    def get_input_directry(e: ft.FilePickerResultEvent):
        global input_TorF, input_path
        input_directry.value = e.path if e.path else "キャンセルされました。"
        # print(e.path)
        input_path = e.path
        if os.path.isdir(input_path):
            input_TorF = True
        input_directry.update()

    input_directry_dialog = ft.FilePicker(on_result=get_input_directry)
    input_directry = ft.Text()

    page.overlay.extend([input_directry_dialog])



    def get_output_directry(e: ft.FilePickerResultEvent):
        global output_TorF, output_path
        output_directry.value = e.path if e.path else "キャンセルされました。"
        # print(e.path)
        output_path = e.path
        if os.path.isdir(output_path):
            output_TorF = True
            if input_TorF:
                visible_running_button()
        output_directry.update()

    output_directry_dialog = ft.FilePicker(on_result=get_output_directry)
    output_directry = ft.Text()

    page.overlay.extend([output_directry_dialog])


    def running(e):
        global input_path, output_path
        input_dir = input_path
        output_dir = output_path

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
        # 画面を更新する
        page.update()


    running_button = ft.ElevatedButton("処理開始", icon=ft.icons.DIRECTIONS_RUN, visible=False, on_click=running)








# レイアウト部分
# icon: https://gallery.flet.dev/icons-browser/
    page.add(
        ft.Column(
            [
                ft.Text("1. 入力画像フォルダを選択"),
                ft.ElevatedButton(
                    "フォルダを指定",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=lambda _: input_directry_dialog.get_directory_path(
                    ),
                    disabled=page.web
                ),
                ft.Text("選択したフォルダ:"),
                input_directry,

                ft.Text("2. 出力フォルダを選択"),
                ft.ElevatedButton(
                    "フォルダを指定",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=lambda _: output_directry_dialog.get_directory_path(
                    ),
                    disabled=page.web
                ),
                ft.Text("選択したフォルダ:"),
                output_directry,

                running_button
            ]
        )
    )





if __name__ == "__main__":
    ft.app(target = main)


