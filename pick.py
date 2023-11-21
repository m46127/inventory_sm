import streamlit as st
import pandas as pd
from io import BytesIO

def create_data_entry_form():
    # データ入力フォームの作成
    with st.form("data_entry_form"):
        # ユーザーがデータを入力できるフィールドを作成
        jan_code = st.text_input("JANコード")
        quantity = st.number_input("数量", min_value=0)
        name = st.text_input("名称")
        submit_button = st.form_submit_button("データを追加")

    # 入力されたデータを返す
    return jan_code, quantity, name, submit_button

def picking_page():
    st.title('PDFファイル処理アプリ')

    # 空のデータフレームを作成
    processed_data = pd.DataFrame(columns=["JANコード", "数量", "名称"])

    # データ入力フォームを表示
    jan_code, quantity, name, submitted = create_data_entry_form()

    # データが送信された場合、データフレームに追加
    if submitted and jan_code and name:
        new_row = {"JANコード": jan_code, "数量": quantity, "名称": name}
        processed_data = processed_data.append(new_row, ignore_index=True)
        st.success("データが追加されました")

    # データフレームを表示
    if not processed_data.empty:
        st.write(processed_data)

        # データをExcelファイルとしてダウンロード可能にする
        towrite = BytesIO()
        processed_data.to_excel(towrite, index=False)
        towrite.seek(0)
        st.download_button(label="Excelファイルとしてダウンロード", 
                           data=towrite, 
                           file_name="total_pickinglist.xlsx", 
                           mime="application/vnd.ms-excel")

picking_page()
