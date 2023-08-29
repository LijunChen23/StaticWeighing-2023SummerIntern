import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import ttk


class InnerTab2:
    def __init__(self, parent_tab):
        self.inner_tab2 = tk.Frame(parent_tab, bg="whitesmoke")

        self.plot_frame = None
        self.weigh_pos_checkboxes = []
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

        # 创建多选框列表框
        row = 2
        for pos_label in self.pos_weight_mapping.keys():
            checkbox_var = tk.IntVar()
            checkbox = ttk.Checkbutton(self.inner_tab2, text=pos_label, variable=checkbox_var, onvalue=1, offvalue=0,
                                       command=self.generate_data)
            checkbox.grid(row=row, column=1, padx=5, pady=5, sticky="w")
            #checkbox.bind("<Button-1>", self.generate_data)  # Bind the generate_data method to checkbox click event
            self.weigh_pos_checkboxes.append((pos_label, checkbox_var))
            row += 1

        # 辅助排版 ------------------------------------------------------------------------------------------------------
        self.inner_tab2.grid_rowconfigure(0, weight=1)  # Empty row at the top
        self.inner_tab2.grid_rowconfigure(3, weight=1)  # Empty row at the end
        self.inner_tab2.grid_columnconfigure(0, weight=1)
        self.inner_tab2.grid_columnconfigure(1, weight=1)

    # 更新InnerTab2的内容 ================================================================================================
    def update_content(self, df, controller_serial_number):
        self.table_name = controller_serial_number
        self.filtered_df = df[(df["WeighRef1"] == 0) & (df["WeighRef2"] == 0) & (df["WeighRef3"] == 0)]
        print(self.filtered_df)
        self.clear_plot()
        for _, var in self.weigh_pos_checkboxes:
            var.set(0)

    # 生成”称重次数vs相对重量“的散点图 ======================================================================================
    def generate_data(self):
        selected_values = [pos_label for pos_label, var in self.weigh_pos_checkboxes if var.get() == 1]
        print(selected_values)
        self.clear_plot()

        if selected_values:
            plt.rcParams["font.sans-serif"] = "SimHei"  # 设置字体为简体中文黑体
            plt.rcParams["axes.unicode_minus"] = False  # 解决负号无法正常显示的问题
            plt.figure(figsize=(9, 4))
            '''for selected_value in selected_values:
                weigh_relative_list = self.filtered_df[self.pos_weight_mapping[selected_value]].tolist()
                timestamp_list = pd.to_datetime(self.filtered_df["Timestamp"]).tolist()
                plt.plot(timestamp_list, weigh_relative_list, marker='o', label=selected_value)'''

            for selected_value in selected_values:
                weigh_relative_list = self.filtered_df[self.pos_weight_mapping[selected_value]].tolist()
                count_list = list(range(1, len(weigh_relative_list) + 1))
                plt.scatter(count_list, weigh_relative_list, label=selected_value, s=5)

            plt.xlabel("时间戳")
            plt.ylabel("相对重量")
            plt.title("相对重量随时间变化")
            plt.legend()
            #plt.xticks(rotation=45)
            plt.tight_layout()

            canvas = FigureCanvasTkAgg(plt.gcf(), master=self.plot_frame)
            canvas.get_tk_widget().configure(width=900, height=345)
            canvas.draw()

            toolbar_frame = tk.Frame(master=self.plot_frame, bg="white")
            toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
            toolbar.update()
            toolbar.configure(background="white")
            canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
            toolbar_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

    # 清空图表框 ========================================================================================================
    def clear_plot(self):
        plt.close('all')  # 关闭所有之前的图形
        plt.clf()         # 清除之前绘图
        self.plot_frame.destroy()
        self.plot_frame = tk.Frame(self.inner_tab2, bg="white", width=900, height=400)
        self.plot_frame.grid(row=1, column=0, columnspan=2, padx=40, pady=20, sticky="ns")
