import os, sys
import fitz
import flet as ft

def extract_images(fname):
    dist = os.path.splitext(fname)[0]
    os.makedirs(dist, exist_ok=True)  # ディレクトリが存在しない場合は作成

    with fitz.open(fname) as doc:
        for i, page in enumerate(doc):
            for j, img in enumerate(page.get_images(full=True)):
                x = doc.extract_image(img[0])
                name = os.path.join(dist, f"{i:04}_{j:02}.{x['ext']}")
                with open(name, "wb") as ofh:
                    ofh.write(x['image'])

def get_application_directory():
    if getattr(sys, 'frozen', False):
        # In built executable
        application_path = sys._MEIPASS
    else:
        # In dev environment
        application_path = os.path.dirname(__file__)
    
    return application_path

def main(page: ft.Page):

    page.window.width = 400
    page.window.height = 300
    page.title = "PDFから画像を抽出"
    page.theme = ft.Theme(color_scheme_seed="cyan")

    icon_path = os.path.join(get_application_directory(), "icon.ico")
    print(icon_path)
    page.window.icon = icon_path

    def on_file_picker_result(e: ft.FilePickerResultEvent):
        if e.files:
            file_path.value = e.files[0].path
            page.update()

    def on_extract_click(e):
        if file_path.value:
            extract_images(file_path.value)
            result.value = "画像の抽出が完了しました。"
            page.update()

    file_picker = ft.FilePicker(on_result=on_file_picker_result)
    file_path = ft.TextField(label="選択されたファイル", read_only=True)
    pick_file_button = ft.ElevatedButton(text="ファイルを選択", on_click=lambda _: file_picker.pick_files())
    extract_button = ft.ElevatedButton(text="画像を抽出", on_click=on_extract_click)
    result = ft.Text()

    page.overlay.append(file_picker)
    page.add(pick_file_button, file_path, extract_button, result)

if __name__ == "__main__":
    ft.app(target=main)