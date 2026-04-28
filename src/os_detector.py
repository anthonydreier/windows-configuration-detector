import platform


def _parse_build_number(build_number: str) -> int | None:
    """Extract the numeric build component from a registry build string."""
    text = str(build_number).strip()
    if not text:
        return None

    # Some systems report dotted values such as "22631.4460".
    # Only the leading build segment is needed for version checks.
    first_segment = text.split(".", 1)[0]
    return int(first_segment) if first_segment.isdigit() else None


def _normalize_windows_product_name(product_name: str, build_number: str) -> str:
    """
    Correct ProductName when Windows 11 reports a legacy Windows 10 prefix.

    This keeps edition text intact, such as Pro or Home, and only adjusts
    the major version label when the build threshold proves it is Windows 11.
    """
    build_int = _parse_build_number(build_number)
    if build_int is None:
        return product_name

    # Windows 11 begins at build 22000.
    if build_int >= 22000 and product_name.startswith("Windows 10"):
        return product_name.replace("Windows 10", "Windows 11", 1)

    return product_name


def get_windows_os_info() -> dict:
    """
    Read operating system identity from the Windows registry.

    Returns a dictionary with product name, build number, and architecture.
    On non-Windows hosts, returns a safe testing payload instead of failing.
    """
    # Non-Windows fallback keeps the UI usable during development and demos.
    if platform.system() != "Windows":
        return {
            "product_name": "Not Windows (Testing Mode)",
            "build_number": "N/A",
            "architecture": platform.machine()
        }

    # Delayed import avoids importing winreg on unsupported platforms.
    import winreg  # only import on Windows

    # Default values provide a predictable shape if a lookup fails mid-read.
    product_name = "Unknown Windows"
    build_number = "Unknown"

    # Architecture is inferred from machine type reported by Python runtime.
    architecture = "64-bit" if "64" in platform.machine() else "32-bit"

    key_path = "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion"

    try:
        # Read only the fields required for reporting and display.
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
            product_name, _ = winreg.QueryValueEx(key, "ProductName")
            build_number, _ = winreg.QueryValueEx(key, "CurrentBuild")
    except Exception as e:
        # Raise a single clear runtime error for the GUI status line.
        raise RuntimeError(f"Registry read failed: {e}")

    # Normalize Windows 11 naming where registry labels are historically stale.
    product_name = _normalize_windows_product_name(str(product_name), str(build_number))

    return {
        "product_name": product_name,
        "build_number": build_number,
        "architecture": architecture
    }
