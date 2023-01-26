import requests
import os
import json
import logging
from datetime import datetime

notion_api_url = "https://api.notion.com/v1"

headers = {
    "Authorization": f"Bearer {os.environ['KINO_NOTION_TOKEN']}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}


def retrieve_books():
    """Retrieve book block info from Notion Page"""

    response = requests.get(f"{notion_api_url}/blocks/{os.environ['KINO_PAGE_ID']}/children", headers=headers)
    data = json.loads(response.content)

    book_blocks = []
    for block in data["results"]:
        if block["type"] == "child_page":
            block_info = {"title": block["child_page"]["title"], "id": block["id"]}
            book_blocks.append(block_info)

    return book_blocks


def export_highlights_to_notion(highlights, notion_book_titles):
    """Export highlights to Notion via API"""

    for book_info in highlights:

        book_title_display = book_info["title"].split(":")[0]

        if book_title_display in notion_book_titles:
            logging.info(f"Skipping title already in Notion: {book_title_display}")
            continue

        logging.info(f"Creating Notion Page for title: {book_title_display}")

    return


#response = requests.get(f"{notion_api_url}/databases/{os.environ['KINO_DB_ID']}", headers=headers)

#data = {"parent": {"type": "database_id", "database_id": os.environ["KINO_DB_ID"]}, "properties": {"Name": {"type": "title", "title": [{"type": "text", "text": {"content": "Tomatoes"}}]}, "test": {"type": "number", "number": 1}}}
#data = json.dumps(data)
#response = requests.post(f"{notion_api_url}/pages", headers=headers, data=data)

"""
notion_book_titles = retrieve_book_titles_in_notion()
print(notion_book_titles)

highlights = import_highlights()

export_highlights_to_notion(highlights, notion_book_titles)

from IPython import embed; embed()
"""
