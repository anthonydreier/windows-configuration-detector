from os_detector import get_windows_os_info
from csv_exporter import export_csv

def main():
	info = get_windows_os_info()

	print("Detected OS Information")
	print("-----------------------")
	print(f"Product name: {info["product_name"]}")
	print(f"Build number: {info["build_number"]}")
	print(f"Architecture: {info["architecture"]}")

	output_path = "output/osinfo.csv"
	export_csv(info, output_path)

	print(f"\nCSV report saved to: {output_path}")
	

if __name__ == "__main__":
	main()