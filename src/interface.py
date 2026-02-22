# GUI/interface.py
import os
import asyncio
import flet as ft

import process


class App:
    def __init__(self):
        self.input_dir: str | None = None
        self.output_dir: str | None = None

    def main(self, page: ft.Page):
        # ===== UI state helpers =====
        def is_valid_dir(p: str | None) -> bool:
            return bool(p) and os.path.isdir(p)

        def refresh_buttons():
            running_button.visible = is_valid_dir(self.input_dir) and is_valid_dir(self.output_dir)
            running_button.disabled = processing.value
            running_button.update()

        def set_finished_message(msg: str, color: str):
            finished_message.value = msg
            finished_message.color = color
            finished_message.visible = True
            finished_message.update()

        # ===== event handlers (Flet 0.80.x style) =====
        async def pick_input_dir(e):
            # FilePicker is a SERVICE in 0.80.x: call it and await the result
            path = await ft.FilePicker().get_directory_path()
            self.input_dir = path if path else None

            selected_input_dir.value = self.input_dir if self.input_dir else "キャンセルされました。"
            selected_input_dir.update()

            refresh_buttons()

        async def pick_output_dir(e):
            path = await ft.FilePicker().get_directory_path()
            self.output_dir = path if path else None

            selected_output_dir.value = self.output_dir if self.output_dir else "キャンセルされました。"
            selected_output_dir.update()

            refresh_buttons()

        async def running(e):
            # validate
            if not is_valid_dir(self.input_dir) or not is_valid_dir(self.output_dir):
                set_finished_message("入力/出力フォルダが正しく選択されていません。", "red")
                return

            processing.value = True
            refresh_buttons()
            finished_message.visible = False
            finished_message.update()

            try:
                # 重い処理ならUIフリーズ防止のため別スレッドで実行
                await asyncio.to_thread(process.process, self.input_dir, self.output_dir)

                set_finished_message("処理が完了しました！", "green")
            except Exception as ex:
                set_finished_message(f"エラーが発生しました: {ex}", "red")
            finally:
                processing.value = False
                refresh_buttons()

        # ===== page setup =====
        page.theme_mode = ft.ThemeMode.LIGHT
        page.title = "Image EXIF adder for mac"
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.window_height = 600
        page.window_width = 800

        # ===== controls =====
        processing = ft.Ref[bool]()
        processing.value = False

        finished_message = ft.Text(
            value="",
            visible=False,
            color="green",
            size=20,
            text_align=ft.TextAlign.CENTER,
        )

        selected_input_dir = ft.Text(value="選択されていません", color="blue")
        selected_output_dir = ft.Text(value="選択されていません", color="blue")

        running_button = ft.ElevatedButton(
            "処理開始",
            icon=ft.Icons.DIRECTIONS_RUN,
            visible=False,
            on_click=running,  # asyncio.run() は使わない
        )

        finish_button = ft.ElevatedButton(
            "ウィンドウを閉じる",
            icon=ft.Icons.CLOSE,
            on_click=lambda _: page.window_close(),
        )

        # ===== layout =====
        page.add(
            ft.Column(
                [
                    ft.Text("Image EXIF adder for mac", size=30, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=20, thickness=1),

                    ft.Text("1. 入力フォルダを選択してください", size=18),
                    ft.ElevatedButton(
                        "フォルダを指定",
                        icon=ft.Icons.DRIVE_FOLDER_UPLOAD_ROUNDED,
                        on_click=pick_input_dir,
                    ),
                    ft.Text("選択フォルダ:", size=16),
                    selected_input_dir,

                    ft.Divider(height=20, thickness=1),

                    ft.Text("2. 出力先を選択してください", size=18),
                    ft.ElevatedButton(
                        "フォルダを指定",
                        icon=ft.Icons.DRIVE_FOLDER_UPLOAD_ROUNDED,
                        on_click=pick_output_dir,
                    ),
                    ft.Text("選択フォルダ:", size=16),
                    selected_output_dir,

                    ft.Divider(height=20, thickness=1),

                    running_button,
                    finished_message,

                    ft.Divider(height=20, thickness=1),
                    finish_button,
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

        refresh_buttons()
