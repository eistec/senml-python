"""@package senml
Top-level namespace for the senml module
"""

#pylint: disable=too-few-public-methods

from .senml import SenMLDocument, SenMLMeasurement

__version__ = '0.1.0'

__all__ = [
    'SenMLDocument',
    'SenMLMeasurement',
]
