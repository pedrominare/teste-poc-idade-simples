from src.utils.load_file import create_df_from_large_xlsx


class BuildDF:
    def __init__(self, xlsx_name, sheet_name, skiprows, chunk_size):
        self.skiprows = skiprows
        self.sheet_name = sheet_name
        self.df = create_df_from_large_xlsx(
            file_name=xlsx_name,
            start_row=skiprows,
            chunk_size=chunk_size
        )
        self.variables = None

    def get_variables(self):
        self.variables = self.df.columns.tolist()
