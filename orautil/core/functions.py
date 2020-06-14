import os
from pathlib import Path

from lxml import etree

from orautil.core.exceptions import LocationError

__all__ = [
    "to_path",
    "is_dir",
    "is_file",
    "is_readable",
    "is_writable",
    "is_executable",
    "get_tree",
]


def to_path(location: [str, Path]) -> Path:
    try:
        p = Path(location)
    except TypeError:
        raise LocationError(empty=True)
    else:
        return p


def is_dir(location: [str, Path]) -> Path:
    p = to_path(location)
    try:
        if not p.is_dir():
            raise LocationError(dirname=p)
        else:
            return p
    except PermissionError:
        is_readable(p.as_posix())


def is_file(location: [str, Path]) -> Path:
    p = to_path(location)
    try:
        if not p.is_file():
            raise LocationError(filename=p)
        else:
            return p
    except PermissionError:
        is_readable(p.as_posix())


def is_readable(location: [str, Path]) -> Path:
    p = to_path(location)
    if not os.access(p.as_posix(), os.R_OK):
        raise LocationError(readable=p)
    else:
        return p


def is_writable(location: [str, Path]) -> Path:
    p = to_path(location)
    if not os.access(p.as_posix(), os.W_OK):
        raise LocationError(writeable=p)
    else:
        return p


def is_executable(location: [str, Path]) -> Path:
    p = to_path(location)
    if not os.access(p.as_posix(), os.X_OK):
        raise LocationError(executable=p)
    else:
        return p


def get_tree(xml: Path) -> etree:
    try:
        assert isinstance(xml, Path)
    except AssertionError:
        xml = to_path(xml)
    finally:
        is_file(xml)
        is_readable(xml)
        return etree.parse(xml.as_posix())
