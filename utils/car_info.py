import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def get_car_list():
    try:
        url = "https://www.nyc2way.com/nyc2waymap/CarListXML.aspx?clickCounter=1731540432464&CarNo=&Comp=0&CarType=0&JobStat=0&JobType=0"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return ET.fromstring(response.content)
    except Exception as e:
        logger.error(f"Error retrieving car list: {e}")
    return None

def find_car_in_list(root, car_number):
    for marker in root.findall("marker"):
        if marker.get("CarNo") == str(car_number):
            return {
                "lat": marker.get("lat"),
                "lng": marker.get("lng"),
                "CarNo": marker.get("CarNo"),
                "Comp": marker.get("Comp"),
                "CarType": marker.get("CarType"),
                "InShift": marker.get("InShift"),
                "shiftday": marker.get("shiftday")
            }
    return None

def get_car_details(car_number, company):
    try:
        url = f"https://www.nyc2way.com/nyc2waymap/frmOneCarInfo.aspx?clickCounter=1731537369909&Carno={car_number}&Comp={company}&ConfNo="
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            details = soup.find("span", {"id": "Label1"}).get_text(separator=" ", strip=True)

            image_tag = soup.find("img", {"id": "Image1"})
            image_url = f"https://www.nyc2way.com/nyc2waymap/{image_tag['src']}" if image_tag else None

            hidden_field = soup.find("input", {"id": "txtoAddress"})
            hidden_value = hidden_field.get("value") if hidden_field else "Unavailable"

            return details, image_url, hidden_value
    except Exception as e:
        logger.error(f"Error retrieving detailed car information: {e}")
    return None, None, None
