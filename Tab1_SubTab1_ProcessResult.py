"""
此代码服务于Tab1的子tab1。
"""

import pandas as pd


# 为dataframe添加第0行，即平均值，并将dataframe的内容保留三位小数 =============================================================
def add_average_row(df):
    # 使用布尔索引过滤掉值为0的行，并计算剩余行的平均值
    mean_values = df[df != 0].mean()

    # 新增判断语句，将某一列所有值为0的均值设置为0
    for col in df.columns:
        if (df[col] == 0).all():
            mean_values[col] = 0

    # 将平均值存到dataframe的第0行
    df_new = pd.concat([mean_values.to_frame().T, df])
    # 重置索引
    df_new.reset_index(drop=True, inplace=True)
    df_new.loc[0, "小车ID"] = 0
    return df_new


# 计算中位值 ============================================================================================================
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


# 计算平均值 ============================================================================================================
def calculate_average(df, shuttle_id_value, position):
    df_set_index = df.set_index(f"ShuttleIDPos{position}")

    value_count = df[f"ShuttleIDPos{position}"].value_counts()
    value_count = pd.DataFrame(value_count)
    list_index_value = value_count.index.tolist()

    if shuttle_id_value not in list_index_value or shuttle_id_value == 0:
        average = 0
    elif value_count.loc[shuttle_id_value, f"ShuttleIDPos{position}"] <= 5:
        average = 0
    else:
        try:
            average = df_set_index.at[shuttle_id_value, f"WeighRelative{position}"].mean()
        except KeyError:
            average = 0
    return average


# 计算称重偏差 ===========================================================================================================
def calculate_diff(df, shuttle_id_value, position):
    df_set_index = df.set_index(f"ShuttleIDPos{position}")

    value_count = df[f"ShuttleIDPos{position}"].value_counts()
    value_count = pd.DataFrame(value_count)
    list_index_value = value_count.index.tolist()

    if shuttle_id_value not in list_index_value or shuttle_id_value == 0:
        diff = 0
    elif value_count.loc[shuttle_id_value, f"ShuttleIDPos{position}"] <= 5:
        diff = 0
    else:
        try:
            rows = df_set_index.loc[shuttle_id_value]
            diff = rows[f"WeighRelative{position}"].max() - rows[f"WeighRelative{position}"].min()
        except KeyError:
            diff = 0
    return diff


# ======================================================================================================================
def process_data(df, result):
    if result == "中位值":
        # Create empty DataFrame to store the results
        rows_median = []
        # Calculate the required values for each shuttle ID and store them in average_rows, diff_rows, and rows_median
        for shuttle_id in range(1, 17):
            median_pos1 = calculate_median(df, shuttle_id, 1)
            median_pos2 = calculate_median(df, shuttle_id, 2)
            median_pos3 = calculate_median(df, shuttle_id, 3)

            rows_median.append({
                "小车ID": shuttle_id,
                "称重位置1(g)": median_pos1,
                "称重位置2(g)": median_pos2,
                "称重位置3(g)": median_pos3}
            )

        # Create the corresponding dataframe
        df_median = pd.DataFrame(rows_median)
        df_median["小车平均(g)"] = df_median[["称重位置1(g)", "称重位置2(g)", "称重位置3(g)"]].mean(axis=1)
        # 添加第0行，中位值的平均值
        df_median_new = add_average_row(df_median)
        df_median_new = df_median_new.round(3)  # 保留小数点后三位
        df_median_new["小车ID"] = df_median_new["小车ID"].astype(int).astype(str)
        return df_median_new

    # ------------------------------------------------------------------------------------------------------------------
    if result == "平均值":
        # Create empty DataFrame to store the results
        rows_average = []
        # Calculate the required values for each shuttle ID and store them in average_rows, diff_rows, and rows_median
        for shuttle_id in range(1, 17):
            average_pos1 = calculate_average(df, shuttle_id, 1)
            average_pos2 = calculate_average(df, shuttle_id, 2)
            average_pos3 = calculate_average(df, shuttle_id, 3)

            rows_average.append({
                "小车ID": shuttle_id,
                "称重位置1(g)": average_pos1,
                "称重位置2(g)": average_pos2,
                "称重位置3(g)": average_pos3}
            )

        # Create the corresponding dataframe
        df_average = pd.DataFrame(rows_average)
        df_average["小车平均(g)"] = df_average[["称重位置1(g)", "称重位置2(g)", "称重位置3(g)"]].mean(axis=1)
        # 添加第0行，中位值的平均值
        df_average_new = add_average_row(df_average)
        df_average_new = df_average_new.round(3)  # 保留小数点后三位
        df_average_new["小车ID"] = df_average_new["小车ID"].astype(int).astype(str)
        return df_average_new

    # ------------------------------------------------------------------------------------------------------------------
    if result == "称重偏差":
        # Create empty DataFrame to store the results
        rows_diff = []
        # Calculate the required values for each shuttle ID and store them in average_rows, diff_rows, and rows_median
        for shuttle_id in range(1, 17):
            diff_pos1 = calculate_diff(df, shuttle_id, 1)
            diff_pos2 = calculate_diff(df, shuttle_id, 2)
            diff_pos3 = calculate_diff(df, shuttle_id, 3)

            rows_diff.append({
                "小车ID": shuttle_id,
                "称重位置1(g)": diff_pos1,
                "称重位置2(g)": diff_pos2,
                "称重位置3(g)": diff_pos3}
            )

        # Create the corresponding dataframe
        df_diff = pd.DataFrame(rows_diff)
        df_diff["小车平均(g)"] = df_diff[["称重位置1(g)", "称重位置2(g)", "称重位置3(g)"]].mean(axis=1)
        # 添加第0行，中位值的平均值
        df_diff_new = add_average_row(df_diff)
        df_diff_new = df_diff_new.round(3)  # 保留小数点后三位
        df_diff_new["小车ID"] = df_diff_new["小车ID"].astype(int).astype(str)
        return df_diff_new


# ======================================================================================================================
def main():
    df = pd.read_csv(r"C:\Users\21872\Desktop\calibration\称重数据.csv")
    df_median = process_data(df, "中位值")
    df_average = process_data(df, "平均值")
    df_diff = process_data(df, "称重偏差")
    print(df_median, df_average, df_diff)


if __name__ == "__main__":
    main()
