#Windows Installation
1) PyCharm installieren
2) Projekt öffnen
3) Interpreter auswählen: "VZE_VirtualEnv" (→ Alle Module etc. sind hier enthalten, daher zukünftige Modul-Installationen bitte nur via PyCharm GUI oder per CLI in der entsprechenden VirtualEnv.)
4) Tk installieren http://www.tkdocs.com/tutorial/install.html

##Erstmalige Projekteinrichtung (muss nicht nochmal gemacht werden)
1) Erstellen einer Virtual Environment mit "Create new Project" → Interpreter: Create VirtualEnv (mit Basis Python 3.6.3 und ohne Modul-Vererbung)
2) **Installation von OpenCV:** 
    1) Download .whl Datei `opencv_python-3.3.1-cp36-cp36m-win_amd64.whl` von https://www.lfd.uci.edu/~gohlke/pythonlibs/#apsw
    2) In Konsole (nicht PowerShell): `App\VZE_VirtualEnv\Scripts\activate.bat` 
    3) In virtualenv: `cd ../..`  `pip install opencv_python-3.3.1-cp36-cp36m-win_amd64.whl`
    4) In PyCharm: Installation von `numpy` via Package Manager GUI
    5) `import cv2`

**Installation von Tensorflow:** 
1) Installation via PIP GUI: tensorflow

##Liste der Requirements
Nur zur Doku
- pip
- setuptools
- opencv_python...
- opencv-contrib-python
- numpy
- PyInstaller
- tensorflow
- appjar
- cx_freeze