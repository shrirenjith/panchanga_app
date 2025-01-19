# panchanga_app/core/lookup_service.py

# Tithi Names
TITHI_NAMES = {
    "english": [
        "Prathama", "Dvitiya", "Trtiya", "Chaturthi", "Panchami", "Shashti",
        "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dvadashi",
        "Trayodashi", "Chaturdashi", "Pournami",  # Shukla Paksha
        "Prathama", "Dvitiya", "Trtiya", "Chaturthi", "Panchami", "Shashti",
        "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dvadashi",
        "Trayodashi", "Chaturdashi", "Amavasya"  # Krishna Paksha
    ],
    "malayalam": [
        "പ്രഥമ", "ദ്വിതീയ", "തൃതീയ", "ചതുര്‍ത്ഥി", "പഞ്ചമി", "ഷഷ്ഠി",
        "സപ്തമി", "അഷ്ടമി", "നവമി", "ദശമി", "എകാദശി", "ദ്വാദശി",
        "ത്രയോദശി", "ചതുര്ദശി", "പൗര്‍ണമി",  # Shukla Paksha
        "പ്രഥമ", "ദ്വിതീയ", "തൃതീയ", "ചതുര്‍ത്ഥി", "പഞ്ചമി", "ഷഷ്ഠി",
        "സപ്തമി", "അഷ്ടമി", "നവമി", "ദശമി", "എകാദശി", "ദ്വാദശി",
        "ത്രയോദശി", "ചതുര്ദശി", "അമാവാസ്യ"  # Krishna Paksha
    ]
}

# Nakshatra Names
NAKSHATRA_NAMES = {
    "english": [
        "Ashwati", "Bharani", "Karthika", "Rohini", "Makayiram", "Thiruvathira",
        "Punartham", "Pooyam", "Ayilyam", "Makam", "Pooram", "Uthram",
        "Atham", "Chithira", "Chothi", "Visakham", "Anizham", "Thrikketta",
        "Moolam", "Pooradam", "Uthradam", "Thiruvonam", "Avittam", "Chatayam",
        "Pururuttathi", "Uthrittathi", "Revathi"
    ],
    "malayalam": [
        "അശ്വതി", "ഭരണി", "കാര്‍ത്തിക", "രോഹിണി", "മകയിരം", "തിരുവാതിര",
        "പുനര്‍തം", "പൂയം", "അയില്യം", "മകം", "പൂരം", "ഉത്രം",
        "അത്തം", "ചിത്ര", "ചോതി", "വിശാഖം", "അനിഴം", "തൃക്കേട്ട",
        "മൂലം", "പൂരാടം", "ഉത്രാടം", "തിരുവോണം", "അവിട്ടം", "ചതയം",
        "പൂര്‍രുട്ടാതി", "ഉത്രട്ടാതി", "രേവതി"
    ]
}

def get_tithi_name(tithi_idx, language="english"):
    """
    Fetch Tithi name in the specified language.
    :param tithi_idx: Index of the Tithi (0-29)
    :param language: "english" or "malayalam"
    :return: Tithi name as a string
    """
    return TITHI_NAMES[language][tithi_idx]

def get_nakshatra_name(nakshatra_idx, language="english"):
    """
    Fetch Nakshatra name in the specified language.
    :param nakshatra_idx: Index of the Nakshatra (0-26)
    :param language: "english" or "malayalam"
    :return: Nakshatra name as a string
    """
    return NAKSHATRA_NAMES[language][nakshatra_idx]
