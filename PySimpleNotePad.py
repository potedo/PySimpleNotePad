# coding: utf-8

import os
import sys
# import pyperclip
import PySimpleGUI as sg
import tkinter as tk
from tkinter import messagebox

# Constants: For Key Bind
CTRL_PLUS_S = "s:83"

# 21/06/02 
# Undo/Redo(ctrl + Z, ctrl + Y)の機能を追加したい
# → https://github.com/PySimpleGUI/PySimpleGUI/issues/2836
# にかかれている、TKinterにある機能を上手く使用してRedo/Undoを実装するか。
# https://teratail.com/questions/255389
# あるいはteratailのこの情報とか。

def resource_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(os.path.abspath('.'), relative)


# textはMultiline.Widgetを指す(->TKtext?)
def redo(event, text):
    try:
        text.edit_redo()
    except:
        pass


menu_def_en = [["&File", ["New",
                          "Open", 
                          "&Save        Ctrl+S", 
                          "Save as", 
                          "&Quit"]],
               ["&Edit", ["Undo    Ctrl+Z",
                          "Redo    Ctrl+Y",
                          "Cut",
                          "Copy",
                          "Paste",]],
               ["&Format", ["Font"]],
               ["&Help", ["Help", "Version"]]]

menu_def_jp = [["&ファイル", ["新規",
                            "開く", 
                            "&上書き保存        Ctrl+S", 
                            "名前を付けて保存", 
                            "&終了"]],
                       ["&編集", ["元に戻す    Ctrl+Z",
                                 "再実行　    Ctrl+Y",
                                  "切り取り",
                                  "コピー",
                                  "貼り付け",]],
                       ["&書式", ["フォント"]],
                       ["&ヘルプ", ["バージョン情報"]]]

