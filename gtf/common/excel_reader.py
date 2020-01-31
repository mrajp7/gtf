import pandas as pd

class ExcelReader():
    def __init__(self, file_path):
        self.file_path = file_path
        self.excel = pd.ExcelFile(file_path)


    def read_sheet(self, sheet_name, index_col=None):
        df = self.excel.parse(sheet_name, index_col=index_col)
        self.curr_df = df
        return df


    def get_value(self, row_index, column_key, default_val=None):
        return self.curr_df.loc[row_index].get(column_key, default_val)