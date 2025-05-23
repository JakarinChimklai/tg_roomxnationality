import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from collections import defaultdict
import copy

@st.cache_data()
def get_google_sheet_database(secret_connection_name, work_sheet):
    #secret_connection_name = เป็นชื่อของ secret ของไฟล์นั้น ๆ
    #column_map = ดูว่าต้องใช้คอลัมน์ไหนบ้าง
    #
    conn = st.connection(secret_connection_name, type=GSheetsConnection)
    data = conn.read(worksheet = work_sheet)
    #st.dataframe()
    return data


def map_nationality(nationality):
    # Dictionary สำหรับแมปชื่อประเทศเป็นตัวย่อ
    map_nationality = {
    "OTHER": "OTH", "Algerian": "DZA","Angolan": "AGO", "Beninese": "BEN", "Botswana": "BWA", "Burkina Faso": "BFA",
    "Burundi": "BDI", "Cameroonian": "CMR", "Cape Verdean": "CPV", "Central African": "CAF", "Chadian": "TCD",
    "Comoros": "COM", "Congolese": "COD", "Djibouti": "DJI", "Egyptian": "EGY", "Equatorial Guinean": "GNQ",
    "Eritrean": "ERI", "Ethiopian": "ETH", "Gabonese": "GAB", "Gambian": "GMB", "Ghanaian": "GHA", "Guinea-Bissauan": "GNB",
    "Guinean": "GIN", "Ivory Coast": "CIV", "Kenyan": "KEN", "Lesothon": "LSO", "Liberian": "LBR", "Libyan": "LBY",
    "Malagasy": "MDG", "Malawian": "MWI", "Maliian": "MLI", "Mauritanian": "MRT", "Mauritian": "MUS", "Mayotte": "MYT",
    "Moroccan": "MAR", "Mozambican": "MOZ", "Namibian": "NAM", "Nigerian": "NGA", "Reunion Islander": "REU", "Rwandan": "RWA",
    "Sao Tome/Principe": "STP", "Senegalese": "SEN", "Seychellois": "SYC", "Sierra Leonean": "SLE", "Somali": "SOM",
    "South African": "ZAF", "St. Helena": "SHN", "Sudanese": "SDN", "Swazi": "SWZ", "Tanzanian": "TZA", "The Niger": "NER",
    "Togolese": "TGO", "Tunisian": "TUN", "Ugandan": "UGA","Zambian": "ZMB", "Zimbabwean": "ZWE", "Antarctica": "ATA",
    "Afghan": "AFG", "Armenian": "ARM", "Azerbaijani": "AZE", "Bahraini": "BHR", "Bangladesh": "BGD", "Bhutanese": "BTN",
    "Brunei Darussalam": "BRN", "Cambodian": "KHM", "China-Hong Kong": "HKG", "Chinese": "CHN", "Christmas Island": "CXR",
    "Cocos (Keeling) Islands": "CCK", "Georgian": "GEO", "Indian": "IND", "Indonesian": "IDN", "Irantan": "IRN", "Iraqi": "IRQ",
    "Israeli": "ISR", "Japanese": "JPN", "Jordanian": "JOR", "Kazakh": "KAZ", "Kuwaiti": "KWT", "Kyrgyz": "KGZ", "Lao": "LAO",
    "Lebanese": "LBN", "Macao": "MAC", "Malasian": "MYS", "Maldivian": "MDV", "Mongolia": "MNG", "Myanmar": "MMR",
    "Nepalese": "NPL","Omani": "OMN","Pakistan": "PAK","Palestinian": "PSE","Philippine": "PHL","Qatar": "QAT","Saudi Arabian": "SAU",
    "Singaporean": "SGP","Sri Lankan": "LKA","Syrian": "SYR","Taiwanese": "TWN","Tajik": "TJK","Thai": "THA",
    "The Democralic People'S Republ": "PRK","The Republic Of Korea": "KOR","The United Arab Emirates": "ARE","Turkish": "TUR",
    "Turkmen": "TKM","Uzbek": "UZB", "Vietnamese": "VNM","Yemeni": "YEM","Albanian": "ALB","andorain": "AND","Austrian": "AUT",
    "Belarusian": "BLR","Belgian": "BEL","Bosnia and Herzegovina": "BIH","British": "GBR","Bulgarian": "BGR","Crna Gora Montenegro": "MNE",
    "Croatia": "HRV","Cypriot": "CYP","Czech": "CZE","Danish": "DNK","Estonian": "EST","Faeroes Islander": "FRO","Finnish": "FIN",
    "French": "FRA","German": "DEU","Gibraltar": "GIB","Greek": "GRC","Hungarian": "HUN","Icelandic": "ISL","Irish": "IRL","Italian": "ITA",
    "Latvian": "LVA","Liechtenstein": "LIE","Lithuanian": "LTU","Luxemburgerg": "LUX","Maltese": "MLT","Moldovan": "MDA","Netherlands": "NLD",
    "Norway": "NOR","Polish": "POL","Portuguese": "PRT","Republic Of Kosovo": "XKX","Romanian": "ROU","San Marino": "SMR","Serbia": "SRB",
    "Slovak": "SVK","Slovene": "SVN","Spanish": "ESP","Swedish": "SWE","Swiss": "CHE","The Former Yugoslav Republic": "RSB","The Holy See": "VAT",
    "The Russian Federation": "RUS","Ukranian": "UKR","Yogoslav": "MKD","American": "USA","Anguilla": "AIA","Antiguan and Barbuda": "ATG",
    "Aruba": "ABW","Bahamian": "BHS","Barbadian": "BRB","Belizean": "BLZ","Bermudan": "BMU","Canadian": "CAN","Cayman Islander": "CYM",
    "Costa Rica": "CRI","Cuban": "CUB","Curacaoan": "CUW","Dominica": "DMA","Dominican": "DOM","Greenlander": "GRL","Grenadian": "GRD",
    "Guadeloupean": "GLP","Guatemalan": "GTM","Haitian": "HTI","Honduran": "HND","Jamaican": "JAM","Martinique": "MTQ","Maxican": "MEX",
    "Montserrat": "MSR","Netherlands Antilles": "ANT","Nicaraguan": "NIC","Panamanian": "PAN","Puerto Rican": "PRI","Saint Lucian": "LCA",
    "Saint Vincent and The Grenadin": "VCT","Salvadoran": "SLV","St. Peirre and Miquelon": "SPM","Trinidad and Tobago": "TTO",
    "Turks and Caicos Islands": "TCA","Virgin Islander": "VIR","Virgin Islands (British)": "VGB","America Samoa": "ASM","Australian": "AUS",
    "Cook Islander": "COK","East Timor": "TLS","Fiji": "FJI","French Polynesia": "PYF","Guamanian": "GUM","Kiribatian": "KIR","Marianan": "MNP",
    "Marshall Islands": "MHL","Nauruan": "NRU","New Zealander": "NZL","Newcaledonian": "NCL","Niue": "NIU","Norfolk Island": "NFK","Palau": "PLW",
    "Papua New Guinea": "PNG","Samoan": "WSM","Solomon Islands": "SLB","The Federated States   Microne": "FSM","Tokelau": "TKL",
    "Tongan": "TON","Tuvaluan": "TUV","Vanuatu": "VUT","Wallis and Futuna Islands": "WLF","Argentine": "ARG","Bolivian": "BOL","Brazilian": "BRA",
    "Chilean": "CHL","Colombian": "COL","Ecuadorian": "ECU","Falkland Islands (Malvinas)": "FLK","French Guiana": "GUF","Guyanese": "GUY",
    "Paraguayan": "PRY","Peruvian": "PER","Surinam": "SUR","Uruguayan": "URY","Venezuelan": "VEN"
}

    
    # คืนค่าตัวย่อถ้าพบใน dictionary, ถ้าไม่พบให้ใช้ชื่อเดิม
    return map_nationality.get(nationality, nationality)




