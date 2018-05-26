#!/usr/bin/env python

"""
    Verkehrszeichenerkennung – Studienarbeit
    © Copyright 2018 Alexander Melde, Stefan Schneider
    This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
    License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
    later version.
    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
"""

from appJar import gui
app = None

if __name__ == '__main__':
    print("Starting traffic sign detection, please wait...")

import numpy as np
import cv2
from time import clock, time
from classes.Sign import Sign
from classification import analyse_frame
from detection import gettrafficsigns
# from cv2 import TrackerKCF_create


def show_about_window(called_by):
    global app
    app.infoBox("Help: About/Info", "Authors: Alexander Melde, Stefan Schneider\n\nRead LICENSE File for licensing info.")


def configuration_saving_help(called_by):
    global app
    app.infoBox("Help: Save output after...", "each frame:\n writing video frame by frame to the output file. Might be a bit slower, but you get a better live preview\n\nfull conversion:\n file will be saved in RAM until 100% completed, and then saved to the specified path. Might be faster, but takes some time to save after the live preview.")


def chooseInputFile(called_by):
    global app
    path = app.openBox(title="Select Video Source", fileTypes=[('Videos', '*.mp4'), ('Videos', '*.mpeg'), ('Bilder', '*.jpg'), ('Bilder', '*.jpeg'), ('Bilder', '*.png')])
    if path == "":
        app.infoBox("Input Error", "No Input File specified.")
        return False
    if path == app.getEntry("output_file"):
        app.infoBox("Input=Output", "You can not write to the file you are reading from.")
        return False
    app.setEntry("input_file", path)
    app.setRadioButton("input", "File")


def chooseOutputFile(called_by):
    global app
    path = app.saveBox(title="Choose Output File", fileExt=".mp4", fileTypes=[('Videos', '*.mp4'), ('Videos', '*.mpeg')])
    if path == "":
        app.infoBox("Output Error", "No Output Path specified.")
        return False
    if path == app.getEntry("input_file"):
        app.infoBox("Input=Output", "You can not write to the file you are reading from.")
        return False
    app.setEntry("output_file", path)
    app.setRadioButton("output", "File")


def removeUmlauts(i_str):
    return i_str.translate(str.maketrans({
        "Ä": "Ae",
        "ä": "ae",
        "Ö": 'Oe',
        "ö": "oe",
        "Ü": "Ue",
        "ü": "ue",
        "ß": "ss"
    }))


