# example/st_app.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection

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
    nationality_map = {
        "Afghan": "AFG", "American": "USA", "Australian": "AUS", "Austrian": "AUT",
        "Belgian": "BEL", "Brazilian": "BRA", "British": "GBR", "Cambodian": "KHM",
        "Canadian": "CAN", "China-Hong Kong": "HKG", "Chinese": "CHN", "Congolese": "COD",
        "Croatia": "HRV", "Cuban": "CUB", "Czech": "CZE", "Danish": "DNK",
        "Egyptian": "EGY", "Estonian": "EST", "Finnish": "FIN", "French": "FRA",
        "French Polynesia": "PYF", "German": "DEU", "Greek": "GRC", "Hungarian": "HUN",
        "Indian": "IND", "Indonesian": "IDN", "Irantan": "IRN", "Irish": "IRL",
        "Israeli": "ISR", "Italian": "ITA", "Japanese": "JPN", "Jordanian": "JOR",
        "Kazakh": "KAZ", "Kenyan": "KEN", "Kuwaiti": "KWT", "Lao": "LAO",
        "Lithuanian": "LTU", "Macao": "MAC", "Malasian": "MYS", "Maldivian": "MDV",
        "Maltese": "MLT", "Mauritian": "MRT", "Mongolia": "MNG", "Myanmar": "MMR",
        "Netherlands": "NLD", "New Zealander": "NZL", "Norway": "NOR", "Norwegian": "NOR",
        "Philippine": "PHL", "Polish": "POL", "Portuguese": "PRT", "Romanian": "ROU",
        "Saudi Arabian": "SAU", "Singaporean": "SGP", "Slovene": "SVN", "Spanish": "ESP",
        "Sri Lankan": "LKA", "Swedish": "SWE", "Swiss": "CHE", "Taiwanese": "TWN",
        "Thai": "THA", "The Republic Of Korea": "KOR", "The Russian Federation": "RUS",
        "The United Arab Emirates": "ARE", "Turkish": "TUR", "Turks and Caicos Islands": "TCA",
        "Uzbek": "UZB", "Vanuatu": "VUT", "Vietnamese": "VNM", "Yemeni": "YEM"
    }
    
    # คืนค่าตัวย่อถ้าพบใน dictionary, ถ้าไม่พบให้ใช้ชื่อเดิม
    return nationality_map.get(nationality, nationality)
