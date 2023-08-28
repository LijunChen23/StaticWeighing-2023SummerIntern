import sys
import tkinter as tk
from tkinter import ttk
from Tab0_MainTab import WeighingDataTab
from Tab1_MainTab import DataProcessingTab
from Tab2_MainTab import CalibrationDataTab


class WeighingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weight GUI")
        self.root.geometry("1100x700")

        self.tabs = None
        self.tab_classes = None
        self.create_tabs()

        # 捕捉窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_tabs(self):
        self.tabs = ttk.Notebook(self.root)
        tab_labels = ["称重数据", "数据处理", "标定数据"]
        self.tab_classes = [WeighingDataTab, DataProcessingTab, CalibrationDataTab]

        for idx, label in enumerate(tab_labels):
            tab = ttk.Frame(self.tabs)
            self.tabs.add(tab, text=label)
            tab_class = self.tab_classes[idx](tab)
        self.tabs.pack(fill="both", expand=True)

    # 关闭窗口并结束程序
    def on_closing(self):
        self.root.destroy()  # 关闭主窗口
        sys.exit(0)  # 结束程序


root = tk.Tk()
app = WeighingApp(root)
root.mainloop()
