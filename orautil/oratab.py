from orautil.core.helpers import SpecialDict


class Oratab(object):
    def __init__(self, tab="/etc/oratab"):
        self.tab = tab

    def __call__(self, tab):
        self.tab = tab

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
        return entries

    @property
    def sid(self):
        return list(set([item for item in self.entries.keys()]))

    @property
    def home(self):
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
