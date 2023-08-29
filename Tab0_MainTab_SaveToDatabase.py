"""
此代码服务于Tab0的主Tab
"""

import os
import pyodbc
from tkinter import filedialog, messagebox


# 检查指定的表名是否在数据库中 #############################################################################################
def check_if_table_exists(conn, table_name):
    cursor = conn.cursor()                        # 创建游标
    db_tables = cursor.tables(tableType="TABLE")  # 获取数据库中已经存在的表
    table_exists = False
    for table_info in db_tables:
        if table_info.table_name == table_name:
            table_exists = True
    # 如果表名不存在
    if not table_exists:
        # 使用SQL语句创建表格
        sql_create_table = f"CREATE TABLE `{table_name}` (ID AUTOINCREMENT," \
                           f"[ShuttleIDPos1] SMALLINT, [ShuttleIDPos2] SMALLINT, [ShuttleIDPos3] SMALLINT," \
                           f"[WeighDuration] FLOAT," \
                           f"[Seg2CPUTempEmpty] FLOAT, [Seg4CPUTempEmpty] FLOAT," \
                           f"[Seg2CPUTempFull] FLOAT, [Seg4CPUTempFull] FLOAT," \
                           f"[WeighEmptyPos1] FLOAT, [WeighEmptyPos2] FLOAT, [WeighEmptyPos3] FLOAT," \
                           f"[WeighFullPos1] FLOAT, [WeighFullPos2] FLOAT, [WeighFullPos3] FLOAT," \
                           f"[WeighRelative1] FLOAT, [WeighRelative2] FLOAT, [WeighRelative3] FLOAT," \
                           f"[WeighResult1] FLOAT, [WeighResult2] FLOAT, [WeighResult3] FLOAT," \
                           f"[WeighTempOffset1] FLOAT, [WeighTempOffset2] FLOAT, [WeighTempOffset3] FLOAT," \
                           f"[WeighOut1] FLOAT, [WeighOut2] FLOAT, [WeighOut3] FLOAT," \
                           f"[WeighRef1] FLOAT, [WeighRef2] FLOAT, [WeighRef3] FLOAT," \
                           f"[WeighEmptyStatus(0)] YESNO, [WeighEmptyStatus(1)] YESNO," \
                           f"[WeighEmptyStatus(2)] YESNO, [WeighEmptyStatus(3)] YESNO," \
                           f"[WeighEmptyStatus(4)] YESNO, [WeighFullStatus(0)] YESNO," \
                           f"[WeighFullStatus(1)] YESNO, [WeighFullStatus(2)] YESNO," \
                           f"[WeighFullStatus(3)] YESNO, [WeighFullStatus(4)] YESNO," \
                           f"[WeighStatus] SMALLINT, [TimeStamp] VARCHAR(255)" \
                           f");"
        cursor.execute(sql_create_table)  # 执行SQL语句
    cursor.close()


# 生成 SQL 查询语句 ######################################################################################################
def get_sql_for_saving_a_row(df, table_name):
    sql = " (["
    values = "VALUES ("
    for idx, col in enumerate(df.columns):
        sql += col
        values += "?"
        if idx != len(df.columns) - 1:
            sql += "], ["
            values += ", "
    sql = "INSERT INTO " + table_name + sql + "]) " + values + ")"
    return sql


# 获取数据库中的TimeStamp数据 #############################################################################################
def get_timestamps_from_db(conn, table_name):
    query = f"SELECT DISTINCT TimeStamp FROM `{table_name}`;"  # SQL查找语句：选择TimeStamp列的值
    cursor = conn.cursor()  # 创建新的游标
    cursor.execute(query)  # 执行查找语句
    timestamps = [row.TimeStamp for row in cursor]
    cursor.close()
    return timestamps


