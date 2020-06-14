from orautil.core.exceptions import BaseTemplateError


class OratabError(BaseTemplateError):
    def __init__(self, calling_object, oratab=None, sid=None, home=None, flags=None):
        self.calling_object = calling_object
        self.msg = f"SID value cannot be empty or None"
        if oratab is not None:
            self.msg = f"Oratab file cannot be void of entries: {oratab}"
        if sid is not None:
            self.msg = f"Oracle SID not found in oratab: {sid}"
        elif home is not None:
            self.msg = f"Oracle home not found in oratab: {home}"
        elif flags is not None:
            self.msg = f"Oracle home autostart flag needs to be: {','.join(flags)}"
        super().__init__(self.msg)


class OracleHomeError(BaseTemplateError):
    def __init__(self, versions=None):
        if versions is not None:
            self.msg = f"Versions {', '.join(str(x) for x in versions)} do not have an Oracle base"
        super().__init__(self.msg)


class InventoryError(BaseTemplateError):
    def __init__(self, orainst_loc=None):
        if orainst_loc is not None:
            self.msg = f"The {orainst_loc} file is devoid of any meaningful content"
        super().__init__(self.msg)
