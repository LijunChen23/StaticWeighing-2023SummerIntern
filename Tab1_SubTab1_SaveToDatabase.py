import numpy as np
import pandas as pd
import os
import pyodbc
from tkinter import filedialog, messagebox


def melt_dataframe(df):
    # 使用melt函数转换成1列多行的DataFrame
    dataframe_melted = df.melt(var_name="Columns")
    # 删除Columns列
    dataframe_melted = dataframe_melted.drop(columns="Columns")
    return dataframe_melted


# 为dataframe添加第0行，即平均值，并将dataframe的内容保留三位小数
def add_average_row(df):
    # 使用布尔索引过滤掉值为0的行，并计算剩余行的平均值
    mean_values = df[df != 0].mean()

    # 新增判断语句，将某一列所有值为0的均值设置为0
    for col in df.columns:
        if (df[col] == 0).all():
            mean_values[col] = 0

    # 将平均值存到dataframe的第0行
    dataframe_new = pd.concat([mean_values.to_frame().T, df])
    # 重置索引
    dataframe_new.reset_index(drop=True, inplace=True)
    return dataframe_new


# 计算中位值
def calculate_median(df, shuttle_id_value, position):
    df_set_index = df.set_index(f"ShuttleIDPos{position}")

    value_count = df[f"ShuttleIDPos{position}"].value_counts()
    value_count = pd.DataFrame(value_count)
    list_index_value = value_count.index.tolist()

    if shuttle_id_value not in list_index_value or shuttle_id_value == 0:
        median = 0
    elif value_count.loc[shuttle_id_value, f"ShuttleIDPos{position}"] <= 5:
        median = 0
    else:
        try:
            median = df_set_index.at[shuttle_id_value, f"WeighRelative{position}"].median()
        except KeyError:
            median = 0
    return median


# 获取某一称重位置的所有小车ID的温度拟合线的斜率
def calculate_temp_slope(df, shuttle_id, position):
    value_count = df[f"ShuttleIDPos{position}"].value_counts()
    value_count = pd.DataFrame(value_count)
    list_index_value = value_count.index.tolist()

    if shuttle_id not in list_index_value or shuttle_id == 0:
        temp_slope = 0
    elif value_count.loc[shuttle_id, f"ShuttleIDPos{position}"] <= 5:
        temp_slope = 0
    else:
        seg_no = 4 if position == 1 or position == 2 else 2
        # 使用groupby方法按"shuttleID"列进行分组，并选择特定shuttleID的所有"WeighFull"值
        groups = df[df[f"ShuttleIDPos{position}"] == shuttle_id].groupby(f"ShuttleIDPos{position}")
        weigh_full = groups.get_group(shuttle_id)[f"WeighFullPos{position}"]
        cpu_temp_full = groups.get_group(shuttle_id)[f"Seg{seg_no}CPUTempFull"]
        fit_temp = np.polyfit(cpu_temp_full, weigh_full, 1)
        temp_slope = fit_temp[0]
    return temp_slope


# 返回中位值数据的dataframe
def get_df_median(df):
    # Create empty DataFrame to store the results
    rows_median = []
    # Calculate the required values for each shuttle ID and store them in average_rows, diff_rows, and rows_median
    for shuttle_id in range(1, 17):
        median_pos1 = calculate_median(df, shuttle_id, 1)
        median_pos2 = calculate_median(df, shuttle_id, 2)
        median_pos3 = calculate_median(df, shuttle_id, 3)

        rows_median.append({"ShuttleIDPos1": median_pos1,
                            "ShuttleIDPos2": median_pos2,
                            "ShuttleIDPos3": median_pos3})

    # Create the corresponding dataframe
    df_median = pd.DataFrame(rows_median)
    # 添加第0行，中位值的平均值
    df_median_new = add_average_row(df_median)
    return df_median_new


