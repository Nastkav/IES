import json
import logging
from typing import List

import requests

from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_api_gateway import StoreGateway


class StoreApiAdapter(StoreGateway):
    api_base_url: str

    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]) -> bool:
        # Make a POST request to the Store API endpoint with the processed data
        try:
            sent_data = [processed_agent_data.serialize() for processed_agent_data in processed_agent_data_batch]
            response = requests.post(self.api_base_url+'/processed_agent_data/',
                                     data=json.dumps(sent_data))
            if response.status_code in (200, 201):
                logging.info("Data sent to Store API")
                return True
            else:
                logging.info("Sending data failed with status code" + str(response.status_code))
                return False
        except requests.exceptions.RequestException as e:
            logging.info("Request failed with error: " + str(e))
            return False
