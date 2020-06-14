from orautil.oratab import Oratab
from orautil.core.logging import initialize_logging
from orautil.oraclehome import OracleHome
from orautil.core.exceptions import *
from orautil.exceptions import *

log = initialize_logging(__name__)


def get_oratab(tab="/etc/oratab"):
    try:
        oratab = Oratab(tab)
    except (LocationError, OratabError) as e:
        log.error(e)
        return None
    else:
        return oratab


def oraenv(sid: str, tab="/etc/oratab"):
    oratab = get_oratab(tab)
    if not oratab:
        return None
    try:
        oracle_home = OracleHome(oratab.get_home(sid))
    except OratabError as e:
        log.error(e)
        return None
    else:
        import os

        os.environ["ORACLE_SID"] = sid
        os.environ["ORACLE_HOME"] = oracle_home.oracle_home
        os.environ["LD_LIBRARY_PATH"] = oracle_home.ld_library_path
        os.environ["ORACLE_BASE"] = oracle_home.oracle_base
        os.environ["PATH"] += os.pathsep + oracle_home.bindir
        os.environ["PATH"] += os.pathsep + oracle_home.opatch
        os.environ["TNS_ADMIN"] = oracle_home.tns_admin
        return oracle_home