# 返回标定系数数据的dataframe
def get_df_factor(df_median, dividend1, dividend2, dividend3):
    # 创建新的DataFrame保存结果
    df_factor = df_median.copy()
    # 使用条件过滤处理分母为0的情况，即若值不为0，则运行除法，若值为0，则返回0
    df_factor["ShuttleIDPos1"] = np.where(df_factor["ShuttleIDPos1"] != 0,
                                          dividend1 / df_factor["ShuttleIDPos1"], 0)
    df_factor["ShuttleIDPos2"] = np.where(df_factor["ShuttleIDPos2"] != 0,
                                          dividend2 / df_factor["ShuttleIDPos2"], 0)
    df_factor["ShuttleIDPos3"] = np.where(df_factor["ShuttleIDPos3"] != 0,
                                          dividend3 / df_factor["ShuttleIDPos3"], 0)
    return df_factor


# 返回斜率的dataframe
def get_df_temp_slope(df):
    # Create empty DataFrame to store the results
    rows_temp_slope = []

    # Calculate the required values for each shuttle ID and store them in rows_median
    for shuttle_id in range(1, 17):
        temp_slope_pos1 = calculate_temp_slope(df, shuttle_id, 1)  # Position1
        temp_slope_pos2 = calculate_temp_slope(df, shuttle_id, 2)  # Position2
        temp_slope_pos3 = calculate_temp_slope(df, shuttle_id, 3)  # Position3

        rows_temp_slope.append({"ShuttleIDPos1": temp_slope_pos1,
                                "ShuttleIDPos2": temp_slope_pos2,
                                "ShuttleIDPos3": temp_slope_pos3})
        # rows_temp_slope.append([temp_slope_pos1, temp_slope_pos2, temp_slope_pos3])

    # Create the corresponding dataframe
    dataframe_temp_slope = pd.DataFrame(rows_temp_slope)
    # 添加第0行，斜率的平均值
    dataframe_temp_slope = add_average_row(dataframe_temp_slope)
    return dataframe_temp_slope


def get_df_value(weigh_status, df):
    # 读取真实重量
    weigh_ref1 = df["WeighRef1"].unique()[0]
    weigh_ref2 = df["WeighRef2"].unique()[0]
    weigh_ref3 = df["WeighRef3"].unique()[0]

    df_status_and_ref = pd.DataFrame({"value": [weigh_status, weigh_ref1, weigh_ref2, weigh_ref3]})
    df_median = get_df_median(df=df)
    df_factor = get_df_factor(df_median=df_median, dividend1=weigh_ref1, dividend2=weigh_ref2, dividend3=weigh_ref3)
    df_temp_slope = get_df_temp_slope(df=df)

    df_median = df_median.round(3)  # 保留小数点后三位
    df_factor = df_factor.round(4)  # 保留小数点后四位
    df_temp_slope = df_temp_slope.round(3)  # 保留小数点后三位

    # 将dataframe转换成1列51行的dataframe
    df_median_melted = melt_dataframe(df=df_median)
    df_factor_melted = melt_dataframe(df=df_factor)
    df_temp_slope_melted = melt_dataframe(df=df_temp_slope)

    # 合并中位值、标定系数和斜率的dataframe，变成一个1列157行的dataframe，代表了标定数据中的Value列
    df_value = pd.concat([df_status_and_ref, df_median_melted, df_factor_melted, df_temp_slope_melted], axis=0)
    df_value.reset_index(drop=True, inplace=True)  # 重置索引
    return df_value.T


# 生成坐标DataFrame
def get_df_field():
    df_field = pd.DataFrame()
    categories = ["Weight6D", "Factor", "TempSlope"]
    for category in categories:
        df = pd.DataFrame()
        df["col1"] = [f"{category}(0,{i})" for i in range(17)]
        df["col2"] = [f"{category}(1,{i})" for i in range(17)]
        df["col3"] = [f"{category}(2,{i})" for i in range(17)]
        df_field_col_melted = melt_dataframe(df)
        df_field = pd.concat([df_field, df_field_col_melted], axis=0)

    df_header = pd.DataFrame({"value": ["WeighStatus", "WeightRef1", "WeightRef2", "WeightRef3"]})
    df_field = pd.concat([df_header, df_field], axis=0)
    df_field.reset_index(drop=True, inplace=True)  # 重置索引
    return df_field.T


