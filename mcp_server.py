import pandas as pd
from mcp.server.mcpserver import MCPServer

from pathlib import Path
from datetime import datetime

from src.ingest import DataLoader
from src.anomaly_detector import AnomalyDetector
from src.anomaly_report import AnomalyReport
from utils import stats

# define paramters
CONTAMINATION = 0.02
RANDOM_STATE = 42

# make object of classes
dataloader = DataLoader()
anomaly_detector = AnomalyDetector()
anomaly_report = AnomalyReport()

mcp = MCPServer("Vehicle Sensor Measurement Analysis")

@mcp.tool()
def ingest_csv(csv_path: str) -> str:
    """read the csv file present at the path passed in argument and outputs summary containing shape, name of columns and the csv file path.

    Args:
        csv_path (str): path of the csv file in the repository

    Returns:
        str: summary of csv file containing shape of the file, name of columns present in the file and the file path
    """
    df = dataloader.csv_extractor(Path(csv_path))

    return f"shape: {df.shape}, columns: {df.columns}, file path: {csv_path}"

@mcp.tool()
def detect(path:str) -> str:
    """detect anomalies from the csv file present at the path passed in the argument using the Isolation forest algorithm and save it at a certain path in the csv format.

    Args:
        path (str): path of the input csv file

    Returns:
        str: summary of anomalies csv file containing shape of the file, name of columns present in the file and the file path
    """
    save_folder_path = Path(__file__).parent/"csv_log"
    save_folder_path.mkdir(parents = True, exist_ok = True)

    timestamp = datetime.now().strftime("%d:%m:%Y,%H:%M:%S")
    save_path = save_folder_path/f"detect_{timestamp}.csv"

    df = dataloader.csv_extractor(Path(path))
    anomalies = anomaly_detector.detect(df)
    anomalies.to_csv(save_path)

    return f"shape of anomalies: {anomalies.shape}, columns in anomalies: {anomalies.columns}, anomalies saved as a csv at the following path: {save_path}"

@mcp.tool()
def report_csv(data_path:str, anomaly_data_path:str) -> str:
    """make a report (in the form of csv) from anomalies stored in the csv format at the input anomaly_data_path, report contains a additional column named analysis
    which have information about |z| values of parameters in a row if their |z| values are greater than 3

    Args:
        data_path (str): path of the csv file containing original data
        anomaly_data_path(str): path of the csv file containing anomaly data

    Returns:
        str: summary of the report containing shape of the report, columns in the report and path where report is stored
    """
    
    # get data in the format of pd.DataFrame from csv files
    df = dataloader.csv_extractor(data_path)
    anomalies = dataloader.csv_extractor(anomaly_data_path)

    # paths
    report_folder_path = Path(__file__).parent/"report"

    timestamp = datetime.now().strftime("%d:%m:%Y,%H:%M:%S")
    report_name = f"report_{timestamp}"

    # generate report
    _ = anomaly_report.report(df, anomalies, report_folder_path, report_name)

    # conversion of csv to dataframe to get meta data
    df_report = dataloader.csv_extractor(report_folder_path/(report_name + ".csv"))

    return f"shape of the report: {df_report.shape}, columns in the report: {df_report.columns}, path of report: {report_folder_path/(report_name + ".csv")}"

@mcp.tool()
def filtered_report(data_path:str, anomaly_data_path:str) -> str:
    """output the filtered report (in the form of string) with its meta data for further task like ai summary from the given data and anomalies  

    Args:
        data_path (str): path of the csv containing given data
        anomaly_data_path (str): path of the csv containing anomalies data

    Returns:
        str: filtered report dataframe and its meta data
    """
    # get data in the format of pd.DataFrame from csv files
    df = dataloader.csv_extractor(data_path)
    anomalies = dataloader.csv_extractor(anomaly_data_path)

    # generate filtered anomaly dataframe
    filtered_anomalies = anomaly_report.report(df, anomalies, make_report = False)

    return f"filtered anomalies: {filtered_anomalies}, shape of the filtered anomalies: {filtered_anomalies.shape}, columns: {filtered_anomalies.columns}"

@mcp.tool()
def get_columns_stats(data_path:str, column_name:str) -> str:
    """output the mean and standard deviation of the requested column in the given dataframe

    Args:
        data_path (str): path of the csv containing given data
        column_name (str): column name

    Returns:
        str: mean and standard deviation of the column
    """
    # get data in the format of pd.DataFrame from csv files
    df = dataloader.csv_extractor(data_path)

    if column_name not in df.columns:
        return "column not found in dataframe"
    
    mean, std = stats.get_columns_stats(df, column_name)

    return f"mean of the {column_name}: {mean} and standard deviation of the {column_name}: {std}"


if __name__ == "__main__":
    mcp.run()