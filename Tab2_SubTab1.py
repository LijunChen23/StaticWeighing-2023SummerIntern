import tkinter as tk
from tkinter import messagebox, ttk

import pandas as pd


class InnerTab1:
    def __init__(self, parent_tab):
        self.inner_tab1 = tk.Frame(master=parent_tab, bg="whitesmoke")

        self.master_frame = None
        self.canvas = None
        self.canvas_frame = None
        self.gen_cali_button = None
        self.df = None
        self.table_name = None
        self.count_weight_ref_0_text = None
        self.count_weight_ref_1_text = None
        self.count_weight_ref_2_text = None
        self.count_weight_ref_3_text = None
        self.count_weight_ref_4_text = None
        self.count_weight_ref_5_text = None
        self.plot_frame0 = None
        self.plot_frame1 = None
        self.plot_frame2 = None
        self.plot_frame3 = None
        self.plot_frame4 = None
        self.plot_frame5 = None
        self.checkbox_vars0 = {}
        self.checkbox_vars1 = {}
        self.checkbox_vars2 = {}
        self.checkbox_vars3 = {}
        self.checkbox_vars4 = {}
        self.checkbox_vars5 = {}

        self.create_widgets()

    # ==================================================================================================================
    def create_widgets(self):
        style = ttk.Style()
        style.configure("Tab2_SubTab1.TFrame", background="white")
        style.configure("Tab2_SubTab1.TLabel", background="whitesmoke")
        style.configure("Tab2_SubTab1.TCheckbutton", background="white", font=("SimHei", 12))
        style.configure("Tab2_SubTab1.TButton", font=("SimHei", 12), padding=(10, 20),
                        background="white", foreground="black")

        self.master_frame = tk.Frame(self.inner_tab1, bg="whitesmoke", width=900, height=400,
                                     takefocus=False, borderwidth=1, relief="solid")
        self.master_frame.grid(row=1, column=0, padx=5, pady=20, sticky="ns")
        self.master_frame.grid_propagate(False)  # 设置为0可使组件大小不变
        self.create_canvas_in_master_frame()

        # 创建按钮，用于生成标定数据文件 -----------------------------------------------------------------------------------
        self.gen_cali_button = ttk.Button(self.inner_tab1, text="生成标定数据", command=self.generate_calibration,
                                          width=20, style="Tab2_SubTab1.TButton", state="normal")
        self.gen_cali_button.grid(row=2, column=0, padx=5, pady=5, sticky="ns")

        # 辅助排版 ------------------------------------------------------------------------------------------------------
        self.inner_tab1.grid_rowconfigure(0, weight=1)
        self.inner_tab1.grid_rowconfigure(3, weight=1)
        self.inner_tab1.grid_columnconfigure(0, weight=1)

    # ==================================================================================================================
    def create_canvas_in_master_frame(self):
        self.canvas = tk.Canvas(self.master_frame, bg="whitesmoke", width=900, height=380, takefocus=False)
        self.canvas.grid(row=0, column=0, sticky="ns")

        # Create a horizontal scrollbar for the canvas
        x_scrollbar = ttk.Scrollbar(self.master_frame, orient="horizontal", command=self.canvas.xview)
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        self.canvas.configure(xscrollcommand=x_scrollbar.set)

        self.canvas_frame = tk.Frame(self.canvas, takefocus=False, bg="whitesmoke")
        self.canvas.create_window((0, 0), window=self.canvas_frame, anchor="nw")
        self.canvas_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.create_master_frame_widgets()

    # ==================================================================================================================
    def create_master_frame_widgets(self):
        # 创建标签 ------------------------------------------------------------------------------------------------------
        status0_label = ttk.Label(self.canvas_frame, text="Status[0]:",
                                  font=("SimHei", 12), style="Tab2_SubTab1.TLabel")
        status0_label.grid(row=0, column=0, padx=1, pady=10, sticky="w")

        # 创建一个Text组件
        status0_description_text = tk.Text(self.canvas_frame, height=3, width=17, font=("SimHei", 12))
        status0_description_text.grid(row=0, column=1, padx=1, pady=10, sticky="w")
        status0_description_text.insert("1.0", "      Clean Photo\nEmpty   0     0\nFull    0     0")  # 将值插入到文本框中
        status0_description_text["state"] = "disabled"

        weight_ref_0_label = ttk.Label(self.canvas_frame, text="WeightRef组数:",
                                       font=("SimHei", 12), style="Tab2_SubTab1.TLabel")
        weight_ref_0_label.grid(row=1, column=0, padx=1, pady=5, sticky="w")

        self.count_weight_ref_0_text = tk.Text(self.canvas_frame, height=1, width=17, font=("SimHei", 12))
        self.count_weight_ref_0_text.grid(row=1, column=1, padx=1, pady=10, sticky="w")

        self.plot_frame0 = tk.Frame(self.canvas_frame, bg="white", width=220, height=200,
                                    takefocus=False, borderwidth=1, relief="solid")
        self.plot_frame0.grid(row=2, column=0, columnspan=2, padx=5, pady=20, sticky="ns")

        # 在第1列和第3列之间创建一个分割线（模拟）---------------------------------------------------------------------------
        separator = ttk.Separator(self.canvas_frame, orient="vertical")
        separator.grid(row=0, column=2, rowspan=4, sticky="ns", padx=5)

        # 创建标签 ------------------------------------------------------------------------------------------------------
        status1_label = ttk.Label(self.canvas_frame, text="Status[1]",
                                  font=("SimHei", 12), style="Tab2_SubTab1.TLabel")
        status1_label.grid(row=0, column=3, padx=1, pady=10, sticky="w")

        # 创建一个Text组件
        status1_description_text = tk.Text(self.canvas_frame, height=3, width=17, font=("SimHei", 12))
        status1_description_text.grid(row=0, column=4, padx=1, pady=10, sticky="w")
        status1_description_text.insert("1.0", "      Clean Photo\nEmpty   0     0\nFull    1     0")  # 将值插入到文本框中
        status1_description_text["state"] = "disabled"

        weight_ref_1_label = ttk.Label(self.canvas_frame, text="WeightRef组数:",
                                       font=("SimHei", 12), style="Tab2_SubTab1.TLabel")
        weight_ref_1_label.grid(row=1, column=3, padx=1, pady=5, sticky="w")

        self.count_weight_ref_1_text = tk.Text(self.canvas_frame, height=1, width=17, font=("SimHei", 12))
        self.count_weight_ref_1_text.grid(row=1, column=4, padx=1, pady=10, sticky="w")

        self.plot_frame1 = tk.Frame(self.canvas_frame, bg="white", width=220, height=200,
                                    takefocus=False, borderwidth=1, relief="solid")
        self.plot_frame1.grid(row=2, column=3, columnspan=2, padx=5, pady=20, sticky="ns")

        # 在第4列和第6列之间创建一个分割线（模拟）---------------------------------------------------------------------------
        separator = ttk.Separator(self.canvas_frame, orient="vertical")
        separator.grid(row=0, column=5, rowspan=4, sticky="ns", padx=5)

        # 创建标签 ------------------------------------------------------------------------------------------------------
        status2_label = ttk.Label(self.canvas_frame, text="Status[2]:",
                                  font=("SimHei", 12), style="Tab2_SubTab1.TLabel")
        status2_label.grid(row=0, column=6, padx=5, pady=10, sticky="w")

        # 创建一个Text组件
        status2_description_text = tk.Text(self.canvas_frame, height=3, width=17, font=("SimHei", 12))
        status2_description_text.grid(row=0, column=7, padx=1, pady=10, sticky="w")
        status2_description_text.insert("1.0", "      Clean Photo\nEmpty   0     1\nFull    1     1")  # 将值插入到文本框中
        status2_description_text["state"] = "disabled"

        weight_ref_2_label = ttk.Label(self.canvas_frame, text="WeightRef组数:",
                                       font=("SimHei", 12), style="Tab2_SubTab1.TLabel")
        weight_ref_2_label.grid(row=1, column=6, padx=1, pady=5, sticky="w")

        self.count_weight_ref_2_text = tk.Text(self.canvas_frame, height=1, width=17, font=("SimHei", 12))
        self.count_weight_ref_2_text.grid(row=1, column=7, padx=1, pady=10, sticky="w")

        self.plot_frame2 = tk.Frame(self.canvas_frame, bg="white", width=220, height=200,
                                    takefocus=False, borderwidth=1, relief="solid")
        self.plot_frame2.grid(row=2, column=6, columnspan=2, padx=5, pady=20, sticky="ns")

        # 在第7列和第9列之间创建一个分割线（模拟）---------------------------------------------------------------------------
        separator = ttk.Separator(self.canvas_frame, orient="vertical")
        separator.grid(row=0, column=8, rowspan=4, sticky="ns", padx=5)

        # 创建标签 ------------------------------------------------------------------------------------------------------
        status3_label = ttk.Label(self.canvas_frame, text="Status[3]:",
                                  font=("SimHei", 12), style="Tab2_SubTab1.TLabel")
        status3_label.grid(row=0, column=9, padx=1, pady=10, sticky="w")

        # 创建一个Text组件
        status3_description_text = tk.Text(self.canvas_frame, height=3, width=17, font=("SimHei", 12))
        status3_description_text.grid(row=0, column=10, padx=1, pady=10, sticky="w")
        status3_description_text.insert("1.0", "      Clean Photo\nEmpty   0     1\nFull    0     1")  # 将值插入到文本框中
        status3_description_text["state"] = "disabled"

        weight_ref_3_label = ttk.Label(self.canvas_frame, text="WeightRef组数:",
                                       font=("SimHei", 12), style="Tab2_SubTab1.TLabel")
        weight_ref_3_label.grid(row=1, column=9, padx=1, pady=5, sticky="w")

        self.count_weight_ref_3_text = tk.Text(self.canvas_frame, height=1, width=17, font=("SimHei", 12))
        self.count_weight_ref_3_text.grid(row=1, column=10, padx=1, pady=10, sticky="w")

        self.plot_frame3 = tk.Frame(self.canvas_frame, bg="white", width=220, height=200,
                                    takefocus=False, borderwidth=1, relief="solid")
        self.plot_frame3.grid(row=2, column=9, columnspan=2, padx=5, pady=20, sticky="ns")

        # 在第6列和第8列之间创建一个分割线（模拟）---------------------------------------------------------------------------
        separator = ttk.Separator(self.canvas_frame, orient="vertical")
        separator.grid(row=0, column=11, rowspan=4, sticky="ns", padx=5)

        # 创建标签 ------------------------------------------------------------------------------------------------------
        status4_label = ttk.Label(self.canvas_frame, text="Status[4]:",
                                  font=("SimHei", 12), style="Tab2_SubTab1.TLabel")
        status4_label.grid(row=0, column=12, padx=1, pady=10, sticky="w")

        # 创建一个Text组件
        status4_description_text = tk.Text(self.canvas_frame, height=3, width=17, font=("SimHei", 12))
        status4_description_text.grid(row=0, column=13, padx=1, pady=10, sticky="w")
        status4_description_text.insert("1.0", "      Clean Photo\nEmpty   1     0\nFull    1     0")  # 将值插入到文本框中
        status4_description_text["state"] = "disabled"

        weight_ref_4_label = ttk.Label(self.canvas_frame, text="WeightRef组数:",
                                       font=("SimHei", 12), style="Tab2_SubTab1.TLabel")
        weight_ref_4_label.grid(row=1, column=12, padx=1, pady=5, sticky="w")

        self.count_weight_ref_4_text = tk.Text(self.canvas_frame, height=1, width=17, font=("SimHei", 12))
        self.count_weight_ref_4_text.grid(row=1, column=13, padx=1, pady=10, sticky="w")

        self.plot_frame4 = tk.Frame(self.canvas_frame, bg="white", width=220, height=200,
                                    takefocus=False, borderwidth=1, relief="solid")
        self.plot_frame4.grid(row=2, column=12, columnspan=2, padx=5, pady=20, sticky="ns")

        # 在第6列和第8列之间创建一个分割线（模拟）---------------------------------------------------------------------------
        separator = ttk.Separator(self.canvas_frame, orient="vertical")
        separator.grid(row=0, column=14, rowspan=4, sticky="ns", padx=5)

        # 创建标签 ------------------------------------------------------------------------------------------------------
        status5_label = ttk.Label(self.canvas_frame, text="Status[5]:",
                                  font=("SimHei", 12), style="Tab2_SubTab1.TLabel")
        status5_label.grid(row=0, column=15, padx=1, pady=10, sticky="w")

        # 创建一个Text组件
        status5_description_text = tk.Text(self.canvas_frame, height=3, width=17, font=("SimHei", 12))
        status5_description_text.grid(row=0, column=16, padx=1, pady=10, sticky="w")
        status5_description_text.insert("1.0", "      Clean Photo\nEmpty   1     1\nFull    1     1")  # 将值插入到文本框中
        status5_description_text["state"] = "disabled"

        weight_ref_5_label = ttk.Label(self.canvas_frame, text="WeightRef组数:",
                                       font=("SimHei", 12), style="Tab2_SubTab1.TLabel")
        weight_ref_5_label.grid(row=1, column=15, padx=1, pady=5, sticky="w")

        self.count_weight_ref_5_text = tk.Text(self.canvas_frame, height=1, width=17, font=("SimHei", 12))
        self.count_weight_ref_5_text.grid(row=1, column=16, padx=1, pady=10, sticky="w")

        self.plot_frame5 = tk.Frame(self.canvas_frame, bg="white", width=220, height=200,
                                    takefocus=False, borderwidth=1, relief="solid")
        self.plot_frame5.grid(row=2, column=15, columnspan=2, padx=5, pady=20, sticky="ns")

    # ==================================================================================================================
    def update_content(self, df, controller_serial_number):
        # 更新InnerTab1的内容
        self.df = df
        self.table_name = controller_serial_number

        self.clear_frame()

        options0 = self.get_weight_ref_options(status=0)
        options1 = self.get_weight_ref_options(status=1)
        options2 = self.get_weight_ref_options(status=2)
        options3 = self.get_weight_ref_options(status=3)
        options4 = self.get_weight_ref_options(status=4)
        options5 = self.get_weight_ref_options(status=5)

        self.count_weight_ref_0_text["state"] = "normal"
        self.count_weight_ref_1_text["state"] = "normal"
        self.count_weight_ref_2_text["state"] = "normal"
        self.count_weight_ref_3_text["state"] = "normal"
        self.count_weight_ref_4_text["state"] = "normal"
        self.count_weight_ref_5_text["state"] = "normal"

        self.count_weight_ref_0_text.delete("1.0", "end")               # 清除文本框中的值
        self.count_weight_ref_1_text.delete("1.0", "end")               # 清除文本框中的值
        self.count_weight_ref_2_text.delete("1.0", "end")               # 清除文本框中的值
        self.count_weight_ref_3_text.delete("1.0", "end")               # 清除文本框中的值
        self.count_weight_ref_4_text.delete("1.0", "end")               # 清除文本框中的值
        self.count_weight_ref_5_text.delete("1.0", "end")               # 清除文本框中的值

        self.count_weight_ref_0_text.insert("1.0", str(len(options0)))  # 将值插入到文本框中
        self.count_weight_ref_1_text.insert("1.0", str(len(options1)))  # 将值插入到文本框中
        self.count_weight_ref_2_text.insert("1.0", str(len(options2)))  # 将值插入到文本框中
        self.count_weight_ref_3_text.insert("1.0", str(len(options3)))  # 将值插入到文本框中
        self.count_weight_ref_4_text.insert("1.0", str(len(options4)))  # 将值插入到文本框中
        self.count_weight_ref_5_text.insert("1.0", str(len(options5)))  # 将值插入到文本框中

        self.count_weight_ref_0_text["state"] = "disabled"
        self.count_weight_ref_1_text["state"] = "disabled"
        self.count_weight_ref_2_text["state"] = "disabled"
        self.count_weight_ref_3_text["state"] = "disabled"
        self.count_weight_ref_4_text["state"] = "disabled"
        self.count_weight_ref_5_text["state"] = "disabled"

        self.create_options0(options=options0)
        self.create_options1(options=options1)
        self.create_options2(options=options2)
        self.create_options3(options=options3)
        self.create_options4(options=options4)
        self.create_options5(options=options5)

    # 清空图表框 ========================================================================================================
    def clear_frame(self):
        self.plot_frame0.destroy()
        self.plot_frame0 = tk.Frame(self.canvas_frame, width=220, height=200,
                                    takefocus=False, borderwidth=1, relief="solid")
        self.plot_frame0.grid(row=2, column=0, columnspan=2, padx=5, pady=20, sticky="ns")

        self.plot_frame1.destroy()
        self.plot_frame1 = tk.Frame(self.canvas_frame, width=220, height=200,
                                    takefocus=False, borderwidth=1, relief="solid")
        self.plot_frame1.grid(row=2, column=3, columnspan=2, padx=5, pady=20, sticky="ns")

        self.plot_frame2.destroy()
        self.plot_frame2 = tk.Frame(self.canvas_frame, width=220, height=200,
                                    takefocus=False, borderwidth=1, relief="solid")
        self.plot_frame2.grid(row=2, column=6, columnspan=2, padx=5, pady=20, sticky="ns")

        self.plot_frame3.destroy()
        self.plot_frame3 = tk.Frame(self.canvas_frame, width=220, height=200,
                                    takefocus=False, borderwidth=1, relief="solid")
        self.plot_frame3.grid(row=2, column=9, columnspan=2, padx=5, pady=20, sticky="ns")

        self.plot_frame4.destroy()
        self.plot_frame4 = tk.Frame(self.canvas_frame, width=220, height=200,
                                    takefocus=False, borderwidth=1, relief="solid")
        self.plot_frame4.grid(row=2, column=12, columnspan=2, padx=5, pady=20, sticky="ns")

        self.plot_frame5.destroy()
        self.plot_frame5 = tk.Frame(self.canvas_frame, width=220, height=200,
                                    takefocus=False, borderwidth=1, relief="solid")
        self.plot_frame5.grid(row=2, column=15, columnspan=2, padx=5, pady=20, sticky="ns")

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
    def create_options0(self, options):
        # 创建Canvas控件 ------------------------------------------------------------------------------------------------
        canvas0 = tk.Canvas(master=self.plot_frame0, bg="white", width=200, height=200, takefocus=False)
        canvas0.grid(row=0, column=0, sticky="nsew")

        # 创建垂直滚动条 -------------------------------------------------------------------------------------------------
        scrollbar0 = ttk.Scrollbar(self.plot_frame0, orient="vertical", command=canvas0.yview)
        scrollbar0.grid(row=0, column=1, sticky="ns")
        canvas0.configure(yscrollcommand=scrollbar0.set)

        # 创建Canvas内部Frame -------------------------------------------------------------------------------------------
        canvas0_frame = ttk.Frame(canvas0, takefocus=False, style="Tab2_SubTab1.TFrame")
        canvas0.create_window((0, 0), window=canvas0_frame, anchor="nw")

        for row, option in enumerate(options):
            var = tk.IntVar(value=0)
            self.checkbox_vars0[option] = var
            checkbutton = ttk.Checkbutton(canvas0_frame, text=option, variable=var, style="Tab2_SubTab1.TCheckbutton")
            checkbutton.grid(row=row, column=0, sticky="w")

        canvas0_frame.bind("<Configure>", lambda event: canvas0.configure(scrollregion=canvas0.bbox("all")))

    # ==================================================================================================================
    def create_options1(self, options):
        # 创建Canvas控件 ------------------------------------------------------------------------------------------------
        canvas1 = tk.Canvas(master=self.plot_frame1, bg="white", width=200, height=200, takefocus=False)
        canvas1.grid(row=0, column=0, sticky="nsew")

        # 创建垂直滚动条 -------------------------------------------------------------------------------------------------
        scrollbar1 = ttk.Scrollbar(self.plot_frame1, orient="vertical", command=canvas1.yview)
        scrollbar1.grid(row=0, column=1, sticky="ns")
        canvas1.configure(yscrollcommand=scrollbar1.set)

        # 创建Canvas内部Frame -------------------------------------------------------------------------------------------
        canvas1_frame = ttk.Frame(canvas1, takefocus=False, style="Tab2_SubTab1.TFrame")
        canvas1.create_window((0, 0), window=canvas1_frame, anchor="nw")

        for row, option in enumerate(options):
            var = tk.IntVar(value=0)
            self.checkbox_vars1[option] = var
            checkbutton = ttk.Checkbutton(canvas1_frame, text=option, variable=var, style="Tab2_SubTab1.TCheckbutton")
            checkbutton.grid(row=row, column=0, sticky="w")

        canvas1_frame.bind("<Configure>", lambda event: canvas1.configure(scrollregion=canvas1.bbox("all")))

    # ==================================================================================================================
    def create_options2(self, options):
        # 创建Canvas控件 ------------------------------------------------------------------------------------------------
        canvas2 = tk.Canvas(master=self.plot_frame2, bg="white", width=200, height=200, takefocus=False)
        canvas2.grid(row=0, column=0, sticky="nsew")

        # 创建垂直滚动条 -------------------------------------------------------------------------------------------------
        scrollbar2 = ttk.Scrollbar(self.plot_frame2, orient="vertical", command=canvas2.yview)
        scrollbar2.grid(row=0, column=1, sticky="ns")
        canvas2.configure(yscrollcommand=scrollbar2.set)

        # 创建Canvas内部Frame -------------------------------------------------------------------------------------------
        canvas2_frame = ttk.Frame(canvas2, takefocus=False, style="Tab2_SubTab1.TFrame")
        canvas2.create_window((0, 0), window=canvas2_frame, anchor="nw")

        for row, option in enumerate(options):
            var = tk.IntVar(value=0)
            self.checkbox_vars2[option] = var
            checkbutton = ttk.Checkbutton(canvas2_frame, text=option, variable=var, style="Tab2_SubTab1.TCheckbutton")
            checkbutton.grid(row=row, column=0, sticky="w")

        canvas2_frame.bind("<Configure>", lambda event: canvas2.configure(scrollregion=canvas2.bbox("all")))

    # ==================================================================================================================
    def create_options3(self, options):
        # 创建Canvas控件 ------------------------------------------------------------------------------------------------
        canvas3 = tk.Canvas(master=self.plot_frame3, bg="white", width=200, height=200, takefocus=False)
        canvas3.grid(row=0, column=0, sticky="nsew")

        # 创建垂直滚动条 -------------------------------------------------------------------------------------------------
        scrollbar3 = ttk.Scrollbar(self.plot_frame3, orient="vertical", command=canvas3.yview)
        scrollbar3.grid(row=0, column=1, sticky="ns")
        canvas3.configure(yscrollcommand=scrollbar3.set)

        # 创建Canvas内部Frame -------------------------------------------------------------------------------------------
        canvas3_frame = ttk.Frame(canvas3, takefocus=False, style="Tab2_SubTab1.TFrame")
        canvas3.create_window((0, 0), window=canvas3_frame, anchor="nw")

        for row, option in enumerate(options):
            var = tk.IntVar(value=0)
            self.checkbox_vars3[option] = var
            checkbutton = ttk.Checkbutton(canvas3_frame, text=option, variable=var, style="Tab2_SubTab1.TCheckbutton")
            checkbutton.grid(row=row, column=0, sticky="w")

        canvas3_frame.bind("<Configure>", lambda event: canvas3.configure(scrollregion=canvas3.bbox("all")))

    # ==================================================================================================================
    def create_options4(self, options):
        # 创建Canvas控件 ------------------------------------------------------------------------------------------------
        canvas4 = tk.Canvas(master=self.plot_frame4, bg="white", width=200, height=200, takefocus=False)
        canvas4.grid(row=0, column=0, sticky="nsew")

        # 创建垂直滚动条 -------------------------------------------------------------------------------------------------
        scrollbar4 = ttk.Scrollbar(self.plot_frame4, orient="vertical", command=canvas4.yview)
        scrollbar4.grid(row=0, column=1, sticky="ns")
        canvas4.configure(yscrollcommand=scrollbar4.set)

        # 创建Canvas内部Frame -------------------------------------------------------------------------------------------
        canvas4_frame = ttk.Frame(canvas4, takefocus=False, style="Tab2_SubTab1.TFrame")
        canvas4.create_window((0, 0), window=canvas4_frame, anchor="nw")

        for row, option in enumerate(options):
            var = tk.IntVar(value=0)
            self.checkbox_vars4[option] = var
            checkbutton = ttk.Checkbutton(canvas4_frame, text=option, variable=var, style="Tab2_SubTab1.TCheckbutton")
            checkbutton.grid(row=row, column=0, sticky="w")

        canvas4_frame.bind("<Configure>", lambda event: canvas4.configure(scrollregion=canvas4.bbox("all")))

    # ==================================================================================================================
    def create_options5(self, options):
        # 创建Canvas控件 ------------------------------------------------------------------------------------------------
        canvas5 = tk.Canvas(master=self.plot_frame5, bg="white", width=200, height=200, takefocus=False)
        canvas5.grid(row=0, column=0, sticky="nsew")

        # 创建垂直滚动条 -------------------------------------------------------------------------------------------------
        scrollbar5 = ttk.Scrollbar(self.plot_frame5, orient="vertical", command=canvas5.yview)
        scrollbar5.grid(row=0, column=1, sticky="ns")
        canvas5.configure(yscrollcommand=scrollbar5.set)

        # 创建Canvas内部Frame -------------------------------------------------------------------------------------------
        canvas5_frame = ttk.Frame(canvas5, takefocus=False, style="Tab2_SubTab1.TFrame")
        canvas5.create_window((0, 0), window=canvas5_frame, anchor="nw")

        for row, option in enumerate(options):
            var = tk.IntVar(value=0)
            self.checkbox_vars5[option] = var
            checkbutton = ttk.Checkbutton(canvas5_frame, text=option, variable=var, style="Tab2_SubTab1.TCheckbutton")
            checkbutton.grid(row=row, column=0, sticky="w")

        canvas5_frame.bind("<Configure>", lambda event: canvas5.configure(scrollregion=canvas5.bbox("all")))

    # ==================================================================================================================
    def generate_calibration(self):
        selected_options0 = [option for option, var in self.checkbox_vars0.items() if var.get() == 1]
        selected_options1 = [option for option, var in self.checkbox_vars1.items() if var.get() == 1]
        selected_options2 = [option for option, var in self.checkbox_vars2.items() if var.get() == 1]
        selected_options3 = [option for option, var in self.checkbox_vars3.items() if var.get() == 1]
        selected_options4 = [option for option, var in self.checkbox_vars4.items() if var.get() == 1]
        selected_options5 = [option for option, var in self.checkbox_vars5.items() if var.get() == 1]

        if selected_options0 == [] and selected_options1 == [] and selected_options2 == [] and \
                selected_options3 == [] and selected_options4 == [] and selected_options5 == []:
            messagebox.showinfo("提示", "请至少选择一组重量")  # 弹窗告知用户未储存标定数据

        else:
            df_cali = pd.DataFrame()

            status = 0
            # 遍历选项列表
            for selected_options in [selected_options0, selected_options1, selected_options2,
                                     selected_options3, selected_options4, selected_options5]:

                for selected_option in selected_options:
                    selected_values = [float(val) for val in selected_option.strip("()").split(", ")]
                    # 在DataFrame中进行筛选
                    df_row = self.df[
                        (self.df["WeighStatus"] == status) &
                        (self.df["WeightRef1"] == selected_values[0]) &
                        (self.df["WeightRef2"] == selected_values[1]) &
                        (self.df["WeightRef3"] == selected_values[2])
                        ]
                    df_cali = pd.concat([df_cali, df_row], axis=0)
                    df_cali.reset_index(drop=True, inplace=True)
                status += 1

            print(df_cali)
            from Tab2_SubTab1_GenerateCSV import gen_calibration_data
            gen_calibration_data(df=df_cali, table_name=self.table_name)
