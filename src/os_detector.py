import platform
import winreg

def get_windows_os_info() -> dict:
	""" Returns Windows OS info:
	- product_name
	- build_number
	- architecture (x64 or x32)
	"""

	if platform.system() != "Windows":
		raise RuntimeError("This configuration detector is Windows only.")

	#defaults
	product_name = "Unknown Windows"
	build_number = "Unknown"
	architecture = "Unknown"
	if("32" in platform.machine()):
		architecture = "32-bit"
	elif("64" in platform.machine()):
		architecture = "64-bit"

	key_path = "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion"

	try:
		with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
			try:
				product_name, _ = winreg.QueryValueEx(key, "ProductName")
			except FileNotFoundError:
				pass


			try:
				build_number, _ = winreg.QueryValueEx(key, "CurrentBuild")
			except FileNotFoundError:
				try:
					build_number, _ = winreg.QueryValueEx(key, "CurrentBuildNumber")
				except FileNotFoundError:
					pass

	except OSError as e:
		raise RuntimeError(f"Read of Windows registry failed: {e}") from e

	return {
		"product_name": product_name,
		"build_number": build_number,
		"architecture": architecture,
	}