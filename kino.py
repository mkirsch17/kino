import logging
import collect, test

def main():
    logging.basicConfig(filename="log", level=logging.INFO)

    highlights = collect.retrieve_highlights()
    collect.save_highlights(highlights)

    return


if __name__ == "__main__":
	main()
