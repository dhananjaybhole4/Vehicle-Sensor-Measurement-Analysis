import pandas as pd
from google import genai
from google.genai import errors
from google.genai import types

import logging

from utils.stats import get_columns_stats_tool

logger = logging.getLogger()

get_stats_declaration = {
    "name":"get_columns_stats_tool",
    "description":"Returns the mean and standard deviation of a given column in the vehicle sensor dataset, so you can judge whether a value is normal or anomalous",
    "parameters":{
        "type": "object",
        "properties":{
            "column": {
                "type": "string",
                "description": "the exact column name to get statistic for"
            },
        },
        "required": ["column"]
    },
}

class AnomalyExplainer():
    def __init__(self, api_key: str, max_tool_iteration: int):
        self.api_key = api_key
        self.client = genai.Client(api_key = self.api_key)
        self.max_tool_iteration = max_tool_iteration

    def ai_explainer(self, df: pd.DataFrame, filtered_dataframe: pd.DataFrame, file_name: str) -> str:

        prompt = (
            "following is the anomalies found in the given data with extra column named as analysis describing parameters with |z| value higher than 3"
            "about the dataset please refer - CSV data containing ten vehicle signals logged via the OBD-II interface: ..."
            f"please find the given anomalies {str(filtered_dataframe)} and file name : {file_name}"
            " your task is to give the summary in short about the anomalies of the given data."
            " You may call get_columns_stats_tool if you need the normal mean/std for a column to judge how unusual a value is."
        )

        tool = types.Tool(function_declarations = [get_stats_declaration])
        config = types.GenerateContentConfig( tools = [tool])

        contents = [
            types.Content(role = "user", parts = [types.Part.from_text(text = prompt)])
        ]

        try:
            response = self.client.models.generate_content(
                model = "gemini-3-flash-preview",
                contents = contents,
                config = config
            )
            i = 0
            while (response.function_calls):

                i += 1
                if i >= self.max_tool_iteration:
                    return "incomplete: exceeded maximum tool call attempts"
                
                function_call = response.function_calls[0]
                logger.info("Model requested tool call: %s with args %s", function_call.name, function_call.args)

                if function_call.name == "get_columns_stats_tool":
                    result = get_columns_stats_tool(df, **function_call.args)
                else:
                    result = "unknown function called"

                contents.append(response.candidates[0].content)
                contents.append(
                    types.Content(
                        role = "user",
                        parts = [types.Part.from_function_response(
                            name = function_call.name,
                            response = {"result": result}
                        )]
                    )
                )

                response = self.client.models.generate_content(
                    model = "gemini-3-flash-preview",
                    contents = contents,
                    config = config,
                )

            return response.text
        
        except errors.ServerError:
            logger.warning("Failed to get response from the Gemini")
            return "Ai summary not available due to some error"