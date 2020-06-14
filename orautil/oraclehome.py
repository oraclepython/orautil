from orautil import VERSIONS
from orautil.core.functions import (
    is_file,
    is_dir,
    is_readable,
    is_executable,
    to_path,
    get_tree,
)
from .exceptions import OracleHomeError


class OracleHome(object):
    def __init__(self, oracle_home):
        self.oracle_home = oracle_home

    @property
    def oracle_home(self):
        """
        Retrieves the Oracle home Path object
        :return: a Path object
        """
        return self._oracle_home

    @oracle_home.setter
    def oracle_home(self, location: str):
        """
        Sets the Oracle home constructor of the OracleHome object. The rest of the properties are determined based
        on this oracle_home
        :param location: string
        :return: None
        """
        is_dir(location)
        is_readable(location)
        self._oracle_home = to_path(location)

    @property
    def comps_xml(self):
        xml = self.oracle_home / "inventory" / "ContentsXML" / "comps.xml"
        is_readable(xml)
        return xml

    @property
    def _xpath_comps_xml(self):
        return get_tree(self.comps_xml).xpath("//COMP")

    @property
    def oracle_home_type(self):
        """
        Oracle home type, i.e. "oracle.server" or "oracle.crs". It is also used in composing the path to the
        globalvariables.xml file
        :return: a string
        """
        return self._xpath_comps_xml[0].get("NAME")

    @property
    def edition(self):
        """
        Based on the major version, it returns the Oracle edition, i.e.: "SE", "EE". Oracle 9, 10 have different
        locations for the global variables, in comparison with 11, 12, 18, 19
        :return: a string
        """
        if self.major_version in VERSIONS[2:]:
            # define the $ORACLE_HOME/inventory/globalvariables/oracle.server/globalvariables.xml
            global_variables_xml = (
                self.oracle_home
                / "inventory"
                / "globalvariables"
                / f"{self.oracle_home_type}"
                / "globalvariables.xml"
            )
            return [
                item.get("VALUE")
                for item in get_tree(global_variables_xml).xpath("//GLOBALVARS/VAR")
                if item.get("NAME") == "oracle_install_db_InstallType"
            ][0]
        elif VERSIONS[1:2] == self.major_version:
            # define the $ORACLE_HOME/inventory/Components21/oracle.server/{full_version}/context.xml
            context_xml = (
                self.oracle_home
                / "inventory"
                / "Components21"
                / "oracle.server"
                / f"{self.version}"
                / "context.xml"
            )
            for item in get_tree(context_xml).xpath("//COMP_CONTEXT/VAR_LIST/VAR"):
                if item.get("NAME") in ["s_serverInstallType", "s_installType"]:
                    return to_path(item.get("VAL"))

    @property
    def version(self):
        """
        Full version of the Oracle home
        https://tinyurl.com/y9np5xpk
        :returns: a tuple of integers
        """
        return tuple(int(ver) for ver in self._xpath_comps_xml[0].get("VER").split("."))

    @property
    def major_version(self):
        """
        Major version of the Oracle home
        :returns: an integer
        """
        return self.version[0]

    @property
    def readable_version_short(self):
        """
        Human readable version of the Oracle home, in format "12.1", "11.2"
        :returns: a string
        """
        return ".".join((f"{i}" for i in self.version[:2]))

    @property
    def readable_version_full(self):
        """
        Full human readable version of the Oracle home, in format "12.1.0.2.0", "11.2.0.4.0"
        :returns: a string
        """
        return ".".join((f"{i}" for i in self.version))

    @property
    def database_maintenance_version(self):
        """
        Database maintenance version of the Oracle home
        :returns: an integer
        """
        return self.version[1]

    @property
    def application_server_version(self):
        """
        Application server version of the Oracle home
        :returns: an integer
        """
        return self.version[2]

    @property
    def component_specific_version(self):
        """
        Component specific version of the Oracle home
        :returns: an integer
        """
        return self.version[3]

    @property
    def platform_specific_version(self):
        """
        Platform specific version of the Oracle home
        :returns: an integer
        """
        return self.version[4]

    @property
    def oracle_base(self):
        if self.major_version == VERSIONS[1]:
            raise OracleHomeError(VERSIONS[:2])
        elif self.major_version in VERSIONS[2:]:
            ohp_xml = (
                self.oracle_home
                / "inventory"
                / "ContentsXML"
                / "oraclehomeproperties.xml"
            )
            is_file(ohp_xml)
            is_readable(ohp_xml)
            xpath_ohp_xml = get_tree(ohp_xml).xpath(
                "//ORACLEHOME_INFO/PROPERTY_LIST/PROPERTY"
            )
            oracle_base = [
                item.get("VAL")
                for item in xpath_ohp_xml
                if item.get("NAME") == "ORACLE_BASE"
            ][0]
            is_dir(oracle_base)
            is_readable(oracle_base)
            return to_path(oracle_base)

    @property
    def diagnostic_dest(self):
        folder = self.oracle_base / "diag"
        is_dir(folder)
        is_readable(folder)
        return folder

    @property
    def crs_home(self):
        getcrshome = self.oracle_home / "srvm" / "admin" / "getcrshome"
        from subprocess import Popen, PIPE

        try:
            process = Popen(getcrshome.as_posix(), stdout=PIPE)
            (output, err) = process.communicate()
        except FileNotFoundError:
            return None
        else:
            return output

    @property
    def tns_admin(self):
        """
        retrieves oracle_home + network + admin
        :return: a Path object
        """
        folder = self.oracle_home / "network" / "admin"
        is_dir(folder)
        is_readable(folder)
        return folder

    @property
    def ld_library_path(self):
        """
        retrieves oracle_home + lib
        :return: a Path object
        """
        folder = self.oracle_home / "lib"
        is_dir(folder)
        is_readable(folder)
        return folder

    @property
    def opatch(self):
        """
        retrieves oracle_home + OPatch + opatch binary
        :return: a Path object
        """
        binary = self.oracle_home / "OPatch" / "opatch"
        is_file(binary)
        is_executable(binary)
        return binary

    @property
    def opatchauto(self):
        """
        retrieves oracle_home + OPatch + opatchauto binary
        :return: a Path object
        """
        binary = self.oracle_home / "OPatch" / "opatchauto"
        is_file(binary)
        is_executable(binary)
        return binary

    @property
    def sqlplus(self):
        """
        retrieves oracle_home + bin + sqlplus binary
        :return: a Path object
        """
        binary = self.oracle_home / "bin" / "sqlplus"
        is_file(binary)
        is_executable(binary)
        return binary

    @property
    def rman(self):
        """
        retrieves oracle_home + bin + rman binary
        :return: a Path object
        """
        binary = self.oracle_home / "bin" / "rman"
        is_file(binary)
        is_executable(binary)
        return binary
