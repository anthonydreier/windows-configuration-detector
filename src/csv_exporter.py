import os
import csv


def export_csv(os_info: dict, software_list: list[dict], output_path: str):
    """Export OS info and installed software info to a CSV file."""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # OS info section
        writer.writerow(["Field", "Value"])
        writer.writerow(["Product Name", os_info["product_name"]])
        writer.writerow(["Build Number", os_info["build_number"]])
        writer.writerow(["Architecture", os_info["architecture"]])

        # Blank line
        writer.writerow([])

        # Installed software section
        writer.writerow(["Installed Software"])
        writer.writerow(["Name", "Version", "Publisher", "Install Date"])

        for entry in software_list:
            writer.writerow([
                entry["name"],
                entry["version"],
                entry["publisher"],
                entry["install_date"],
            ])