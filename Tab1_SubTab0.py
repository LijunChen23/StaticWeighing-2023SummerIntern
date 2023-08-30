import pandas as pd
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class InnerTab0:
    def __init__(self, parent_tab):
        self.inner_tab0 = tk.Frame(parent_tab, bg="whitesmoke")

        self.plot_frame = None
        self.view_data_amount_button = None
        self.df = None
        self.table_name = None

        self.create_widgets()

    # ==================================================================================================================
    def create_widgets(self):
        # Create a custom style for the button
        style = ttk.Style()
        style.configure("Sub_tab.TButton", font=("SimHei", 12), padding=(10, 20))

        # 创建一个框用于展示折线图 ------------------------------------------------------------------------------------------
        self.plot_frame = tk.Frame(self.inner_tab0, bg="white", width=900, height=400)
        self.plot_frame.grid(row=1, column=0, padx=40, pady=20, sticky="ns")

        # 创建“查看数据量”按钮 --------------------------------------------------------------------------------------------
        self.view_data_amount_button = ttk.Button(self.inner_tab0, text="查看数据量", command=self.view_data_amount,
                                                  width=10, style="Sub_tab.TButton", state="normal")
        self.view_data_amount_button.grid(row=2, column=0, padx=40, pady=5, sticky="ns")

        # 辅助排版 ------------------------------------------------------------------------------------------------------
        self.inner_tab0.grid_rowconfigure(0, weight=1)  # Empty row at the top
        self.inner_tab0.grid_rowconfigure(3, weight=1)  # Empty row at the end
        self.inner_tab0.grid_columnconfigure(0, weight=1)

    def update_content(self, df, controller_serial_number):
        # 更新InnerTab0的内容
        self.df = df
        self.table_name = controller_serial_number
        self.clear_plot()  # 清空图表框，以用于绘制新的图

    # “查看数据库”按钮的事件处理函数，读取称重数据库，获取日期信息以及数据量信息 ====================================================
    def view_data_amount(self):
        x, y = process_data(df=self.df)
        self.clear_plot()  # 清空图表框，以用于绘制新的图

        date = x.tolist()         # Convert pandas Index to a list
        data_amount = y.tolist()  # Convert numpy array to a list

        # 避免数据不够而无法生成图
        if date is not None and data_amount is not None:
            plt.rcParams["font.sans-serif"] = "SimHei"  # 设置字体为简体中文黑体
            plt.figure(figsize=(9, 4))
            plt.plot(date, data_amount, marker="o")     # 绘制折线图
            plt.xlabel("日期")
            plt.ylabel("数据量")
            plt.title(f"机器{self.table_name}")
            plt.xticks(rotation=45, fontsize=8)
            plt.yticks(fontsize=8)
            plt.tight_layout()

            canvas = FigureCanvasTkAgg(plt.gcf(), master=self.plot_frame)  # plt.gcf() 返回当前的 Matplotlib 图形对象
            canvas.draw()  # canvas.draw() 调用画布的 draw 方法，以绘制图形。
            # 获取画布的 Tkinter 控件（widget）并将其使用 pack 方法放置在 GUI 窗口中。
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # 清空图表框 =========================================================================================================
    def clear_plot(self):
        plt.close('all')  # 关闭所有之前的图形
        plt.clf()  # 清除之前绘图
        self.plot_frame.destroy()
        self.plot_frame = tk.Frame(self.inner_tab0, bg="white", width=900, height=400)
        self.plot_frame.grid(row=1, column=0, padx=40, pady=20, sticky="ns")


# 处理时间数据并计算每个日期的数据量 ==========================================================================================
def process_data(df):
    timestamp_column = pd.to_datetime(df["TimeStamp"])  # 将数据先转成datetime格式
    # 筛选数据，将没有时间或有错误时间的数据都筛掉
    filtered_timestamps = timestamp_column[(timestamp_column != "") &                     # 未记录时间
                                           (timestamp_column != "1970-01-01 00:00:00") &  # 未记录时间
                                           (timestamp_column.dt.year != 2021)]            # 错误时间
    date_counts = filtered_timestamps.dt.date.value_counts()  # 计算每个日期的数据量
    date_counts = date_counts.sort_index()                    # 按照时间顺序排序
    return date_counts.index, date_counts.values  # index的值就是日期，values的值就是数据量
