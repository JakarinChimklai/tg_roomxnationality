import streamlit as st
import pandas as pd
from datetime import datetime
from function import get_google_sheet_database, map_nationality
import streamlit.components.v1 as components  # import components สำหรับ HTML

st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    .stApp {
        background-color: #c5c3c2;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

sensitive = ["AUT", "BEL", "GBR", "HRV", "CZE", "DNK", "EST", "FIN", "FRA",
             "DEU", "GRC", "HUN", "IRL", "ITA", "LTU", "MLT", "NLD", "NOR", "POL",
             "PRT", "ROU", "SVN", "ESP", "SWE", "CHE", "RUS", "TUR", "THA", "KOR"]

nationality_map = {
    "OTH": "OTHER","DZA": "Algerian","AGO": "Angolan","BEN": "Beninese","BWA": "Botswana","BFA": "Burkina Faso","BDI": "Burundi",
    "CMR": "Cameroonian","CPV": "Cape Verdean","CAF": "Central African","TCD": "Chadian","COM": "Comoros","COD": "Congolese",
    "DJI": "Djibouti","EGY": "Egyptian","GNQ": "Equatorial Guinean","ERI": "Eritrean","ETH": "Ethiopian","GAB": "Gabonese",
    "GMB": "Gambian","GHA": "Ghanaian","GNB": "Guinea-Bissauan","GIN": "Guinean","CIV": "Ivory Coast","KEN": "Kenyan","LSO": "Lesothon",
    "LBR": "Liberian","LBY": "Libyan","MDG": "Malagasy","MWI": "Malawian","MLI": "Maliian","MRT": "Mauritanian","MUS": "Mauritian",
    "MYT": "Mayotte","MAR": "Moroccan","MOZ": "Mozambican","NAM": "Namibian","NGA": "Nigerian","REU": "Reunion Islander","RWA": "Rwandan",
    "STP": "Sao Tome/Principe","SEN": "Senegalese","SYC": "Seychellois","SLE": "Sierra Leonean","SOM": "Somali","ZAF": "South African",
    "SHN": "St. Helena","SDN": "Sudanese","SWZ": "Swazi","TZA": "Tanzanian","NER": "The Niger","TGO": "Togolese","TUN": "Tunisian",
    "UGA": "Ugandan","ZMB": "Zambian","ZWE": "Zimbabwean","ATA": "Antarctica","AFG": "Afghan","ARM": "Armenian","AZE": "Azerbaijani",
    "BHR": "Bahraini","BGD": "Bangladesh","BTN": "Bhutanese","BRN": "Brunei Darussalam","KHM": "Cambodian","HKG": "China-Hong Kong",
    "CHN": "Chinese","CXR": "Christmas Island","CCK": "Cocos (Keeling) Islands","GEO": "Georgian","IND": "Indian","IDN": "Indonesian",
    "IRN": "Irantan","IRQ": "Iraqi","ISR": "Israeli","JPN": "Japanese","JOR": "Jordanian","KAZ": "Kazakh","KWT": "Kuwaiti","KGZ": "Kyrgyz",
    "LAO": "Lao","LBN": "Lebanese","MAC": "Macao","MYS": "Malasian","MDV": "Maldivian","MNG": "Mongolia","MMR": "Myanmar","NPL": "Nepalese",
    "OMN": "Omani","PAK": "Pakistan","PSE": "Palestinian","PHL": "Philippine","QAT": "Qatar","SAU": "Saudi Arabian","SGP": "Singaporean",
    "LKA": "Sri Lankan","SYR": "Syrian","TWN": "Taiwanese","TJK": "Tajik","THA": "Thai","PRK": "The Democralic People'S Republ",
    "KOR": "The Republic Of Korea","ARE": "The United Arab Emirates","TUR": "Turkish","TKM": "Turkmen","UZB": "Uzbek","VNM": "Vietnamese",
    "YEM": "Yemeni","ALB": "Albanian","AND": "andorain","AUT": "Austrian","BLR": "Belarusian","BEL": "Belgian","BIH": "Bosnia and Herzegovina",
    "GBR": "British","BGR": "Bulgarian","MNE": "Crna Gora Montenegro","HRV": "Croatia","CYP": "Cypriot","CZE": "Czech","DNK": "Danish",
    "EST": "Estonian","FRO": "Faeroes Islander","FIN": "Finnish","FRA": "French","DEU": "German","GIB": "Gibraltar","GRC": "Greek",
    "HUN": "Hungarian","ISL": "Icelandic","IRL": "Irish","ITA": "Italian","LVA": "Latvian","LIE": "Liechtenstein","LTU": "Lithuanian",
    "LUX": "Luxemburgerg","MLT": "Maltese","MDA": "Moldovan","NLD": "Netherlands","NOR": "Norway", "POL": "Polish", "PRT": "Portuguese",
    "XKX": "Republic Of Kosovo","ROU": "Romanian","SMR": "San Marino","SRB": "Serbia","SVK": "Slovak","SVN": "Slovene","ESP": "Spanish",
    "SWE": "Swedish","CHE": "Swiss","RSB": "The Former Yugoslav Republic","VAT": "The Holy See","RUS": "The Russian Federation","UKR": "Ukranian",
    "MKD": "Yogoslav","USA": "American","AIA": "Anguilla","ATG": "Antiguan and Barbuda","ABW": "Aruba","BHS": "Bahamian","BRB": "Barbadian",
    "BLZ": "Belizean","BMU": "Bermudan","CAN": "Canadian","CYM": "Cayman Islander","CRI": "Costa Rica","CUB": "Cuban","CUW": "Curacaoan",
    "DMA": "Dominica","DOM": "Dominican","GRL": "Greenlander","GRD": "Grenadian","GLP": "Guadeloupean","GTM": "Guatemalan","HTI": "Haitian",
    "HND": "Honduran","JAM": "Jamaican","MTQ": "Martinique","MEX": "Maxican","MSR": "Montserrat","ANT": "Netherlands Antilles","NIC": "Nicaraguan",
    "PAN": "Panamanian","PRI": "Puerto Rican","LCA": "Saint Lucian","VCT": "Saint Vincent and The Grenadin","SLV": "Salvadoran",
    "SPM": "St. Peirre and Miquelon","TTO": "Trinidad and Tobago","TCA": "Turks and Caicos Islands","VIR": "Virgin Islander","VGB": "Virgin Islands (British)",
    "ASM": "America Samoa","AUS": "Australian","COK": "Cook Islander","TLS": "East Timor","FJI": "Fiji","PYF": "French Polynesia","GUM": "Guamanian",
    "KIR": "Kiribatian","MNP": "Marianan","MHL": "Marshall Islands","NRU": "Nauruan","NZL": "New Zealander","NCL": "Newcaledonian","NIU": "Niue",
    "NFK": "Norfolk Island","PLW": "Palau","PNG": "Papua New Guinea","WSM": "Samoan","SLB": "Solomon Islands","FSM": "The Federated States   Microne",
    "TKL": "Tokelau","TON": "Tongan","TUV": "Tuvaluan","VUT": "Vanuatu","WLF": "Wallis and Futuna Islands","ARG": "Argentine","BOL": "Bolivian",
    "BRA": "Brazilian","CHL": "Chilean","COL": "Colombian","ECU": "Ecuadorian","FLK": "Falkland Islands (Malvinas)","GUF": "French Guiana",
    "GUY": "Guyanese","PRY": "Paraguayan","PER": "Peruvian","SUR": "Surinam","URY": "Uruguayan","VEN": "Venezuelan"
}

# Prepare Date Time
if not pd.api.types.is_datetime64_any_dtype(df["date"]):
    df["date"] = pd.to_datetime(df["date"], errors='coerce', dayfirst=True)
df["date"] = df["date"].dt.date

# แบ่ง 3 column สำหรับพวก filter
col1, col2, col3 = st.columns([4.5, 1, 4.5])

# Filter วันที่
with col1:
    selected_date = st.date_input("date", value=datetime.today().date())
    df_filtered = df[df["date"] == selected_date]

with col2:
    st.write("")

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
    ["BA01", "BA02", "BA03", "BA04", "BA05", "BA06", 
     "BA07", "ช่องช๊าฟ", "BA08", "BA09", "BA10", "BA11", "", "BB01", 
     "BB02", "BB03", "BB04", "BB05", "BB06", "BB07", "BB08", 
     "BB09", "BB10", "BB11", "BB12"],
    [""] * 25,
    ["BA20", "ดับเพลิง", "BA19", "BA18", "BA17", "BA16", "BA15",
     "ดับเพลิง", "ลิฟต์", "บันได", "BA14", "BA12", "", "BB22", "BB21", 
     "บันได", "ลิฟต์", "BB20", "BB19",
     "BB18", "BB17", "BB16", "BB15", "", "BB14"],
    [""] * 25
]

