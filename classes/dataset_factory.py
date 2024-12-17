import pandas as pd
from typing import Dict


class DatasetFactory:
    def __init__(self):
        pass


    def merge_datasets(files: list, output_file: str) -> tuple:
        """
        Merge multiple datasets into a single file
        Return:
        - (Merged dataframe, output file path)
        """
        # Load all files into a list
        dfs = [pd.read_csv(file) for file in files]

        # Concatenate all dataframes
        df = pd.concat(dfs, ignore_index=True)

        # Save to a new file
        df.to_csv(output_file, index=False)

        return df, output_file
    


    def split_dataset(file_path: str, output_dir: str, split_ratio: float) -> tuple:
        """
        Split a dataset into train and test sets
        Return:
        - (Train dataframe, Test dataframe)
        """
        df = pd.read_csv(file_path)
        train_df = df.sample(frac=split_ratio, random_state=42)
        test_df = df.drop(train_df.index)
        

        train_df.to_csv(f"{output_dir}/train.csv", index=False)
        test_df.to_csv(f"{output_dir}/test.csv", index=False)

        return train_df, test_df
    


    def filter_dataset(file_path: str, output_file: str, filters: Dict[str, str]) -> pd.DataFrame:
        """
        Filter a dataset based on multiple column values
        Parameters:
        - file_path: str - Path to the input CSV file
        - output_file: str - Path to the output CSV file
        - filters: Dict[str, str] - Dictionary of column names and their corresponding filter values
        Return:
        - Filtered dataframe
        """
        df = pd.read_csv(file_path)
        for column, value in filters.items():
            df = df[df[column] == value]
        df.to_csv(output_file, index=False)

        return df