from scripts import collect, notion
import logging
import click


def import_highlights(filepath="./highlights.json"):
    """Import locally saved highlights JSON file"""
    logging.info(f"Importing highlights from {filepath}...")
    with open(filepath, "r") as filename:
        highlights = json.load(filename)
    return highlights


def export_highlights(highlights, filepath="./highlights.json"):
    """Export highlights locally as JSON file"""
    logging.info(f"Saving highlights to {filepath}")
    with open(filepath, "w") as outfile:
        json.dump(highlights, outfile)
    return


def retrieve_highlights(collect_highlights):
    """Retrieve highlights via Kindle Notebook or local file"""

    if collect_highlights:
        highlights = collect.retrieve_highlights()
        export_highlights(highlights)
    else:
        logging.info("Skipping collection of highlights...")
        highlights = import_highlights()

    return highlights


@click.command()
@click.option("--collect-highlights", type=bool, default=True)
@click.option("--upload-highlights", type=bool, default=True)
def main(collect_highlights, upload_highlights):

    logging.basicConfig(filename="log", level=logging.INFO)

    highlights = retrieve_highlights(collect_highlights)

    if upload_highlights:
        notion_books = notion.retrieve_books()
    else:
        logging.info("Skipping upload of highlights...")

    from IPython import embed; embed()

    logging.info("Finished.")
    return


if __name__ == "__main__":
	main()
