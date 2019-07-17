from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import atexit
import ssl


class VMProxy(object):
    def __init__(self, vm):
        self.vm = vm

    def __getattr__(self, name):
        return getattr(self.vm, name)

    @property
    def interfaces(self):
        return [dev for dev in self.vm.config.hardware.device if isinstance(dev, vim.vm.device.VirtualEthernetCard)]


class Client(object):
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    @property
    def connection(self):
        if not hasattr(self, '_connection'):
            conn = SmartConnect(host=self.host, user=self.user, pwd=self.password,
                                sslContext=ssl._create_unverified_context())
            atexit.register(Disconnect, conn)
            setattr(self, '_connection', conn)

        return self._connection

    def view(self, type):
        content = self.connection.RetrieveContent()
        view = content.viewManager.CreateContainerView(content.rootFolder, [type], True)
        obj = list(view.view)
        view.Destroy()

        return obj

    @property
    def system(self):
        if not hasattr(self, '_system'):
            setattr(self, '_system', self.view(vim.HostSystem)[0])

        return self._system

    @property
    def vms(self):
        if not hasattr(self, '_vms'):
            setattr(self, '_vms', [VMProxy(vm) for vm in self.view(vim.VirtualMachine)])

        return self._vms

    @property
    def portgroups(self):
        return list(self.system.config.network.portgroup)
