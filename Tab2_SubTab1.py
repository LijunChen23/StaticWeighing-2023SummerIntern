import tkinter as tk
from tkinter import messagebox, ttk

import pandas as pd


class InnerTab1:
    def __init__(self, parent_tab):
        self.inner_tab1 = tk.Frame(master=parent_tab, bg="whitesmoke")

        self.count_weight_ref_0_text = None
        self.plot_frame0 = None
        self.count_weight_ref_3_text = None
        self.plot_frame3 = None
        self.gen_cali_button = None
        self.df = None
        self.table_name = None
        self.checkbox_vars1 = {}
        self.checkbox_vars2 = {}

        self.create_widgets()

    # ==================================================================================================================
    def create_widgets(self):
        style = ttk.Style()
        style.configure("CanvasFrame.TFrame", background="white")
        style.configure("Sub_tab.TLabel", background="whitesmoke")
        style.configure("Sub_tab.TButton", font=("SimHei", 12), padding=(10, 20),
                        background="white", foreground="black")

        # 创建标签 ------------------------------------------------------------------------------------------------------
        status0_label = ttk.Label(self.inner_tab1, text="Status[0]",
                                  font=("SimHei", 12), style="Sub_tab.TLabel")
        status0_label.grid(row=1, column=0, padx=5, pady=10, sticky="ns")

        # 创建一个Text组件
        status0_description_text = tk.Text(self.inner_tab1, height=2, width=25, font=("SimHei", 12))
        status0_description_text.grid(row=1, column=1, padx=5, pady=10, sticky="w")
        status0_description_text.insert("1.0", "Empty: Clean 0, Photo 0\nFull:  Clean 0, Photo 0")  # 将值插入到文本框中
        status0_description_text["state"] = "disabled"

        weight_ref_0_label = ttk.Label(self.inner_tab1, text="WeightRef组数：",
                                       font=("SimHei", 12), style="Sub_tab.TLabel")
        weight_ref_0_label.grid(row=2, column=0, padx=5, pady=5, sticky="ns")

        self.count_weight_ref_0_text = tk.Text(self.inner_tab1, height=1, width=25, font=("SimHei", 12))
        self.count_weight_ref_0_text.grid(row=2, column=1, padx=5, pady=10, sticky="w")

        self.plot_frame0 = tk.Frame(self.inner_tab1, bg="white", width=220, height=150,
                                    takefocus=False, borderwidth=1, relief="solid")
        self.plot_frame0.grid(row=3, column=0, columnspan=2, padx=5, pady=20, sticky="ns")

        # 在第2列和第4列之间创建一个分割线（模拟）---------------------------------------------------------------------------
        separator = ttk.Separator(self.inner_tab1, orient="vertical")
        separator.grid(row=0, column=2, rowspan=4, sticky="ns", padx=5)

        # 创建标签 ------------------------------------------------------------------------------------------------------
        status3_label = ttk.Label(self.inner_tab1, text="Status[3]",
                                  font=("SimHei", 12), style="Sub_tab.TLabel")
        status3_label.grid(row=1, column=3, padx=5, pady=10, sticky="ns")

        # 创建一个Text组件
        status3_description_text = tk.Text(self.inner_tab1, height=2, width=25, font=("SimHei", 12))
        status3_description_text.grid(row=1, column=4, padx=5, pady=10, sticky="w")
        status3_description_text.insert("1.0", "Empty: Clean 0, Photo 1\nFull:  Clean 1, Photo 1")  # 将值插入到文本框中
        status3_description_text["state"] = "disabled"

        weight_ref_3_label = ttk.Label(self.inner_tab1, text="WeightRef组数：",
                                       font=("SimHei", 12), style="Sub_tab.TLabel")
        weight_ref_3_label.grid(row=2, column=3, padx=5, pady=5, sticky="ns")

        self.count_weight_ref_3_text = tk.Text(self.inner_tab1, height=1, width=25, font=("SimHei", 12))
        self.count_weight_ref_3_text.grid(row=2, column=4, padx=5, pady=10, sticky="w")

        self.plot_frame3 = tk.Frame(self.inner_tab1, bg="white", width=220, height=150,
                                    takefocus=False, borderwidth=1, relief="solid")
        self.plot_frame3.grid(row=3, column=3, columnspan=2, padx=5, pady=20, sticky="ns")

        # 创建按钮，用于生成标定数据文件 -----------------------------------------------------------------------------------
        self.gen_cali_button = ttk.Button(self.inner_tab1, text="生成标定数据", command=self.generate_calibration,
                                          width=20, style="Sub_tab.TButton", state="normal")
        self.gen_cali_button.grid(row=5, column=0, columnspan=5, padx=5, pady=5, sticky="ns")

        # 辅助排版 ------------------------------------------------------------------------------------------------------
        self.inner_tab1.grid_rowconfigure(0, weight=1)
        self.inner_tab1.grid_rowconfigure(4, weight=1)
        self.inner_tab1.grid_rowconfigure(6, weight=1)
        self.inner_tab1.grid_columnconfigure(0, weight=1)
        self.inner_tab1.grid_columnconfigure(1, weight=1)
        self.inner_tab1.grid_columnconfigure(2, weight=1)
        self.inner_tab1.grid_columnconfigure(3, weight=1)
        self.inner_tab1.grid_columnconfigure(4, weight=1)

    # ==================================================================================================================
    def update_content(self, df, controller_serial_number):
        # 更新InnerTab1的内容
        self.df = df
        self.table_name = controller_serial_number

        self.clear_frame()

        options1 = self.get_weight_ref_options(status=0)
        options2 = self.get_weight_ref_options(status=3)
        self.count_weight_ref_0_text["state"] = "normal"
        self.count_weight_ref_3_text["state"] = "normal"
        self.count_weight_ref_0_text.delete("1.0", "end")               # 清除文本框中的值
        self.count_weight_ref_3_text.delete("1.0", "end")               # 清除文本框中的值
        self.count_weight_ref_0_text.insert("1.0", str(len(options1)))  # 将值插入到文本框中
        self.count_weight_ref_3_text.insert("1.0", str(len(options2)))  # 将值插入到文本框中
        self.count_weight_ref_0_text["state"] = "disabled"
        self.count_weight_ref_3_text["state"] = "disabled"
        self.create_options1(options=options1)
        self.create_options2(options=options2)

    # 清空图表框 ========================================================================================================
    def clear_frame(self):
        self.plot_frame0.destroy()
        self.plot_frame0 = tk.Frame(self.inner_tab1, width=220, height=150,
                                    takefocus=False, borderwidth=1, relief="solid")
        self.plot_frame0.grid(row=3, column=0, columnspan=2, padx=5, pady=20, sticky="ns")

        self.plot_frame3.destroy()
        self.plot_frame3 = tk.Frame(self.inner_tab1, width=220, height=150,
                                    takefocus=False, borderwidth=1, relief="solid")
        self.plot_frame3.grid(row=3, column=3, columnspan=2, padx=5, pady=20, sticky="ns")

    # ==================================================================================================================
    def get_weight_ref_options(self, status):
        df_status_filtered = self.df[self.df["WeighStatus"] == status]
        df_status_filtered = df_status_filtered.drop(columns=["WeighStatus"])

        # 格式化成"(x, y, z)"的字符串
        options = []
        for index, row in df_status_filtered.iterrows():
            option = f"({row['WeightRef1']}, {row['WeightRef2']}, {row['WeightRef3']})"
            options.append(option)
        return options

    # ==================================================================================================================
    def create_options1(self, options):
        style = ttk.Style()
        style.configure("Sub_tab.TCheckbutton", font=("SimHei", 12), padding=(5, 5),
                        background="white", foreground="black")
        style.configure("CanvasFrame.TFrame", background="white")

        # 创建Canvas控件 ------------------------------------------------------------------------------------------------
        canvas1 = tk.Canvas(master=self.plot_frame0, bg="white", width=200, height=150, takefocus=False)
        canvas1.grid(row=0, column=0, sticky="nsew")

        # 创建垂直滚动条 -------------------------------------------------------------------------------------------------
        scrollbar1 = ttk.Scrollbar(self.plot_frame0, orient="vertical", command=canvas1.yview)
        scrollbar1.grid(row=0, column=1, sticky="ns")
        canvas1.configure(yscrollcommand=scrollbar1.set)

        # 创建Canvas内部Frame -------------------------------------------------------------------------------------------
        canvas1_frame = ttk.Frame(canvas1, takefocus=False, style="CanvasFrame.TFrame")
        canvas1.create_window((0, 0), window=canvas1_frame, anchor="nw")

        for row, option in enumerate(options):
            var = tk.IntVar(value=0)
            self.checkbox_vars1[option] = var
            checkbutton = ttk.Checkbutton(canvas1_frame, text=option, variable=var, style="Sub_tab.TCheckbutton")
            checkbutton.grid(row=row, column=0, sticky="w")

        canvas1_frame.bind("<Configure>", lambda event: canvas1.configure(scrollregion=canvas1.bbox("all")))

    # ==================================================================================================================
    def create_options2(self, options):
        style = ttk.Style()
        style.configure("Sub_tab.TCheckbutton", font=("SimHei", 12), padding=(5, 5),
                        background="white", foreground="black")
        style.configure("CanvasFrame.TFrame", background="white")

        # 创建Canvas控件 ------------------------------------------------------------------------------------------------
        canvas2 = tk.Canvas(master=self.plot_frame3, bg="white", width=200, height=150, takefocus=False)
        canvas2.grid(row=0, column=0, sticky="nsew")

        # 创建垂直滚动条 -------------------------------------------------------------------------------------------------
        # orient="vertical" 表示垂直方向的滚动条。command=canvas.yview 设置了滚动条与 Canvas 的垂直滚动联动
        scrollbar2 = ttk.Scrollbar(self.plot_frame3, orient="vertical", command=canvas2.yview)
        scrollbar2.grid(row=0, column=1, sticky="ns")
        # yscrollcommand=scrollbar.set 表示将滚动条的位置信息传递给 Canvas，以便 Canvas 根据滚动条的位置进行垂直滚动。
        canvas2.configure(yscrollcommand=scrollbar2.set)

        # 创建Canvas内部Frame -------------------------------------------------------------------------------------------
        # 创建了一个内部的 Frame，用于在 Canvas 中放置图表
        canvas2_frame = ttk.Frame(canvas2, takefocus=False, style="CanvasFrame.TFrame")
        # 在 Canvas 中创建一个窗口，将内部的 Frame 放置在窗口内，以实现在 Canvas 中滚动 Frame。
        # (0, 0) 指定了窗口的初始位置，即左上角坐标。anchor="nw" 表示使用锚点 "nw"（表示左上角）来定位窗口内的 Frame。
        canvas2.create_window((0, 0), window=canvas2_frame, anchor="nw")

        for row, option in enumerate(options):
            var = tk.IntVar(value=0)
            self.checkbox_vars2[option] = var
            checkbutton = ttk.Checkbutton(canvas2_frame, text=option, variable=var, style="Sub_tab.TCheckbutton")
            checkbutton.grid(row=row, column=0, sticky="w")

        canvas2_frame.bind("<Configure>", lambda event: canvas2.configure(scrollregion=canvas2.bbox("all")))

    # ==================================================================================================================
    def generate_calibration(self):
        selected_options1 = [option for option, var in self.checkbox_vars1.items() if var.get() == 1]
        selected_options2 = [option for option, var in self.checkbox_vars2.items() if var.get() == 1]

        if selected_options1 == [] and selected_options2 == []:
            messagebox.showinfo("提示", "请至少选择一组重量")  # 弹窗告知用户未储存标定数据

        else:
            df_cali = pd.DataFrame()
            # 解析选项中的值
            for selected_option1 in selected_options1:
                selected_values = [float(val) for val in selected_option1.strip("()").split(", ")]
                # 在DataFrame中进行筛选
                df_row = self.df[
                    (self.df["WeighStatus"] == 0) &
                    (self.df["WeightRef1"] == selected_values[0]) &
                    (self.df["WeightRef2"] == selected_values[1]) &
                    (self.df["WeightRef3"] == selected_values[2])
                    ]
                df_cali = pd.concat([df_cali, df_row], axis=0)
                df_cali.reset_index(drop=True, inplace=True)

            for selected_option2 in selected_options2:
                selected_values = [float(val) for val in selected_option2.strip("()").split(", ")]
                # 在DataFrame中进行筛选
                df_row = self.df[
                    (self.df["WeighStatus"] == 3) &
                    (self.df["WeightRef1"] == selected_values[0]) &
                    (self.df["WeightRef2"] == selected_values[1]) &
                    (self.df["WeightRef3"] == selected_values[2])
                    ]
                df_cali = pd.concat([df_cali, df_row], axis=0)
                df_cali.reset_index(drop=True, inplace=True)

            print(df_cali)
            from Tab2_SubTab1_GenerateCSV import gen_calibration_data
            gen_calibration_data(df=df_cali, table_name=self.table_name)
