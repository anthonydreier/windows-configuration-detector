import platform

if platform.system() == "Windows":
    import winreg


def _read_reg_value(key, value_name, default="N/A"):
    """Read a registry value and return a fallback when the value is missing."""
    try:
        value, _ = winreg.QueryValueEx(key, value_name)
        return str(value).strip()
    except FileNotFoundError:
        return default


def _format_install_date(raw_date: str) -> str:
    """Convert InstallDate from YYYYMMDD to YYYY-MM-DD when possible."""
    text = str(raw_date).strip()
    if len(text) == 8 and text.isdigit():
        return f"{text[:4]}-{text[4:6]}-{text[6:8]}"
    return text


def get_installed_software() -> list[dict]:
    """
    Scan standard uninstall registry paths and return installed software data.

    Each result contains name, version, publisher, and install date fields.
    Entries without a valid display name are ignored.
    """
    # Non-Windows systems return an empty list for safe testing behavior.
    if platform.system() != "Windows":
        return []

    software_list = []

    # Query both native and WOW6432Node uninstall locations.
    uninstall_paths = [
        "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
        "SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
    ]

    for path in uninstall_paths:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as parent_key:
                subkey_count = winreg.QueryInfoKey(parent_key)[0]

                # Each subkey typically represents one installed application.
                for i in range(subkey_count):
                    try:
                        subkey_name = winreg.EnumKey(parent_key, i)

                        with winreg.OpenKey(parent_key, subkey_name) as app_key:
                            # DisplayName is treated as the minimum validity check.
                            name = _read_reg_value(app_key, "DisplayName", "").strip()

                            if not name:
                                continue

                            # Optional values fall back to readable defaults.
                            version = _read_reg_value(app_key, "DisplayVersion", "N/A")
                            publisher = _read_reg_value(app_key, "Publisher", "Unknown")
                            install_date = _format_install_date(
                                _read_reg_value(app_key, "InstallDate", "N/A")
                            )

                            software_list.append(
                                {
                                    "name": name,
                                    "version": version,
                                    "publisher": publisher,
                                    "install_date": install_date,
                                }
                            )

                    except OSError:
                        # Skip unreadable entries and continue scanning.
                        continue

        except OSError:
            # Skip unavailable uninstall path and continue with remaining paths.
            continue

    return software_list
