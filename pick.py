import streamlit as st
import pandas as pd
import numpy as np
import tabula
from io import BytesIO

def picking_page():
    # Streamlitアプリのタイトルを設定
    st.title('PDFファイル処理アプリ')

    # ファイルアップローダーを設置
    uploaded_files = st.file_uploader("PDFファイルを選択してください", accept_multiple_files=True, type="pdf")

    if uploaded_files:
        df_all = pd.DataFrame()

        for uploaded_file in uploaded_files:
            # BytesIOを使用してPDFファイルを読み込む
            df_list = tabula.read_pdf(BytesIO(uploaded_file.read()), pages='all', stream=True, pandas_options={'header': None})

            for data_frame in df_list:
                # 各PDFファイルからデータを抽出し、データフレームに変換
                header_row = data_frame[data_frame[1] == 'JANコード'].index[0]
                data_frame.columns = data_frame.iloc[header_row]
                data_frame = data_frame.drop(header_row)
                data_frame = data_frame[['JANコード', '数量 名称']].dropna()
                data_frame[['数量', '名称']] = data_frame['数量 名称'].str.split(' ', n=1, expand=True)
                data_frame = data_frame.drop(columns=['数量 名称', '名称'])
                data_frame['数量'] = pd.to_numeric(data_frame['数量'], errors='coerce').astype(np.int64)

                df_all = pd.concat([df_all, data_frame], ignore_index=True)


        # '合計'行を削除
        df_all = df_all[df_all['JANコード'] != '合計']

        # JANコードでグループ化して数量を合計
        df_all = df_all.groupby('JANコード').sum().reset_index()

        # 結果を表示
        st.write(df_all)

        # データをExcelファイルとしてダウンロードするためのボタンを配置
        towrite = BytesIO()
        df_all.to_excel(towrite, index=False)  # towriteにデータを書き込む
        towrite.seek(0)  # ファイルポインターを先頭に戻す
        st.download_button(label="Excelファイルとしてダウンロード", 
                           data=towrite, 
                           file_name="total_pickinglist.xlsx", 
                           mime="application/vnd.ms-excel")
        