def nationality_dictionary():
    # Dictionary for mapping country codes to nationality names
    nationality_dict = {
        "OTH": "OTHER", "DZA": "Algerian", "AGO": "Angolan", "BEN": "Beninese", "BWA": "Botswana",
        "BFA": "Burkina Faso", "BDI": "Burundi", "CMR": "Cameroonian", "CPV": "Cape Verdean",
        "CAF": "Central African", "TCD": "Chadian", "COM": "Comoros", "COD": "Congolese",
        "DJI": "Djibouti", "EGY": "Egyptian", "GNQ": "Equatorial Guinean", "ERI": "Eritrean",
        "ETH": "Ethiopian", "GAB": "Gabonese", "GMB": "Gambian", "GHA": "Ghanaian",
        "GNB": "Guinea-Bissauan", "GIN": "Guinean", "CIV": "Ivory Coast", "KEN": "Kenyan",
        "LSO": "Lesothon", "LBR": "Liberian", "LBY": "Libyan", "MDG": "Malagasy", "MWI": "Malawian",
        "MLI": "Malian", "MRT": "Mauritanian", "MUS": "Mauritian", "MYT": "Mayotte",
        "MAR": "Moroccan", "MOZ": "Mozambican", "NAM": "Namibian", "NGA": "Nigerian",
        "REU": "Reunion Islander", "RWA": "Rwandan", "STP": "Sao Tome/Principe", "SEN": "Senegalese",
        "SYC": "Seychellois", "SLE": "Sierra Leonean", "SOM": "Somali", "ZAF": "South African",
        "SHN": "St. Helena", "SDN": "Sudanese", "SWZ": "Swazi", "TZA": "Tanzanian", "NER": "The Niger",
        "TGO": "Togolese", "TUN": "Tunisian", "UGA": "Ugandan", "ZMB": "Zambian", "ZWE": "Zimbabwean",
        "ATA": "Antarctica", "AFG": "Afghan", "ARM": "Armenian", "AZE": "Azerbaijani",
        "BHR": "Bahraini", "BGD": "Bangladesh", "BTN": "Bhutanese", "BRN": "Brunei Darussalam",
        "KHM": "Cambodian", "HKG": "China-Hong Kong", "CHN": "Chinese", "CXR": "Christmas Island",
        "CCK": "Cocos (Keeling) Islands", "GEO": "Georgian", "IND": "Indian", "IDN": "Indonesian",
        "IRN": "Iranian", "IRQ": "Iraqi", "ISR": "Israeli", "JPN": "Japanese", "JOR": "Jordanian",
        "KAZ": "Kazakh", "KWT": "Kuwaiti", "KGZ": "Kyrgyz", "LAO": "Lao", "LBN": "Lebanese",
        "MAC": "Macao", "MYS": "Malaysian", "MDV": "Maldivian", "MNG": "Mongolian", "MMR": "Myanmar",
        "NPL": "Nepalese", "OMN": "Omani", "PAK": "Pakistani", "PSE": "Palestinian", "PHL": "Filipino",
        "QAT": "Qatari", "SAU": "Saudi Arabian", "SGP": "Singaporean", "LKA": "Sri Lankan",
        "SYR": "Syrian", "TWN": "Taiwanese", "TJK": "Tajik", "THA": "Thai", "PRK": "North Korean",
        "KOR": "South Korean", "ARE": "Emirati", "TUR": "Turkish", "TKM": "Turkmen", "UZB": "Uzbek",
        "VNM": "Vietnamese", "YEM": "Yemeni", "ALB": "Albanian", "AND": "Andorran", "AUT": "Austrian",
        "BLR": "Belarusian", "BEL": "Belgian", "BIH": "Bosnian", "GBR": "British", "BGR": "Bulgarian",
        "MNE": "Montenegrin", "HRV": "Croatian", "CYP": "Cypriot", "CZE": "Czech", "DNK": "Danish",
        "EST": "Estonian", "FRO": "Faeroese", "FIN": "Finnish", "FRA": "French", "DEU": "German",
        "GIB": "Gibraltar", "GRC": "Greek", "HUN": "Hungarian", "ISL": "Icelander", "IRL": "Irish",
        "ITA": "Italian", "LVA": "Latvian", "LIE": "Liechtenstein", "LTU": "Lithuanian", "LUX": "Luxembourg",
        "MLT": "Maltese", "MDA": "Moldovan", "NLD": "Dutch", "NOR": "Norwegian", "POL": "Polish",
        "PRT": "Portuguese", "XKX": "Kosovar", "ROU": "Romanian", "SMR": "San Marinese", "SRB": "Serbian",
        "SVK": "Slovak", "SVN": "Slovenian", "ESP": "Spanish", "SWE": "Swedish", "CHE": "Swiss",
        "RSB": "Former Yugoslav Republic", "VAT": "Vatican", "RUS": "Russian", "UKR": "Ukrainian",
        "MKD": "Macedonian", "USA": "American", "AIA": "Anguillan", "ATG": "Antiguan", "ABW": "Aruban",
        "BHS": "Bahamian", "BRB": "Barbadian", "BLZ": "Belizean", "BMU": "Bermudan", "CAN": "Canadian",
        "CYM": "Cayman Islander", "CRI": "Costa Rican", "CUB": "Cuban", "CUW": "Curaçaoan", "DMA": "Dominican",
        "DOM": "Dominican", "GRL": "Greenlandic", "GRD": "Grenadian", "GLP": "Guadeloupean", "GTM": "Guatemalan",
        "HTI": "Haitian", "HND": "Honduran", "JAM": "Jamaican", "MTQ": "Martinican", "MEX": "Mexican",
        "MSR": "Montserratian", "ANT": "Netherlands Antillean", "NIC": "Nicaraguan", "PAN": "Panamanian",
        "PRI": "Puerto Rican", "LCA": "Saint Lucian", "VCT": "Saint Vincentian", "SLV": "Salvadoran",
        "SPM": "Saint Pierre and Miquelon", "TTO": "Trinidadian", "TCA": "Turks and Caicos Islander",
        "VIR": "Virgin Islander", "VGB": "British Virgin Islander", "ASM": "American Samoan",
        "AUS": "Australian", "COK": "Cook Islander", "TLS": "East Timorese", "FJI": "Fijian", "PYF": "French Polynesian",
        "GUM": "Guamanian", "KIR": "Kiribatian", "MNP": "Northern Mariana Islander", "MHL": "Marshallese",
        "NRU": "Nauruan", "NZL": "New Zealander", "NCL": "New Caledonian", "NIU": "Niuean", "NFK": "Norfolk Islander",
        "PLW": "Palauan", "PNG": "Papua New Guinean", "WSM": "Samoan", "SLB": "Solomon Islander", "FSM": "Micronesian",
        "TKL": "Tokelauan", "TON": "Tongan", "TUV": "Tuvaluan", "VUT": "Vanuatuan", "WLF": "Wallisian", "ARG": "Argentine",
        "BOL": "Bolivian", "BRA": "Brazilian", "CHL": "Chilean", "COL": "Colombian", "ECU": "Ecuadorian",
        "FLK": "Falkland Islander", "GUF": "French Guianese", "GUY": "Guyanese", "PRY": "Paraguayan", "PER": "Peruvian",
        "SUR": "Surinamese", "URY": "Uruguayan", "VEN": "Venezuelan"
    }

    return nationality_dict 




