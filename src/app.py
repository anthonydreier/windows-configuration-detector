import tkinter as tk
from tkinter import ttk

from os_detector import get_windows_os_info
from csv_exporter import export_csv, export_txt
from software_scanner import get_installed_software

class GUI:
    """Builds and controls the desktop interface for scanning and export."""

    def __init__(self, root):
        """Create the full window layout and initialize empty scan state."""
        self.root = root
        self.root.geometry("900x600")
        self.root.title("OS Configuration Detector")

        # These fields are filled only after a successful scan.
        self.os_info = None
        self.software_list = []

        # Top control row for actions a user performs directly.
        controls_frame = tk.Frame(root)
        controls_frame.pack(fill=tk.X, padx=12, pady=(12, 8))

        self.scan_button = tk.Button(controls_frame, text="Scan", command=self.scan)
        self.scan_button.pack(side=tk.LEFT, padx=(0, 8))

        self.export_button = tk.Button(controls_frame, text="Export CSV + TXT", command=self.export_info)
        self.export_button.pack(side=tk.LEFT, padx=(0, 8))

        self.quit_button = tk.Button(controls_frame, text="Quit", command=self.root.destroy)
        self.quit_button.pack(side=tk.LEFT)

        # Read-only summary area for the detected operating system.
        os_frame = tk.LabelFrame(root, text="OS Information")
        os_frame.pack(fill=tk.X, padx=12, pady=(0, 8))

        self.product_name_var = tk.StringVar(value="Product Name: Not scanned")
        self.build_number_var = tk.StringVar(value="Build Number: Not scanned")
        self.architecture_var = tk.StringVar(value="Architecture: Not scanned")
        self.software_count_var = tk.StringVar(value="Detected software entries: 0")

        tk.Label(os_frame, textvariable=self.product_name_var, anchor="w").pack(fill=tk.X, padx=10, pady=(8, 2))
        tk.Label(os_frame, textvariable=self.build_number_var, anchor="w").pack(fill=tk.X, padx=10, pady=2)
        tk.Label(os_frame, textvariable=self.architecture_var, anchor="w").pack(fill=tk.X, padx=10, pady=2)
        tk.Label(os_frame, textvariable=self.software_count_var, anchor="w").pack(fill=tk.X, padx=10, pady=(2, 8))

        # Main results table for installed software entries.
        table_frame = tk.Frame(root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 8))

        self.software_table = ttk.Treeview(
            table_frame,
            columns=("name", "version", "publisher", "install_date"),
            show="headings",
        )
        self.software_table.heading("name", text="Name")
        self.software_table.heading("version", text="Version")
        self.software_table.heading("publisher", text="Publisher")
        self.software_table.heading("install_date", text="Install Date")

        self.software_table.column("name", width=320, anchor="w")
        self.software_table.column("version", width=120, anchor="w")
        self.software_table.column("publisher", width=240, anchor="w")
        self.software_table.column("install_date", width=120, anchor="w")

        table_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.software_table.yview)
        self.software_table.configure(yscrollcommand=table_scrollbar.set)

        self.software_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        table_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Single status line for success, warning, and error feedback.
        self.status_var = tk.StringVar(value="Ready.")
        self.status_label = tk.Label(root, textvariable=self.status_var, anchor="w")
        self.status_label.pack(fill=tk.X, padx=12, pady=(0, 12))

    def _set_status(self, message: str):
        """Show a short status message in the footer area."""
        self.status_var.set(message)

    def _clear_software_table(self):
        """Remove all current rows before inserting fresh scan data."""
        self.software_table.delete(*self.software_table.get_children())

    def _update_os_labels(self):
        """Refresh OS labels from current state, or reset when no scan exists."""
        if not self.os_info:
            self.product_name_var.set("Product Name: Not scanned")
            self.build_number_var.set("Build Number: Not scanned")
            self.architecture_var.set("Architecture: Not scanned")
            return

        self.product_name_var.set(f"Product Name: {self.os_info['product_name']}")
        self.build_number_var.set(f"Build Number: {self.os_info['build_number']}")
        self.architecture_var.set(f"Architecture: {self.os_info['architecture']}")

    def scan(self):
        """Run OS and software detection, then render all results in the UI."""
        try:
            self.os_info = get_windows_os_info()
            self.software_list = get_installed_software()
            self._update_os_labels()
            self._clear_software_table()

            for entry in self.software_list:
                self.software_table.insert(
                    "",
                    tk.END,
                    values=(
                        entry["name"],
                        entry["version"],
                        entry["publisher"],
                        entry["install_date"],
                    ),
                )

            self.software_count_var.set(f"Detected software entries: {len(self.software_list)}")
            self._set_status(f"Scan complete. Found {len(self.software_list)} software entries.")
        except Exception as e:
            self.os_info = None
            self.software_list = []
            self._update_os_labels()
            self._clear_software_table()
            self.software_count_var.set("Detected software entries: 0")
            self._set_status(f"Error: {e}")

    def export_info(self):
        """Write the latest scan data to both CSV and TXT report files."""
        if not self.os_info:
            self._set_status("No data to export. Run Scan first.")
            return

        csv_output_path = "output/osinfo.csv"
        txt_output_path = "output/osinfo.txt"
        export_csv(self.os_info, self.software_list, csv_output_path)
        export_txt(self.os_info, self.software_list, txt_output_path)

        self._set_status(f"Exported: {csv_output_path} and {txt_output_path}")


if __name__ == "__main__":
    """Launch the GUI application loop."""
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
