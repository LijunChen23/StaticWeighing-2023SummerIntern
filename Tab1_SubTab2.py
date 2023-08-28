import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import ttk


class InnerTab2:
    def __init__(self, parent_tab):
        self.inner_tab2 = tk.Frame(parent_tab, bg="whitesmoke")

        self.plot_frame = None
        self.weigh_pos_dropdown = None
        self.pos_weight_mapping = {
            "称重位置1": "WeighRelative1",
            "称重位置2": "WeighRelative2",
            "称重位置3": "WeighRelative3"
                                   }
        self.table_name = None
        self.filtered_df = None

        self.create_widgets()

    # ==================================================================================================================
    def create_widgets(self):
        style = ttk.Style()
        style.configure("Sub_tab.TLabel", background="whitesmoke")
        style.configure("Sub_tab.TButton", font=("SimHei", 12), padding=(10, 20))

        # 创建一个框用于展示散点图 -----------------------------------------------------------------------------------------
        self.plot_frame = tk.Frame(self.inner_tab2, bg="white", width=900, height=400)
        self.plot_frame.grid(row=1, column=0, columnspan=2, padx=40, pady=20, sticky="ns")

        # 创建”称重位置“标签 ----------------------------------------------------------------------------------------------
        weigh_pos_label = ttk.Label(self.inner_tab2, text="称重位置：", font=("SimHei", 12), style="Sub_tab.TLabel")
        weigh_pos_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")

        # 创建”称重位置“下拉列表框
        self.weigh_pos_dropdown = ttk.Combobox(self.inner_tab2, values=list(self.pos_weight_mapping.keys()),
                                               state="readonly", font=("SimHei", 12))
        self.weigh_pos_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.weigh_pos_dropdown.bind("<<ComboboxSelected>>", self.generate_data)

        # 辅助排版 ------------------------------------------------------------------------------------------------------
        self.inner_tab2.grid_rowconfigure(0, weight=1)  # Empty row at the top
        self.inner_tab2.grid_rowconfigure(3, weight=1)  # Empty row at the end
        self.inner_tab2.grid_columnconfigure(0, weight=1)
        self.inner_tab2.grid_columnconfigure(1, weight=1)

    # 更新InnerTab2的内容 ================================================================================================
    def update_content(self, df, controller_serial_number):
        self.table_name = controller_serial_number
        self.filtered_df = df[(df["WeighRef1"] == 0) & (df["WeighRef2"] == 0) & (df["WeighRef3"] == 0)]
        self.clear_plot()
        self.weigh_pos_dropdown.set("")

    # 生成”称重次数vs相对重量“的散点图 ======================================================================================
    def generate_data(self, event):
        selected_option = self.weigh_pos_dropdown.get()            # 获取选择的选项
        selected_value = self.pos_weight_mapping[selected_option]  # 获取对应的值

        self.clear_plot()  # 清空图表框，以用于显示表格

        # 读取 "WeighRelative1"、"WeighRelative2" 和 "WeighRelative3" 列的值，并存入对应的列表中
        weigh_relative_list = self.filtered_df[selected_value].tolist()

        # 创建称重次数列表
        count_list = list(range(1, len(weigh_relative_list) + 1))

        plt.rcParams["font.sans-serif"] = "SimHei"  # 设置字体为简体中文黑体
        plt.rcParams["axes.unicode_minus"] = False  # 解决负号无法正常显示的问题
        # 绘制散点图
        plt.figure(figsize=(9, 4))
        plt.scatter(count_list, weigh_relative_list)
        plt.xlabel("称重次数")
        plt.ylabel("相对重量")
        plt.title("称重次数vs相对重量")
        plt.tight_layout()

        # 创建一个 Tkinter 可以容纳 Matplotlib 图形的画布 (canvas)
        canvas = FigureCanvasTkAgg(plt.gcf(), master=self.plot_frame)  # plt.gcf() 返回当前的 Matplotlib 图形对象
        canvas.get_tk_widget().configure(width=900, height=345)        # 设置画布大小
        canvas.draw()                                                  # 调用画布的 draw 方法，以绘制图形。
        # 添加导航工具栏
        toolbar_frame = tk.Frame(master=self.plot_frame, bg="white")
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()
        toolbar.configure(background="white")  # 设置工具栏背景颜色为白色
        # 将canvas和滚动条放置在GUI中
        canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        toolbar_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

    # 清空图表框 ========================================================================================================
    def clear_plot(self):
        plt.close('all')  # 关闭所有之前的图形
        plt.clf()         # 清除之前绘图
        self.plot_frame.destroy()
        self.plot_frame = tk.Frame(self.inner_tab2, bg="white", width=900, height=400)
        self.plot_frame.grid(row=1, column=0, columnspan=2, padx=40, pady=20, sticky="ns")
