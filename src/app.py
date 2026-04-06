import tkinter as tk
from os_detector import get_windows_os_info
from csv_exporter import export_csv

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x400")
        self.root.title("OS Configuration Detector")

        # Scan Button
        self.scan_button = tk.Button(root, text="Scan", command=self.scan)
        self.scan_button.pack(pady=10)

        # Print Button
        self.print_button = tk.Button(root, text="Print", command=self.print_info)
        self.print_button.pack(pady=10)

        # Text Display Area
        self.text_area = tk.Text(root, height=10, width=60)
        self.text_area.pack(pady=10)

        self.os_info = None

    def scan(self):
        try:
            self.os_info = get_windows_os_info()

            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, "Detected OS Information\n")
            self.text_area.insert(tk.END, "-----------------------\n")

            for key, value in self.os_info.items():
                self.text_area.insert(tk.END, f"{key}: {value}\n")

        except Exception as e:
            self.text_area.insert(tk.END, f"Error: {e}\n")

    def print_info(self):
        if not self.os_info:
            self.text_area.insert(tk.END, "\nNo data to export.\n")
            return

        output_path = "output/osinfo.csv"
        export_csv(self.os_info, output_path)

        self.text_area.insert(tk.END, f"\nCSV saved to: {output_path}\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()