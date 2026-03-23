import os
import csv

def export_csv(os_info: dict, output_path: str):
	""" Exports Windows OS info to csv file

	Something like:
	{
		"product_name": "...",
		"build_number": "...",
		"architecture": "...",
	}"""

	os.makedirs(os.path.dirname(output_path), exist_ok=True)

	with open(output_path, "w", newline="") as f:
		writer = csv.writer(f)

		writer.writerow(["Field", "Value"])
		writer.writerow(["Product Name", os_info["product_name"]])
		writer.writerow(["Build Number", os_info["build_number"]])
		writer.writerow(["Architecture", os_info["architecture"]])