import tkinter as tk
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


if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()