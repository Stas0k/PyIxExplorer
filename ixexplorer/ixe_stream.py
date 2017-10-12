
from ixexplorer.api.ixapi import TclMember, MacStr
from ixexplorer.ixe_object import IxeObject


class IxeStream(IxeObject):
    __tcl_command__ = 'stream'
    __tcl_members__ = [
            TclMember('bpsRate', type=int),
            TclMember('da', type=MacStr),
            TclMember('name'),
            TclMember('sa', type=MacStr),
    ]

    __tcl_commands__ = ['export', 'write']

    def __init__(self, parent, uri):
        super(self.__class__, self).__init__(uri=uri.replace('/', ' '), parent=parent)

    def remove(self):
        self._ix_command('remove')
        self._ix_command('write')
        self.del_object_from_parent()

    def get_ip(self):
        return self.get_object('_ip', IxeIp)
    ip = property(get_ip)

    def get_protocol(self):
        return self.get_object('_protocol', IxeProtocol)
    protocol = property(get_protocol)

    def get_object(self, field, ixe_object):
        if not hasattr(self, field):
            setattr(self, field, ixe_object(parent=self))
        getattr(self, field).ix_set_default()
        return getattr(self, field)


class IxeStreamObj(IxeObject):

    def __init__(self, parent):
        super(IxeStreamObj, self).__init__(uri=parent.uri[:-2], parent=parent)

    def ix_get(self, member=None):
        self.parent.ix_get(member)
        super(IxeStreamObj, self).ix_get(member)

    def ix_set(self, member=None):
        super(IxeStreamObj, self).ix_set(member)
        self.parent.ix_set(member)


class IxeProtocol(IxeStreamObj):
    __tcl_command__ = 'protocol'
    __tcl_members__ = [
            TclMember('ethernetType'),
            TclMember('name'),
    ]

    def ix_get(self, member=None):
        self.parent.ix_get(member)

    def ix_set(self, member=None):
        pass


class IxeIp(IxeStreamObj):
    __tcl_command__ = 'ip'
    __tcl_members__ = [
            TclMember('destIpAddr'),
            TclMember('destIpAddrMode'),
            TclMember('sourceIpAddr'),
            TclMember('sourceIpAddrMode'),
    ]
