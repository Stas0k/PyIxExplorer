
import logging

from trafficgenerator.tgn_utils import ApiType, TgnError
from trafficgenerator.tgn_app import TgnApp

from ixexplorer.api.tclproto import TclClient
from ixexplorer.api.ixapi import IxTclHalApi, TclMember, FLAG_RDONLY
from ixexplorer.ixe_object import IxeObject
from ixexplorer.ixe_hw import Chassis, PortGroup

log = logging.getLogger(__name__)


def init_ixe(api, logger, host, port=4555, rsa_id=None):
    """ Create STC object.

    :param api: socket/tcl
    :type api: trafficgenerator.tgn_utils.ApiType
    :param logger: python logger object
    :param host: chassis IP address
    :param port: Tcl server port
    :param rsa_id: full path to RSA ID file for Linux based IxVM
    :return: IXE object
    """

    if api == ApiType.tcl:
        raise TgnError('Tcl API not supported in this version.')

    return IxeApp(logger, IxTclHalApi(TclClient(logger, host, port, rsa_id)), host)


class IxeApp(TgnApp):
    """ This version supports only one chassis. """

    def __init__(self, logger, api_wrapper, host):
        super(self.__class__, self).__init__(logger, api_wrapper)
        IxeObject.api = self.api
        IxeObject.logger = logger
        self.chassis = Chassis(host)
        self.session = Session()

    def connect(self):
        self.api._tcl_handler.connect()
        self.chassis.connect()

    def disconnect(self):
        self.chassis.disconnect()
        self.api._tcl_handler.close()

    def discover(self):
        return self.chassis.discover()


class Session(IxeObject):
    __tcl_command__ = 'session'
    __tcl_members__ = [
            TclMember('userName', flags=FLAG_RDONLY),
            TclMember('captureBufferSegmentSize', type=int),
    ]

    __tcl_commands__ = ['login', 'logout']

    def __init__(self):
        super(self.__class__, self).__init__(objRef='', parent=None)
