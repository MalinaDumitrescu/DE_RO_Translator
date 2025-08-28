"""
Run (o singură dată) din PyCharm:
Run → Edit Configurations… → + Python
  • Module name: src.utils_install_argos
  • Working directory: rădăcina proiectului
"""
from argostranslate import package

PAIRS = [("de", "en"), ("en", "ro")]  # instalăm DE→EN și EN→RO

def install_pair(fr: str, to: str):
    print(f"• Caut pachet {fr}→{to} …")
    package.update_package_index()
    available = package.get_available_packages()
    matches = [p for p in available if p.from_code == fr and p.to_code == to]
    if not matches:
        raise RuntimeError(f"Nu găsesc pachet {fr}→{to} în index.")
    pkg = matches[0]
    print(f"  Găsit: {pkg} — instalez…")

    # 1) Cel mai simplu pe multe versiuni: metoda install() pe pachet
    try:
        pkg.install()
        print(f"  OK: {fr}→{to} instalat prin pkg.install().")
        return
    except AttributeError:
        pass  # trecem la fallback

    # 2) Fallback: download() + install_from_path()
    try:
        path = pkg.download()
        package.install_from_path(path)
        print(f"  OK: {fr}→{to} instalat via download() + install_from_path().")
        return
    except AttributeError:
        pass

    # 3) Dacă ai o versiune foarte veche, sugerez upgrade:
    raise RuntimeError(
        "Nu pot instala cu API-ul curent. În terminal:\n"
        "  pip install --upgrade argostranslate"
    )

def main():
    print("Actualizez indexul de pachete Argos…")
    package.update_package_index()

    for fr, to in PAIRS:
        install_pair(fr, to)

    print("✅ Argos instalat pentru DE→EN și EN→RO.")

if __name__ == "__main__":
    main()
