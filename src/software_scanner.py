import platform

if platform.system() == "Windows":
    import winreg


def _read_reg_value(key, value_name, default="N/A"):
    try:
        value, _ = winreg.QueryValueEx(key, value_name)
        return str(value).strip()
    except FileNotFoundError:
        return default


def get_installed_software() -> list[dict]:
    if platform.system() != "Windows":
        return []

    software_list = []

    uninstall_paths = [
        "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
        "SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
    ]

    for path in uninstall_paths:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as parent_key:
                subkey_count = winreg.QueryInfoKey(parent_key)[0]

                for i in range(subkey_count):
                    try:
                        subkey_name = winreg.EnumKey(parent_key, i)

                        with winreg.OpenKey(parent_key, subkey_name) as app_key:
                            name = _read_reg_value(app_key, "DisplayName", "").strip()

                            if not name:
                                continue

                            version = _read_reg_value(app_key, "DisplayVersion", "N/A")
                            publisher = _read_reg_value(app_key, "Publisher", "Unknown")
                            install_date = _read_reg_value(app_key, "InstallDate", "N/A")

                            software_list.append(
                                {
                                    "name": name,
                                    "version": version,
                                    "publisher": publisher,
                                    "install_date": install_date,
                                }
                            )

                    except OSError:
                        continue

        except OSError:
            continue

    return software_list