from argostranslate import translate

def de_to_ro(text_de: str) -> str:
    if not text_de:
        return ""
    en = translate.translate(text_de, "de", "en")
    ro = translate.translate(en, "en", "ro")
    return ro
