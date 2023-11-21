import streamlit as st
import pandas as pd
import base64  # base64をインポート
from io import BytesIO

def process_data(picking_list, stock_list):
    # ピッキングリストからJANコードと数量を取得
    picking_data = picking_list[['JANコード', '数量']]
    
    # 在庫表のデータを処理
    for sheet_name, stock_sheet in stock_list.items():
        # 在庫表のJANコード列とピッキングリストのJANコードを照合し、数量を更新
        stock_sheet = stock_sheet.merge(picking_data, on='JANコード', how='left')
        stock_list[sheet_name] = stock_sheet

    return stock_list

def download_link(object_to_download, download_filename, download_link_text):
    # ダウンロードリンクの生成
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_excel(index=False, engine='openpyxl')

    b64 = base64.b64encode(object_to_download).decode()
    return f'<a href="data:file/xlsx;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

def e_shops_page():
    st.title('在庫管理アプリ')

    # ピッキングリストと在庫表のアップロード
    # e_shops.pyのfile_uploaderの部分を更新
    picking_file = st.file_uploader("ピッキングリストをアップロード", type="xlsx", key="unique_e_shops_picking_file_uploader")
    stock_file = st.file_uploader("在庫表をアップロード", type="xlsx", key="unique_e_shops_stock_file_uploader")


    if picking_file and stock_file:
        # ファイル読み込み
        picking_list = pd.read_excel(picking_file)
        stock_list = pd.read_excel(BytesIO(stock_file.read()), sheet_name=None)

        # データ処理
        processed_data = process_data(picking_list, stock_list)

        # 処理後のデータを新しいExcelファイルに保存
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for sheet_name, data in processed_data.items():
                data.to_excel(writer, sheet_name=sheet_name, index=False)

        # ダウンロードリンクの生成
        st.markdown(download_link(output.getvalue(), 'processed_stock.xlsx', '処理後の在庫表をダウンロード'), unsafe_allow_html=True)

# e_shops_page() の呼び出しを削除
