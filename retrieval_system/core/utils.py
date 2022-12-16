import os
from typing import Tuple
from bs4 import BeautifulSoup


def parse_cranfield_splitter(in_path):
    filenames = os.listdir(in_path)

    for fname in filenames:

        # generate filenames
        infilepath = in_path + "/" + fname

        with open(infilepath) as infile:

            # read all text in a file
            fileData = infile.read()

            # creating BeautifulSoup object to extract text between SGML tags
            soup = BeautifulSoup(fileData)

            # extract text of a particular SGML <tag>
            title = soup.findAll("title")
            text = soup.findAll("text")
            author = soup.findAll("author")

            # converting to string
            title = "".join(map(str, title))
            text = "".join(map(str, text))
            author = "".join(map(str, author))

            # remove the SGML <tag> from text
            title = title.replace("<title>", "")
            title = title.replace("</title>", "")
            text = text.replace("<text>", "")
            text = text.replace("</text>", "")
            author = author.replace("<author>", "")
            author = author.replace("</author>", "")


def parse_cranfield_file(file_path: str) -> Tuple[str, str, str]:
    """Parse a single Cranfield file.

    Args:
        file_path (str): Path to the Cranfield file.

    Returns:
        Tuple[str, str, str]: Tuple containing the title, text and author of the Cranfield file.
    """

    with open(file_path) as infile:

        # read all text in a file
        file_data = infile.read()

        # creating BeautifulSoup object to extract text between SGML tags
        soup = BeautifulSoup(file_data)

        # extract text of a particular SGML <tag>
        title = soup.findAll("title")
        text = soup.findAll("text")
        author = soup.findAll("author")

        # converting to string
        title = "".join(map(str, title))
        text = "".join(map(str, text))
        author = "".join(map(str, author))

        # remove the SGML <tag> from text
        title = title.replace("<title>", "")
        title = title.replace("</title>", "")
        text = text.replace("<text>", "")
        text = text.replace("</text>", "")
        author = author.replace("<author>", "")
        author = author.replace("</author>", "")

        title = title.strip()
        text = text.strip()
        author = author.strip()

        if author == "":
            author = "Unknown"

        return title, text, author
