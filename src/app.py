import tkinter as tk
from os_detector import get_windows_os_info
from csv_exporter import export_csv
from software_scanner import get_installed_software

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x400")
        self.root.title("OS Configuration Detector")

        # Scan Button
        self.scan_button = tk.Button(root, text="Scan", command=self.scan)
        self.scan_button.pack(pady=10)

        # Print Button
        self.print_button = tk.Button(root, text="Export CSV", command=self.export_info)
        self.print_button.pack(pady=10)

        # Text Display Area
        self.text_area = tk.Text(root, height=10, width=60)
        self.text_area.pack(pady=10)

        self.os_info = None
        self.software_list = []

    def scan(self):
        try:
            self.os_info = get_windows_os_info()
            self.software_list = get_installed_software()

            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, "Detected OS Information\n")
            self.text_area.insert(tk.END, "-----------------------\n")

            self.text_area.insert(tk.END, f"Product Name: {self.os_info['product_name']}\n")
            self.text_area.insert(tk.END, f"Build Number: {self.os_info['build_number']}\n")
            self.text_area.insert(tk.END, f"Architecture: {self.os_info['architecture']}\n")

            self.text_area.insert(tk.END, "\nInstalled Software\n")
            self.text_area.insert(tk.END, "------------------\n")
            self.text_area.insert(tk.END, f"Detected {len(self.software_list)} software entries.\n\n")

            for entry in self.software_list:
                self.text_area.insert(
                    tk.END,
                    f"{entry['name']} | {entry['version']} | {entry['publisher']} | {entry['install_date']}\n"
                )

        except Exception as e:
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, f"Error: {e}\n")

    def export_info(self):
        if not self.os_info:
            self.text_area.insert(tk.END, "\nNo data to export.\n")
            return

        output_path = "output/osinfo.csv"
        export_csv(self.os_info, self.software_list, output_path)

        self.text_area.insert(tk.END, f"\nCSV saved to: {output_path}\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()