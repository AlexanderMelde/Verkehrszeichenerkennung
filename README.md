#VZE-Verkehrszeichenerkennung
Installationsanleitung siehe `Installation.md^`.

##Kompilieren
1) Gegebenenfalls alte Ordner löschen: `VZE/build` `VZE/dist` `VZE/__pycache__`
2) `App/openVirtualEnvShell.bat` starten (oder mit cmd.exe /App//VZE_VirtualEnv/Scripts/activate.bat)
3) In virtualenv: in `App/VZE` wechseln 
4) In virtualenv: `pyinstaller main.py -F` (lib-not-found-Warnungen ignorieren)
    - Optionen: https://pyinstaller.readthedocs.io/en/stable/usage.html#options
    - -w um Konsole auszublenden, -F für oneFile, -i für icon
5) Lauffähiges Programm testen: `App/VZE/dist/main.exe`

Bei cx_freeze:
- setup.py Skript ggf anpassen, ergänzen um dlls für zk und tcl (siehe Datei)
- neue __init__.py Dateien in Ordner site-packages/google, site-packages\tensorflow\core\profiler und tf_files erstellen
2) `App/openVirtualEnvShell.bat` starten (oder mit cmd.exe /App//VZE_VirtualEnv/Scripts/activate.bat)
3) In virtualenv: in `App/VZE` wechseln 
4) In virtualenv: `python setup.py build`