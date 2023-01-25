import requests
import os

notion_api_url = "https://api.notion.com/v1"

headers = {
    "Authorization": f"Bearer {os.environ['KINO_NOTION_TOKEN']}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

response = requests.get(f"{notion_api_url}/databases/{os.environ['KINO_DB_ID']}", headers=headers)

from IPython import embed; embed()
