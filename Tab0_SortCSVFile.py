import pandas as pd
import re


# 创建新的column，统一所有规格 # ===========================================================================================
def add_weigh_status_columns(df):
    column_name_list = [
        "WeighEmptyStatus(0)", "WeighEmptyStatus(1)", "WeighEmptyStatus(2)",
        "WeighEmptyStatus(3)", "WeighEmptyStatus(4)",
        "WeighFullStatus(0)", "WeighFullStatus(1)", "WeighFullStatus(2)",
        "WeighFullStatus(3)", "WeighFullStatus(4)"
    ]
    for column_name in column_name_list:
        # 检查column_name是否已经在DataFrame中
        if column_name not in df.columns:
            # 如果不在DataFrame中，就添加新的列，并将所有值初始化为default_value
            df = df.assign(**{column_name: False})
    return df


# 创建新的column，统一所有规格 =============================================================================================
def add_and_sort_columns(df):
    col_name_list = [
        "ShuttleIDPos1", "ShuttleIDPos2", "ShuttleIDPos3", "WeighDuration",
        "Seg2CPUTempEmpty", "Seg4CPUTempEmpty", "Seg2CPUTempFull", "Seg4CPUTempFull",
        "WeighEmptyPos1", "WeighEmptyPos2", "WeighEmptyPos3", "WeighFullPos1", "WeighFullPos2", "WeighFullPos3",
        "WeighRelative1", "WeighRelative2", "WeighRelative3", "WeighResult1", "WeighResult2", "WeighResult3",
        "WeighTempOffset1", "WeighTempOffset2", "WeighTempOffset3",
        "WeighOut1", "WeighOut2", "WeighOut3", "WeighRef1", "WeighRef2", "WeighRef3",
        "WeighEmptyStatus(0)", "WeighEmptyStatus(1)", "WeighEmptyStatus(2)",
        "WeighEmptyStatus(3)", "WeighEmptyStatus(4)",
        "WeighFullStatus(0)", "WeighFullStatus(1)", "WeighFullStatus(2)",
        "WeighFullStatus(3)", "WeighFullStatus(4)",
        "WeighStatus", "TimeStamp"
    ]
    for col_name in col_name_list:
        # 检查column_name是否已经在DataFrame中
        if col_name not in df.columns:
            # 如果不在DataFrame中，就添加新的列，并将所有值初始化为default_value
            if col_name == "TimeStamp":
                df = df.assign(**{col_name: ""})
            else:
                df = df.assign(**{col_name: None})

    # 将数据按照field列排序，方便后续导入数据库
    df = df[col_name_list].reset_index(drop=True)
    return df


# ======================================================================================================================
def parse_filename(filename):
    # 定义正则表达式来匹配文件名的不同部分
    pattern = r"WeighingStatus(\d+)(?:_(\d+))?\(Duration (\d*\.?\d+)s,(\d*\.?\d+)g\)" \
              r"-(\d*\.?\d+)-(\d*\.?\d+)-(\d*\.?\d+)\.csv"

    # 使用正则表达式进行匹配
    match = re.search(pattern, filename)
    if match:
        # 将字符串转换为相应的类型
        weigh_status1 = int(match.group(1))
        weigh_status2 = None if match.group(2) is None else int(match.group(2))
        weigh_duration = float(match.group(3))
        weigh_ref1 = float(match.group(5))
        weigh_ref2 = float(match.group(6))
        weigh_ref3 = float(match.group(7))
        return weigh_status1, weigh_status2, weigh_duration, weigh_ref1, weigh_ref2, weigh_ref3
    else:
        return None, None, None, None, None, None


