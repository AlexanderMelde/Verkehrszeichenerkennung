from cx_Freeze import setup, Executable

import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

# Dependencies are automatically detected, but it might need
# fine tuning.
#buildOptions = dict(packages = [], excludes = [])
additional_mods = ['numpy.core._methods', 'numpy.lib.format']


import sys
#base = 'Win32GUI' if sys.platform=='win32' else None
base = None # for additional console output

executables = [
    Executable('main.py', base=base, targetName = 'start_vze.exe')
]

options = {
    'build_exe': {
		'includes': additional_mods,
        'include_files':[
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
			('tf_files/', 'lib/tf_files/'),
            (os.path.join(os.getcwd(), '..', 'LICENSE.txt'), 'LICENSE.txt'),
            (os.path.join(os.getcwd(), '..', 'NOTICE.txt'), 'NOTICE.txt'),
            (os.path.join(os.getcwd(), '..', 'README.md'), 'README.md')
         ],
		 'packages' : [],
		 'excludes' : []
    },
}

setup(name='VZE',
      version = '1.0',
      description = 'Verkehrszeichenerkennung',
      options = options,
      executables = executables)