def map_heat_color(value):
    if value >= 0.75:
        return "#f0422d"
    elif value >= 0.50:
        return "#f77363"
    elif value >= 0.25:
        return "#fa9c91"
    elif value > 0:
        return "#fac4be"
    elif value == 0:
        return "#ffffff"
    else:
        return "#ffffff"





def sensitive_noisy_ratio(building_data, df3, df_filtered, floor_offset=-10):
    nationality_type_dict = {}
    for _, row in df3.iterrows():
        nationality = row.iloc[2]
        type_group = row.iloc[3]
        if type_group.lower() != 'neutral':
            nationality_type_dict[nationality] = type_group.lower()

    floor_counts = defaultdict(lambda: {'sensitive': 0, 'noisy': 0})
    for _, row in df_filtered.iterrows():
        room_number = str(row.iloc[1])
        nationality = row.iloc[13]
        if len(room_number) >= 2 and nationality in nationality_type_dict:
            floor_key = room_number[:2] + "XX"
            group = nationality_type_dict[nationality]
            floor_counts[floor_key][group] += 1

    floor_percentage = {}
    for floor, counts in floor_counts.items():
        total = counts['sensitive'] + counts['noisy']
        if total > 0:
            percent_sensitive = (counts['sensitive'] / total) * 100
            floor_percentage[floor] = round(percent_sensitive, 2)

    for row in building_data:
        floor = row[0]
        if floor in floor_percentage:
            row[1] = floor_percentage[floor]

    # CSS สำหรับ tooltip
    html_table = """
    <style>
    .tooltip {
        position: relative;
        display: inline-block;
    }

    .tooltip .tooltiptext {
        visibility: hidden;
        width: max-content;
        background-color: #555;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%; 
        left: 50%;
        margin-left: -60px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 12px;
        white-space: nowrap;
    }

    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    </style>
    """

    html_table += "<table style='border-collapse: collapse; width: 150px;'>"
    for row in building_data:
        floor_code = row[0]
        display_floor = str(int(floor_code[:2]) + floor_offset) if floor_code[:2].isdigit() else floor_code
        value = row[1]
        if isinstance(value, (int, float)):
            percent_value = int(round(value))
            percent = f"{percent_value}%"
            tooltip = (
                f"สัญชาติที่ Sensitive เป็น {percent_value}%<br>"
                f"สัญชาติที่ Noisy เป็น {100 - percent_value}%")
            cell_bg = "#132A6D" if percent_value >= 50 else "#FFB618"
            font_color = "white" if percent_value >= 50 else "black"
        else:
            percent = ""
            tooltip = ""
            cell_bg = "white"
            font_color = "black"

        html_table += "<tr>"
        html_table += f"<td style='border: 1px solid #e3dede; padding: 8px; text-align: center;'>{display_floor}</td>"
        html_table += (
            f"<td style='border: 1px solid #e3dede; padding: 8px; text-align: center; background-color: {cell_bg}; "
            f"color: {font_color};'>"
            f"<div class='tooltip'>{percent}<span class='tooltiptext'>{tooltip}</span></div>"
            f"</td>"
        )
        html_table += "</tr>"
    html_table += "</table>"

    return html_table




