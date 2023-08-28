"""
此文件仅用于查看温度拟合曲线绘制以及散点图绘制，并不用于项目中。
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_subplots(axs, dataframe, shuttle_id_pos, seg_no):
    # 设置中文字体为黑体
    plt.rcParams['font.sans-serif'] = 'SimHei'

    # 根据ShuttleIDPos进行分组
    shuttle_id_groups = dataframe.groupby(f'ShuttleIDPos{shuttle_id_pos}')

    # 循环绘制图表
    for index, (shuttle_id, group) in enumerate(shuttle_id_groups):
        ax = axs[index, shuttle_id_pos - 1]
        weigh_empty = group[f'WeighEmptyPos{shuttle_id_pos}']
        weigh_full = group[f'WeighFullPos{shuttle_id_pos}']
        cpu_temp_empty = group[f'Seg{seg_no}CPUTempEmpty']
        cpu_temp_full = group[f'Seg{seg_no}CPUTempFull']

        # 数据拟合
        fit_empty = np.polyfit(cpu_temp_empty, weigh_empty, 1)
        fit_fn_empty = np.poly1d(fit_empty)

        fit_full = np.polyfit(cpu_temp_full, weigh_full, 1)
        fit_fn_full = np.poly1d(fit_full)

        slope_empty = fit_empty[0]  # Get the slope for WeighEmptyPos
        slope_full = fit_full[0]  # Get the slope for WeighFullPos

        ax.plot(cpu_temp_empty, weigh_empty, 'bo', label='空载数据')
        ax.plot(cpu_temp_full, weigh_full, 'go', label='满载数据')
        ax.plot(cpu_temp_empty, fit_fn_empty(cpu_temp_empty), 'r-', label=f'空载拟合曲线\n斜率: {slope_empty:.3f}')
        ax.plot(cpu_temp_full, fit_fn_full(cpu_temp_full), 'm-', label=f'满载拟合曲线\n斜率: {slope_full:.3f}')

        ax.set_xlabel(f'电机{seg_no}温度(\N{DEGREE SIGN}C)')
        ax.set_ylabel('称重结果(g)')
        ax.set_title(f'称重位置{shuttle_id_pos}（小车ID：{int(shuttle_id)}）')
        ax.legend()
        ax.grid(True)


def plot_subplots_relative_weight(axs, dataframe, average_dataframe, median_dataframe, shuttle_id_pos, seg_no):
    # 设置中文字体为黑体
    plt.rcParams['font.sans-serif'] = 'SimHei'

    # 根据ShuttleIDPos进行分组
    shuttle_id_groups = dataframe.groupby(f'ShuttleIDPos{shuttle_id_pos}')

    # 循环绘制图表
    for index, (shuttle_id, group) in enumerate(shuttle_id_groups):
        ax = axs[index, shuttle_id_pos - 1]
        weigh_relative = group[f'WeighRelative{shuttle_id_pos}']
        cpu_temp_empty = group[f'Seg{seg_no}CPUTempEmpty']
        cpu_temp_full = group[f'Seg{seg_no}CPUTempFull']

        ax.plot(cpu_temp_empty, weigh_relative, 'bo', label='空载数据')
        ax.plot(cpu_temp_full, weigh_relative, 'go', label='满载数据')

        ax.set_xlabel(f'电机{seg_no}温度(\N{DEGREE SIGN}C)')
        ax.set_ylabel('称重结果(g)')
        ax.set_title(f'称重位置{shuttle_id_pos}（小车ID：{int(shuttle_id)}）')
        ax.grid(True)

        # 设置纵坐标刻度间隔为0.1
        ax.set_yticks(np.arange(ax.get_yticks()[0], ax.get_yticks()[-1], 0.1))

        average_value = average_dataframe.iloc[int(shuttle_id) - 1, shuttle_id_pos]
        median_value = median_dataframe.iloc[int(shuttle_id) - 1, shuttle_id_pos]
        ax.axhline(y=average_value, color='r', linestyle='--', label=f'平均值:{average_value}')
        ax.axhline(y=median_value, color='b', linestyle='--', label=f'中位值:{median_value}')
        ax.legend()


def weight_vs_temp(dataframe, filename):
    # 定义画布和子图的布局
    figure, axis = plt.subplots(nrows=12, ncols=3, figsize=(12, 42))
    plot_subplots(axis, dataframe, 1, 4)  # For ShuttleIDPos1, Seg4CPUTemp
    plot_subplots(axis, dataframe, 2, 4)  # For ShuttleIDPos2, Seg4CPUTemp
    plot_subplots(axis, dataframe, 3, 2)  # For ShuttleIDPos3, Seg2CPUTemp

    plt.tight_layout()
    # Save the plot to an image file
    plt.savefig(filename, dpi=300)


def relative_weight_vs_temp(dataframe, average_dataframe, median_dataframe, filename):
    # 定义画布和子图的布局
    figure, axis = plt.subplots(nrows=12, ncols=3, figsize=(12, 42))

    # For ShuttleIDPos1, Seg2CPUTemp
    plot_subplots_relative_weight(axis, dataframe, average_dataframe, median_dataframe, 1, 4)

    # For ShuttleIDPos2, Seg2CPUTemp
    plot_subplots_relative_weight(axis, dataframe, average_dataframe, median_dataframe, 2, 4)

    # For ShuttleIDPos3, Seg2CPUTemp
    plot_subplots_relative_weight(axis, dataframe, average_dataframe, median_dataframe, 3, 2)

    plt.tight_layout()

    # Save the plot to an image file
    plt.savefig(filename, dpi=300)