def generate_floors(filtered_floor, table_data):
    table_copy = [row.copy() for row in table_data]
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
            if col in [12]:
                styles.at[row, col] = "background-color: black; color: white; text-align: center;"
            elif cell == "IND" or cell == "CHN":
                styles.at[row, col] = "background-color: #bc4558; color: white; text-align: center;"
            elif cell in sensitive:
                styles.at[row, col] = "background-color: #013766; color: white; text-align: center;"
            else:
                styles.at[row, col] = "background-color: white; color: black; text-align: center;"
    return styles

def display_floor_map(table_data, floor_label):
    # สร้าง DataFrame จาก table_data
    df_table = pd.DataFrame(table_data)
    
    # สร้าง reverse mapping จาก nationality_map
    # (จากชื่อเต็ม -> รหัสประเทศ) ให้ได้ mapping จากรหัสประเทศ -> ชื่อเต็ม
    reverse_nationality_map = {v: k for k, v in nationality_map.items()}
    
    # สร้าง DataFrame สำหรับ tooltips โดยให้เซลล์ที่มีรหัสประเทศมี tooltip เป็นชื่อเต็ม
    tooltips_df = df_table.copy().astype(str)
    for i in tooltips_df.index:
        for j in tooltips_df.columns:
            cell_value = tooltips_df.at[i, j]
            if cell_value in reverse_nationality_map:
                tooltips_df.at[i, j] = reverse_nationality_map[cell_value]
            else:
                tooltips_df.at[i, j] = ""
    
    # กำหนดสไตล์ให้ cell มีขนาดคงที่
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
    
    # ตั้งค่า tooltips ให้กับแต่ละเซลล์
    styler = styler.set_tooltips(tooltips_df)
    
    st.markdown(f"**{floor_label}**")
    # ใช้ components.html() เพื่อแสดงผล HTML ที่ interactive ได้
    components.html(styler.to_html(), height=600, scrolling=True)

def update_table_with_nationality(table_data):
    """
    อัพเดตข้อมูล Nationality ลงในตารางตามตำแหน่งของห้อง
    """
    room_position = {}
    for i, row in enumerate(table_data):
        for j, cell in enumerate(row):
            if cell != "":
                room_position[cell] = (i, j)
    for _, record in df_filtered.iterrows():
        room = str(int(record["#Room"])).strip()
        nationality = record["Nationality"]
        if room in room_position:
            i, j = room_position[room]
            if i == 1:
                table_data[0][j] = nationality
            elif i == 3:
                table_data[4][j] = nationality
    for i in range(len(table_data)):
        for j in range(len(table_data[i])):
            if table_data[i][j] == "":
                table_data[i][j] = "&nbsp;"
    return table_data

# สำหรับแต่ละชั้นที่เลือก เราอัพเดตตารางและแสดงผล
for floor_label in pill_selected_floor:
    floor_values = floor_mapping[floor_label]
    floor_table = generate_floors(floor_values, generic_table_data)
    updated_table = update_table_with_nationality(floor_table)
    floor_number = int(floor_values[0]) - 10
    display_floor_map(updated_table, floor_label)
