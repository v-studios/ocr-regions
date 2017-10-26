#!/usr/bin/env python

import difflib
import sys

from bs4 import BeautifulSoup

# We want to find the boxes containing the labels, then extract their text.
# 1. Find the label's bounding box by its words;
# 2. Move our box "down" to find only the text we want
# 3. Run tesseract on that new bbox
#
# Alternatively:
# 2. Find adjacent boxes left, right and below based on their labels
# 3. Calculate a box based on their borders
# 4. Run tesseract on new box
#
# In all cases tell tesseract to use --psm 7 (single line of text)
# or other Page Segmentation Modes as appropriate

# HOW do we tell tess to only look at a region? there's some UZN file?


# https://stackoverflow.com/questions/43076995/ocr-extracting-fields-from-forms-with-varying-structures


def parse_hocr(hocr_file=None, search_terms=None):
    """Parse the hocr file and find a reasonable bounding box for each of the
    strings in search_terms.  Return a dictionary with values as the bounding
    box to be used for extracting the appropriate text.

    inputs: search_terms = Tuple, A tuple of search terms to look for in the
        HOCR file.

    outputs: box_dict = Dictionary, A dictionary whose keys are the elements of
        search_terms and values are the bounding boxes where those terms are
        located in the document.

    """
    # Make sure the search terms provided are a tuple.
    if not isinstance(search_terms, tuple):
        raise ValueError('The search_terms="{}" parameter must be a tuple, got'
                         ' type={}'.format(search_terms, type(search_terms)))

    # Make sure we got a HOCR file handle when called.
    if not hocr_file:
        raise ValueError('parser must be provided with an HOCR file handle')

    # Open hocr file, read it into BeautifulSoup and extract all the ocr words.
    hocr = open(hocr_file, 'r').read()
    soup = BeautifulSoup(hocr, 'html.parser')
    words = soup.find_all('span', class_='ocrx_word')

    result = dict()

    # Loop through all the words and look for our search terms.
    for word in words:

        w = word.get_text().lower()

        for s in search_terms:

            # If the word is in our search terms, find the bounding box
            if len(w) > 1 and difflib.SequenceMatcher(None, s, w).ratio() > .5:
                bbox = word['title'].split(';')
                bbox = bbox[0].split(' ')
                bbox = tuple([int(x) for x in bbox[1:]])

                # Update the result dictionary or raise an error if the search
                # term is in there twice.
                if s not in result.keys():
                    result.update({s: bbox})

            else:
                pass

    return result


if __name__ == '__main__':
    print('looking in {} for {}'.format(sys.argv[1], tuple(sys.argv[2:])))
    bbox_dict = parse_hocr(hocr_file=sys.argv[1],
                           search_terms=tuple(sys.argv[2:]))
    print(bbox_dict)
    
