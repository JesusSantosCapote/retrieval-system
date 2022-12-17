import os
from bs4 import BeautifulSoup
import re

def cranfield_splitter():
    in_path = 'cranfieldDocs'
    out_path = 'splitted_cranfieldDocs'
    filenames = os.listdir(in_path)

    for fname in filenames:

        # generate filenames
        infilepath = in_path + '/' + fname
        outfilepath = out_path + '/' + fname

        with open(infilepath) as infile:
            with open(outfilepath, 'w') as outfile:

                # read all text in a file
                fileData = infile.read()

                # creating BeautifulSoup object to extract text between SGML tags
                soup = BeautifulSoup(fileData)

                # extract text of a particular SGML <tag>
                title = soup.findAll('title')
                text = soup.findAll('text')

                # converting to string
                title = ''.join(map(str, title))
                text = ''.join(map(str, text))

                # remove the SGML <tag> from text
                title = title.replace('title', '')
                text = text.replace('text', '')

                # write tokens for <title> into new file
                outfile.write(title)
                outfile.write(" ")

                # write tokens for <text> into new file
                outfile.write(text)
            outfile.close()
        infile.close()

def cisi_splitter():
    in_path = 'cisi_corpus'
    out_path = 'splitted_cisi'

    with open(in_path + '/' + 'CISI.txt') as f:
        lines = ""
        for l in f.readlines():
            lines += "\n" + l.strip() if l.startswith(".") else " " + l.strip()
        lines = lines.lstrip("\n").split("\n")
    f.close()

    doc_id = ""
    doc_text = ""
    for l in lines:
        if l.startswith(".I"):
            doc_id = l.split(" ")[1].strip()

        elif l.startswith(".X"):
            outfilepath = out_path + '/' + doc_id
            with open(outfilepath, 'w') as outfile:
                outfile.write(doc_text)
            outfile.close()

            doc_id = ""
            doc_text = ""

        else:
            doc_text += "\n" + l.strip()[3:] + " "