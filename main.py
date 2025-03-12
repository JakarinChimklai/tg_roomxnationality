import streamlit as st
import pandas as pd
from datetime import datetime
from function import get_google_sheet_database, map_nationality





st.set_page_config(layout="wide")
df = get_google_sheet_database('TG_csv_merge_file', 'MergedData')
df["Nationality"] = df["Nationality"].apply(map_nationality)






# ทำให้ Text อยู่ตรงกลาง
with open("style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

with st.container(key="app_title"):
    st.write("")
    st.title("The Grass Serviced Suites")
    st.title("Room Map X Nationality")
    st.write("")





# Prepare Date Time
if not pd.api.types.is_datetime64_any_dtype(df["date"]):
    df["date"] = pd.to_datetime(df["date"], errors='coerce', dayfirst=True)
df["date"] = df["date"].dt.date





#แบ่ง 3 column สำหรับพวก filter
col1, col2, col3 = st.columns([4.5, 1, 4.5])

#Filter วันที่
with col1:
    selected_date = st.date_input("date", value=datetime.today().date())
    df_filtered = df[df["date"] == selected_date]



with col2:
    st.write("")  #เว้นระยะห่าง



# สร้าง mapping ระหว่าง label กับค่า floor list
floor_mapping = {
    "2nd Floor": ["12", "22"],
    "3nd Floor": ["13", "23"],
    "4nd Floor": ["14", "24"],
    "5nd Floor": ["15", "25"],
    "6nd Floor": ["16", "26"],
    "7nd Floor": ["17", "27"],
    "8nd Floor": ["18", "28"],
}
with col3:
    pill_selected_floor = st.pills('Select Floors', list(floor_mapping.keys()), selection_mode="multi", key="floor_pills")
    st.markdown(f"Selected Floors: {pill_selected_floor}.")





generic_table_data = [
    [""] * 25,
    ["", "BA01", "BA02", "BA03", "BA04", "BA05", "BA06", 
     "BA07", "BA08", "BA09", "BA10", "BA11", "", "BB01", 
     "BB02", "BB03", "BB04", "BB05", "BB06", "BB07", "BB08", 
     "BB09", "BB10", "BB11", ""],
    [""] * 25,
    ["", "BA20", "BA19", "BA18", "BA17", "BA16", "BA15",
     "", "", "BA14", "BA13", "BA12", "", "BB20", "BB19",
     "BB18", "BB17", "BB16", "BB15", "", "", "BB14", "BB13", "BB12", ""],
    [""] * 25
]



def generate_floors(filtered_floor, table_data):
    table_copy = [row.copy() for row in table_data]  # ทำสำเนาตารางให้แยกกัน
    for index, item in enumerate(table_copy):
        for subindex, subitem in enumerate(item):
            if subitem != "":
                if subitem.startswith('BA'):
                    x = subitem[2:]
                    item[subindex] = filtered_floor[0] + x
                elif subitem.startswith('BB'):
                    x = subitem[2:]
                    item[subindex] = filtered_floor[1] + x
    return table_copy

def highlight_table(dataframe):
    """
    กำหนดสไตล์ให้แต่ละเซลล์ตามเงื่อนไขที่กำหนด
    """
    styles = pd.DataFrame("", index=dataframe.index, columns=dataframe.columns)
    for col in dataframe.columns:
        for row in dataframe.index:
            cell = dataframe.at[row, col]
            # กำหนดสไตล์สำหรับคอลัมน์แรก, คอลัมน์ที่ 13 และคอลัมน์สุดท้าย
            if col in [0, 12, 24]:
                styles.at[row, col] = "background-color: black; color: white; text-align: center;"
            elif cell == "IND":
                styles.at[row, col] = "background-color: lightcoral; color: black; text-align: center;"
            elif cell == "FRA":
                styles.at[row, col] = "background-color: blue; color: white; text-align: center;"
            else:
                styles.at[row, col] = "background-color: white; color: black; text-align: center;"
    return styles

def display_floor_map(table_data, floor_label):
    # สร้าง DataFrame จาก table_data
    df_table = pd.DataFrame(table_data)
    
    # กำหนดสไตล์:
    # 1. ซ่อน header ของ column (<thead>) และ row (<tbody> th)
    # 2. กำหนดขนาดของแต่ละ cell ให้มีความกว้างและความสูงเท่ากัน
    cell_size_style = {'selector': 'td', 'props': [('min-width', '55px'),
                                                     ('max-width', '55px'),
                                                     ('min-height', '55px'),
                                                     ('max-height', '55px')]}
    styler = df_table.style.apply(lambda df: highlight_table(df_table), axis=None)
    styler = styler.set_table_styles([
        {'selector': 'thead', 'props': [('display', 'none')]},
        {'selector': 'tbody th', 'props': [('display', 'none')]},
        cell_size_style
    ])
    
    st.markdown(f"**{floor_label}**")
    st.write(styler.to_html(), unsafe_allow_html=True)

def update_table_with_nationality(table_data):
    """
    อัพเดตข้อมูล Nationality ลงในตารางตามตำแหน่งของห้อง
    """
    room_position = {}
    for i, row in enumerate(table_data):
        for j, cell in enumerate(row):
            if cell != "":
                room_position[cell] = (i, j)
    # อัพเดต Nationality ลงในแถวบนสุดหรือแถวล่างสุดของตาราง
    for _, record in df_filtered.iterrows():
        room = str(int(record["#Room"])).strip()
        nationality = record["Nationality"]
        if room in room_position:
            i, j = room_position[room]
            if i == 1:
                table_data[0][j] = nationality
            elif i == 3:
                table_data[4][j] = nationality
    return table_data

# สำหรับแต่ละชั้นที่เลือก เราอัพเดตตารางและแสดงผล
for floor_label in pill_selected_floor:
    floor_values = floor_mapping[floor_label]
    floor_table = generate_floors(floor_values, generic_table_data)
    updated_table = update_table_with_nationality(floor_table)
    # คุณสามารถคำนวณ floor number (ตัวเลข) หากต้องการแสดงผลเพิ่มเติม
    floor_number = int(floor_values[0]) - 10
    # ในที่นี้เราจะแสดงผลด้วยชื่อชั้น (floor_label)
    display_floor_map(updated_table, floor_label)
