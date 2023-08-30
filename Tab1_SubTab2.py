import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import ttk


class InnerTab2:
    def __init__(self, parent_tab):
        self.inner_tab2 = tk.Frame(parent_tab, bg="whitesmoke")

        self.plot_frame = None
        self.frame_weigh_pos = None
        self.frame_shuttle_id = None
        self.weigh_pos_checkboxes = []
        self.shuttle_id_checkboxes = []
        self.table_name = None
        self.time_filtered_df = None

        self.create_widgets()

    # ==================================================================================================================
    def create_widgets(self):
        style = ttk.Style()
        style.configure("Sub_tab.TLabel", background="whitesmoke")
        style.configure("Sub_tab.TButton", font=("SimHei", 12), padding=(10, 20))
        style.configure("Sub_tab.TCheckbutton", font=("SimHei", 12), padding=(5, 5),
                        background="white", foreground="black")
        style.configure("CanvasFrame.TFrame", background="white")

        # 创建一个框用于展示散点图 -----------------------------------------------------------------------------------------
        self.plot_frame = tk.Frame(self.inner_tab2, bg="white", width=900, height=400)
        self.plot_frame.grid(row=1, column=1, columnspan=4, padx=40, pady=5, sticky="s")
        self.plot_frame.grid_propagate(False)  # 设置为0可使组件大小不变

        # 创建”小车id“标签 -----------------------------------------------------------------------------------------------
        shuttle_id_label = ttk.Label(self.inner_tab2, text="小车id：", font=("SimHei", 12), style="Sub_tab.TLabel")
        shuttle_id_label.grid(row=2, column=1, padx=5, pady=5, sticky="e")

        # 创建一个frame
        self.frame_shuttle_id = tk.Frame(self.inner_tab2, bg="white", width=103, height=86,
                                         takefocus=False, borderwidth=1, relief="solid")
        self.frame_shuttle_id.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.create_shuttle_id_options()

        # 创建”称重位置“标签 ---------------------------------------------------------------------------------------------
        weigh_pos_label = ttk.Label(self.inner_tab2, text="称重位置：", font=("SimHei", 12), style="Sub_tab.TLabel")
        weigh_pos_label.grid(row=2, column=3, padx=5, pady=5, sticky="e")

        # 创建一个frame
        self.frame_weigh_pos = tk.Frame(self.inner_tab2, bg="white", width=103, height=86,
                                        takefocus=False, borderwidth=1, relief="solid")
        self.frame_weigh_pos.grid(row=2, column=4, padx=5, pady=5, sticky="w")
        self.create_weigh_pos_options()

        # 辅助排版 ------------------------------------------------------------------------------------------------------
        self.inner_tab2.grid_rowconfigure(0, weight=1)  # Empty row at the top
        self.inner_tab2.grid_rowconfigure(3, weight=1)  # Empty row at the end
        self.inner_tab2.grid_columnconfigure(0, weight=1)
        self.inner_tab2.grid_columnconfigure(5, weight=1)

    # 清空图表框 ========================================================================================================
    def clear_plot(self):
        plt.close('all')  # 关闭所有之前的图形
        plt.clf()         # 清除之前绘图
        self.plot_frame.destroy()
        self.plot_frame = tk.Frame(self.inner_tab2, bg="white", width=900, height=400)
        self.plot_frame.grid(row=1, column=1, columnspan=4, padx=40, pady=5, sticky="n")
        self.plot_frame.grid_propagate(False)  # 设置为0可使组件大小不变

    # 更新InnerTab2的内容 ===============================================================================================
    def update_content(self, df, controller_serial_number):
        self.table_name = controller_serial_number
        ref_filtered_df = df[(df["WeighRef1"] == 0) & (df["WeighRef2"] == 0) & (df["WeighRef3"] == 0)]
        self.time_filtered_df = ref_filtered_df.copy()

        self.time_filtered_df["TimeStamp"] = pd.to_datetime(self.time_filtered_df["TimeStamp"], errors="coerce")
        self.time_filtered_df = self.time_filtered_df[
            (self.time_filtered_df["TimeStamp"] != "") &
            (self.time_filtered_df["TimeStamp"] != "1970-01-01 00:00:00") &
            (self.time_filtered_df["TimeStamp"].dt.year != 2021)
        ]
        print(self.time_filtered_df)
        self.clear_plot()
        for _, var in self.weigh_pos_checkboxes:
            var.set(0)

    # ==================================================================================================================
    def create_weigh_pos_options(self):
        # 创建“称重位置”多选框列表框 --------------------------------------------------------------------------------------
        row = 0
        pos_labels = ["称重位置1", "称重位置2", "称重位置3"]
        for pos_label in pos_labels:
            checkbox_var = tk.IntVar()
            checkbox = ttk.Checkbutton(self.frame_weigh_pos, text=pos_label, variable=checkbox_var,
                                       onvalue=1, offvalue=0, command=self.generate_data, style="Sub_tab.TCheckbutton")
            checkbox.grid(row=row, column=0, sticky="w")
            self.weigh_pos_checkboxes.append((pos_label, checkbox_var))
            row += 1

    # ==================================================================================================================
    def create_shuttle_id_options(self):
        style = ttk.Style()
        style.configure("Sub_tab.TCheckbutton", font=("SimHei", 12), padding=(5, 5),
                        background="white", foreground="black")
        style.configure("CanvasFrame.TFrame", background="white")

        # 创建Canvas控件 ------------------------------------------------------------------------------------------------
        canvas_shuttle_id = tk.Canvas(master=self.frame_shuttle_id, bg="white", width=85, height=86, takefocus=False)
        canvas_shuttle_id.grid(row=0, column=0, sticky="nsew")

        # 创建垂直滚动条 -------------------------------------------------------------------------------------------------
        scrollbar_shuttle_id = ttk.Scrollbar(self.frame_shuttle_id, orient="vertical", command=canvas_shuttle_id.yview)
        scrollbar_shuttle_id.grid(row=0, column=1, sticky="ns")
        canvas_shuttle_id.configure(yscrollcommand=scrollbar_shuttle_id.set)

        # 创建Canvas内部Frame -------------------------------------------------------------------------------------------
        frame_canvas_shuttle_id = ttk.Frame(canvas_shuttle_id, takefocus=False, style="CanvasFrame.TFrame")
        canvas_shuttle_id.create_window((0, 0), window=frame_canvas_shuttle_id, anchor="nw")

        row = 0
        # 创建一个多选框列表，包含整数1到16的选项
        for i in range(1, 17):
            checkbox_var = tk.IntVar()
            checkbox = ttk.Checkbutton(frame_canvas_shuttle_id, text=str(i), variable=checkbox_var,
                                       onvalue=1, offvalue=0, command=self.generate_data, style="Sub_tab.TCheckbutton")
            checkbox.grid(row=row, column=0, sticky="w")
            self.shuttle_id_checkboxes.append((i, checkbox_var))
            row += 1

        frame_canvas_shuttle_id.bind(
            "<Configure>", lambda event: canvas_shuttle_id.configure(scrollregion=canvas_shuttle_id.bbox("all"))
        )

    # 生成”称重次数vs相对重量“的散点图 =====================================================================================
    def generate_data(self):
        selected_poss = [
            pos_label.strip("称重位置") for pos_label, var in self.weigh_pos_checkboxes if var.get() == 1]
        selected_shuttle_ids = [
            int(float(shuttle_id)) for shuttle_id, var in self.shuttle_id_checkboxes if var.get() == 1]
        self.clear_plot()

        if selected_poss and selected_shuttle_ids:
            # 创建一个布尔条件列表，用于选择满足任一条件的行
            condition_list = []
            for selected_pos in selected_poss:
                for shuttle_id in selected_shuttle_ids:
                    condition = self.time_filtered_df[f"ShuttleIDPos{selected_pos}"] == shuttle_id
                    condition_list.append(condition)

            # 使用逻辑或将所有条件组合在一起
            combined_condition = condition_list[0]
            for condition in condition_list[1:]:
                combined_condition |= condition

            # 将组合条件应用于原始 DataFrame，得到满足条件的子集 DataFrame
            filtered_df = self.time_filtered_df[combined_condition]

            plt.rcParams["font.sans-serif"] = "SimHei"  # 设置字体为简体中文黑体
            plt.rcParams["axes.unicode_minus"] = False  # 解决负号无法正常显示的问题
            plt.figure(figsize=(9, 4))

            for selected_pos in selected_poss:
                weigh_relative_list = filtered_df[f"WeighRelative{selected_pos}"].tolist()
                timestamp_list = pd.to_datetime(filtered_df["TimeStamp"]).tolist()
                plt.scatter(timestamp_list, weigh_relative_list, label=f"称重位置{selected_pos}", s=5)

            plt.xlabel("时间戳")
            plt.ylabel("相对重量")
            plt.title("相对重量随时间变化")
            plt.legend()
            plt.xticks(rotation=45, fontsize=8)
            plt.yticks(fontsize=8)
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
