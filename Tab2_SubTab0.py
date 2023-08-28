import pandas as pd
import tkinter as tk
from tkinter import ttk


class InnerTab0:
    def __init__(self, parent_tab):
        self.inner_tab0 = tk.Frame(master=parent_tab, bg="whitesmoke")

        self.weigh_status_dropdown = None
        self.status_description_text = None
        self.weight_ref_dropdown = None
        self.result_dropdown = None
        self.plot_frame = None
        self.df = None
        self.table_name = None
        self.df_status_filtered = None
        self.status_description_mapping = {
            "Status[0]": "Empty: Clean 0, Photo 0\nFull:  Clean 0, Photo 0",
            "Status[1]": "Empty: Clean 0, Photo 0\nFull:  Clean 1, Photo 0",
            "Status[2]": "Empty: Clean 0, Photo 1\nFull:  Clean 0, Photo 1",
            "Status[3]": "Empty: Clean 0, Photo 1\nFull:  Clean 1, Photo 1",
            "Status[4]": "Empty: Clean 1, Photo 0\nFull:  Clean 1, Photo 0",
            "Status[5]": "Empty: Clean 1, Photo 1\nFull:  Clean 1, Photo 1"
        }
        self.df_ref_filtered = None

        self.create_widgets()

    # ==================================================================================================================
    def create_widgets(self):
        # 创建style ----------------------------------------------------------------------------------------------------
        style = ttk.Style()
        style.configure("Sub_tab.TLabel", background="whitesmoke")
        style.configure("Sub_tab.TButton", font=("SimHei", 12), padding=(10, 20))

        # 创建”称重状态“标签 ----------------------------------------------------------------------------------------------
        weigh_status_label = ttk.Label(self.inner_tab0, text="称重状态：",
                                       font=("SimHei", 12), style="Sub_tab.TLabel")
        weigh_status_label.grid(row=0, column=0, padx=5, pady=20, sticky="w")

        # 创建”称重状态“下拉列表框
        self.weigh_status_dropdown = ttk.Combobox(self.inner_tab0, values=[], height=2,
                                                  font=("SimHei", 12), state="disabled")
        self.weigh_status_dropdown.grid(row=0, column=1, padx=5, pady=20, sticky="w")
        self.weigh_status_dropdown.bind("<<ComboboxSelected>>", self.show_weigh_status)

        # 创建”称重状态描述“标签 ------------------------------------------------------------------------------------------
        status_description_label = ttk.Label(self.inner_tab0, text="称重状态描述:",
                                             font=("SimHei", 12), style="Sub_tab.TLabel")
        status_description_label.grid(row=1, column=0, columnspan=2, padx=5, pady=10, sticky="w")

        # 创建描述称重状态的文本框
        self.status_description_text = tk.Text(self.inner_tab0, height=2, width=25, font=("SimHei", 12))
        self.status_description_text.grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky="ew")
        self.status_description_text["state"] = "disabled"

        # 创建“真实重量”标签 ----------------------------------------------------------------------------------------------
        weight_ref_label = ttk.Label(self.inner_tab0, text="真实重量：",
                                     font=("SimHei", 12), style="Sub_tab.TLabel")
        weight_ref_label.grid(row=4, column=0, columnspan=1, padx=5, pady=20, sticky="w")

        # 创建”真实重量“下拉列表框，用于选择要查看的生成的表格
        self.weight_ref_dropdown = ttk.Combobox(self.inner_tab0, values=[], height=2,
                                                font=("SimHei", 12), state="disabled")
        self.weight_ref_dropdown.grid(row=4, column=1, columnspan=1, padx=5, pady=20, sticky="w")
        self.weight_ref_dropdown.bind("<<ComboboxSelected>>", self.show_weigh_ref)

        # 创建“结果类型”标签 ----------------------------------------------------------------------------------------------
        result_label = ttk.Label(self.inner_tab0, text="结果类型：",
                                 font=("SimHei", 12), style="Sub_tab.TLabel")
        result_label.grid(row=5, column=0, columnspan=1, padx=5, pady=20, sticky="w")

        # 创建”结果类型“下拉列表框，用于选择要查看的生成的表格
        self.result_dropdown = ttk.Combobox(self.inner_tab0, values=["Weight6D", "Factor", "TempSlope"],
                                            font=("SimHei", 12), state="disabled")
        self.result_dropdown.grid(row=5, column=1, columnspan=1, padx=5, pady=20, sticky="w")
        self.result_dropdown.bind("<<ComboboxSelected>>", self.show_result_table)

        # 创建一个框用于展示生成的表格 --------------------------------------------------------------------------------------
        self.plot_frame = tk.Frame(self.inner_tab0, bg="white", width=500, height=400)
        self.plot_frame.grid(row=0, column=2, rowspan=6, padx=5, pady=20, sticky="ns")

        # 辅助排版 ------------------------------------------------------------------------------------------------------
        self.inner_tab0.grid_rowconfigure(3, weight=1)
        self.inner_tab0.grid_rowconfigure(4, weight=1)
        self.inner_tab0.grid_rowconfigure(5, weight=1)
        self.inner_tab0.grid_columnconfigure(2, weight=1)

    # ==================================================================================================================
    def update_content(self, df, controller_serial_number):
        # 更新InnerTab0的内容
        self.df = df
        self.table_name = controller_serial_number

        # 获取"WeighStatus"列的唯一值
        unique_values = self.df["WeighStatus"].unique().tolist()
        value_list = [f"Status[{int(unique_value)}]" for unique_value in unique_values]

        self.weigh_status_dropdown.set("")
        self.weigh_status_dropdown.config(values=value_list, state="readonly")
        self.status_description_text["state"] = "normal"
        self.status_description_text.delete("1.0", "end")  # 清除文本框内容
        self.status_description_text["state"] = "disabled"
        self.weight_ref_dropdown.set("")
        self.weight_ref_dropdown.config(state="disabled")
        self.result_dropdown.set("")
        self.result_dropdown.config(state="disabled")
        self.clear_frame()

    # ==================================================================================================================
    def show_weigh_status(self, event):
        selected_option = self.weigh_status_dropdown.get()  # 获取用户选择的选项
        weigh_status = float(selected_option.strip("Status[]"))

        self.df_status_filtered = self.df[self.df["WeighStatus"] == weigh_status]
        self.df_status_filtered = self.df_status_filtered.drop(columns=["WeighStatus"])

        # 格式化成"(x, y, z)"的字符串
        options = []
        for index, row in self.df_status_filtered.iterrows():
            option = f"({row['WeightRef1']}, {row['WeightRef2']}, {row['WeightRef3']})"
            options.append(option)

        self.status_description_text["state"] = "normal"
        self.status_description_text.delete("1.0", "end")                                             # 清除文本框内容
        self.status_description_text.insert("1.0", self.status_description_mapping[selected_option])  # 将值插入到文本框中
        self.status_description_text["state"] = "disabled"
        self.weight_ref_dropdown.set("")
        self.weight_ref_dropdown.config(values=options, state="readonly")
        self.result_dropdown.set("")
        self.result_dropdown.config(state="disabled")
        self.clear_frame()

    # 读取选择的WeightRef，筛选DataFrame =================================================================================
    def show_weigh_ref(self, event):
        selected_option = self.weight_ref_dropdown.get()                                   # 获取用户选择的选项
        selected_values = [float(val) for val in selected_option.strip("()").split(", ")]  # 解析选项中的值

        # 在DataFrame中进行筛选
        self.df_ref_filtered = self.df_status_filtered[
            (self.df_status_filtered["WeightRef1"] == selected_values[0]) &
            (self.df_status_filtered["WeightRef2"] == selected_values[1]) &
            (self.df_status_filtered["WeightRef3"] == selected_values[2])
        ]
        self.df_ref_filtered = self.df_ref_filtered.drop(columns=["WeightRef1", "WeightRef2", "WeightRef3"])
        self.result_dropdown.set("")
        self.result_dropdown.config(state="readonly")
        self.clear_frame()

    # 根据选择的结果，生成相应的表格数据 ====================================================================================
    def show_result_table(self, event):
        selected_option = self.result_dropdown.get()  # 获取选择的生成的结果表格
        self.clear_frame()                            # 清空图表框，以用于显示表格

        # 只保留列名中包含"Weight6D"或"Factor"或"TempSlope"的列
        df_result_filtered = self.df_ref_filtered.filter(like=selected_option, axis=1).T

        df1 = df_result_filtered.iloc[0:17, :]
        df1.reset_index(drop=True, inplace=True)
        df2 = df_result_filtered.iloc[17:34, :]
        df2.reset_index(drop=True, inplace=True)
        df3 = df_result_filtered.iloc[34:51, :]
        df3.reset_index(drop=True, inplace=True)

        df_result = pd.concat([df1, df2, df3], axis=1)
        df_result.columns = ["称重位置1", "称重位置2", "称重位置3"]
        df_result["小车ID"] = df_result.index
        df_result.loc[0, "小车ID"] = "平均值"
        df_result = df_result[["小车ID", "称重位置1", "称重位置2", "称重位置3"]]

        columns = list(df_result.columns)
        data = df_result.values.tolist()

        tree = ttk.Treeview(master=self.plot_frame, columns=columns, show="headings")
        # 设置 treeview 的位置和大小
        tree.place(x=0, y=0, width=500, height=400)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        for item in data:
            tree.insert("", "end", values=item)
        # 应用字体样式
        font = ("SimHei", 13)  # 设置字体样式
        style = ttk.Style()
        style.configure("Treeview.Heading", font=font, bd=1)
        style.configure("Treeview", font=font, bd=0)

    # 清空图表框 ========================================================================================================
    def clear_frame(self):
        self.plot_frame.destroy()
        self.plot_frame = tk.Frame(self.inner_tab0, bg="white", width=500, height=400)
        self.plot_frame.grid(row=0, column=2, rowspan=6, padx=5, pady=20, sticky="ns")
