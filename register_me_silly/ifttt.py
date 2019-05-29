"""
Register me silly

Notifies me when classes are available

Author:  Anshul Kharbanda
Created: 5 - 26 - 2019
"""
from requests import post
from flask import current_app

def trigger(event, value1='', value2='', value3=''):
    """
    Trigger event on remote server

    :param event: event name to trigger
    :param value1: first value to send (optional)
    :param value2: second value to send (optional)
    :param value3: third value to send (optional)

    :return: http response
    """
    key = current_app.config['IFTTT_KEY']
    return post(
        f'https://maker.ifttt.com/trigger/{event}/with/key/{key}',
        data={
            'value1': value1,
            'value2': value2,
            'value3': value3
        })