from collections import defaultdict

def sensitive_noisy_ratio(building_data, df3, df_filtered, floor_offset=-10):
    # จัดกลุ่ม nationality เป็น sensitive / noisy จาก df3
    nationality_type_dict = {}
    for _, row in df3.iterrows():
        nationality = row.iloc[2]
        type_group = row.iloc[3]
        if type_group.lower() != 'neutral':
            nationality_type_dict[nationality] = type_group.lower()

    # นับจำนวน sensitive / noisy ในแต่ละชั้น
    floor_counts = defaultdict(lambda: {'sensitive': 0, 'noisy': 0})
    for _, row in df_filtered.iterrows():
        room_number = str(row.iloc[1])
        nationality = row.iloc[13]
        if len(room_number) >= 2 and nationality in nationality_type_dict:
            floor_key = room_number[:2] + "XX"
            group = nationality_type_dict[nationality]
            floor_counts[floor_key][group] += 1

    # คำนวณ % sensitive ของแต่ละชั้น
    floor_percentage = {}
    for floor, counts in floor_counts.items():
        total = counts['sensitive'] + counts['noisy']
        if total > 0:
            percent_sensitive = (counts['sensitive'] / total) * 100
            floor_percentage[floor] = round(percent_sensitive, 2)

    # คำนวณค่าเฉลี่ยรวม
    if floor_percentage:
        average_sensitive = round(sum(floor_percentage.values()) / len(floor_percentage), 2)
    else:
        average_sensitive = None

    # นำข้อมูลมาใส่ใน building_data
    for row in building_data:
        floor = row[0]
        if floor in floor_percentage:
            row[1] = floor_percentage[floor]

    # CSS สำหรับ tooltip และ HTML
    html_table = """
    <style>
    .tooltip {
        position: relative;
        display: inline-block;
    }

    .tooltip .tooltiptext {
        visibility: hidden;
        width: max-content;
        background-color: #555;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%; 
        left: 50%;
        margin-left: -60px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 12px;
        white-space: nowrap;
    }

    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    </style>
    """

    # เพิ่มค่าเฉลี่ยด้านบนตาราง

    # สร้างตารางผลลัพธ์
    html_table += "<table style='border-collapse: collapse; width: 150px;'>"
    for row in building_data:
        floor_code = row[0]
        display_floor = str(int(floor_code[:2]) + floor_offset) if floor_code[:2].isdigit() else floor_code
        value = row[1]
        if isinstance(value, (int, float)):
            percent_value = int(round(value))
            percent = f"{percent_value}%"
            tooltip = (
                f"สัญชาติที่ Sensitive เป็น {percent_value}%<br>"
                f"สัญชาติที่ Noisy เป็น {100 - percent_value}%")
            cell_bg = "#132A6D" if percent_value >= 50 else "#FFB618"
            font_color = "white" if percent_value >= 50 else "black"
        else:
            percent = ""
            tooltip = ""
            cell_bg = "white"
            font_color = "black"

        html_table += "<tr>"
        html_table += f"<td style='border: 1px solid #e3dede; padding: 8px; text-align: center;'>{display_floor}</td>"
        html_table += (
            f"<td style='border: 1px solid #e3dede; padding: 8px; text-align: center; background-color: {cell_bg}; "
            f"color: {font_color};'>"
            f"<div class='tooltip'>{percent}<span class='tooltiptext'>{tooltip}</span></div>"
            f"</td>"
        )
        html_table += "</tr>"
    html_table += "</table>"

    return html_table





