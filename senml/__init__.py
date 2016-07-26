"""This module provides a Python API for SenML handling"""
#pylint: disable=too-few-public-methods

from .senml import SenMLDocument, SenMLMeasurement

__version__ = '0.1.0'

__all__ = [
    'SenMLDocument',
    'SenMLMeasurement',
]