if __name__ == "__main__":
    # print(sys.getdefaultencoding())
    language_mode = "jp" # もう一つは "en"
    default_font = ("Meiryo UI", 9)

    sg.theme("SystemDefault1")

    menu = sg.MenuBar(menu_def_jp,
                      key="menubar", pad=((0,0),(0,0)), font=("メイリオ", 9))
    # save_as_button = sg.FileSaveAs(key="saveas", enable_events=True)

    right_click_menu_en = ['&Right', ['Undo    Ctrl+Z', 'Redo    Ctrl+Y', 'Cut', 'Copy', 'Paste']]
    right_click_menu_jp = ['&Right', ['元に戻す    Ctrl+Z', "再実行　    Ctrl+Y", '切り取り', 'コピー', '貼り付け']]

    # -----------------------------------------------------------------
    #  Custom SaveAs Button: ボタンの機能だけ使いたいが、表示したくないのでカスタム
    #  確認先：10643行目 FileSaveAsクラス Definition
    # -----------------------------------------------------------------
    save_as_custom_button = sg.Button(key="saveas",
                                      button_text="Save as...",
                                      target=(sg.ThisRow, -1),
                                      file_types=(("ALL Files", "*.*"),("Text Files", "*.txt"),),
                                      initial_folder=None,
                                      default_extension="",
                                      disabled=False,
                                      tooltip=None,
                                      size=(None, None),
                                      s=(None, None),
                                      auto_size_button=None,
                                      button_color=None,
                                      change_submits=False,
                                      enable_events=True, # Trueに変更
                                      font=None,
                                      pad=((0,0),(0,0)),
                                      k=None,
                                      metadata=None,
                                      button_type=sg.BUTTON_TYPE_SAVEAS_FILE,
                                      visible=False)

    files_browse_button = sg.Button(key="file_browse",
                                    button_type=sg.BUTTON_TYPE_BROWSE_FILES,
                                    pad=((0,0),(0,0)),
                                    visible=False)


    layout = [[menu],
              [sg.Multiline(key="note", pad=((0,0),(0,0)), border_width=1, right_click_menu=right_click_menu_jp, font=default_font)],
              [sg.StatusBar("行:1 列:1", key="status_bar", pad=((0,0),(0,0)),font=default_font)],
            #    sg.StatusBar("Windows (CRLF)", key="status_bar2", pad=((0, 0), (0, 0))),
            #    sg.StatusBar("UTF-8", key="status_bar3", pad=((0,0),(0,0)))],
              [save_as_custom_button, files_browse_button]] #enable_events=Trueにすると、イベントとして取得可能


    icon_path = resource_path("win_memo.ico")

    # キーボードショートカットを有効にするため、return_keyboard_eventsをTrueにしている
    # margins=(0,0)とすることで、ウインドウ端の余白をなくすことができる
    window = sg.Window("無題 - PySimpleNotePad", layout, size=(600, 400), icon=icon_path, resizable=True, finalize=True, 
                       return_keyboard_events=True, element_padding=((0,0),(0,0)), border_depth=1, margins=(0,0), enable_close_attempted_event=True)
    window["note"].expand(expand_x=True, expand_y=True) # ウィンドウサイズに応じて入力エリアを可変に

    text = window["note"].Widget
    text.configure(undo=True) # Undo機能追加
    text.bind("<Control-Key-Y>", lambda event, text=text:redo(event, text)) #Redo機能追加

    #-------
    # "X"ボタン押下時の確認画面用
    # → 上手く動かなかった
    # windowにenable_close_attempted_event=Trueを追加することで対応
    #------
    # root = window.TKroot

    # def on_closing():
    #     if messagebox.askokcancel("Quit", "Do you want to quit?"):
    #         root.destroy()

    # root.protocol("WM_DELETE_WINDOW", on_closing)

    save_filepath = None

    while True:

        event, values = window.Read()

        print(event, values)
        # print(window["note"].Widget.index("insert"))
        # print(type(window["note"].Widget.index("insert")))



        # Window生成時に、enable_close_attempt_eventをTrueにすれば、
        # "-WINDOW CLOSE ATTEMPTED-"イベントで検出、条件を満たした場合のみ終了、が可能
        if event in (sg.WIN_CLOSED, "Quit", "終了", "-WINDOW CLOSE ATTEMPTED-"):

            confirm_exit = sg.popup_ok_cancel("PySimpleNotePadを閉じますか？", title="PySimpleNotePad", keep_on_top=True, icon=icon_path, font=default_font)

            if confirm_exit == "OK":
                break

        elif event in ("New", "新規"):
            # popup 定義はPySimpleGUI.pyの16034行目に存在

            # popup処理は、要するに別のWindowを作成する処理
            # → 今回の内容に該当するものは関数化しておく？

            # savepathの有無で挙動を変えたい
            # -> save_filepathが存在するときは、普通のボタンとスイッチさせる？
            if save_filepath is None or save_filepath == "":
                save_as_popup_button = sg.Button(key="popup_saveas",
                                                button_text="保存する",
                                                target=(sg.ThisRow, -1),
                                                file_types=(
                                                    ("ALL Files", "*.*"), ("Text Files", "*.txt"),),
                                                initial_folder=None,
                                                default_extension="",
                                                disabled=False,
                                                tooltip=None,
                                                size=(None, None),
                                                s=(None, None),
                                                auto_size_button=None,
                                                button_color=None,
                                                change_submits=False,
                                                enable_events=True,  # Trueに変更
                                                font=default_font,
                                                pad=None,
                                                k=None,
                                                metadata=None,
                                                button_type=sg.BUTTON_TYPE_SAVEAS_FILE,
                                                bind_return_key=True)
            else:
                save_as_popup_button = sg.Button(key="popup_save",
                                                 button_text="保存する",
                                                 font=default_font,
                                                 enable_events=True,
                                                 bind_return_key=True)


            popup_layout_jp = [[sg.Text("この内容を保存しますか？", font=default_font)],
                            [save_as_popup_button,
                             sg.Button("保存しない", font=default_font),
                             sg.Button("キャンセル", font=default_font)]]

            # ここにもicon=icon_pathを指定することで、ウィンドウ左上のアイコンを任意のものに変更可能
            popup_window = sg.Window("PySimpleNotePad", popup_layout_jp, auto_size_text=True,
                                     background_color=None, button_color=None, auto_close=False,
                                     auto_close_duration=None, icon=icon_path, font=None,
                                     no_titlebar=False, grab_anywhere=False, keep_on_top=False,
                                     location=(None, None)
                                     )

            # このポップアップ自体も、現在編集中のファイルが変更されていた場合のみという用に変更したい
            # ポップアップの処理: 参考 → PySimpleGUI.py 16034行目以降
            while True:
                # 最初からノンブロッキング処理にして、__TIMEOUT__ イベントが発生しているときに"popup_saveas"がNoneでなければ保存して遷移、で良いかも
                popup_button, popup_values = popup_window.read(timeout=0)
                print(popup_button, popup_values)                

                if popup_button in (sg.WIN_CLOSED, "キャンセル"):
                    break

                # Save As をクリックしたときの処理、ノンブロッキング処理で対応する
                elif popup_button == "__TIMEOUT__":

                    if "popup_saveas" in popup_values.keys():
                        if popup_values["popup_saveas"] != "":
                            with open(popup_values["popup_saveas"], "w") as f:
                                f.write(values["note"])
                            break

                elif popup_button == "保存しない":
                    break

                elif popup_button == "popup_save":
                    with open(save_filepath, "w") as f:
                        f.write(values["note"])
                    break

            # 終了処理。忘れないこと。
            popup_window.close()
            del popup_window

            # OKボタンを押したか、保存先を指定した場合のみテキスト領域をクリアする
            if popup_button in ("保存しない", "__TIMEOUT__", "popup_save"):
                window["note"].update("")
                save_filepath = None # 保存先もクリア(新しくファイルを開くのに、前のファイルを編集するのはおかしい)
                values["file_browse"] = ""


        elif event in ("Open", "開く"):

            files_browse_button.click()
            event, values = window.read(timeout=0) #ここはノンブロッキングでないと止まってしまう
            save_filepath = values["file_browse"]

            if not save_filepath == "":
                with open(save_filepath, "r") as f:
                    text = f.read() #全文読み込み

                window["note"].update(text)
                # window["status_bar"].update("{} opened.".format(save_filepath))


        # s:83 → ctrl+S のイベントに対応 ： CTRL_PLUS_S = "s:83"といった感じで、定数として管理した方が分かりやすそう
        elif event in("Save", CTRL_PLUS_S, "上書き保存        Ctrl+S"):

            if save_filepath is None or save_filepath == "":
                save_as_custom_button.click()
                event, values = window.read(timeout=0)
                save_filepath = values["saveas"]

            input_texts = values["note"]

            if save_filepath != "":
                with open(save_filepath, "w") as f:
                    f.write(input_texts)

                # window["status_bar2"].update("Text saved.")



        elif event in ("Save as", "名前を付けて保存"):

            save_as_custom_button.click() # 既にあるボタンのインスタンスをクリックする形で実装すればよい(layoutに含まれる必要あり)
            # この処理の後、event が "saveas" になるので、上記処理へ遷移する
            # ということはない。同じくここでwindow.read(timeout=0)を実行し、そのパスで保存を実行しないといけない
            event, values = window.read(timeout=0)
            save_filepath = values["saveas"]

            if save_filepath != "":
                input_texts = values["note"]
                with open(save_filepath, "w") as f:
                    f.write(input_texts)


        elif event in ("Redo    Ctrl+Y", "再実行　    Ctrl+Y"):
            try:
                window["note"].Widget.edit_redo()
            except:
                pass

        elif event in ("Undo    Ctrl+Z", "元に戻す    Ctrl+Z"):
            try:
                window["note"].Widget.edit_undo()
            except:
                pass

        
        elif event in ("Copy", "コピー"):
            # try - except で弾かれたとき用に、バックアップの値を用意しておく
            backup = window["note"].Widget.clipboard_get()
            window["note"].Widget.clipboard_clear()
            try:
                selected_text = window["note"].Widget.selection_get()
                # print(selected_text)
                # print(type(selected_text))
                window["note"].Widget.clipboard_append(selected_text)
            except:
                window["note"].Widget.clipboard_append(backup)
                pass



        elif event in ("Paste", "貼り付け"):
            try:
                clipboard_text = window["note"].Widget.clipboard_get()
                # print(clipboard_text)
                # print(type(clipboard_text))
                insert_pos = window["note"].Widget.index("insert")
                window["note"].Widget.insert(insert_pos, clipboard_text)
            except:
                pass
            
        
        elif event in ("Cut", "切り取り"):
            try:
                selected_text = window["note"].Widget.selection_get()
                window["note"].Widget.clipboard_clear()
                window["note"].Widget.clipboard_append(selected_text)
                window["note"].Widget.delete(tk.SEL_FIRST, tk.SEL_LAST) # 選択範囲の最初から最後までを削除
            except:
                pass

        
        elif event in ("Font", "フォント"):

            size_list = [i for i in range(8, 13)] + [2*i for i in range(7, 15)] + [36, 48, 72]
            size_list_box = sg.Listbox(size_list, key="size", size=(20, 7), default_values=[12], enable_events=True, pad=((0, 0), (0, 20)))
            font_list = [font for font in tk.font.families() if not font[0] == "@"]
            font_list_box = sg.Listbox(font_list, key="font_list", size=(30, 7), default_values=["Meiryo UI"], enable_events=True, pad=((0,0),(0,20)))

            font_layout = [[sg.Text("フォント名：", size=(32, 1), pad=((0,0),(0,0)), font=default_font), sg.Text("サイズ：", size=(20, 1), pad=((0,0),(0,0)), font=default_font)],
                           [font_list_box, size_list_box],
                           [sg.Button("OK", key="OK"), sg.Button("Cansel", key="Cansel")]]

            font_window = sg.Window("フォント", font_layout, auto_size_text=True,
                                    background_color=None, button_color=None, auto_close=False,
                                    auto_close_duration=None, icon=icon_path, font=None,
                                    no_titlebar=False, grab_anywhere=False, keep_on_top=False,
                                    location=(None, None)
                                    )

            while True:

                font_button, font_values = font_window.read()
                print(font_button, font_values)

                if font_button in (sg.WIN_CLOSED, "Cansel"):
                    break

                if font_button == "OK":
                    f = tk.font.Font(family=font_values["font_list"][0], size=font_values["size"][0])
                    window["note"].Widget.configure(font=f)
                    break

            font_window.close()

        
        elif event in ("バージョン情報"):
            sg.popup_ok("PySimpleNotePad \nver. 1.0.0", font=("Meiryo UI", 10), icon=icon_path)

        # 右クリックメニューが変更できなさそうなので断念。ウインドウを作り直せば行ける？
        # elif event in ("Switch Language", "表示言語切り替え"):
        #     if language_mode == "jp":
        #         window["menubar"].Update(menu_definition=menu_def_en)
        #         window["note"].Widget.RightClickMenu = right_click_menu_en
        #         language_mode = "en"
        #     else:
        #         window["menubar"].Update(menu_definition=menu_def_jp)
        #         window["note"].Update(right_click_menu=right_click_menu_jp)
        #         language_mode = "jp"

        # elif event == "Status Bar":
        #     if window["status_bar"].visible:
        #         window["status_bar"].Update(visible=False)
        #     else:
        #         window["status_bar"].Update(visible=True)


        # 編集中のファイルに合わせてタイトルの表示を変更する(ifでbreakする前に配置すると、windowが消えた時にエラーとなるのでここに記述)
        if save_filepath:
            # パスを表示しているが、ファイル名だけ上手く取得したい
            save_filename = os.path.basename(save_filepath)
            window.TKroot.title(save_filename + "- PysimpleNotePad")
        else:
            window.TKroot.title("無題 - PySimpleNotePad")
            # window.TKroot.title("No title - PySimpleNotePad")

        # マウスクリックでカーソルが移動した場合も表示変更されるようにしたい
        insert_pos = window["note"].Widget.index("insert")
        insert_pos = insert_pos.split(".")
        window["status_bar"].update("行:{} 列:{}".format(insert_pos[0], int(insert_pos[1])+1))



    window.close()