def clean_date_column(df, date_col_index=0, drop_invalid=True):
    date_column = df.columns[date_col_index]
    if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce', dayfirst=True)
    df[date_column] = df[date_column].dt.date
    if drop_invalid:
        df = df.dropna(subset=[date_column])
    return df


def room_number_sensitive_noisy(df3, df_filtered, status_column="status", name_column="ชื่อย่อ", room_column="#Room"):
    # แยกข้อมูลตามสถานะ
    df_sensitive = df3[df3[status_column] == "sensitive"]
    df_noisy = df3[df3[status_column] == "noisy"]
    
    # กรองข้อมูล df_filtered ตามชื่อย่อ
    df_filtered_sensitive = df_filtered[df_filtered["Nationality"].isin(df_sensitive[name_column])]
    df_filtered_noisy = df_filtered[df_filtered["Nationality"].isin(df_noisy[name_column])]
    
    # แปลงหมายเลขห้องเป็น string และทำเป็น list
    room_number_sensitive = df_filtered_sensitive[room_column].astype(str).tolist()
    room_number_noisy = df_filtered_noisy[room_column].astype(str).tolist()
    
    return room_number_sensitive, room_number_noisy



def find_duplicates(df, col_index, unique_list, duplicate_list, room_number_list):
    for _, row in df.iterrows():
        value = str(row.iloc[col_index]).strip()
        if value not in unique_list:
            unique_list.append(value)
        else:
            duplicate_list.append(value)

    for _, row in df.iterrows():
        value = str(row.iloc[col_index]).strip()
        room_number = str(row.iloc[1]).strip()
        if value in duplicate_list:
            room_number_list.append(room_number)


