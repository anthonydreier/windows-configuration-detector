from os_detector import get_windows_os_info

def main():
	info = get_windows_os_info()

	print("Detected OS Information")
	print("-----------------------")
	print(f"Product name: {info["product_name"]}")
	print(f"Build number: {info["build_number"]}")
	print(f"Architecture: {info["architecture"]}")


if __name__ == "__main__":
	main()