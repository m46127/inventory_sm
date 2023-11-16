# main.py
import streamlit as st
from streamlit_option_menu import option_menu

# メニューの選択肢を定義
menu_options = ["トップページ", "ピッキング", "e-shops", "店舗"]

# サイドバーでオプションメニューを表示
selected_option = option_menu("メインメニュー", menu_options, icons=['house', 'upload', 'sort', 'file-pdf', 'layers', 'box'], menu_icon="cast", default_index=0)

# 選択肢に応じて表示するページを変更
if selected_option == "トップページ":
    # トップページの内容
    st.title("トップページ")
    st.write("ようこそ！")

elif selected_option == "ピッキング":
    # pick.py の内容をインポートして実行
    from pick import picking_page
    picking_page()

elif selected_option == "e-shops":
    # e_shops.py の内容をインポートして実行
    from e_shops import main as e_shops_page
    e_shops_page()

elif selected_option == "店舗":
    # store.py の内容をインポートして実行
    from store import main as store_page
    store_page()
