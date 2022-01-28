import os
import warnings
import time

try:
    import rpyc
except ImportError:
    warnings.warn("rpyc is needed to access EMIT results")

"""
This module contains these classes: `EmitResults`.

This module provides the capability to interact with EMIT Analysis & Results windows.
"""

class ResultsEmit(object):
    """Provides for interaction with the EMIT Analysis & Results windows

    This class is accessible through the EMIT application results variable
    object( eg. ``emit.results``).

    Parameters
    ----------
    app :
        Inherited parent object.

    Examples
    --------
    >>> from pyaedt import Emit
    >>> app = Emit()
    >>> my_results = app.results
    """

    def __init__(self, app):
        self._app = app
        self._rpyc_connection = None

    # Properties derived from internal parent data
    @property
    def _desktop(self):
        """Desktop."""
        return self._app._desktop

    @property
    def logger(self):
        """Logger."""
        return self._app.logger

    @property
    def _odesign(self):
        """Design."""
        return self._app._odesign

    @property
    def projdir(self):
        """Project directory."""
        return self._app.project_path
   
    @property
    def result_sets(self):
        """List of result set names."""
        return self._odesign.GetResultList()

    @property
    def current_result(self):
        """Return name of current result set, if there is one."""
        current_result = self._odesign.GetCurrentResult()
        if current_result:
            return current_result
        return None

    def activate(self, result_set_name):
        """Activate a result set. In graphical mode, the Analysis & Result window for the result set is shown."""
        # First, show the window and let it load (using a script makes sure this call is blocking until the window 
        # loads).
        self._odesign.ShowResultWindow(result_set_name)
        # Now, send the ShowResultWindow a second time with the script. This should
        # run the script non-blocking.
        script_dir = os.path.dirname(__file__)
        iemit_rpyc_server_script = os.path.join(script_dir, "iemit_rpyc_server.py")
        self._odesign.ShowResultWindow(result_set_name, iemit_rpyc_server_script)
        self._rpyc_connection = rpyc.connect('localhost', 18861)
        app = self._rpyc_connection.application
        warnings.warn(app.app_name())

    def add_result(self, new_result_set_name):
        self._odesign.AddResult(new_result_set_name)

    def result_session(self, result_set_name, use_existing_server=False):
        if result_set_name not in self.result_sets:
            raise RuntimeError('Result set "{}" does not exist'.format(result_set_name))
        return ResultSession(self, result_set_name, use_existing_server)


# Wrap the inner session with a no-__init__ class so that it
# must be used in a "with ResultSession as session:" block and therefore
# the exit is guaranteed to be called
class ResultSession():
    """Launches and communicates with Result & Analysis window.

    ResultSession must be used as a context expression (i.e. using 'with').
    This ensures the window and associate connection gets closed
    when the context is exited (i.e. the 'with' statement is complete)

    Parameters
    ----------
    result_set:
        result_set (str): The name of the result set to connect to.

    Examples
    --------
    >>> from pyaedt import Emit
    >>> app = Emit()
    >>> with app.results.get_result_session('Revision 1') as session:
    >>>    print(session.worst_case_result())
    """
    def __init__(self, emit_results, result_set_name, existing_server=False):
        self.result_set_name = result_set_name
        self.emit_results = emit_results
        self.existing_server = existing_server

    def __enter__(self):
        class InnerResultSession:
            def __init__(self, emit_results, result_set_name, existing_server):
                """Establish a connection with a result set. In graphical mode, the Analysis & Result window is 
                shown."""
                if not existing_server:
                    script_dir = os.path.dirname(__file__)
                    # First, show the window and let it load.
                    emit_results._odesign.ShowResultWindow(result_set_name)
                    # Wait until the window is fully loaded.
                    #TODO: need a better way to know when the window is loaded. If we proceed here too soon, the
                    # next ShowResultWindow call will kill and re-start the process.
                    print('Wait for the result window to show...')
                    time.sleep(10)
                    # Now, send the ShowResultWindow a second time with the script. This should
                    # start the rpyc server script and return from ShowResultWindow (non-blocking).
                    script_dir = os.path.dirname(__file__)
                    iemit_rpyc_server_script = os.path.join(script_dir, "iemit_rpyc_server.py")
                    print('Running {}'.format(iemit_rpyc_server_script))
                    # Establish the connection with the result process (iemit.exe). It will be disconnected when
                    # self._rpyc_connection goes out of scope (when InnerResultSession goes out of scope).
                    success = False
                    while not success:
                        try:
                            emit_results._odesign.ShowResultWindow(result_set_name, iemit_rpyc_server_script)
                            print('Wait for the script to start...')
                            time.sleep(5)
                            self._rpyc_connection = rpyc.connect('localhost', 18861)
                            success = True
                        except:
                            print('Wait and try again...')
                            time.sleep(1)
                else:
                    self._rpyc_connection = rpyc.connect('localhost', 18861)
                app = self._rpyc_connection.root.application
                print('Connected to ' + app.app_name_plus_version())

            def run_all(self):
                project = self._rpyc_connection.root.project
                project.run_simulation()

            def purge_all(self):
                project = self._rpyc_connection.root.project
                project.purge_simulation_results()
                
            def run_1_to_1(self, tx, rx):
                project = self._rpyc_connection.root.project
                project.run_1_to_1(tx, rx)
                
            def worst_case_result(self):
                project = self._rpyc_connection.root.project
                return project.worst_case_result()

            def project(self):
                project = self._rpyc_connection.root.project
                return project
            
            def ui_update(self):
                self._rpyc_connection.root.processEvents()

            def _cleanup(self):
                self._rpyc_connection.close()
                pass
        self.inner = InnerResultSession(self.emit_results, self.result_set_name, self.existing_server)
        return self.inner

    def __exit__(self, exc_type, exc_value, traceback):
        self.inner._cleanup()
