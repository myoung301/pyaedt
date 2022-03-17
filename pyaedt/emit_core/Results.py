import os
import string
import warnings
import time
import win32gui

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
        iemit_rpyc_server_script = os.path.join(script_dir, "iemit_rpyc_start_server.py")
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
                start_time = time.time()
                if not existing_server:
                    # ShowResultWindow without a script and will ensure the result window is loaded.
                    # Then the next time we call ShowResultWindow with the start_server script the
                    # call will be non-blocking. (The ShowResultWindow call with a script when the
                    # window is _not_ showing blocks until the script completes).
                    emit_results._odesign.ShowResultWindow(result_set_name)
                    design_name = emit_results._odesign.GetName()
                    title_substring = " - {} - {} (Created: ".format(design_name, result_set_name)
                    # Make sure the window is showing before proceeding.
                    self.wait_for_window(string_in_title=title_substring, timeout_seconds=30)
                    # Establish the connection with the result process (iemit.exe). It will be disconnected when
                    # self._rpyc_connection goes out of scope (when InnerResultSession goes out of scope).
                    success = False
                    while not success:
                        try:
                            script_dir = os.path.dirname(__file__)
                            start_server_script = os.path.join(script_dir, "iemit_rpyc_start_server.py")
                            print('Running {}'.format(start_server_script))
                            # It would be nice to call this once, before the loop, but the first call
                            # is being missed. Maybe because the window is up but not connected yet?
                            emit_results._odesign.ShowResultWindow(result_set_name, start_server_script)
                            print('Attempt to connect to server...')
                            self._rpyc_connection = rpyc.connect('localhost', 18861)
                            success = True
                        except Exception as e:
                            print('Wait and try again... (message: {})'.format(e))
                            time.sleep(0.05)
                else:
                    self._rpyc_connection = rpyc.connect('localhost', 18861)
                app = self._rpyc_connection.root.application
                print('Connected to {} ({} seconds to establish connection)'.format(app.app_name_plus_version(), time.time()-start_time))

            def wait_for_window(self, string_in_title, timeout_seconds):
                """Wait for a window to open that contains the specified string
                   in its title.
                   Parameters:
                   string_in_title -  A string that must all be in the title of
                       the window for the search to end and return True.
                   timeout_seconds - The number of seconds to attempt to find the
                       window. If the timeout expires, False is returned.
                """
                window_titles = []
                def enumWindowsHandler(hwnd, ctx):
                    if win32gui.IsWindowVisible(hwnd):
                        title = win32gui.GetWindowText(hwnd)
                        window_titles.append(title)
                def window_exists():
                    window_titles.clear()
                    win32gui.EnumWindows(enumWindowsHandler, None)
                    for title in window_titles:
                        if string_in_title in title:
                            return True
                    return False
                start_time = time.time()
                time_expired = lambda : time.time() - start_time > timeout_seconds
                while not window_exists() and not time_expired():
                    time.sleep(0.05)
                    continue
                

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

            def set_marker_background_color(self, color):
                project = self._rpyc_connection.root.project
                project.select_result()
                self.ui_update
                dlx = self._rpyc_connection.root.dlx
                marker = "NODE-*-Windows-*-Result Plot-*-Result Marker"
                mn = project.get_node(marker)
                params = {}
                params['LabelBackgroundColor'] = color
                dlx.startAction('Set Color')
                dlx.sendCommand('SETPROPERTIES', params, marker)
                dlx.endAction()
            
            def ui_update(self):
                self._rpyc_connection.root.processEvents()

            def _cleanup(self):
                self._rpyc_connection.close()
                pass
        self.inner = InnerResultSession(self.emit_results, self.result_set_name, self.existing_server)
        return self.inner

    def __exit__(self, exc_type, exc_value, traceback):
        self.inner._cleanup()
