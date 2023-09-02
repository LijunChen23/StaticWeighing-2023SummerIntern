import os
import pandas as pd
import pyodbc
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from Tab2_SubTab0 import InnerTab0
from Tab2_SubTab1 import InnerTab1


class CalibrationDataTab:
    def __init__(self, parent):
        self.main_tab = parent

        self.db_listbox = None
        self.choose_db_button = None
        self.clear_db_button = None
        self.view_db_button = None
        self.db_table_dropdown = None
        self.inner_tab_control = None
        self.inner_tab0 = None
        self.inner_tab1 = None
        self.controller_and_df_list = None

        self.create_controls()

    # ==================================================================================================================
    def create_controls(self):
        style = ttk.Style()
        style.configure("Main_tab.TButton", font=("SimHei", 12), padding=(10, 20))

        # 创建”标定数据库“标签 --------------------------------------------------------------------------------------------
        db_label = ttk.Label(self.main_tab, text="标定数据库：", font=("SimHei", 12))
        db_label.grid(row=0, column=0, padx=20, pady=5, sticky="w")

        # 创建”标定数据库“列表框
        self.db_listbox = tk.Listbox(self.main_tab, width=40, height=2, font=("SimHei", 12))
        self.db_listbox.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        # 创建“选择数据库”按钮 --------------------------------------------------------------------------------------------
        self.choose_db_button = ttk.Button(self.main_tab, text="选择数据库", command=self.choose_database,
                                           width=10, style="Main_tab.TButton")
        self.choose_db_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # 创建“清空”按钮
        self.clear_db_button = ttk.Button(self.main_tab, text="清空", command=self.clear_db_list,
                                          width=10, style="Main_tab.TButton", state="disabled")
        self.clear_db_button.grid(row=0, column=4, padx=5, pady=5, sticky="ew")

        # 创建“查看数据库”按钮
        self.view_db_button = ttk.Button(self.main_tab, text="查看数据库", command=self.view_database,
                                         width=10, style="Main_tab.TButton", state="disabled")
        self.view_db_button.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

        # 创建”机器序列号“标签 --------------------------------------------------------------------------------------------
        controller_label = ttk.Label(self.main_tab, text="机器序列号：", font=("SimHei", 12))
        controller_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")

        # 创建下拉列表
        self.db_table_dropdown = ttk.Combobox(self.main_tab, values=[], height=2,
                                              font=("SimHei", 12), state="disabled")
        self.db_table_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.db_table_dropdown.bind("<<ComboboxSelected>>", self.controller_dropdown_selected)

        # 创建子tab -----------------------------------------------------------------------------------------------------
        self.inner_tab_control = ttk.Notebook(self.main_tab)
        self.inner_tab0 = InnerTab0(parent_tab=self.inner_tab_control)
        self.inner_tab1 = InnerTab1(parent_tab=self.inner_tab_control)

        self.inner_tab_control.add(self.inner_tab0.inner_tab0, text="查看标定数据", state="disabled")
        self.inner_tab_control.add(self.inner_tab1.inner_tab1, text="生成标定数据文件", state="disabled")
        self.inner_tab_control.grid(row=3, column=0, columnspan=6, rowspan=10, padx=5, pady=5, sticky="ns")

        # 辅助排版 ------------------------------------------------------------------------------------------------------
        self.main_tab.grid_columnconfigure(2, weight=1)

    # “选择数据库”按钮的事件处理函数，弹窗要求用户选择称重数据库位置 ===============================================================
    def choose_database(self):
        db_path = filedialog.askopenfilename(filetypes=[("Access files", "*.accdb")])
        if db_path:
            self.db_listbox.insert(tk.END, db_path)
            self.choose_db_button.config(state="disabled")
            self.clear_db_button.config(state="normal")
            self.view_db_button.config(state="normal")

    # “清空”按钮的事件处理函数 =============================================================================================
    def clear_db_list(self):
        self.db_listbox.delete(0, tk.END)
        self.choose_db_button.config(state="normal")
        self.clear_db_button.config(state="disabled")
        self.view_db_button.config(state="disabled")
        self.db_table_dropdown.set("")  # 清空下拉列表框
        self.db_table_dropdown.config(values=[], state="disabled")
        self.disable_tabs()

    # “查看数据库”按钮的事件处理函数 ========================================================================================
    def view_database(self):
        db_file_path = self.db_listbox.get(0)
        # 以下代码返回数据库中的表格的dataframe
        self.controller_and_df_list = read_db(db_file_path)
        self.db_table_dropdown.set("")  # 清空下拉列表框原先数据
        # 将获得的表格名称作为下拉列表框的选项放入
        self.db_table_dropdown.config(values=[item[0] for item in self.controller_and_df_list], state="readonly")

    # ==================================================================================================================
    def controller_dropdown_selected(self, event):
        selected_table = self.db_table_dropdown.get()  # 获取用户选择的选项
        if selected_table:
            for controller_and_df in self.controller_and_df_list:
                if controller_and_df[0] == selected_table:
                    df = controller_and_df[1]
                    df = df.drop(columns=["ID"])
                    self.inner_tab0.update_content(df=df, controller_serial_number=selected_table)
                    self.inner_tab1.update_content(df=df, controller_serial_number=selected_table)
                    self.enable_tabs()

    # ==================================================================================================================
    def enable_tabs(self):
        self.inner_tab_control.tab(0, state="normal")  # 启用第一个子 Tab
        self.inner_tab_control.tab(1, state="normal")  # 启用第二个子 Tab

    # ==================================================================================================================
    def disable_tabs(self):
        self.inner_tab_control.tab(0, state="disabled")  # 启用第一个子 Tab
        self.inner_tab_control.tab(1, state="disabled")  # 启用第二个子 Tab


# ======================================================================================================================
def read_db(db_file_path):
    db_file = os.path.abspath(db_file_path)
    # 连接数据库
    conn = pyodbc.connect(r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)}; DBQ=" + db_file + ";Uid=;Pwd=;")
    messagebox.showinfo("提示", "数据库连接成功")
    cursor = conn.cursor()                              # 创建游标

    tables = cursor.tables(tableType="TABLE")           # 获取数据库中已经存在的表
    result = []
    for table_info in tables:
        table_name = table_info.table_name              # 读取数据库中的表格名称
        query = f"SELECT * FROM `{table_name}`;"        # 创建SQL语句读取表格内容
        df_database = pd.read_sql(sql=query, con=conn)  # 执行SQL语句
        result.append((table_name, df_database))

    cursor.close()                                      # 关闭光标对象
    conn.close()                                        # 关闭数据库连接
    return result


# ======================================================================================================================
def main():
    root = tk.Tk()
    root.title("Data Processing Application")
    root.geometry("1100x700")

    CalibrationDataTab(root)
    root.mainloop()


if __name__ == "__main__":
    main()
