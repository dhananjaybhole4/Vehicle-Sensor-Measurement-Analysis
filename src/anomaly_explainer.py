import pandas as pd
from google import genai



class AnomalyExplainer():
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = genai.Client(api_key = self.api_key)

    def ai_explainer(self, filtered_dataframe: pd.DataFrame, file_name: str) -> str:
        
        response = self.client.models.generate_content(
            model = "gemini-3-flash-preview",
            contents = "following is the anomalies found in the given data with extra column named as analysis describing parameters with |z| value higher than 3" \
            "about the dataset please refer - CSV data containing ten vehicle signals logged via the OBD-II interface: Engine coolant temperature, intake manifold absolute pressure, engine RPM, vehicle speed sensor, intake air temperature, air flow rate from mass flow sensor, absolute throttle position, ambient air temperature as well as the accelerator pedal positions D and E. The data was recorded with the OBD-II dongle KIWI 3 from PLX Devices in combination with the smartphone application OBD Auto Doctor from Creosys on an iOS device. The file name is assembled according to the following scheme: <yyyy-mm-dd>_<brand>_<model>_<from>_<to>_<condition>_<extension>.csv - <from> and <to> represent start and end position of the log according to the German number plates, i.e. KA = Karlsruhe etc. - <condition> is a label indicating the principle road conditions (e.g. normal, frei/free, Stau/busy) - <extension> is optional and marks special situations occurring in the vehicle speed data" \
            f"please find the given anomalies {str(filtered_dataframe)} and file name : {file_name}"\
            " your task is to give the summary in short about the anomalies of the given data"
        )
        return response.text