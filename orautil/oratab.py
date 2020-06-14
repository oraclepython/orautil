from pathlib import Path
from typing import Any, Union

from orautil.core.functions import is_file, is_readable, to_path
from orautil.core.helpers import SpecialDict
from orautil.exceptions import OratabError


class Oratab(object):
    _oratab: Union[Path, Any]

    def __init__(self, tab=None):
        if tab is not None:
            self.tab = tab
            assert self.entries

    def __call__(self, tab):
        self.tab = tab
        assert self.entries
        return self

    def __getitem__(self, item):
        return self.entries[item]

    @property
    def entries(self):
        entries = {}
        with open(self.tab, "r") as f:
            for line in f.readlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                sid, home, _autostart = line.split(":")
                _autostart = _autostart.split()[0]
                entries[sid] = [home, _autostart]
        if len(entries) == 0:
            raise OratabError(self, oratab=self.tab)
        return entries

    @property
    def sids(self):
        return list(set([item for item in self.entries.keys()]))

    @property
    def homes(self):
        homes = SpecialDict()
        for key, value in self.entries.items():
            home, _ = value
            homes[home] = key
        return homes

    @property
    def autostart(self):
        status = SpecialDict()
        for key, value in self.entries.items():
            _, autostart_status = value
            status[autostart_status] = key
        return status

    @property
    def tab(self):
        return self._oratab

    @tab.setter
    def tab(self, filename):
        is_file(filename)
        is_readable(filename)
        self._oratab = Path(filename)

    def check_oracle_sid(self, sid: str) -> str:
        """
        incoming "sid" is checked against the sanitized list of all SIDs listed in oratab
        :param sid: a string
        :returns: a string
        :raises: OratabError, when sid not found in oratab
        """
        if sid is None:
            raise OratabError(self)
        elif sid.strip("/") not in self.sids:
            raise OratabError(self, sid=sid)
        else:
            return sid

    def check_oracle_home(self, home):
        """
        incoming "home" argument is checked for being a director, for read, write, execution bits, and then checked
        against the sanitized list of all oracle homes listed in oratab
        :param home: a string
        :return: home: a Path
        :raises: OratabError, when oracle home not found in oratab
        """
        if home in self.homes.keys():
            return to_path(home)
        else:
            raise OratabError(self, home=home)

    def get_home(self, sid: str):
        """
        returns the home base on the incoming SID argument. If nocheck is True, it does not call
        "check_oracle_home" function
        :param sid: a string
        :returns: str object
        """
        self.check_oracle_sid(sid)
        return self.entries[sid][0]

    def get_sid(self, home):
        """
        returns the sid(s) associated with a specific Oracle home
        :param home:
        :return:
        """
        self.check_oracle_home(home)
        return self.homes[home]
