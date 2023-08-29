import os
import pyodbc
import tkinter as tk
from tkinter import filedialog, ttk


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
        self.saving_progress_text = None
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
        csv_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10, sticky="w")

        # 创建csv文件列表框
        self.csv_listbox = tk.Listbox(self.parent, width=60, height=8, font=("SimHei", 12))
        self.csv_listbox.grid(row=1, column=0, rowspan=2, columnspan=4, padx=5, pady=1, sticky="nsew")

        # 创建“读取”按钮 -------------------------------------------------------------------------------------------------
        self.read_data_button = ttk.Button(self.parent, text="读取数据", command=self.read_csv,
                                           width=10, style="Main_tab.TButton")
        self.read_data_button.grid(row=1, column=4, padx=5, pady=5, sticky="s")

        # 创建“清空”按钮
        self.clear_csv_button = ttk.Button(self.parent, text="清空", command=self.clear_csv_list,
                                           width=10, style="Main_tab.TButton", state="disabled")
        self.clear_csv_button.grid(row=2, column=4, padx=5, pady=5, sticky="n")

        # 创建“称重数据库”标签 --------------------------------------------------------------------------------------------
        db_label = ttk.Label(self.parent, text="称重数据库:", font=("SimHei", 12))
        db_label.grid(row=4, column=0, columnspan=1, padx=5, pady=1, sticky="w")

        # 创建数据库文件列表框
        self.db_listbox = tk.Listbox(self.parent, width=60, height=2, font=("SimHei", 12))
        self.db_listbox.grid(row=4, column=1, columnspan=1, padx=5, pady=1, sticky="ew")

        # 创建”选择数据库“按钮 --------------------------------------------------------------------------------------------
        self.choose_db_button = ttk.Button(self.parent, text="选择数据库", command=self.choose_database,
                                           width=10, style="Main_tab.TButton")
        self.choose_db_button.grid(row=4, column=2, padx=5, pady=1, sticky="ns")

        # 创建“清空”按钮
        self.clear_db_button = ttk.Button(self.parent, text="清空", command=self.clear_db_list,
                                          width=10, style="Main_tab.TButton", state="disabled")
        self.clear_db_button.grid(row=4, column=3, padx=5, pady=1, sticky="ns")

        # 创建“存入数据库”按钮
        self.save_to_db_button = ttk.Button(self.parent, text="存入数据库", command=self.save_to_database,
                                            width=10, style="Main_tab.TButton", state="disabled")
        self.save_to_db_button.grid(row=4, column=4, padx=5, pady=1, sticky="ns")

        # 创建”存储进度“标签 ------------------------------------------------------------------------------------------
        saving_progress_label = ttk.Label(self.parent, text="存储进度:", font=("SimHei", 12))
        saving_progress_label.grid(row=6, column=0, padx=5, pady=10, sticky="w")

        # 创建描述称重状态的文本框
        self.saving_progress_text = tk.Text(self.parent, height=2, font=("SimHei", 12))
        self.saving_progress_text.grid(row=6, column=1, columnspan=1, padx=5, pady=1, sticky="ew")
        self.saving_progress_text["state"] = "disabled"

        # 创建”存储概览“标签 ------------------------------------------------------------------------------------------
        saving_overview_label = ttk.Label(self.parent, text="存储概览:", font=("SimHei", 12))
        saving_overview_label.grid(row=8, column=0, padx=5, pady=1, sticky="w")

        # 创建描述称重状态的文本框
        self.saving_overview_text = tk.Text(self.parent, height=2, font=("SimHei", 12))
        self.saving_overview_text.grid(row=8, column=1, columnspan=4, padx=5, pady=10, sticky="nsew")
        self.saving_overview_text["state"] = "disabled"

        # --------------------------------------------------------------------------------------------------------------
        self.parent.grid_rowconfigure(3, weight=1)
        self.parent.grid_rowconfigure(5, weight=1)
        self.parent.grid_rowconfigure(1, weight=1)
        self.parent.grid_rowconfigure(8, weight=10)
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
        self.clear_text_box()

        db_file_path = self.db_listbox.get(0)
        db_file = os.path.abspath(db_file_path)
        conn = pyodbc.connect(r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)}; DBQ=" + db_file + ";Uid=;Pwd=;")

        csv_files = self.csv_listbox.get(0, tk.END)  # 获取所有 CSV 文件路径
        total_files = len(csv_files)

        self.saving_progress_text.config(state="normal")  # 启用文本框以进行编辑
        self.saving_overview_text.config(state="normal")  # 启用文本框以进行编辑

        from Tab0_MainTab_SaveToDatabase import save_csv_to_db  # 导入存数据库.py文件，确保文件位于相同目录下
        for idx, csv_file in enumerate(csv_files, start=1):
            progress_text = f"共 {total_files} 个文件，正在处理第 {idx} 个文件\n"
            self.saving_progress_text.delete("1.0", "end")  # 删除原先的第一行进度文本
            self.saving_progress_text.insert("1.0", progress_text)
            self.saving_progress_text.update()  # 更新文本框显示
            self.parent.update()  # 更新主窗口，以便文本框更新显示

            overview = save_csv_to_db(conn=conn, csv_file=csv_file)  # 将当前文件存入数据库

            self.saving_overview_text.insert("end", overview + "\n")  # 将新的消息添加到文本框末尾
            self.saving_overview_text.update()  # 更新文本框显示
            self.parent.update()  # 更新主窗口，以便文本框更新显示

        conn.commit()  # 提交更改
        conn.close()  # 关闭数据库连接

        progress_text = f"已储存全部 {total_files} 个文件\n"
        self.saving_progress_text.delete("1.0", "end")  # 删除原先的第一行进度文本
        self.saving_progress_text.insert("1.0", progress_text)
        self.saving_progress_text.config(state="disabled")  # 禁用文本框以防止编辑
        self.saving_overview_text.config(state="disabled")  # 禁用文本框以防止编辑

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
        self.clear_text_box()
        self.choose_db_button.config(state="normal")
        self.clear_db_button.config(state="disabled")

    def clear_text_box(self):
        self.saving_progress_text["state"] = "normal"
        self.saving_progress_text.delete("1.0", "end")  # 清除文本框内容
        self.saving_progress_text["state"] = "disabled"
        self.saving_overview_text["state"] = "normal"
        self.saving_overview_text.delete("1.0", "end")  # 清除文本框内容
        self.saving_overview_text["state"] = "disabled"


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
