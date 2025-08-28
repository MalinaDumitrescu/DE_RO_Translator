from argostranslate import package

PAIRS = [("de", "en"), ("en", "ro")]

def install_pair(fr: str, to: str):
    print(f"Searching for package {fr}→{to} …")
    package.update_package_index()
    available = package.get_available_packages()
    matches = [p for p in available if p.from_code == fr and p.to_code == to]
    if not matches:
        raise RuntimeError(f"Package {fr}→{to} not found in index.")
    pkg = matches[0]
    print(f"  Found: {pkg} — installing…")

    try:
        pkg.install()
        print(f"  OK: {fr}→{to} installed via pkg.install().")
        return
    except AttributeError:
        pass

    try:
        path = pkg.download()
        package.install_from_path(path)
        print(f"  OK: {fr}→{to} installed via download() + install_from_path().")
        return
    except AttributeError:
        pass

    raise RuntimeError(
        "Unable to install with current API. Try upgrading:\n"
        "  pip install --upgrade argostranslate"
    )

def main():
    print("Updating Argos package index…")
    package.update_package_index()
    for fr, to in PAIRS:
        install_pair(fr, to)
    print("✅ Argos installed for DE→EN and EN→RO.")

if __name__ == "__main__":
    main()
