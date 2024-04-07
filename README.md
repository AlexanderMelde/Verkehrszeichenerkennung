# Verkehrszeichenerkennung - Studienarbeit
<table>
<tr><th>Autor</th><td>Alexander Melde (7939560), Stefan Schneider (5280242)</td></tr>
<tr><th>Betreuer</th><td>Martin Kissel</td></tr>
<tr><th>Studiengang/Kurs</th><td>B. Sc. Angewandte Informatik – Kommunikationsinformatik TINF15K</td></tr>
<tr><th>Titel der Arbeit</th><td>Verkehrszeichenerkennung</td></tr>
<tr><th>Anlass</th><td>Studienarbeit, 3. Studienjahr</td></tr>
<tr><th>Bearbeitungszeitraum</th><td>16.10.2017 - 04.06.2018</td></tr>
<tr><th>Abgabedatum</th><td>04.06.2018</td></tr>
</table>

## Download und Installation
Die Studienarbeit inklusive der praktischen Implementierung wurde veröffentlicht und kann von der Internetplattform [Github](https://github.com/AlexanderMelde/Verkehrszeichenerkennung) heruntergeladen werden:

Es gibt zwei Möglichkeiten zur Installation:
- Projekt anhand des Python Sourcecodes selbst kompilieren
- Lauffähiges Programm herunterladen und starten 
	1) Vollständiger Download der [build-Dateien](http://wwwlehre.dhbw-stuttgart.de/~it15111/vze/)
	2) Den für das Betriebssystem passende Ordner öffnen
	3) Die ausführbare Datei `start_vze.exe` mit einem Doppelklick öfffnen

## Einrichten der Entwicklungsumgebung
Da es sich bei dem Quelltext um Skripte der Skriptsprache Python 3.6.3 handelt, kann das Programm auf verschiedenen Betriebssystemen gestartet werden.
Für Start und Entwicklung sind neben einer Python3-Installation die folgenden Module sowie deren Abhängigkeiten („Dependencies“) erforderlich:
- appJar (0.82.1)
- cx-Freeze (5.1.1)
- numpy (1.14.2)
- opencv-contrib-python (3.4.0.12)
- opencv-python (3.3.1)
- pip (9.0.2)
- setuptools (38.5.1)
- tensorflow (1.4.0)
- virtualenv (15.1.0)
- wheel (0.30.0)

Die Verwendung des Moduls virtualenv ist optional, wird aber zur besseren Trennung mehrerer Python-Projekte auf einem System empfohlen. Eine Einführung in Virtual Environments ist kein Teil dieser Arbeit, eine gute Anleitung zur Einrichtung befindet sich [hier](https://www.geeksforgeeks.org/python-virtual-environment/).

Wurde die virtualenv eingerichtet können alle weiteren Module innerhalb der Environment (Umgebung) installiert und das Skript innerhalb der Umgebung gestartet werden.
Das Modul cx-Freeze wird lediglich zum Erstellen von ausführbaren Dateien benötigt, eine Installation ist also nur notwendig, wenn der Python Code später ohne Interpreter ausgeführt können werden soll.
Für die Darstellung der GUI wird in der nicht-kompilierten Version zudem das GUI-Framework Tk benötigt. Dieses wird bei den meisten Python-Installationen bereits als Tkinter mitgeliefert. Sollte Tk noch nicht vorhanden sein, kann [diese Anleitung](http://www.tkdocs.com/tutorial/install.html) genutzt werden.

Nach der Installation von Python 3.6 könnnen die benötigten Pakete installiert werden mit ``pip install -r requirements.txt`` (im Ordner ``VZE``).

##	Ausführung
Vor der ersten Ausführung des Programms zur Verkehrszeichenerkennung muss, nachdem die Entwicklungsumgebung wie im vorherigen Abschnitt beschrieben, eingerichtet wurde, das neuronale Netz für die Klassifikation trainiert werden. Dies geschieht mit dem folgenden Befehl:

	python classification/retrain.py --bottleneck_dir=${PWD}/tf_files/bottlenecks --how_many_training_steps=500 --model_dir=${PWD}/tf_files/inception --output_graph=${PWD}/tf_files/retrained_graph.pb --output_labels=${PWD}/tf_files/retrained_labels.txt --image_dir=${PWD}/data/signs

Nach dem Trainieren des neuronalen Netzes kann die Verkehrszeichenerkennung mit dem folgenden Befehl (innerhalb der virtualenv) gestartet werden:
``python main.py``

In der Konsole erscheint nach dem Aufruf der Hinweis, dass die grafische Oberfläche nun geladen wird.
Die Bedienung der grafischen Oberfläche wird als selbsterklärend angesehen, kleine Buttons und Hilfetexte unterstützen den Anwender innerhalb der grafischen Oberfläche.

##	Kompilieren
Um das entwickelte Programm auch ohne die Einrichtung einer Entwicklungsumgebung starten zu können, kann eine ausführbare Datei kompiliert werden.
Hierfür wird das Modul cx-Freeze verwendet, das die mitgelieferte Konfigurationsdatei `setup.py` beim Aufruf einliest und aus den Skripten eine passende Datei kompiliert.
Das Build-Skript kann mit dem folgenden Befehl aufgerufen werden:
``python setup.py build``

Hierbei wird ein neuer Ordner `build` erstellt, der die ausführbare Datei `start_vze` enthält.

## Lizenz
Die Studienarbeit inklusive der praktischen Implementierung darf unter den Bedingungen der 
GNU GPL v3 weitergegeben und modifiziert werden. Die vollständigen Lizenzbedingungen können [unter dieser Adresse](https://www.gnu.org/licenses/gpl) und in der Datei `LICENSE.txt` im Quelltext nachgelesen werden.
Die Lizenz erlaubt die private und kommerzielle Nutzung, Weitergabe und Modifikation der Software und die Nutzung dieser in Patenten unter den folgenden Bedingungen: Die Modifikation darf nur unter derselben Lizenz veröffentlicht werden und muss einen Hinweis auf die Autoren der ursprünglichen Software sowie eine Übersicht über die Änderungen enthalten. Es wird explizit keine Haftung oder Garantie übernommen.

	Verkehrszeichenerkennung – Studienarbeit
	© Copyright 2018 Alexander Melde, Stefan Schneider
	This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
	This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

Die praktische Implementierung dieser Studienarbeitet verwendet Teile von Open Source Software. Die für diese geltenden Lizenzen sind in der Datei `NOTICE.txt` im Quelltext aufgeführt
