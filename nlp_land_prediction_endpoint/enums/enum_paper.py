"""This module implements all enums used."""
from enum import Enum


class ExtractionMethod(str, Enum):
    """Which extraction method to use.

    Args:
        str ([type]): The type of this enum.
        Enum ([Any]): The parent class of this enum.
    """

    GROBID = "grobid"
    ANTHOLOGY = "anthology"
    RULEBASED = "rulebased"


class TypeOfPaper(str, Enum):
    """Which type of paper to use.

    Args:
        str ([type]): The type of this enum.
        Enum ([Any]): The parent class of this enum.
    """

    JOURNAL = "journal"
    CONFERENCE = "conference"
    DEMO = "demo"
    WORKSHOP = "workshop"
    POSTER = "poster"
    TUTORIAL = "tutorial"
    DOCTORAL_CONSORTIUM = "doctoral_consortium"
    OTHER = "other"


class ShortLong(str, Enum):
    """Which size of paper to use.

    Args:
        str ([type]): The type of this enum.
        Enum ([Any]): The parent class of this enum.
    """

    SHORT = "short"
    LONG = "long"
    UNKNOWN = "unknown"
