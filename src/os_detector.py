import platform

def get_windows_os_info() -> dict:
    if platform.system() != "Windows":
        return {
            "product_name": "Not Windows (Testing Mode)",
            "build_number": "N/A",
            "architecture": platform.machine()
        }

    import winreg  # only import on Windows

    product_name = "Unknown Windows"
    build_number = "Unknown"

    architecture = "64-bit" if "64" in platform.machine() else "32-bit"

    key_path = "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion"

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
            product_name, _ = winreg.QueryValueEx(key, "ProductName")
            build_number, _ = winreg.QueryValueEx(key, "CurrentBuild")
    except Exception as e:
        raise RuntimeError(f"Registry read failed: {e}")

    return {
        "product_name": product_name,
        "build_number": build_number,
        "architecture": architecture
    }