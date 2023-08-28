import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog, ttk


class InnerTab1:
    def __init__(self, parent_tab):
        self.inner_tab1 = tk.Frame(parent_tab, bg="whitesmoke")

        self.db_listbox = None
        self.choose_db_button = None
        self.clear_db_button = None
        self.update_db_button = None
        self.weigh_status_dropdown = None
        self.status_description_text = None
        self.weigh_ref_dropdown = None
        self.result_dropdown = None
        self.plot_frame = None
        self.df = None
        self.table_name = None
        self.condition_status0 = None
        self.condition_status3 = None
        self.df_status_filtered = None
        self.status_description_mapping = {
            "Status[0]": "Empty: Clean 0, Photo 0\nFull:  Clean 0, Photo 0",
            "Status[1]": "Empty: Clean 0, Photo 0\nFull:  Clean 1, Photo 0",
            "Status[2]": "Empty: Clean 0, Photo 1\nFull:  Clean 0, Photo 1",
            "Status[3]": "Empty: Clean 0, Photo 1\nFull:  Clean 1, Photo 1",
            "Status[4]": "Empty: Clean 1, Photo 0\nFull:  Clean 1, Photo 0",
            "Status[5]": "Empty: Clean 1, Photo 1\nFull:  Clean 1, Photo 1"
        }
        self.weigh_ref_lists = None
        self.df_ref_filtered = None

        self.create_widgets()

    # ==================================================================================================================
    def create_widgets(self):
        # Create a custom style for the button
        style = ttk.Style()
        style.configure("Sub_tab.TLabel", background="whitesmoke")
        style.configure("Sub_tab.TButton", font=("SimHei", 12), padding=(10, 20))

        # 创建”标定数据库“标签 --------------------------------------------------------------------------------------------
        db_label = ttk.Label(self.inner_tab1, text="标定数据库：", font=("SimHei", 12), style="Sub_tab.TLabel")
        db_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # 创建”标定数据库“列表框
        self.db_listbox = tk.Listbox(self.inner_tab1, width=40, height=2, font=("SimHei", 12))
        self.db_listbox.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        # 创建“选择数据库”按钮 --------------------------------------------------------------------------------------------
        self.choose_db_button = ttk.Button(self.inner_tab1, text="选择数据库", command=self.choose_database,
                                           width=10, style="Sub_tab.TButton")
        self.choose_db_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # 创建“清空”按钮
        self.clear_db_button = ttk.Button(self.inner_tab1, text="清空", command=self.clear_db_list,
                                          width=10, style="Sub_tab.TButton", state="disabled")
        self.clear_db_button.grid(row=0, column=4, padx=5, pady=5, sticky="ew")

        # 创建“更新数据库”按钮
        self.update_db_button = ttk.Button(self.inner_tab1, text="更新数据库", command=self.update_database,
                                           width=10, style="Sub_tab.TButton", state="disabled")
        self.update_db_button.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

        # 创建”称重状态“标签 ---------------------------------------------------------------------------------------------
        weigh_status_label = ttk.Label(self.inner_tab1, text="称重状态：", font=("SimHei", 12), style="Sub_tab.TLabel")
        weigh_status_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # 创建”称重状态“下拉列表框
        self.weigh_status_dropdown = ttk.Combobox(self.inner_tab1, values=[],
                                                  height=2, state="disabled", font=("SimHei", 12))
        self.weigh_status_dropdown.grid(row=1, column=1, padx=5, pady=20, sticky="w")
        self.weigh_status_dropdown.bind("<<ComboboxSelected>>", self.show_weigh_status)

        # 创建”称重状态描述“标签 ------------------------------------------------------------------------------------------
        status_description_label = ttk.Label(self.inner_tab1, text="称重状态描述:",
                                             font=("SimHei", 12), style="Sub_tab.TLabel")
        status_description_label.grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky="w")

        # 创建描述称重状态的文本框
        self.status_description_text = tk.Text(self.inner_tab1, height=2, width=25, font=("SimHei", 12))
        self.status_description_text.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky="ew")
        self.status_description_text["state"] = "disabled"

        # 创建”真实重量“标签 ---------------------------------------------------------------------------------------------
        weigh_ref_label = ttk.Label(self.inner_tab1, text="真实重量：", font=("SimHei", 12), style="Sub_tab.TLabel")
        weigh_ref_label.grid(row=5, column=0, padx=5, pady=10, sticky="w")

        # 创建”真实重量“下拉列表框
        self.weigh_ref_dropdown = ttk.Combobox(self.inner_tab1, values=[], height=2,
                                               font=("SimHei", 12), state="disabled")
        self.weigh_ref_dropdown.grid(row=5, column=1, padx=5, pady=10, sticky="w")
        self.weigh_ref_dropdown.bind("<<ComboboxSelected>>", self.show_weigh_ref)

        # 创建”结果类型“标签 ---------------------------------------------------------------------------------------------
        result_label = ttk.Label(self.inner_tab1, text="结果类型：", font=("SimHei", 12), style="Sub_tab.TLabel")
        result_label.grid(row=6, column=0, padx=5, pady=10, sticky="w")

        # 创建第四个下拉列表框，用于选择要查看的生成的表格
        self.result_dropdown = ttk.Combobox(self.inner_tab1, values=["中位值", "平均值", "称重偏差", "温度拟合"],
                                            font=("SimHei", 12), state="disabled")
        self.result_dropdown.grid(row=6, column=1, padx=5, pady=10, sticky="w")
        self.result_dropdown.bind("<<ComboboxSelected>>", self.show_result)

        # 创建一个框用于展示折线图 -----------------------------------------------------------------------------------------
        self.plot_frame = tk.Frame(self.inner_tab1, bg="white", width=730, height=400)
        self.plot_frame.grid(row=1, column=2, rowspan=6, columnspan=4, padx=5, pady=5, sticky="w")

        # 辅助排版 ------------------------------------------------------------------------------------------------------
        self.inner_tab1.grid_rowconfigure(4, weight=1)
        self.inner_tab1.grid_rowconfigure(5, weight=1)
        self.inner_tab1.grid_rowconfigure(6, weight=1)
        self.inner_tab1.grid_columnconfigure(2, weight=1)

    # ==================================================================================================================
    def update_content(self, df, controller_serial_number):
        # 更新InnerTab1的内容
        self.df = df
        self.table_name = controller_serial_number
        self.condition_status0 = (self.df["WeighEmptyStatus(0)"] == True) & \
                                 (self.df["WeighEmptyStatus(1)"] == False) & \
                                 (self.df["WeighEmptyStatus(2)"] == False) & \
                                 (self.df["WeighEmptyStatus(3)"] == True) & \
                                 (self.df["WeighEmptyStatus(4)"] == True) & \
                                 (self.df["WeighFullStatus(0)"] == True) & \
                                 (self.df["WeighFullStatus(1)"] == False) & \
                                 (self.df["WeighFullStatus(2)"] == False) & \
                                 (self.df["WeighFullStatus(3)"] == True) & \
                                 (self.df["WeighFullStatus(4)"] == True)

        self.condition_status3 = (self.df["WeighEmptyStatus(0)"] == True) & \
                                 (self.df["WeighEmptyStatus(1)"] == False) & \
                                 (self.df["WeighEmptyStatus(2)"] == True) & \
                                 (self.df["WeighEmptyStatus(3)"] == False) & \
                                 (self.df["WeighEmptyStatus(4)"] == True) & \
                                 (self.df["WeighFullStatus(0)"] == True) & \
                                 (self.df["WeighFullStatus(1)"] == False) & \
                                 (self.df["WeighFullStatus(2)"] == True) & \
                                 (self.df["WeighFullStatus(3)"] == False) & \
                                 (self.df["WeighFullStatus(4)"] == True)

        list_weigh_status = []
        # 检查是否满足 condition_status0 或 condition_status3 中的任意一个条件
        if any([self.condition_status0.any()]):
            list_weigh_status.append(0)
        if any([self.condition_status3.any()]):
            list_weigh_status.append(3)
        print(list_weigh_status)

        self.weigh_status_dropdown.set("")
        self.weigh_status_dropdown.config(values=[f"Status[{item}]" for item in list_weigh_status], state="readonly")
        self.status_description_text["state"] = "normal"
        self.status_description_text.delete("1.0", "end")  # 清除文本框内容
        self.status_description_text["state"] = "disabled"
        self.weigh_ref_dropdown.set("")
        self.weigh_ref_dropdown.config(state="disabled")
        self.result_dropdown.set("")
        self.result_dropdown.config(state="disabled")
        self.clear_plot()

    # ==================================================================================================================
    def choose_database(self):
        db_path = filedialog.askopenfilename(filetypes=[("Access files", "*.accdb")])
        if db_path:
            self.db_listbox.insert(tk.END, db_path)
            self.choose_db_button.config(state="disabled")
            self.clear_db_button.config(state="normal")
            self.update_db_button.config(state="normal")

    # “清空”按钮的事件处理函数 ============================================================================================
    def clear_db_list(self):
        self.db_listbox.delete(0, tk.END)
        self.choose_db_button.config(state="normal")
        self.clear_db_button.config(state="disabled")
        self.update_db_button.config(state="disabled")

    # “更新数据库”按钮的事件处理函数，读取称重数据库，获取日期信息以及数据量信息 ==================================================
    def update_database(self):
        db_file_path = self.db_listbox.get(0)
        # 以下代码返回数据库中的表格的dataframe
        from Tab1_SubTab1_SaveToDatabase import save
        save(df=self.df, db_file_path=db_file_path, table_name=self.table_name)

    # 根据下拉列表框中的选项，生成相应的折线图，放在图表框中 ===================================================================
    def show_weigh_status(self, event):
        selected_option = self.weigh_status_dropdown.get()  # 获取用户选择的选项
        if selected_option == "Status[0]":
            self.df_status_filtered = self.df[self.condition_status0]
        if selected_option == "Status[3]":
            self.df_status_filtered = self.df[self.condition_status3]

        list_weigh_ref1 = self.df_status_filtered["WeighRef1"].unique().tolist()  # 读取WeighRef有几组值
        list_weigh_ref1 = [x for x in list_weigh_ref1 if x != 0]                  # 筛选掉值为0的元素
        list_weigh_ref2 = self.df_status_filtered["WeighRef2"].unique().tolist()  # 读取WeighRef有几组值
        list_weigh_ref2 = [x for x in list_weigh_ref2 if x != 0]                  # 筛选掉值为0的元素
        list_weigh_ref3 = self.df_status_filtered["WeighRef3"].unique().tolist()  # 读取WeighRef有几组值
        list_weigh_ref3 = [x for x in list_weigh_ref3 if x != 0]                  # 筛选掉值为0的元素
        # 重新排列三个列表，并生成新的列表
        self.weigh_ref_lists = [group for group in zip(list_weigh_ref1, list_weigh_ref2, list_weigh_ref3)]
        # 将重新排列后的列表作为下拉列表框的选项值

        self.status_description_text["state"] = "normal"
        self.status_description_text.delete("1.0", "end")  # 清除文本框内容
        self.status_description_text.insert("1.0", self.status_description_mapping[selected_option])  # 将值插入到文本框中
        self.status_description_text["state"] = "disabled"
        self.weigh_ref_dropdown.set("")
        self.weigh_ref_dropdown.config(values=[str(item) for item in self.weigh_ref_lists], state="readonly")
        self.result_dropdown.set("")
        self.result_dropdown.config(state="disabled")
        self.clear_plot()

    # 根据下拉列表框中的选项，生成相应的折线图，放在图表框中 ===================================================================
    def show_weigh_ref(self, event):
        selected_option = self.weigh_ref_dropdown.get()  # 获取用户选择的选项
        for item in self.weigh_ref_lists:
            if str(item) == selected_option:
                weigh_ref1 = item[0]
                weigh_ref2 = item[1]
                weigh_ref3 = item[2]
                self.df_ref_filtered = self.df_status_filtered[
                    (self.df_status_filtered["WeighRef1"] == weigh_ref1) &
                    (self.df_status_filtered["WeighRef2"] == weigh_ref2) &
                    (self.df_status_filtered["WeighRef3"] == weigh_ref3)
                ]

        # print(self.df_ref_filtered)
        self.result_dropdown.set("")
        self.result_dropdown.config(state="readonly")
        self.clear_plot()

    # 根据选择的数据库表格和生成的结果表格，显示相应的表格数据 =================================================================
    def show_result(self, event):
        selected_option = self.result_dropdown.get()  # 获取选择的生成的结果表格

        from Tab1_SubTab1_ProcessResult import process_data
        df_result = process_data(self.df_ref_filtered, selected_option)

        """销毁之前的Frame，创建新的Frame"""
        self.clear_plot()

        # 如果选择的是“称重偏差” ------------------------------------------------------------------------------------------
        if selected_option == "称重偏差":

            def get_color(value):
                if 0 <= value <= 0.2:
                    return "mediumseagreen"
                elif 0.2 < value <= 0.4:
                    return "khaki"
                else:
                    return "salmon"

            color_df = df_result[["称重位置1(g)", "称重位置2(g)", "称重位置3(g)"]].applymap(get_color)
            color_df["小车ID"] = "white"       # 将"小车ID"这一列的颜色设置为白色
            color_df["小车平均(g)"] = "white"  # 将"小车平均(g)"这一列的颜色设置为白色
            color_df.loc[0] = "white"         # 将第[0]行颜色设置为白色
            column_name_list = ["小车ID", "称重位置1(g)", "称重位置2(g)", "称重位置3(g)", "小车平均(g)"]
            color_df = color_df[column_name_list].reset_index(drop=True)

            plt.rcParams["font.sans-serif"] = "SimHei"  # 设置字体为简体中文黑体
            fig = plt.figure(figsize=(6, 4))
            ax = fig.add_subplot(111, frameon=False, xticks=[], yticks=[])

            table = plt.table(cellText=df_result.values, cellColours=color_df.values,
                              colLabels=df_result.columns, loc="center", cellLoc="center")

            col_widths = [0.09, 0.12, 0.12, 0.12, 0.12]  # 设置每列的宽度比例
            for i, width in enumerate(col_widths):
                table.auto_set_column_width([i])
                cell = table.get_celld()[(0, i)]
                cell.set_width(width)

            table.auto_set_font_size(True)
            plt.tight_layout()

            # 创建一个 Tkinter 可以容纳 Matplotlib 图形的画布（canvas）。
            # plt.gcf() 返回当前的 Matplotlib 图形对象，master=self.plot_frame 则指定了画布的父容器，即创建的 GUI 中用于显示图形的框。
            canvas = FigureCanvasTkAgg(plt.gcf(), master=self.plot_frame)
            # canvas.draw() 调用画布的 draw 方法，以绘制图形。
            canvas.draw()
            # 获取画布的 Tkinter 控件（widget）并将其使用 pack 方法放置在 GUI 窗口中。
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.grid(row=0, column=0)
            # 设置图表大小
            canvas_widget.config(width=730, height=400)

        # 如果选择的是“平均值”或“中位值” -----------------------------------------------------------------------------------
        elif selected_option == "中位值" or selected_option == "平均值":

            columns = list(df_result.columns)
            data = df_result.values.tolist()

            tree = ttk.Treeview(master=self.plot_frame, columns=columns, show="headings")
            # 设置 treeview 的位置和大小
            tree.place(x=0, y=0, width=730, height=400)
            for col in columns:
                if col == "小车ID":
                    tree.heading(col, text=col)
                    tree.column(col, width=45)
                else:
                    tree.heading(col, text=col)
                    tree.column(col, width=80)
            for item in data:
                tree.insert("", "end", values=item)

        # 如果选择的是“温度拟合” ------------------------------------------------------------------------------------------
        else:

            def plot_subplots(axs, dataframe, shuttle_id_pos, seg_no):
                plt.rcParams["font.sans-serif"] = "SimHei"  # 设置中文字体为黑体
                plt.rc("font", size=7)                      # 设置 Matplotlib 的默认字体大小

                # 根据ShuttleIDPos进行分组
                shuttle_id_groups = dataframe.groupby(f"ShuttleIDPos{shuttle_id_pos}")

                # 循环绘制图表
                for index, (shuttle_id, group) in enumerate(shuttle_id_groups):
                    ax = axs[index, shuttle_id_pos - 1]
                    weigh_empty = group[f"WeighEmptyPos{shuttle_id_pos}"]
                    weigh_full = group[f"WeighFullPos{shuttle_id_pos}"]
                    cpu_temp_empty = group[f"Seg{seg_no}CPUTempEmpty"]
                    cpu_temp_full = group[f"Seg{seg_no}CPUTempFull"]

                    """根据数据点进行拟合"""
                    # np.polyfit 是用于多项式拟合的函数，会返回一个多项式的系数数组，以便用来表示拟合的函数。
                    # np.polyfit 第一项是 x 轴数据，第二项是对应的 y 轴数据，1 表示进行一次线性拟合。
                    # fit_empty, fit_full 数组中存放着拟合的线性函数的系数。
                    # np.poly1d 则是将拟合系数转化为一个多项式对象，这个对象可以用来计算拟合的函数值。
                    fit_empty = np.polyfit(cpu_temp_empty, weigh_empty, 1)
                    fit_fn_empty = np.poly1d(fit_empty)
                    fit_full = np.polyfit(cpu_temp_full, weigh_full, 1)
                    fit_fn_full = np.poly1d(fit_full)
                    # 对于一次线性拟合，fit_empty 中有两个元素，分别代表截距和斜率。
                    # fit_empty[0] 表示拟合线的斜率（即一次项的系数），而 fit_empty[1] 表示拟合线的截距（即常数项的系数）。
                    slope_empty = fit_empty[0]
                    slope_full = fit_full[0]

                    # "bo" 指定了绘制散点的样式，"b" 表示蓝色（blue）的点，"o" 表示使用圆圈样式的点。
                    ax.plot(cpu_temp_empty, weigh_empty, "bo", label="空载数据")
                    # "go" 指定了绘制散点的样式，"g" 表示绿色（green）的点，"o" 表示使用圆圈样式的点。
                    ax.plot(cpu_temp_full, weigh_full, "go", label="满载数据")
                    # fit_fn_empty(cpu_temp_empty) 使用之前计算的拟合函数 fit_fn_full，计算对应 cpu_temp_full 数据点的拟合曲线上的 y 轴值。
                    # "r-" 指定了绘制拟合曲线的样式，"r" 表示红色（red），"-" 表示使用实线。
                    ax.plot(cpu_temp_empty, fit_fn_empty(cpu_temp_empty), "r-",
                            label=f"空载拟合曲线\n斜率: {slope_empty:.3f}")
                    # fit_fn_full(cpu_temp_full) 使用之前计算的拟合函数 fit_fn_full，计算对应 cpu_temp_full 数据点的拟合曲线上的 y 轴值。
                    # "m-" 指定了绘制拟合曲线的样式，"m" 表示洋红色（magenta），"-" 表示使用实线。
                    ax.plot(cpu_temp_full, fit_fn_full(cpu_temp_full), "m-",
                            label=f"满载拟合曲线\n斜率: {slope_full:.3f}")
                    ax.tick_params(axis="x", labelsize=7)                        # 设置刻度标签的字体大小为 7
                    ax.tick_params(axis="y", labelsize=7)                        # 设置刻度标签的字体大小为 7
                    ax.set_xlabel(f"电机{seg_no}温度(\N{DEGREE SIGN}C)", size=7)  # 设置 x 轴标签的字体大小为 7
                    ax.set_ylabel("称重结果(g)", size=7)                          # 设置 y 轴标签的字体大小为 7
                    ax.set_title(f"称重位置{shuttle_id_pos}（小车ID：{int(shuttle_id)}）", size=7)
                    ax.legend()
                    ax.grid(True)

            figure, axis = plt.subplots(nrows=12, ncols=3, figsize=(7, 27))  # 定义画布大小和子图的布局
            plot_subplots(axis, self.df_ref_filtered, 1, 4)                  # 称重位置1，电机4
            plot_subplots(axis, self.df_ref_filtered, 2, 4)                  # 称重位置2，电机4
            plot_subplots(axis, self.df_ref_filtered, 3, 2)                  # 称重位置3，电机2
            plt.tight_layout()                                               # 自动调整子图之间的间距，以及图表的整体布局

            """创建Canvas控件"""
            # 创建了一个 Canvas 控件，放置在 Tkinter Frame 控件中
            canvas = tk.Canvas(master=self.plot_frame, bg="white", width=707, height=397)
            canvas.grid(row=0, column=0, sticky="nsew")

            """创建垂直滚动条"""
            # orient="vertical" 表示垂直方向的滚动条。command=canvas.yview 设置了滚动条与 Canvas 的垂直滚动联动
            scrollbar = ttk.Scrollbar(self.plot_frame, orient="vertical", command=canvas.yview)
            scrollbar.grid(row=0, column=1, sticky="ns")
            # yscrollcommand=scrollbar.set 表示将滚动条的位置信息传递给 Canvas，以便 Canvas 根据滚动条的位置进行垂直滚动。
            canvas.configure(yscrollcommand=scrollbar.set)

            """创建Canvas内部Frame"""
            # 创建了一个内部的 Frame，用于在 Canvas 中放置图表
            inner_frame = ttk.Frame(canvas)
            # 在 Canvas 中创建一个窗口，将内部的 Frame 放置在窗口内，以实现在 Canvas 中滚动 Frame。
            # (0, 0) 指定了窗口的初始位置，即左上角坐标。anchor="nw" 表示使用锚点 "nw"（表示左上角）来定位窗口内的 Frame。
            canvas.create_window((0, 0), window=inner_frame, anchor="nw")

            """将图表绘制于Canvas上"""
            # 这行代码创建了一个FigureCanvasTkAgg对象，用于将Matplotlib图表添加到Tkinter窗口中。
            # master=inner_frame表示将图表添加到之前创建的内部Frame inner_frame中。
            canvas_widget = FigureCanvasTkAgg(figure, master=inner_frame)
            canvas_widget.draw()
            # 这行代码将包含图表的Tkinter控件添加到内部Frame中，以便在Canvas控件中显示图表。
            # .get_tk_widget()获取图表的 Tkinter控件对象。.pack()方法将图表的Tkinter控件添加到内部Frame中，自动调整大小和布局。
            canvas_widget.get_tk_widget().pack(fill=tk.NONE, expand=False)

            """实现滚动效果"""
            # 定义一个事件处理函数 on_configure，它在 Canvas 大小改变时被调用，实现滚动区域的设置
            def on_configure(event):
                # scrollregion 是 Canvas 的属性，它定义了可滚动区域的范围。
                # canvas.bbox("all") 获取了内部 Frame inner_frame 中所有元素的边界框（bounding box）。
                # 这个边界框表示了内部 Frame 中的内容范围，即需要滚动的区域。
                canvas.configure(scrollregion=canvas.bbox("all"))
            # <Configure> 事件表示窗口大小改变事件，当内部 Frame 大小发生变化时，这个事件将被触发。
            inner_frame.bind("<Configure>", on_configure)

    # 清空图表框 ========================================================================================================
    def clear_plot(self):
        plt.close('all')  # 关闭所有之前的图形
        plt.clf()  # 清除之前绘图
        self.plot_frame.destroy()
        self.plot_frame = tk.Frame(self.inner_tab1, bg="white", width=730, height=400)
        self.plot_frame.grid(row=1, column=2, rowspan=6, columnspan=4, padx=5, pady=5, sticky="w")
