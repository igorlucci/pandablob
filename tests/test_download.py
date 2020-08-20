"""Test downloading a blob and returning a DataFrame."""

import io
from pathlib import Path

import pandas as pd
import pytest

import pandablob

FILES = Path.cwd().joinpath("tests", "test_files")
FILES_IO = Path.cwd().joinpath("tests", "test_io")

PANDAS_ARGUMENTS = {
    "csv": {"delimiter": ",", "index_col": 0},
    "json": {"orient": "index"},
    "txt": {"delimiter": ",", "index_col": 0},
    "xls": {"index_col": 0},
    "xlsx": {"index_col": 0},
}


@pytest.mark.parametrize("file", ["csv", "json", "txt", "xls", "xlsx"])
def test_download(file, mock_download):
    """Mock uploading to the azure blob."""

    # Create required input
    file_name = f"test_data.{file}"
    file_location = FILES.joinpath(file_name)
    extension = file_location.suffix

    # Get mock object from fixture
    MockAzureBlob = mock_download(file_name, file_location)

    # Download blob and make DataFrame
    df = pandablob.blob_to_df(MockAzureBlob)

    # Make DataFrame from original file and compare
    if extension == ".csv" or extension == ".txt":
        compare_df = pd.read_table(file_location)
        assert df.equals(compare_df)
    if extension == ".json":
        compare_df = pd.read_json(file_location)
        assert df.equals(compare_df)
    if extension == ".xlsx" or extension == ".xls":
        compare_df = pd.read_excel(file_location)
        assert df.equals(compare_df)
