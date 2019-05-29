"""
Register me silly

Notifies me when classes are available

Author:  Anshul Kharbanda
Created: 5 - 26 - 2019
"""
from requests import get
from bs4 import BeautifulSoup

def is_enrollment_row(tag):
    """
    True if the tag is an enrollment row

    :param tag: the tag to check

    :return: true if the tag is an enrollment row
    """
    is_tr = tag.name == 'tr'
    cells = tag.find_all('td')
    has_2_cells = len(cells) == 2
    has_enrollment_title = cells[0].get_text() == 'Enroll' \
        if has_2_cells else False
    return is_tr and has_2_cells and has_enrollment_title


def has_enrollment_available(url):
    """
    Returns true if the url has enrollment available

    :param url: the url of the class to pull from

    :return: true if the url has enrollment available
    """
    try:

        # Get soup
        soup = BeautifulSoup(get(url).content, 'html.parser')

        # Return true if enrollment row is not closed
        return soup.find(is_enrollment_row).find_all('td')[1].get_text() != 'CLOSED'

    # Retrn false if anything
    except Exception as e:
        return False
