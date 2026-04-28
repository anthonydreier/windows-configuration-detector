import os
import csv


def _write_report_rows(os_info: dict, software_list: list[dict], output_path: str):
    """
    Write report content as CSV rows to the target file path.

    The same row structure is reused for both .csv and .txt exports.
    """

    # Ensure the output directory exists before writing report files.
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Section 1: operating system summary.
        writer.writerow(["Field", "Value"])
        writer.writerow(["Product Name", os_info["product_name"]])
        writer.writerow(["Build Number", os_info["build_number"]])
        writer.writerow(["Architecture", os_info["architecture"]])

        # Spacer row for readability between sections.
        writer.writerow([])

        # Section 2: installed software table.
        writer.writerow(["Installed Software"])
        writer.writerow(["Name", "Version", "Publisher", "Install Date"])

        for entry in software_list:
            writer.writerow([
                entry["name"],
                entry["version"],
                entry["publisher"],
                entry["install_date"],
            ])


def export_csv(os_info: dict, software_list: list[dict], output_path: str):
    """Export scan results to a standard CSV file."""
    _write_report_rows(os_info, software_list, output_path)


def export_txt(os_info: dict, software_list: list[dict], output_path: str):
    """Export scan results to a TXT file using the same CSV row format."""
    _write_report_rows(os_info, software_list, output_path)
