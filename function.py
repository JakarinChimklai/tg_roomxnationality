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
    nationality_map = nationality_map = {
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
    return nationality_map.get(nationality, nationality)