def check_guests_traveling_together(df_filtered, floors):
    """Check if guests traveling together are not in nearby rooms"""
    duplicate_guest_names = []
    duplicate_rsvn = []
    room_number_duplicate_guest_name = []
    room_number_duplicate_rsvn = []
    
    # Find duplicates in guest names and reservation numbers
    find_duplicates(df_filtered, 5, [], duplicate_guest_names, room_number_duplicate_guest_name)
    find_duplicates(df_filtered, 19, [], duplicate_rsvn, room_number_duplicate_rsvn)
    
    # Combined duplicate room lists
    room_number_duplicate = room_number_duplicate_guest_name + room_number_duplicate_rsvn
    unique_room_numbers = []
    duplicate_room_numbers = []
    
    # Find truly duplicate rooms
    for room in room_number_duplicate:
        if room not in unique_room_numbers:
            unique_room_numbers.append(room)
        else:
            duplicate_room_numbers.append(room)
    
    # Convert floor plans to show guest names and reservation numbers
    guest_name_plans = {}
    rsvn_plans = {}
    
    for floor_num in range(2, 9):
        # Create guest name floor plan
        guest_plan = copy.deepcopy(floors[floor_num]) 
        for i, row in enumerate(guest_plan):
            for j, cell in enumerate(row):
                if isinstance(cell, str) and len(cell) == 4 and cell in room_number_duplicate_guest_name:
                    # FIX: Use proper dataframe filtering instead of list indexing
                    room_data = df_filtered[df_filtered["#Room"].astype(str) == cell]
                    if not room_data.empty:
                        guest_name = room_data.iloc[0]["Guest Name"]
                        guest_plan[i][j] = guest_name
        guest_name_plans[floor_num] = guest_plan
        
        # Create reservation floor plan
        rsvn_plan = copy.deepcopy(floors[floor_num])
        for i, row in enumerate(rsvn_plan):
            for j, cell in enumerate(row):
                if isinstance(cell, str) and len(cell) == 4 and cell in room_number_duplicate_rsvn:
                    # FIX: Use proper dataframe filtering instead of list indexing
                    room_data = df_filtered[df_filtered["#Room"].astype(str) == cell]
                    if not room_data.empty:
                        rsvn = str(room_data.iloc[0]["Rsvn."])
                        rsvn_plan[i][j] = rsvn
        rsvn_plans[floor_num] = rsvn_plan
    
    # Find rooms with adjacent matched values
    together_rooms = []
    
    # Check guest name plans
    for floor_num in range(2, 9):
        guest_plan = guest_name_plans[floor_num]
        floor_plan = floors[floor_num]
        
        for i, row in enumerate(guest_plan):
            for j, cell in enumerate(row):
                if cell and isinstance(cell, str) and not (cell.startswith("1") or cell.startswith("2")):
                    # Check left
                    if j > 0 and row[j-1] == cell:
                        together_rooms.append(floor_plan[i][j])
                    # Check right
                    elif j < len(row) - 1 and row[j+1] == cell:
                        together_rooms.append(floor_plan[i][j])
                    # Check above
                    elif i > 0 and j < len(guest_plan[i-1]) and guest_plan[i-1][j] == cell:
                        together_rooms.append(floor_plan[i][j])
                    # Check below
                    elif i < len(guest_plan) - 1 and j < len(guest_plan[i+1]) and guest_plan[i+1][j] == cell:
                        together_rooms.append(floor_plan[i][j])
    
    # Check reservation plans
    for floor_num in range(2, 9):
        rsvn_plan = rsvn_plans[floor_num]
        floor_plan = floors[floor_num]
        
        for i, row in enumerate(rsvn_plan):
            for j, cell in enumerate(row):
                if cell and isinstance(cell, str) and not (cell.startswith("1") or cell.startswith("2")):
                    # Check left
                    if j > 0 and row[j-1] == cell:
                        together_rooms.append(floor_plan[i][j])
                    # Check right
                    elif j < len(row) - 1 and row[j+1] == cell:
                        together_rooms.append(floor_plan[i][j])
                    # Check above
                    elif i > 0 and j < len(rsvn_plan[i-1]) and rsvn_plan[i-1][j] == cell:
                        together_rooms.append(floor_plan[i][j])
                    # Check below
                    elif i < len(rsvn_plan) - 1 and j < len(rsvn_plan[i+1]) and rsvn_plan[i+1][j] == cell:
                        together_rooms.append(floor_plan[i][j])
    
    # Find rooms that should be together but aren't
    unique_together_rooms = set(together_rooms)
    together_rooms_by_occurrence = {}
    
    for room in together_rooms:
        if room in together_rooms_by_occurrence:
            together_rooms_by_occurrence[room] += 1
        else:
            together_rooms_by_occurrence[room] = 1
    
    duplicate_together_rooms = [room for room, count in together_rooms_by_occurrence.items() if count > 1]
    not_together_rooms = [room for room in duplicate_room_numbers if room not in duplicate_together_rooms]
    
    return not_together_rooms


def get_room_info(room_number, df_filtered, problem_dict):
    """Return a formatted string showing room info and problems"""
    room_info = df_filtered[df_filtered["#Room"].astype(str) == str(room_number)]
    
    if room_info.empty:
        return f"Room {room_number} is unoccupied or not found."

    row = room_info.iloc[0]
    nationality = row["Nationality"]
    guest_name = row["Guest Name"]
    nights = row["Nights"]
    
    problems = [label for key, label in problem_dict.items() if room_number in label["rooms"]]
    
    return {
        "Room": room_number,
        "Guest": guest_name,
        "Nationality": nationality,
        "Nights": nights,
        "Problems": [label["label"] for label in problems]
    }


def get_rooms_for_problem(index, problem_dict):
    """Return room list for the selected problem index"""
    if index in problem_dict:
        return problem_dict[index]["rooms"]
    return []


def get_rooms_on_floor(floor_number, floors):
    """Flatten the floor plan into a list of room numbers"""
    floor_plan = floors.get(floor_number, [])
    return [cell for row in floor_plan for cell in row if isinstance(cell, str) and len(cell) == 4 and cell[:2].isdigit()]


#############################################
#Check 7 Rule 

