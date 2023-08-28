"""
此代码服务于Tab2的子tab1。
"""

import pandas as pd
from tkinter import filedialog, messagebox


# ======================================================================================================================
def create_header_df(name):
    # 创建包含数据的列表
    header = [
        ["MpRecipe.Header", "$Type", "STRING", "HeaderData"],
        ["MpRecipe.Header", "Name", "STRING", ""],
        ["MpRecipe.Header", "Description", "STRING", ""],
        ["MpRecipe.Header", "Version", "STRING", ""],
        ["MpRecipe.Header", "Created", "UDINT", 0],
        ["MpRecipe.Header", "CreatedReadable", "STRING", "1970-01-01 00:00:00"],
        ["gFactor", "$Type", "STRING", "PvParameter"],
        ["gFactor", "gFactor.ControllerSerialNo", "STRING", ""]
    ]
    # 创建DataFrame
    df_header = pd.DataFrame(header, columns=["Parameter", "Field", "DataType", "Value"])
    # 设置最后一行最后一列的值为一个变量的值
    df_header.iloc[-1, -1] = name
    return df_header


# 生成坐标DataFrame =====================================================================================================
def get_df_field(status, weight):
    df_field = pd.DataFrame()
    categories = ["Weight6D", "Factor", "TempSlope"]
    for category in categories:
        df = pd.DataFrame()
        df["col1"] = [f"gFactor.Status[{status}].Weight[{weight}].{category}[0,{i}]" for i in range(17)]
        df["col2"] = [f"gFactor.Status[{status}].Weight[{weight}].{category}[1,{i}]" for i in range(17)]
        df["col3"] = [f"gFactor.Status[{status}].Weight[{weight}].{category}[2,{i}]" for i in range(17)]

        # 使用melt函数转换成1列多行的DataFrame
        df_melted = df.melt(var_name="Columns", value_name="Field")
        df_melted = df_melted.drop(columns="Columns")  # 删除Columns列
        df_field = pd.concat([df_field, df_melted], axis=0)
    # 重置索引
    df_weight_ref1 = pd.DataFrame({"Field": [f"gFactor.Status[{status}].Weight[{weight}].WeightRef[0]"]})
    df_weight_ref2 = pd.DataFrame({"Field": [f"gFactor.Status[{status}].Weight[{weight}].WeightRef[1]"]})
    df_weight_ref3 = pd.DataFrame({"Field": [f"gFactor.Status[{status}].Weight[{weight}].WeightRef[2]"]})

    df_field = pd.concat([df_weight_ref1, df_weight_ref2, df_weight_ref3, df_field], axis=0)
    df_field.reset_index(drop=True, inplace=True)
    return df_field


# ======================================================================================================================
def gen_calibration_data(df, table_name):
    weigh_ref_counts = df["WeighStatus"].value_counts()  # 查看 "WeighStatus" 列中不同值的数量
    max_weigh_ref_count = weigh_ref_counts.max()  # 获取最大的数量
    print(max_weigh_ref_count)

    df_gfactor = pd.DataFrame({"Parameter": ["gFactor"] * 156})
    df_real = pd.DataFrame({"DataType": ["REAL"] * 156})

    df_all_status = pd.DataFrame()
    for weigh_status in list(range(6)):
        print(weigh_status)
        df_all_weight = pd.DataFrame()
        # 若在数据库中，则生成相应的dataframe ------------------------------------------------------------------------------
        if weigh_status in df["WeighStatus"].values:
            # 保留 "WeighStatus" 列的值为 weigh_status 的行
            df_filtered = df[df["WeighStatus"] == weigh_status]
            df_filtered = df_filtered.drop(columns=["WeighStatus"])
            df_filtered.reset_index(drop=True, inplace=True)
            print(df_filtered)
            for weigh_ref_no in range(max_weigh_ref_count):
                if weigh_ref_no in df_filtered.index:
                    print(f"{weigh_ref_no} in df values")
                    df_value = df_filtered[df_filtered.index == weigh_ref_no].T
                    df_value.columns = ["Value"]
                    df_value.reset_index(drop=True, inplace=True)
                else:
                    df_value = pd.DataFrame({"Value": [0] * 156})
                print(f"df_value is {df_value}")
                df_field = get_df_field(weigh_status, weigh_ref_no)
                df_field_and_value = pd.concat([df_field, df_value], axis=1)

                # 添加Parameter列，即gFactor，和DataType列，即Real
                df_weigh_ref_and_result = pd.concat([df_field_and_value, df_gfactor, df_real], axis=1)
                # 在此weight下，将新获得的结果存入dataframe中
                df_all_weight = pd.concat([df_all_weight, df_weigh_ref_and_result], axis=0)
                df_all_weight.reset_index(drop=True, inplace=True)  # 重置索引

        # 如果不在数据库中，则创建为0的dataframe以满足格式需求 ---------------------------------------------------------------
        else:
            for weigh_ref_no in range(max_weigh_ref_count):
                df_value = pd.DataFrame({"Value": [0] * 156})
                df_field = get_df_field(weigh_status, weigh_ref_no)
                df_field_and_value = pd.concat([df_field, df_value], axis=1)

                # 添加Parameter列，即gFactor，和DataType列，即Real
                df_weigh_ref_and_result = pd.concat([df_field_and_value, df_gfactor, df_real], axis=1)
                # 在此weight下，将新获得的结果存入dataframe中
                df_all_weight = pd.concat([df_all_weight, df_weigh_ref_and_result], axis=0)
                df_all_weight.reset_index(drop=True, inplace=True)  # 重置索引

        # 在包含所有状态即重量的dataframe中加入新的重量的dataframe -----------------------------------------------------------
        df_all_status = pd.concat([df_all_status, df_all_weight], axis=0)
    df_all_status.reset_index(drop=True, inplace=True)  # 重置索引

    # 按照需求重置列的位置
    list_column_name = ["Parameter", "Field", "DataType", "Value"]
    df_all_status = df_all_status[list_column_name].reset_index(drop=True)

    # 添加header dataframe
    df_header = create_header_df(table_name)
    df_final = pd.concat([df_header, df_all_status], axis=0)
    df_final.reset_index(drop=True, inplace=True)  # 重置索引

    # 用户选择保存标定数据的位置
    default_file_name = table_name + ".csv"
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")],
                                             initialfile=default_file_name)
    if file_path:
        df_final.to_csv(file_path, index=False)  # 将DataFrame保存为CSV文件
        messagebox.showinfo("提示", f"标定数据已储存为：\n{file_path}")  # 弹窗告知用户已储存标定数据
    else:
        messagebox.showinfo("提示", "标定数据未储存")  # 弹窗告知用户未储存标定数据


# ======================================================================================================================
def main():
    df = pd.read_csv(r"C:\Users\21872\Desktop\calibration\标定数据库.csv")
    print(df)

    gen_calibration_data(df, "28A")


if __name__ == "__main__":
    main()