def mapIDtoName(labelid):
    # accepts integer, returns strings
    return removeUmlauts({
        274030: "zulässige Höchstgeschwindigkeit 30 km/h",
        274050: "zulässige Höchstgeschwindigkeit 50 km/h",
        274060: "zulässige Höchstgeschwindigkeit 60 km/h",
        274070: "zulässige Höchstgeschwindigkeit 70 km/h",
        274080: "zulässige Höchstgeschwindigkeit 80 km/h",
        274100: "zulässige Höchstgeschwindigkeit 100 km/h",
        274120: "zulässige Höchstgeschwindigkeit 120 km/h",
        274130: "zulässige Höchstgeschwindigkeit 130 km/h",
        278070: "Ende der zulässigen Höchstgeschwindigkeit 70 km/",
        278080: "Ende der zulässigen Höchstgeschwindigkeit 80 km/",
        276000: "Überholverbot für Kraftfahrzeuge aller Art",
        277000: "Überholverbot für Kraftfahrzeuge > 3,5t",
        301000: "Vorfahrt",
        306000: "Vorfahrtstraße",
        205000: "Vorfahrt gewähren!",
        206000: "Halt! Vorfahrt gewähren! ",
        250000: "Verbot für Fahrzeuge aller Art",
        253000: "Verbot für Kraftfahrzeuge mit einem > 3,5t",
        267000: "Verbot der Einfahrt",
        101000: "Gefahrstelle",
        103010: "Kurve (links)",
        103020: "Kurve (rechts)",
        105010: "Doppelkurve (zunächst rechts)",
        112000: "Unebene Fahrbahn",
        114000: "Schleudergefahr bei Nässe oder Schmutz",
        121010: "einseitig (rechts) verengte Fahrbahn",
        123000: "Arbeitsstelle",
        131000: "Lichtzeichenanlage",
        133010: "Fußgänger (Aufstellung rechts)",
        136010: "Kinder (Aufstellung rechts)",
        138010: "Radfahrer (Aufstellung rechts)",
        101051: "Schnee- oder Eisglätte",
        282000: "Ende sämtlicher Streckenverbote",
        209000: "vorgeschriebene Fahrtrichtung - rechts",
        209010: "vorgeschriebene Fahrtrichtung - links",
        209030: "vorgeschriebene Fahrtrichtung - geradeaus",
        214000: "vorgeschriebene Fahrtrichtung - geradeaus oder rechts",
        214010: "vorgeschriebene Fahrtrichtung - geradeaus oder links",
        222000: "vorgeschriebene Vorbeifahrt - rechts vorbei",
        222010: "vorgeschriebene Vorbeifahrt - links vorbei",
        211000: "vorgeschriebene Fahrtrichtung - hier rechts",
        215000: "Kreisverkehr",
        280000: "Ende des Überholverbotes für Kraftfahrzeuge aller Art",
        281000: "Ende des Überholverbotes für Kraftfahrzeuge > 3,5t",
        260000: "Verbot für ein- und mehrspurige Kraftfahrzeuge",
        283010: "Haltverbot (Anfang)",
        283020: "Haltverbot (Ende)",
        391000: "Maut-Pflicht nach dem Autobahnmautgesetz (ABMG)",
        996001: "Durchgestrichen: zulässige Höchstgeschwindigkeit 120 km/h",
        237000: "Sonderweg Radfahrer",
        286010: "Eingeschränktes Haltverbot (Anfang - Aufstellung rechts)",
        286020: "Eingeschränktes Haltverbot (Ende - Aufstellung rechts)",
        286030: "Eingeschränktes Haltverbot (Mitte - Aufstellung rechts)",
        245000: "Linienomnibusse",
        996002: "Durchgestrichen: vorgeschriebene Fahrtrichtung - links",
        999003: "ampel rechts gelb",
        240000: "gemeinsamer Fuß- und Radweg",
        999001: "ampel gruen",
        999002: "ampel gelb",
        283030: "Absolutes Haltverbot (Mitte - Aufstellung rechts)",
        239000: "Sonderweg Fußgänger",
        307000: "Ende der Vorfahrtstraße",
        350010: "Fussgängerüberweg (Aufstellung rechts)",
        350020: "Fussgängerüberweg (Aufstellung links)",
        439000: "gegliederter Vorwegweiser",
        434000: "Wegweisertafel",
        365061: "Informationsstelle",
        142010: "Wildwechsel (Aufstellung rechts)",
        142020: "Wildwechsel (Aufstellung links)",
        120000: "verengte Fahrbahn",
        117010: "Seitenwind von rechts",
        117020: "Seitenwind von links",
        101015: "Steinschlag (Aufstellung rechts)",
        101020: "Flugbetrieb (Aufstellung links)",
        996003: "Umgedrehtes Gefahrzeichen",
        996004: "Umgedrehtes Vorfahrt Gewähren!-Zeichen",
        996005: "Umgedrehtes Vorfahrtstraße-Zeichen",
        996006: "Umgedrehtes rundes Schild",
        625010: "Richtungstafel in Kurven (linksweisend)",
        625020: "Richtungstafel in Kurven (rechtsweisend)",
        445000: "Ankündigungstafel (Autobahn)",
        450000: "Vorwegweiser auf Autobahnen",
        626030: "Leitplatte",
        458000: "Planskizze",
        124000: "Stau",
        108000: "Gefälle",
        110000: "Steigung",
        363000: "Polizei",
        450052: "Ankündigungsbake (blau, dreistreifig)",
        365058: "Toilette",
        365052: "Tankstelle",
        365053: "Tankstelle mit Autogas",
        328000: "Nothalte- und Pannenbucht",
        365056: "Autobahngasthaus",
        552000: "Fahrstreifentafel - mit Gegenverkehr",
        314000: "Parken",
        254000: "Verbot für Radverkehr",
        365050: "Fernsprecher",
        1052031: "Fahrzeuge mit besonderer Ladung",
        -1: "unknown sign",
        0: "circle shaped sign",
        3: "triangle shaped sign",
        4: "rectangle shaped sign"
    }[labelid])