# 整理数据，创建新的表格存储数据 # ==========================================================================================
def sort_dataframe(file_name):
    # 读取csv文件的原始数据
    df_original = pd.read_csv(file_name, skiprows=list(range(1, 8)))

    # 将Field列分成两列，并从"Category"列提取`Index`的值作为新列
    df_original[["Category", "Field"]] = df_original["Field"].str.split(".", expand=True)
    df_original["Index"] = df_original["Category"].str.extract(r"\[(\d+)\]")
    df_original["Index"] = pd.to_numeric(df_original["Index"])

    # 重塑包含原始数据的数据帧
    df = df_original.pivot(index="Index", columns="Field", values="Value")

    # 将无用数据删除，即`ID`为0的数据
    df["ID"] = pd.to_numeric(df["ID"]).astype(int)
    df = df[df["ID"] != 0]

    # 将dataframe的列表名中包含`[]`字符的改成`()`
    df.rename(columns=lambda x: x.replace("[", "(").replace("]", ")"), inplace=True)

    if "TimeStamp" in df.columns:
        df["TimeStamp"] = pd.to_datetime(df["TimeStamp"], unit="s")

    # 获取Controller Serial Number，并删除此列
    if "ControllerSerialNo" in df.columns:
        controller_serial_no = df["ControllerSerialNo"].dropna().unique()
        controller_serial_no = controller_serial_no[0]
        df.drop(columns="ControllerSerialNo", inplace=True)
    else:
        controller_serial_no = None

    # 将列名中有"WeighStatus"的列的数据格式改成整形
    if "WeighStatus" in df.columns:
        df["WeighStatus"] = pd.to_numeric(df["WeighStatus"]).astype(int)
    else:
        if "WeighDuration" not in df.columns and "WeighRef" not in df.columns:
            weigh_status1, weigh_status2, weigh_duration, weigh_ref1, weigh_ref2, weigh_ref3 = parse_filename(file_name)
            df["WeighStatus"] = df["Comment"].astype(str).replace("nan", str(weigh_status1)).astype(float).astype(int)
            df["WeighDuration"] = weigh_duration
            df["WeighRef1"] = weigh_ref1
            df["WeighRef2"] = weigh_ref2
            df["WeighRef3"] = weigh_ref3

    if "WeighStatus" in df.columns and "WeighEmptyStatus" not in df.columns and "WeighFullStatus" not in df.columns:
        df = add_weigh_status_columns(df)
        # 根据WeighStatus列的值更新其他列的值
        for index, row in df.iterrows():
            weigh_status = row["WeighStatus"]
            ref1 = row["WeighRef1"]
            ref2 = row["WeighRef2"]
            ref3 = row["WeighRef3"]
            if weigh_status == 1 and ref1 != 0 and ref2 != 0 and ref3 != 0:
                df.at[index, "WeighEmptyStatus(0)"] = True
                df.at[index, "WeighEmptyStatus(3)"] = True
                df.at[index, "WeighEmptyStatus(4)"] = True
                df.at[index, "WeighFullStatus(0)"] = True
                df.at[index, "WeighFullStatus(3)"] = True
                df.at[index, "WeighFullStatus(4)"] = True
            elif weigh_status == 4 and ref1 != 0 and ref2 != 0 and ref3 != 0:
                df.at[index, "WeighEmptyStatus(0)"] = True
                df.at[index, "WeighEmptyStatus(2)"] = True
                df.at[index, "WeighEmptyStatus(4)"] = True
                df.at[index, "WeighFullStatus(0)"] = True
                df.at[index, "WeighFullStatus(2)"] = True
                df.at[index, "WeighFullStatus(4)"] = True

    # 将数据按照field列排序，方便后续导入数据库
    df_result = add_and_sort_columns(df)

    for col in df_result.columns:
        if "WeighEmptyStatus" in col or "WeighFullStatus" in col:
            df_result[col] = df_result[col].replace({"false": False, "true": True})
        elif "ID" in col or "WeighStatus" in col:
            df_result[col] = df_result[col].fillna(0).astype(int)
        elif "CPUTemp" in col:
            df_result[col] = pd.to_numeric(df_result[col]).astype(float)
            df_result[col] = df_result[col].round(2)  # 保留小数点后四位
        elif "Weigh" in col and "Status" not in col:
            df_result[col] = pd.to_numeric(df_result[col]).fillna(0).astype(float)
            df_result[col] = df_result[col].round(3)  # 保留小数点后四位
        elif "WeighDuration" in col:
            df_result[col] = df_result[col].round(1)  # 保留小数点后四位
        elif "TimeStamp" in col:
            df_result[col] = df_result[col].astype(str)

    # df_result.info()
    return df_result, controller_serial_no


# ======================================================================================================================
def main():
    # filepath = r"C:\Users\21872\Desktop\original\2023-06-30_WeighingStatus1_3(Duration 1s,8g)-8.78-8.79-8.75.csv"
    # filepath = r"C:\Users\21872\Desktop\original\2023-07-26_Line2_Weighing data.csv"
    filepath = r"C:\Users\21872\Desktop\original\2023-08-01_Line2_Weighing data.csv"
    df, controller_serial_no = sort_dataframe(filepath)
    df.to_csv(r"C:\Users\21872\Desktop\original\测试dataframe.csv", index=False)


if __name__ == "__main__":
    main()
