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
        self.weigh_status_checkboxes = []
        self.table_name = None
        self.time_filtered_df = None
        self.status_descriptions = {
            "[0]: Empty: Clean 0, Photo 0\n     Full:  Clean 0, Photo 0": 0,
            "[1]: Empty: Clean 0, Photo 0\n     Full:  Clean 1, Photo 0": 1,
            "[2]: Empty: Clean 0, Photo 1\n     Full:  Clean 1, Photo 1": 2,
            "[3]: Empty: Clean 0, Photo 1\n     Full:  Clean 0, Photo 1": 3,
            "[4]: Empty: Clean 1, Photo 0\n     Full:  Clean 1, Photo 0": 4,
            "[5]: Empty: Clean 1, Photo 1\n     Full:  Clean 1, Photo 1": 5
        }

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
        self.plot_frame.grid(row=1, column=1, columnspan=6, padx=40, pady=5, sticky="s")
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

        # 创建”称重状态“标签 ---------------------------------------------------------------------------------------------
        weigh_status_label = ttk.Label(self.inner_tab2, text="称重状态：", font=("SimHei", 12), style="Sub_tab.TLabel")
        weigh_status_label.grid(row=2, column=5, padx=5, pady=5, sticky="e")

        # 创建一个frame
        self.frame_weigh_status = tk.Frame(self.inner_tab2, bg="white", width=280, height=86,
                                           takefocus=False, borderwidth=1, relief="solid")
        self.frame_weigh_status.grid(row=2, column=6, padx=5, pady=5, sticky="w")
        self.create_weigh_status_options()

        # 辅助排版 ------------------------------------------------------------------------------------------------------
        self.inner_tab2.grid_rowconfigure(0, weight=1)  # Empty row at the top
        self.inner_tab2.grid_rowconfigure(3, weight=1)  # Empty row at the end
        self.inner_tab2.grid_columnconfigure(0, weight=1)
        self.inner_tab2.grid_columnconfigure(7, weight=1)

    # 清空图表框 ========================================================================================================
    def clear_plot(self):
        plt.close('all')  # 关闭所有之前的图形
        plt.clf()         # 清除之前绘图
        self.plot_frame.destroy()
        self.plot_frame = tk.Frame(self.inner_tab2, bg="white", width=900, height=400)
        self.plot_frame.grid(row=1, column=1, columnspan=6, padx=40, pady=5, sticky="n")
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

    # ==================================================================================================================
    def create_shuttle_id_options(self):
        row = 0
        col = 0
        # 创建一个多选框列表，包含整数1到16的选项
        for i in range(1, 17):
            checkbox_var = tk.IntVar()
            checkbox = ttk.Checkbutton(self.frame_shuttle_id, text=str(i), variable=checkbox_var,
                                       onvalue=1, offvalue=0, command=self.generate_data, style="Sub_tab.TCheckbutton")
            checkbox.grid(row=row, column=col, sticky="w")
            self.shuttle_id_checkboxes.append((i, checkbox_var))
            row += 1
            if row >= 4:  # 每行放4个选项
                row = 0
                col += 1

    # ==================================================================================================================
    def create_weigh_pos_options(self):
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
    def create_weigh_status_options(self):
        # 创建Canvas控件 ------------------------------------------------------------------------------------------------
        canvas_weigh_status = tk.Canvas(master=self.frame_weigh_status, bg="white",
                                        width=262, height=86, takefocus=False)
        canvas_weigh_status.grid(row=0, column=0, sticky="nsew")

        # 创建垂直滚动条 -------------------------------------------------------------------------------------------------
        scrollbar_weigh_status = ttk.Scrollbar(self.frame_weigh_status, orient="vertical",
                                               command=canvas_weigh_status.yview)
        scrollbar_weigh_status.grid(row=0, column=1, sticky="ns")
        canvas_weigh_status.configure(yscrollcommand=scrollbar_weigh_status.set)

        # 创建Canvas内部Frame -------------------------------------------------------------------------------------------
        frame_canvas_weigh_status = ttk.Frame(canvas_weigh_status, takefocus=False, style="CanvasFrame.TFrame")
        canvas_weigh_status.create_window((0, 0), window=frame_canvas_weigh_status, anchor="nw")

        row = 0

        for status_description, status in self.status_descriptions.items():
            checkbox_var = tk.IntVar()
            checkbox = ttk.Checkbutton(
                frame_canvas_weigh_status, text=status_description, variable=checkbox_var,
                onvalue=1, offvalue=0, command=self.generate_data, style="Sub_tab.TCheckbutton"
            )
            checkbox.grid(row=row, column=0, sticky="w")
            self.weigh_status_checkboxes.append((status, checkbox_var))
            row += 1

        frame_canvas_weigh_status.bind(
            "<Configure>", lambda event: canvas_weigh_status.configure(scrollregion=canvas_weigh_status.bbox("all"))
        )

    # 生成”称重次数vs相对重量“的散点图 =====================================================================================
    def generate_data(self):
        selected_poss = [
            pos_label.strip("称重位置") for pos_label, var in self.weigh_pos_checkboxes if var.get() == 1]
        selected_shuttle_ids = [
            int(float(shuttle_id)) for shuttle_id, var in self.shuttle_id_checkboxes if var.get() == 1]
        selected_statuses = [status for status, var in self.weigh_status_checkboxes if var.get() == 1]
        print(f"selected_statuses: {selected_statuses}\n")
        self.clear_plot()

        if selected_poss and selected_shuttle_ids and selected_statuses:
            # 创建一个布尔条件列表，用于选择满足任一条件的行
            condition_list = []
            for selected_pos in selected_poss:
                for shuttle_id in selected_shuttle_ids:
                    condition = self.time_filtered_df[f"ShuttleIDPos{selected_pos}"] == shuttle_id
                    condition_list.append(condition)
            print(f"condition_list:\n{condition_list}\n")
            # 使用逻辑或将所有条件组合在一起
            combined_condition = condition_list[0]
            for condition in condition_list[1:]:
                combined_condition |= condition
            filtered_df = self.time_filtered_df[combined_condition]

            print(f"self.time_filtered_df[combined_condition]:\n{filtered_df}\n")

            columns_to_check = [
                "WeighEmptyStatus(0)", "WeighEmptyStatus(1)", "WeighEmptyStatus(2)", "WeighEmptyStatus(3)",
                "WeighEmptyStatus(4)", "WeighFullStatus(0)", "WeighFullStatus(1)", "WeighFullStatus(2)",
                "WeighFullStatus(3)", "WeighFullStatus(4)"
            ]
            filtered_df = filtered_df[~(filtered_df[columns_to_check] == False).all(axis=1)]

            print(f"filtered_df[~(filtered_df[columns_to_check] == False).all(axis=1)]:\n{filtered_df}\n")

            status_condition_list = []
            for selected_status in selected_statuses:
                if selected_status == 0:
                    status_condition_list.append(
                        (filtered_df["WeighEmptyStatus(1)"] == False) & (filtered_df["WeighEmptyStatus(2)"] == False) &
                        (filtered_df["WeighFullStatus(1)"] == False) & (filtered_df["WeighFullStatus(2)"] == False)
                    )
                elif selected_status == 1:
                    status_condition_list.append(
                        (filtered_df["WeighEmptyStatus(1)"] == False) & (filtered_df["WeighEmptyStatus(2)"] == False) &
                        (filtered_df["WeighFullStatus(1)"] == True) & (filtered_df["WeighFullStatus(2)"] == False)
                    )
                elif selected_status == 2:
                    status_condition_list.append(
                        (filtered_df["WeighEmptyStatus(1)"] == False) & (filtered_df["WeighEmptyStatus(2)"] == True) &
                        (filtered_df["WeighFullStatus(1)"] == True) & (filtered_df["WeighFullStatus(2)"] == True)
                    )
                elif selected_status == 3:
                    status_condition_list.append(
                        (filtered_df["WeighEmptyStatus(1)"] == False) & (filtered_df["WeighEmptyStatus(2)"] == True) &
                        (filtered_df["WeighFullStatus(1)"] == False) & (filtered_df["WeighFullStatus(2)"] == True)
                    )
                elif selected_status == 4:
                    status_condition_list.append(
                        (filtered_df["WeighEmptyStatus(1)"] == True) & (filtered_df["WeighEmptyStatus(2)"] == False) &
                        (filtered_df["WeighFullStatus(1)"] == True) & (filtered_df["WeighFullStatus(2)"] == False)
                    )
                else:
                    status_condition_list.append(
                        (filtered_df["WeighEmptyStatus(1)"] == True) & (filtered_df["WeighEmptyStatus(2)"] == True) &
                        (filtered_df["WeighFullStatus(1)"] == True) & (filtered_df["WeighFullStatus(2)"] == True)
                    )

            # 使用逻辑或将所有条件组合在一起
            combined_status_condition = status_condition_list[0]
            for condition in status_condition_list[1:]:
                combined_status_condition |= condition
            print(f"combined_status_condition:\n{combined_status_condition}\n")
            status_filtered_df = filtered_df[combined_status_condition]
            print(f"filtered_df[combined_condition]:\n{status_filtered_df}\n")

            plt.rcParams["font.sans-serif"] = "SimHei"  # 设置字体为简体中文黑体
            plt.rcParams["axes.unicode_minus"] = False  # 解决负号无法正常显示的问题
            plt.figure(figsize=(9, 4))

            for selected_pos in selected_poss:
                weigh_relative_list = status_filtered_df[f"WeighRelative{selected_pos}"].tolist()
                timestamp_list = pd.to_datetime(status_filtered_df["TimeStamp"]).tolist()
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