# 1. India ไม่ควรอยู่ High Floor (6-8)
def check_indian_high_floor(df_filtered):
    problem_rooms = []
    high_floors = ["6", "7", "8"]
        
    for _, row in df_filtered.iterrows():
        room_number = str(row.iloc[1])
        nationality = row.iloc[13]
        floor = room_number[1]
        if nationality == 'IND' and floor in high_floors:
            problem_rooms.append(room_number)
                
    return problem_rooms


# 2. Long stay (7 วันขึ้นไป) ต้องอยู่ชั้น 7/8 และเป็นตึก 2
def check_long_stay_low_floor(df_filtered):
    problem_rooms = []
    long_stay_floors = ["7", "8"]
        
    for _, row in df_filtered.iterrows():
        room_number = str(row.iloc[1])
        nights = row.iloc[9]
        floor = room_number[1]
        if nights > 6 and floor not in long_stay_floors:
            problem_rooms.append(room_number)
                
    return problem_rooms


# 3. ชาติอื่นไม่ควรเสียบต่ออินเดีย นอกจากอินเดียเสียบต่อกันเอง
def check_indian_to_not_indian(df_previous, df_filtered):
    ind_yesterday = df_previous[df_previous["Nationality"] == 'IND']
    room_number_ind_today = df_filtered[df_filtered["#Room"].isin(ind_yesterday["#Room"])]
    indian_to_not_indian_df = room_number_ind_today[room_number_ind_today["Nationality"] != 'IND']
    return indian_to_not_indian_df["#Room"].astype(str).tolist()


# 4. จีนกับเกาหลีไม่ควรอยู่ชั้น 7 ตึก 2 เพราะเป็นพื้นที่ห้ามสูบบุหรี่ แต่จีนกับเกาหลีชอบสูบ
def check_smoking_china_korea(df_filtered):
    """Check if Chinese or Korean guests are on floor 7 building 2 (no-smoking zone)"""
    problem_rooms = []
    smoking_nationalities = ["KOR", "CHN"]
    
    for _, row in df_filtered.iterrows():
        nationality = row.iloc[13]
        room_number = str(row.iloc[1])
        floor = room_number[1]
        building = room_number[0]
        if nationality in smoking_nationalities and floor == "7" and building == "2":
            problem_rooms.append(room_number)
            
    return problem_rooms

# 5. สีน้ำเงินไม่ควรถูกล้อมด้วยสีเหลือง
def check_sensitive_nearby_noisy(df3, df_filtered, floors):
    room_number_sensitive, room_number_noisy = room_number_sensitive_noisy(df3, df_filtered)
    problem_rooms = []
    
    for floor_num in range(2, 9):
        floor_plan = floors[floor_num]
        
        for i, row in enumerate(floor_plan):
            for j, cell in enumerate(row):
                if isinstance(cell, str) and len(cell) == 4 and cell in room_number_sensitive:
                    # Check left
                    if j > 0 and isinstance(floor_plan[i][j-1], str) and floor_plan[i][j-1] in room_number_noisy:
                        problem_rooms.append(cell)
                    # Check right
                    elif j < len(row) - 1 and isinstance(floor_plan[i][j+1], str) and floor_plan[i][j+1] in room_number_noisy:
                        problem_rooms.append(cell)
                    # Check above
                    elif i > 0 and isinstance(floor_plan[i-1][j], str) and floor_plan[i-1][j] in room_number_noisy:
                        problem_rooms.append(cell)
                    # Check below
                    elif i < len(floor_plan) - 1 and isinstance(floor_plan[i+1][j], str) and floor_plan[i+1][j] in room_number_noisy:
                        problem_rooms.append(cell)
    
    return problem_rooms


# 6. ชั้น 6-8 ไม่ควรมีสีเหลืองมากกว่า
def check_sensitive_noisy_high_floor(df3, df_filtered):
    room_number_sensitive, room_number_noisy = room_number_sensitive_noisy(df3, df_filtered)
    problem_rooms = []
    
    sensitive_floor_6 = []
    sensitive_floor_7 = []
    sensitive_floor_8 = []
    noisy_floor_6 = []
    noisy_floor_7 = []
    noisy_floor_8 = []
    
    # Categorize sensitive rooms by floor
    for room in room_number_sensitive:
        try:
            floor = int(room[1])
            if floor == 6:
                sensitive_floor_6.append(room)
            elif floor == 7:
                sensitive_floor_7.append(room)
            elif floor == 8:
                sensitive_floor_8.append(room)
        except (IndexError, ValueError):
            continue
    
    # Categorize noisy rooms by floor
    for room in room_number_noisy:
        try:
            floor = int(room[1])
            if floor == 6:
                noisy_floor_6.append(room)
            elif floor == 7:
                noisy_floor_7.append(room)
            elif floor == 8:
                noisy_floor_8.append(room)
        except (IndexError, ValueError):
            continue
    
    # Check if noisy > sensitive for each high floor
    if len(noisy_floor_6) > len(sensitive_floor_6):
        problem_rooms.extend(noisy_floor_6)
    
    if len(noisy_floor_7) > len(sensitive_floor_7):
        problem_rooms.extend(noisy_floor_7)
    
    if len(noisy_floor_8) > len(sensitive_floor_8):
        problem_rooms.extend(noisy_floor_8)
    
    return problem_rooms


