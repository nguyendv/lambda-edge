"""
tests.test_config
~~~~~~~~~~~~~~~~~

Unit testing for ledge.config module
"""

from ledge import config

def test_set():
    config.set('test94032xcx', 'value')
    assert config.get('test94032xcx') == 'value'

    config.set('bleubleu', 2)
    assert config.get('bleubleu') == 2

def test_delete():
    config.delete('test94032xcx')
    assert config.get('test94032xcx') == None

    config.delete('bleubleu')
    assert config.get('bleubleu') == None