def label_sign(sign, frame, framenr=0):
    # This uses Tensorflow to label the sign
    advancedLabeling = app.getCheckBox("detection_labeltrafficsigns_advanced")
    saveCropouts = app.getCheckBox("configuration_savecropouts")


    crop_img = frame[sign.pos[framenr].y:sign.pos[framenr].y + sign.pos[framenr].h, sign.pos[framenr].x:sign.pos[framenr].x + sign.pos[framenr].w]

    if advancedLabeling:
        tf_result = analyse_frame.analyse_frame(crop_img)
        if len(tf_result) > 0:
            signname = mapIDtoName(int(tf_result[0][0])) + " (" + str(format(float(tf_result[0][1]) * 100, '.2f')) + "%)"
            print("  advanced labeling for "+str(sign)+" in framenr "+str(framenr)+" result: "+signname)
            if saveCropouts:  # Test: save cropouts to improve machine learning
                cv2.imwrite("cropouts/" + str(time()) + "f" + str(framenr) + "x" + str(sign.pos[framenr].x) + "y" + str(sign.pos[framenr].y) + "h" + str(sign.pos[framenr].h) + "w" + str(sign.pos[framenr].w) + "e" + str(sign.edgecount) + "_" + str(int(tf_result[0][0])) + ".jpg", crop_img)

            # return (name_id, probability)
            return int(tf_result[0][0]), float(tf_result[0][1])
            # TODO: if score<15% do not display as a sign

    if saveCropouts:  # Test: save cropouts to improve machine learning
        cv2.imwrite("cropouts/"+str(time())+"f"+str(framenr)+"x"+str(sign.pos[framenr].x)+"y"+str(sign.pos[framenr].y)+"h"+str(sign.pos[framenr].h)+"w"+str(sign.pos[framenr].w)+"e"+str(sign.edgecount)+"_unknown.jpg", crop_img)

    return sign.edgecount, 1 if sign.edgecount is not None else -1, 1


def number_plate_detection(frame):
    # This uses OpenALPR to detect number plates
    # and compares detected plates with list (AA-->Aachen)
    return [(200, 200, 80, 23, "AA-BB-123", "Aachen")]  # x,y,w,h


