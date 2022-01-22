import rpyc
from rpyc.utils.server import ThreadedServer
from rpyc.utils.server import OneShotServer
from PythonQt.Qt import QApplication

#TODO: Make sure there isn't a port conflict
port = 18861

class EmitService(rpyc.Service):
    def on_connect(self, conn):
        # code that runs when a connection is created
        # (to init the service, if needed)
        pass

    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        # (to finalize the service, if needed)
        pass

    exposed_application = application
    exposed_project = project
    exposed_dlx = dlx
    exposed_dlxgui = dlxgui
    exposed_emitgui = emitgui

    def exposed_processEvents(self):
        QApplication.processEvents()

# Start a OneShotServer that will serve one client and then exit.
# TODO: Timeout if no connection is made for a few seconds.

while True:
    t = OneShotServer(EmitService, port=port, protocol_config={
            'allow_public_attrs': True,
        })
    print("Starting server on port {}".format(port))
    t.start()
    print("Server ended")

# Exit the result window
#emitgui.serverModeEditDialogClickOk()