# 7. มาด้วยกัน ควรอยู่ใกล้กัน
def check_guests_traveling_together(df_filtered, floors):
    duplicate_guest_names = []
    duplicate_rsvn = []
    room_number_duplicate_guest_name = []
    room_number_duplicate_rsvn = []
    
    find_duplicates(df_filtered, 5, [], duplicate_guest_names, room_number_duplicate_guest_name)
    find_duplicates(df_filtered, 19, [], duplicate_rsvn, room_number_duplicate_rsvn)
    
    # Combined duplicate room lists
    room_number_duplicate = room_number_duplicate_guest_name + room_number_duplicate_rsvn
    unique_room_numbers = []
    duplicate_room_numbers = []
    
    # Find truly duplicate rooms
    for room in room_number_duplicate:
        if room not in unique_room_numbers:
            unique_room_numbers.append(room)
        else:
            duplicate_room_numbers.append(room)
    
    # Convert floor plans to show guest names and reservation numbers
    guest_name_plans = {}
    rsvn_plans = {}
    
    for floor_num in range(2, 9):
        # Create guest name floor plan
        guest_plan = copy.deepcopy(floors[floor_num]) 
        for i, row in enumerate(guest_plan):
            for j, cell in enumerate(row):
                if cell in room_number_duplicate_guest_name:
                    idx = room_number_duplicate_guest_name.index(cell)
                    guest_name = df_filtered.iloc[idx, 5]
                    guest_plan[i][j] = guest_name
        guest_name_plans[floor_num] = guest_plan
        
        # Create reservation floor plan
        rsvn_plan = copy.deepcopy(floors[floor_num])
        for i, row in enumerate(rsvn_plan):
            for j, cell in enumerate(row):
                if cell in room_number_duplicate_rsvn:
                    idx = room_number_duplicate_rsvn.index(cell)
                    rsvn = str(df_filtered.iloc[idx, 19])
                    rsvn_plan[i][j] = rsvn
        rsvn_plans[floor_num] = rsvn_plan
    
    # Find rooms with adjacent matched values
    together_rooms = []
    
    # Check guest name plans
    for floor_num in range(2, 9):
        guest_plan = guest_name_plans[floor_num]
        floor_plan = floors[floor_num]
        
        for i, row in enumerate(guest_plan):
            for j, cell in enumerate(row):
                if cell and not cell.startswith("1") and not cell.startswith("2"):
                    # Check left
                    if j > 0 and row[j-1] == cell:
                        together_rooms.append(floor_plan[i][j])
                    # Check right
                    elif j < len(row) - 1 and row[j+1] == cell:
                        together_rooms.append(floor_plan[i][j])
                    # Check above
                    elif i > 0 and guest_plan[i-1][j] == cell:
                        together_rooms.append(floor_plan[i][j])
                    # Check below
                    elif i < len(guest_plan) - 1 and guest_plan[i+1][j] == cell:
                        together_rooms.append(floor_plan[i][j])
    
    # Check reservation plans
    for floor_num in range(2, 9):
        rsvn_plan = rsvn_plans[floor_num]
        floor_plan = floors[floor_num]
        
        for i, row in enumerate(rsvn_plan):
            for j, cell in enumerate(row):
                if cell and not cell.startswith("1") and not cell.startswith("2"):
                    # Check left
                    if j > 0 and row[j-1] == cell:
                        together_rooms.append(floor_plan[i][j])
                    # Check right
                    elif j < len(row) - 1 and row[j+1] == cell:
                        together_rooms.append(floor_plan[i][j])
                    # Check above
                    elif i > 0 and rsvn_plan[i-1][j] == cell:
                        together_rooms.append(floor_plan[i][j])
                    # Check below
                    elif i < len(rsvn_plan) - 1 and rsvn_plan[i+1][j] == cell:
                        together_rooms.append(floor_plan[i][j])
    
    # Find rooms that should be together but aren't
    unique_together_rooms = set(together_rooms)
    together_rooms_by_occurrence = {}
    
    for room in together_rooms:
        if room in together_rooms_by_occurrence:
            together_rooms_by_occurrence[room] += 1
        else:
            together_rooms_by_occurrence[room] = 1
    
    duplicate_together_rooms = [room for room, count in together_rooms_by_occurrence.items() if count > 1]
    not_together_rooms = [room for room in duplicate_room_numbers if room not in duplicate_together_rooms]
    
    return not_together_rooms


@st.cache_data(ttl=300)
def imports():
    """Import all necessary data from Google Sheets"""
    df = get_google_sheet_database('TG_csv_merge_file', 'MergedData')
    df["Nationality"] = df["Nationality"].apply(map_nationality)
    
    df2 = get_google_sheet_database('tg_noise_complaint_log', 'Merged Data')
    df3 = get_google_sheet_database('tg_sensitive_nationality', 'Sheet1')
    nationality_map = nationality_dictionary()
    
    return df, df2, df3, nationality_map