def get_all_weigh_refs_filtering(df):
    # 删除所有"WeighRef1", "WeighRef2", "WeighRef3"列都为0的行
    df_filtered = df[(df["WeighRef1"] != 0) | (df["WeighRef2"] != 0) | (df["WeighRef3"] != 0)]
    # 创建新的dataframe，只保留"WeighRef1", "WeighRef2", "WeighRef3"三列
    df_weigh_ref_columns = df_filtered[["WeighRef1", "WeighRef2", "WeighRef3"]].copy()
    # 删除重复的行，以此获得WeighRef的唯一值
    df_weigh_ref_columns.drop_duplicates(subset=["WeighRef1", "WeighRef2", "WeighRef3"], inplace=True)
    df_weigh_ref_columns.reset_index(drop=True, inplace=True)
    return df_weigh_ref_columns


def get_all_weigh_refs_calibration(weigh_status, df):
    df_weigh_ref_columns = get_all_weigh_refs_filtering(df=df)
    df_all_weigh_ref = pd.DataFrame()
    for index, row in df_weigh_ref_columns.iterrows():
        condition_weigh_refs = (df["WeighRef1"] == row[0]) & \
                               (df["WeighRef2"] == row[1]) & \
                               (df["WeighRef3"] == row[2])
        df_ref_filtered = df[condition_weigh_refs]
        # df_ref_filtered.to_csv(f"C:/Users/21872/Desktop/calibration/重量筛选{index}.csv", index=False)

        # 处理数据
        df_value = get_df_value(weigh_status=weigh_status, df=df_ref_filtered)
        df_value.reset_index(drop=True, inplace=True)                           # 重置索引
        df_all_weigh_ref = pd.concat([df_all_weigh_ref, df_value], axis=0)
        df_all_weigh_ref.reset_index(drop=True, inplace=True)                   # 重置索引

    return df_all_weigh_ref


def get_all_weigh_status_calibration(df):
    condition_status0 = (df["WeighEmptyStatus(0)"] == True) & \
                        (df["WeighEmptyStatus(1)"] == False) & \
                        (df["WeighEmptyStatus(2)"] == False) & \
                        (df["WeighEmptyStatus(3)"] == True) & \
                        (df["WeighEmptyStatus(4)"] == True) & \
                        (df["WeighFullStatus(0)"] == True) & \
                        (df["WeighFullStatus(1)"] == False) & \
                        (df["WeighFullStatus(2)"] == False) & \
                        (df["WeighFullStatus(3)"] == True) & \
                        (df["WeighFullStatus(4)"] == True)

    condition_status3 = (df["WeighEmptyStatus(0)"] == True) & \
                        (df["WeighEmptyStatus(1)"] == False) & \
                        (df["WeighEmptyStatus(2)"] == True) & \
                        (df["WeighEmptyStatus(3)"] == False) & \
                        (df["WeighEmptyStatus(4)"] == True) & \
                        (df["WeighFullStatus(0)"] == True) & \
                        (df["WeighFullStatus(1)"] == False) & \
                        (df["WeighFullStatus(2)"] == True) & \
                        (df["WeighFullStatus(3)"] == False) & \
                        (df["WeighFullStatus(4)"] == True)

    df_all_weigh_status = pd.DataFrame()
    list_weigh_status = [0, 3]  # 称重状态1和称重状态4
    for weigh_status in list_weigh_status:
        if weigh_status == 0:
            condition_status = condition_status0
        else:
            condition_status = condition_status3

        df_status_filtered = df[condition_status]  # 保留称重状态为称重状态0或称重状态3的所有行
        df_all_weigh_ref = get_all_weigh_refs_calibration(weigh_status=weigh_status, df=df_status_filtered)
        df_all_weigh_status = pd.concat([df_all_weigh_status, df_all_weigh_ref], axis=0)
        df_all_weigh_status.reset_index(drop=True, inplace=True)  # 重置索引

    return df_all_weigh_status


