import pandas as pd
import streamlit as st
import tabula
import io
import base64

# バイナリファイルダウンローダーのHTMLを生成する関数
def get_binary_file_downloader_html(bin_file, file_label='File'):
    bin_str = base64.b64encode(bin_file).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}">Download {file_label}</a>'
    return href

# PDFファイルからピッキングリストを処理する関数
def process_picking_list_pdf(uploaded_file):
    # PDFからテーブルを読み込む
    tables = tabula.read_pdf(uploaded_file, pages='all', multiple_tables=True)
    # 複数のテーブルを1つのDataFrameに結合する
    picking_list = pd.concat(tables, ignore_index=True)
    # 必要な列に基づいてデータを集計する
    # ここでは 'メーカー型番' と '注文数量の合計' 列が必要
    # 実際のPDF構造に応じて列名を調整する必要がある
    return picking_list.groupby('Unnamed: 1')['Unnamed: 2'].sum().reset_index()

def e_shops_page():
    uploaded_file_picking1 = st.file_uploader("1つ目のピッキングリストPDFをアップロードしてください", type=['pdf'], key='picking1')
    uploaded_file_picking2 = st.file_uploader("2つ目のピッキングリストPDFをアップロードしてください（任意）", type=['pdf'], key='picking2')
    uploaded_file_inventory = st.file_uploader("在庫表ファイルをアップロードしてください", type=['xlsx'], key='inventory')

    if uploaded_file_inventory is not None and uploaded_file_picking1 is not None:
        # 1つ目のピッキングリストの処理
        picking_list_grouped = process_picking_list_pdf(uploaded_file_picking1)

        # 2つ目のピッキングリストがあれば処理
        if uploaded_file_picking2 is not None:
            picking_list_grouped2 = process_picking_list_pdf(uploaded_file_picking2)
            # 2つのピッキングリストを結合
            picking_list_grouped = pd.concat([picking_list_grouped, picking_list_grouped2]).groupby('Unnamed: 1')['Unnamed: 2'].sum().reset_index()

        # 在庫表の各シートを処理
        inventory_sheets = ["在庫表 (PB)", "在庫表 (賞味期限あり)", "ファンケル（賞味期限あり）", "在庫表（賞味期限なし）", "在庫表(資材）"]

        # Excelファイルとして出力
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for sheet in inventory_sheets:
                try:
                    inventory = pd.read_excel(uploaded_file_inventory, sheet_name=sheet, header=5)
                    # 在庫表とピッキングリストの結合
                    result_df = pd.merge(inventory[['ＪＡＮ']], picking_list_grouped, left_on='ＪＡＮ', right_on='Unnamed: 1', how='left')
                    result_df = result_df[['ＪＡＮ', 'Unnamed: 2']]
                    result_df.rename(columns={'Unnamed: 2': '数量'}, inplace=True)
                    # シートごとに結果を保存
                    result_df.to_excel(writer, sheet_name=sheet, index=False)
                except Exception as e:
                    st.error(f"シート {sheet} の読み込み中にエラーが発生しました: {e}")

        binary_excel = output.getvalue()
        st.markdown(get_binary_file_downloader_html(binary_excel, '結果.xlsx'), unsafe_allow_html=True)

if __name__ == "__main__":
    e_shops_page()