########################################################################################################################
def save_csv_to_db(conn, csv_file):

    from Tab0_SortCSVFile import sort_dataframe
    df, controller_serial_no = sort_dataframe(csv_file)  # 使用外接function来处理csv数据

    # ==============================================================================================================
    if not controller_serial_no:  # 如果文件里没有写controller_serial_no，则在文件名中读取
        if "Line1" in csv_file:
            controller_serial_no = "28A10168507"
        elif "Line2" in csv_file:
            controller_serial_no = "28A10168515"

    # ==============================================================================================================
    if controller_serial_no:  # 如果有明确的controller serial number
        # 检查表是否在数据库中，不在则创建表
        check_if_table_exists(conn=conn, table_name=controller_serial_no)
        # 获取sql语句
        sql_save_row = get_sql_for_saving_a_row(df=df, table_name=controller_serial_no)

        # 读取一个csv文件中有几条数据
        num_df_rows = df.shape[0]
        num_saved_rows = 0
        # 将DataFrame中的数据存储进Access数据库中新建的表格内
        for index, row in df.iterrows():

            cursor = conn.cursor()
            # ------------------------------------------------------------------------------------------------------
            timestamp = row["TimeStamp"]  # 获取dataframe中某一行的"TimeStamp"所对应的值
            if timestamp != "" and timestamp != "1970-01-01 00:00:00":
                timestamps = get_timestamps_from_db(conn=conn, table_name=controller_serial_no)
                if timestamp not in timestamps:
                    # 执行SQL语句，储存这一行数据
                    conn.execute(sql_save_row, *row)
                    conn.commit()
                    num_saved_rows = num_saved_rows + 1
            # ------------------------------------------------------------------------------------------------------
            else:
                # 对于其他情况，检查row[4:19]是否在数据库中存在
                cursor.execute(
                    f"SELECT * FROM `{controller_serial_no}` "
                    f"WHERE WeighEmptyPos1 =? AND WeighEmptyPos2=? AND WeighEmptyPos3=? "
                    f"AND WeighFullPos1=? AND WeighFullPos2=? AND WeighFullPos3=? "
                    f"AND WeighRelative1=? AND WeighRelative2=? AND WeighRelative3=? "
                    f"AND WeighResult1=? AND WeighResult2=? AND WeighResult3=?;",
                    tuple(row[8:20])
                )
                if not cursor.fetchall():
                    # 执行SQL语句，储存这一行数据
                    conn.execute(sql_save_row, *row)
                    conn.commit()
                    num_saved_rows = num_saved_rows + 1
            cursor.close()
        # ----------------------------------------------------------------------------------------------------------
        # 弹窗告知用户哪个 CSV 文件已储存完毕
        if num_df_rows == num_saved_rows:
            message = f"文件 {csv_file} 含有{num_df_rows}条数据。\n" \
                      f"储存了{num_saved_rows}条数据\n"
        else:
            message = f"文件 {csv_file} 含有{num_df_rows}条数据。\n" \
                      f"储存了{num_saved_rows}条数据，" \
                      f"剩余{num_df_rows - num_saved_rows}条数据没有被储存，因为其已存在于数据库中\n"
    else:  # 如果没有明确的controller serial number
        message = f"文件 {csv_file} 未储存\n" \
                  f"原因：未获取控制器序列号"

    return message


########################################################################################################################
def main():
    import tkinter as tk
    import sys
    # create a tkinter window
    root = tk.Tk()
    root.withdraw()

    print("Please select the CSV files")
    # 弹窗让用户选择需要处理并存储进数据库的CSV数据文件
    csv_files = filedialog.askopenfilenames(filetypes=[("CSV Files", "*.csv")])
    # 检查用户是否选择了需要处理的CSV数据文件
    if not csv_files:
        sys.exit("Program terminated: No CSV files selected.")

    print("Please select the database file.")
    # 弹窗让用户选择数据库位置
    db_file_path = filedialog.askopenfilename(filetypes=[("Microsoft Access Files", "*.mdb;*.accdb")])
    # 检查用户是否选择了Access数据库
    if not db_file_path:
        sys.exit("Program terminated: No database file selected.")

    #save_csv_files_to_db(db_file_path, csv_files)


if __name__ == "__main__":
    main()
