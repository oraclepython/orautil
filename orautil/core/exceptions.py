class BaseTemplateError(Exception):
    def __init__(self, msg=""):
        self.msg = msg
        super(BaseTemplateError, self).__init__(self.msg)

    def __str__(self):
        return self.msg

    def __repr__(self):
        return self.msg


class LocationError(BaseTemplateError):
    def __init__(
        self,
        empty=None,
        dirname=None,
        filename=None,
        readable=None,
        writeable=None,
        executable=None,
    ):
        if empty is True:
            self.msg = f"Location argument cannot be empty"
        elif dirname is not None:
            self.msg = f"Folder does not exist: {dirname}"
        elif filename is not None:
            self.msg = f"Filename does not exist: {filename}"
        elif readable is not None:
            self.msg = f"Location not readable: {readable}"
        elif writeable is not None:
            self.msg = f"Location not writable: {writeable}"
        elif executable is not None:
            self.msg = f"Location not executable: {executable}"
        super().__init__(self.msg)