def startDetection(called_by):
    global app

    print("Press Q to exit video playback")
    starttime = clock()

    if app.getRadioButton("input") == "Webcam":
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(app.getEntry("input_file"))

    if not cap.isOpened():
        app.infoBox("Input Error", "Could not open file: "+app.getEntry("input_file"))
        return False

    framecount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if app.getRadioButton("input") == "Webcam":
        fps = 30
    else:
        fps = cap.get(cv2.CAP_PROP_FPS)

    print("file info: framecount: ", framecount, " w: ", width, " h: ", height, " fps: ", fps, " time: ", framecount / fps, "s")

    if app.getRadioButton("output") == "File":
        fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
        out = cv2.VideoWriter(app.getEntry("output_file"), fourcc, fps, (width, height))
        previewOnly = False
    else:
        previewOnly = True

    if app.getRadioButton("input") == "Webcam" or app.getRadioButton("configuration_saving") == "Each Frame" or previewOnly:
        directWrite = True
    else:
        directWrite = False
        framelist = []  # [OpenCV-Image, OpenCV-Image, ...]

    framenr = 0
    signlist = []  # [Sign, Sign, Sign, ...]

    showframecounter = app.getCheckBox("detection_showframecounter")
    #feature not implemented yet
    #detect_numberplates = app.getCheckBox("detection_numberplates")
    draw_bordertrafficsigns = app.getCheckBox("detection_bordertrafficsigns")
    labelSignsInEachFrame = app.getCheckBox("configuration_labeleachframe")
    draw_lowprob = app.getCheckBox("draw_lowprob")
    # labeltrafficsigns = app.getCheckBox("detection_labeltrafficsigns")

    activeTrackers = []  # [(id, tracker)]

    while True:
        # read and modify video
        framenr += 1

        ret, frame = cap.read()
        if ret:
            """
                Modify frame
            """
            modifiedFrame = frame.copy()

            # evaluate active Trackers
            for s in signlist:
                if s.tracker is not None:
                    foundTrackedObject, oPos = s.tracker.update(frame)
                    if foundTrackedObject:
                        # cut to fit into frame
                        h, w = frame.shape[:2]
                        # Add Sign Position to Sign Object for Tracking Multiple Frames
                        s.addPos(framenr, oPos[0] if oPos[0] > 0 else 0,
                                          oPos[1] if oPos[1] > 0 else 0,
                                          oPos[2] if oPos[0]+oPos[2] < w else w,
                                          oPos[3] if oPos[1]+oPos[3] < w else h)

                        # Tracking success
                        #p1 = (int(oPos[0]), int(oPos[1]))
                        #p2 = (int(oPos[0] + oPos[2]), int(oPos[1] + oPos[3]))
                        #cv2.rectangle(modifiedFrame, p1, p2, (255, 0, 0), 2, 1)
                        #cv2.putText(modifiedFrame, "Tracking active", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                        #print("Tracking Position added to " + str(s))
                    else:
                        s.tracker.clear()
                        s.tracker = None
                        #print("Tracking ended for "+str(s))

            # Shape Detection
            # TODO: Add check for number of frames to skip
            detected_shapes = gettrafficsigns.gettrafficsigns(frame)  # Returns Array of Coordinate-Pairs that might describe a traffic sign

            if len(detected_shapes) > 0:
                print("shape detection found " + str(len(detected_shapes)) + " interesting shapes in frame #" + str(framenr) + ": " + str(detected_shapes))

            for c in detected_shapes:  # x,y,w,h,edgecount, TODO: c[5] for rotation
                addedToExistingSign = False
                # if there was a sign at the shape-position in the previous frame, add a new position to that sign, else create a new sign
                for pSign in signlist:  # TODO: This loops through every sign and every position the sign had. To improve performance, old signs (that did not appear for X frames and have no trackers) should be deleted from the signlist.
                    if (framenr - 1) in pSign.pos:
                        if pSign.sameSignPosition(c[0], c[1], c[2], c[3], c[4]):
                            pSign.addPos(framenr, c[0], c[1], c[2], c[3])
                            addedToExistingSign = True
                if not addedToExistingSign:
                    print("Transformed Shape "+str(c)+" into new "+str(Sign(framenr, c[0], c[1], c[2], c[3], c[4])))
                    signlist.append(Sign(framenr, c[0], c[1], c[2], c[3], c[4]))

            # Get Signs relevant for this frame: Shapes detected this frame (that formed new signs or got added to existing ones) as well as Signs that are relevant due to Trackers
            relevantSigns = []
            for s in signlist:
                if framenr in s.pos:
                    relevantSigns.append(s)

            # Compute Shapes
            for rSign in relevantSigns:
                # Label Signs
                rLabel = rSign.getLabel()
                if rLabel is None or labelSignsInEachFrame:
                    rLabel = rSign.addLabel(framenr, label_sign(rSign, frame, framenr))

                prob_threshold = 0.2  # This is the Threshhold to hide signs detected with a propability < x %
                boxcolor = (102, 204, 0) if rLabel[1] > prob_threshold else (165, 165, 165)

                if rLabel[1] > prob_threshold or draw_lowprob:  # only draw if high chance or low prob drawing is explicity enabled
                    # Draw
                    spos = rSign.pos[framenr]
                    if draw_bordertrafficsigns:
                        if rSign.edgecount == 0:
                            cv2.circle(modifiedFrame, (int(spos.x+spos.w/2), int(spos.y+spos.h/2)), int((spos.w/2+spos.h/2)/2), boxcolor, thickness=3)
                        elif rSign.edgecount == 3:
                            pts = np.array([[spos.x, spos.y], [spos.x+spos.w, spos.y], [spos.x+spos.w/2, spos.y+spos.h]], np.int32) # Spitze unten
                            pts = pts.reshape((-1, 1, 2))
                            cv2.polylines(modifiedFrame, [pts], True, boxcolor, thickness=3)
                            pts = np.array([[spos.x + spos.w / 2, spos.y], [spos.x + spos.w, spos.y + spos.h], [spos.x, spos.y + spos.h]], np.int32)  # Spitze oben
                            pts = pts.reshape((-1, 1, 2))
                            cv2.polylines(modifiedFrame, [pts], True, boxcolor, thickness=3)
                        elif rSign.edgecount == 8:
                            pts = np.array([[spos.x+spos.w/3, spos.y], [spos.x+2*spos.w/3, spos.y], [spos.x + spos.w, spos.y+spos.h/3], [spos.x + spos.w, spos.y+2*spos.h/3], [spos.x + 2*spos.w/3, spos.y+spos.h], [spos.x + spos.w/3, spos.y+spos.h], [spos.x, spos.y+2*spos.h/3], [spos.x, spos.y+spos.h/3]], np.int32)
                            pts = pts.reshape((-1, 1, 2))
                            cv2.polylines(modifiedFrame, [pts], True, boxcolor, thickness=3)
                        else:
                            cv2.rectangle(modifiedFrame, (spos.x, spos.y), (spos.x + spos.w, spos.y + spos.h), boxcolor, thickness=3)

                    signname = mapIDtoName(rLabel[0]) + " (" + str(format(rLabel[1] * 100, '.2f')) + "%)"
                    cv2.putText(modifiedFrame, signname, (spos.x, spos.y + spos.h + 15), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.4, color=boxcolor, lineType=2)

                    if rSign.tracker is None:
                        rSign.addTracker().init(frame, (spos.x, spos.y, spos.w, spos.h))


            # Number Plate Recognition: Feature not yet implemented
            #if detect_numberplates:
            #    plates = number_plate_detection(frame)
            #
            #    for p in plates:
            #        cv2.rectangle(modifiedFrame, (p[0], p[1]), (p[0] + p[2], p[1] + p[3]), (6, 75, 178), thickness=3)
            #        cv2.putText(modifiedFrame, p[4], (p[0]+10, p[1]+10), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.3, color=(6, 75, 178), lineType=2)
            #        cv2.putText(modifiedFrame, p[5], (p[0]+10, p[1]+20), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.3, color=(6, 75, 178), lineType=2)

            progress_percent = str(round((framenr/framecount)*100)) +"%" if framecount is not -1 else ""
            # Frame-Index einblenden
            if showframecounter:
                modifiedFrame = cv2.putText(modifiedFrame, str(framenr) + "/" + str(framecount) + " ("+ progress_percent +")", (10, 10), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.2, color=(255, 255, 255), lineType=2)
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            """
                Preview & save modified Frame 
            """
            # TODO: Entweder alle Frames zeigen oder keine
            # if framenr % 10 == 0:
            cv2.imshow('Preview (Cancel with Q key)', modifiedFrame)
            # cv2.imshow('Originalbild', frame)

            # cv2.imshow('grayF', gray)
            if directWrite:
                if not previewOnly:
                    out.write(modifiedFrame)
            else:
                framelist.append(modifiedFrame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # if cv2.getWindowProperty('windowname', 1) == -1:
                # break

        else:
            break

    cap.release()
    cv2.destroyAllWindows()

    if not directWrite:
        print("Writing File, please wait...")
        for i in range(len(framelist)):
            out.write(framelist[i])

    if not previewOnly:
        print("Video exported in ", (clock()-starttime), "s to "+app.getEntry("output_file"))
        out.release()
    else:
        print("Finished after ", (clock() - starttime), "s")

    print("\n---------------------------\n")
    print("This is the Signlist:\n")
    for s in signlist:
        print ("- "+str(s))

    print("\n---------------------------\n")

def createGUI():
    """ GUI uses a twenty-width-grid
    .setGuiPadding(x, y)
    """
    global app

    app = gui("Traffic Sign Detection")
    app.setGuiPadding(20, 10)
    app.setGeometry(690, 580) #width, height
    app.setLocation("CENTER")
    app.setStretch("both")

    app.startScrollPane("VZE")
    # app.setIcon("icon.ico")

    curRow = 0
    app.addLabel("title", "Traffic Sign Detection", curRow, 0, 15)  # Row 0,Column 0,Span 2
    app.getLabelWidget("title").config(font="Verdana 20")
    app.setLabelAlign("title", "left")
    app.addButton("title_about", show_about_window, curRow, 15, 5)
    app.setButton("title_about", "About/Info")

    curRow += 1
    app.addLabel("title_about", "Student Research by Alexander Melde and Stefan Schneider", curRow, 0, 20)  # Row 0,Column 0,Span 2
    app.getLabelWidget("title_about").config(font="Verdana 15")
    app.setLabelAlign("title_about", "left")

    curRow += 1
    app.startLabelFrame("Input", curRow, 0, 20)
    app.addRadioButton("input", "Webcam", curRow, 0, 20)
    curRow += 1
    app.addRadioButton("input", "File", curRow, 0, 5)
    app.addEntry("input_file", curRow, 5, 10)
    app.addButton("Choose_Input", chooseInputFile, curRow, 15, 5)
    app.setButton("Choose_Input", "Choose")
    app.stopLabelFrame()
    #TODO: Setting to start at Frame X (to continue long/stopped conversions)

    curRow += 1
    app.startLabelFrame("Output", curRow, 0, 20)
    app.addRadioButton("output", "None (Preview Only)", curRow, 0, 20)
    curRow += 1
    app.addRadioButton("output", "File", curRow, 0, 5)
    app.addEntry("output_file", curRow, 5, 10)
    app.addButton("Choose_Output", chooseOutputFile, curRow, 15, 5)
    app.setButton("Choose_Output", "Choose")
    app.stopLabelFrame()

    curRow += 1
    app.startLabelFrame("Configuration", curRow, 0, 20)

    app.addLabel("configuration_saving_label", "Save Output after", curRow, 0, 5)
    app.addRadioButton("configuration_saving", "Each Frame", curRow, 5, 5)
    app.addRadioButton("configuration_saving", "Full Conversion", curRow, 10, 5)
    app.addButton("configuration_saving_help", configuration_saving_help, curRow, 15, 5)
    app.setButton("configuration_saving_help", "?")

    #feature not fully implemented
    #curRow += 1
    #app.addLabel("configuration_frameskip", "Nr. of frames to skip between Shape detections:", curRow, 0, 15)
    #app.addEntry("configuration_frameskip_entry", curRow, 15, 5)

    curRow += 1
    app.addNamedCheckBox("Repeat Labeling in each frame (do not remember old labels)", "configuration_labeleachframe", curRow, 0, 20)
    app.setCheckBox("configuration_labeleachframe", ticked=False, callFunction=False)

    curRow += 1
    app.addNamedCheckBox("Save each labeled sign to the cropouts/ folder (for testing and to improve ml)", "configuration_savecropouts", curRow, 0, 20)
    app.setCheckBox("configuration_savecropouts", ticked=False, callFunction=False)



    app.stopLabelFrame()

    curRow += 1
    app.startLabelFrame("Drawing Settings", curRow, 0, 20)
    app.addNamedCheckBox("Show frame-counter in video", "detection_showframecounter", curRow, 0, 20)
    app.setCheckBox("detection_showframecounter", ticked=True, callFunction=False)

    # feature not fully implemented
    #curRow += 1
    #app.addNamedCheckBox("Detect numberplates", "detection_numberplates", curRow, 0, 20)
    #app.setCheckBox("detection_numberplates", ticked=False, callFunction=False)

    curRow += 1
    app.addNamedCheckBox("Draw a border around traffic signs", "detection_bordertrafficsigns", curRow, 0, 20)
    app.setCheckBox("detection_bordertrafficsigns", ticked=True, callFunction=False)
    curRow += 1
    app.addNamedCheckBox("Show low-propability Detections", "draw_lowprob", curRow, 0, 20)
    app.setCheckBox("draw_lowprob", ticked=True, callFunction=False) # Change this to False in final version

    # curRow += 1
    # app.addNamedCheckBox("Label traffic signs with shape", "detection_labeltrafficsigns", curRow, 0, 20)
    # app.setCheckBox("detection_labeltrafficsigns", ticked=True, callFunction=False)

    curRow += 1
    app.addNamedCheckBox("Label traffic signs with type (Classify)", "detection_labeltrafficsigns_advanced", curRow, 0, 20)
    app.setCheckBox("detection_labeltrafficsigns_advanced", ticked=True, callFunction=False)

    app.stopLabelFrame()

    #Error Feedback is not needed here
    #curRow += 1
    #app.addLabel("start_detection_title", "Error: No Input File selected!", curRow, 0, 12)
    #app.setLabelBg("start_detection_title", "red")
    #app.setLabelFg("start_detection_title", "white")
    #app.setLabelAlign("start_detection_title", "left")
    app.addNamedButton("Start Detection", "start_detection", startDetection, curRow, 12, 8)


    app.stopScrollPane()

    app.go()


if __name__ == '__main__':
    print("Loaded!")

    # Only create GUI, everything else is async in onClick() functions...
    createGUI()
