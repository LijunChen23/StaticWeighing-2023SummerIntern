import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class WeighingDataTab:
    def __init__(self, parent):
        self.parent = parent

        self.csv_listbox = None
        self.read_data_button = None
        self.clear_csv_button = None
        self.db_listbox = None
        self.choose_db_button = None
        self.clear_db_button = None
        self.save_to_db_button = None
        self.current_csv_files = []
        self.selected_database = None

        self.create_controls()

    # ==================================================================================================================
    def create_controls(self):
        # Create a custom style for the button
        style = ttk.Style()
        style.configure("Main_tab.TButton", font=("SimHei", 12), padding=(10, 20))

        # --------------------------------------------------------------------------------------------------------------
        csv_label = ttk.Label(self.parent, text="包含称重数据的csv文件:", font=("SimHei", 12))
        csv_label.grid(row=1, column=0, columnspan=2, padx=40, pady=1, sticky="w")

        """创建csv文件列表框"""
        self.csv_listbox = tk.Listbox(self.parent, width=60, height=10, font=("SimHei", 12))
        self.csv_listbox.grid(row=2, column=0, columnspan=2, padx=40, pady=1, sticky="nsew")

        """创建选择csv文件的按钮"""
        self.read_data_button = ttk.Button(self.parent, text="读取数据", command=self.read_csv,
                                           width=15, style="Main_tab.TButton")
        self.read_data_button.grid(row=3, column=0, padx=40, pady=5, sticky="e")

        """创建清空csv文件列表框的按钮"""
        self.clear_csv_button = ttk.Button(self.parent, text="清空", command=self.clear_csv_list,
                                           width=15, style="Main_tab.TButton", state="disabled")
        self.clear_csv_button.grid(row=3, column=1, padx=40, pady=5, sticky="w")

        # --------------------------------------------------------------------------------------------------------------
        db_label = ttk.Label(self.parent, text="称重数据库:", font=("SimHei", 12))
        db_label.grid(row=5, column=0, columnspan=2, padx=40, pady=1, sticky="w")

        """创建数据库文件列表框"""
        self.db_listbox = tk.Listbox(self.parent, width=60, height=2, font=("SimHei", 12))
        self.db_listbox.grid(row=6, column=0, columnspan=2, padx=40, pady=1, sticky="nsew")

        """创建选择数据库文件的按钮"""
        self.choose_db_button = ttk.Button(self.parent, text="选择数据库", command=self.choose_database,
                                           width=15, style="Main_tab.TButton")
        self.choose_db_button.grid(row=7, column=0, padx=40, pady=5, sticky="e")

        """创建数据库文件列表框的按钮"""
        self.clear_db_button = ttk.Button(self.parent, text="清空", command=self.clear_db_list,
                                          width=15, style="Main_tab.TButton", state="disabled")
        self.clear_db_button.grid(row=7, column=1, padx=40, pady=5, sticky="w")

        """创建将csv文件存入数据库的按钮"""
        self.save_to_db_button = ttk.Button(self.parent, text="存入数据库", command=self.save_to_database,
                                            width=20, style="Main_tab.TButton", state="disabled")
        self.save_to_db_button.grid(row=8, column=0, columnspan=2, padx=100, pady=20, sticky="ns")

        # --------------------------------------------------------------------------------------------------------------
        self.parent.grid_rowconfigure(0, weight=1)  # Empty row at the top
        self.parent.grid_rowconfigure(2, weight=1)
        self.parent.grid_rowconfigure(4, weight=1)
        self.parent.grid_rowconfigure(9, weight=1)  # Empty row at the end
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_columnconfigure(1, weight=1)

    # ==================================================================================================================
    def read_csv(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
        if file_paths:
            for file_path in file_paths:
                if file_path not in self.current_csv_files:  # Check if file is not already in the list
                    self.csv_listbox.insert(tk.END, file_path)
                    self.current_csv_files.append(file_path)
            self.update_save_button_state()

            self.clear_csv_button.config(state="normal")

    # ==================================================================================================================
    def choose_database(self):
        db_path = filedialog.askopenfilename(filetypes=[("Access files", "*.accdb")])
        self.update_save_button_state()
        if db_path:
            self.db_listbox.insert(tk.END, db_path)
            self.selected_database = db_path
            self.update_save_button_state()

            self.choose_db_button.config(state="disabled")
            self.clear_db_button.config(state="normal")

    # ==================================================================================================================
    def update_save_button_state(self):
        if self.current_csv_files and self.selected_database:
            self.save_to_db_button["state"] = "normal"
        else:
            self.save_to_db_button["state"] = "disabled"

    # ==================================================================================================================
    def save_to_database(self):
        db_file_path = self.db_listbox.get(0)
        csv_files = self.csv_listbox.get(0, tk.END)  # 获取所有 CSV 文件路径

        from Tab0_MainTab_SaveToDatabase import save_csv_to_db  # 导入存数据库.py文件，确保文件位于相同目录下
        save_csv_to_db(db_file_path, csv_files)  # 将文件存入数据库

        messagebox.showinfo("提示", "已储存数据")
        self.clear_csv_list()
        self.update_save_button_state()

    # ==================================================================================================================
    def clear_csv_list(self):
        self.csv_listbox.delete(0, tk.END)
        self.current_csv_files = []
        self.update_save_button_state()
        self.clear_csv_button.config(state="disabled")

    # ==================================================================================================================
    def clear_db_list(self):
        self.db_listbox.delete(0, tk.END)
        self.selected_database = None
        self.update_save_button_state()

        self.choose_db_button.config(state="normal")
        self.clear_db_button.config(state="disabled")


# ======================================================================================================================
def main():
    root = tk.Tk()
    root.title("Weighing Data Application")
    root.geometry("1100x700")

    tab = WeighingDataTab(root)
    tab.create_controls()
    root.mainloop()


if __name__ == "__main__":
    main()
