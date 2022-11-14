import os
from bs4 import BeautifulSoup

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

cranfield_splitter()