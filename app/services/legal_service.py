import requests
import xmltodict
import json

class LegalService:
    def __init__(self):
        self.service_key = "qaIu0fhma+YF2g/jj6oxgyyeU9gGRfpKuRlKYjrqMhf/Wy3X55zHijRfQO9Z+9ww85Uu1/edmz5ftXjo7rm4mA=="
        self.base_url = "http://openapi.ccourt.go.kr/openapi/services/IncidentInfoSvc/getIncdntTotalInfo"



    def fetch_incident_info(self, event_no):
        """
        Fetch detailed information about an incident.
        :param event_no: The event number to query.
        :return: JSON response from the API or an error message.
        """
        params = {
            "ServiceKey": self.service_key,
            "eventNo": event_no,
        }
   
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            # XML 데이터를 JSON으로 변환
            xml_data = response.text
            data_dict = xmltodict.parse(xml_data)
            json_data = json.loads(json.dumps(data_dict))  # JSON 형식으로 변환

            # 출력 확인 (필요에 따라 삭제)
            # print(json_data.get("response", {}).get("body", {}).get("items", []))
            
            # 필요한 데이터만 반환
            return json_data.get("response", {}).get("body", {}).get("items", [])
        except requests.exceptions.RequestException as e:
            print(f"HTTP Request Error: {e}")
            return []
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return []