# 生成 SQL 更新一行标定数据的语句
def get_sql_for_creating_table(table_name, column_names):
    sql_body = "(ID AUTOINCREMENT, "
    for column_name in column_names:
        if column_name != column_names[-1]:
            sql_body += f"[{column_name}] FLOAT, "
    sql = f"CREATE TABLE `{table_name}` " + sql_body + f"[{column_names[-1]}] FLOAT);"
    return sql


# 存入数据库
def get_sql_for_saving_row(table_name, column_names):
    sql_body = "("
    values = " VALUES ("
    for column_name in column_names:
        if column_name != column_names[-1]:
            sql_body += f"[{column_name}], "
            values += "?, "
    sql_body += f"[{column_names[-1]}])"
    values += "?)"
    sql = f"INSERT INTO `{table_name}` " + sql_body + values
    return sql


def save_to_db(conn, table_name, df, sql_save):
    cursor = conn.cursor()
    # 获取数据库中的数据
    cursor.execute(f"SELECT * FROM {table_name}")
    rows_of_db = cursor.fetchall()

    # 遍历DataFrame的每一行
    for index_df, row_of_df in df.iterrows():
        # 在数据库中查找匹配行
        for index_db, row_of_db in enumerate(rows_of_db):
            if row_of_db[1] == row_of_df["WeighStatus"] and row_of_db[2] == row_of_df["WeightRef1"] and \
                    row_of_db[3] == row_of_df["WeightRef2"] and row_of_db[4] == row_of_df["WeightRef3"]:
                delete_sql = f"DELETE FROM `{table_name}` WHERE id = ?"
                cursor.execute(delete_sql, rows_of_db[index_db][0])
        cursor.execute(sql_save, *row_of_df)
    cursor.close()


def save(df, db_file_path, table_name):
    db_file = os.path.abspath(db_file_path)
    # 连接数据库
    conn = pyodbc.connect(r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)}; DBQ=" + db_file + ";Uid=;Pwd=;")
    # 连接成功后弹窗告知用户连接成功
    messagebox.showinfo("提示", "数据库连接成功")

    get_all_weigh_status_calibration(df=df)
    df_all_weigh_status = get_all_weigh_status_calibration(df=df)

    # 得到1行157列的dataframe
    df_field = get_df_field()
    # 将 df_field 的值作为 df_all_weigh_status 的列名
    df_all_weigh_status.columns = df_field.values.flatten()

    def check_if_table_exists(conn, table_name):
        cursor = conn.cursor()
        db_tables = cursor.tables(tableType="TABLE")  # 获取数据库中已经存在的表
        table_exists = False
        for table_info in db_tables:
            if table_info.table_name == table_name:
                table_exists = True
        if not table_exists:
            sql_create = get_sql_for_creating_table(table_name=table_name, column_names=df_field.values.flatten())
            cursor.execute(sql_create)
            cursor.close()
    check_if_table_exists(conn=conn, table_name=table_name)

    sql_save = get_sql_for_saving_row(table_name=table_name, column_names=df_field.values.flatten())
    save_to_db(conn=conn, table_name=table_name, df=df_all_weigh_status, sql_save=sql_save)

    # 提交更改
    conn.commit()
    # 关闭数据库连接
    conn.close()
    # 连接成功后弹窗告知用户连接成功
    messagebox.showinfo("提示", "已更新标定数据库")


def main():
    import tkinter as tk
    import sys
    # create a tkinter window
    root = tk.Tk()
    root.withdraw()

    print("Please select the database file.")
    # 弹窗让用户选择数据库位置
    db_file_path = filedialog.askopenfilename(filetypes=[("Microsoft Access Files", "*.mdb;*.accdb")])
    # 检查用户是否选择了Access数据库
    if not db_file_path:
        sys.exit("Program terminated: No database file selected.")

    df = pd.read_csv(r"C:\Users\21872\Desktop\calibration\机器1的所有数据.csv")
    table_name = "28A10168507"
    save(df=df, db_file_path=db_file_path, table_name=table_name)


if __name__ == "__main__":
    main()
