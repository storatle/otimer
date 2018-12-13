#!/usr/bin/env python
#coding: utf8 e

import xml.etree.ElementTree as ET
import numpy as np
import argparse
import sys
#from wand.image import Image


class Xml:

    def __init__(self, filename):
        self.read_xml(filename)
    # Denne er tatt fra worldfile.py
    def read_xml(filnavn):

        # Henter inn data fra IOF utveklsingsfil
        try:
            tree = ET.parse(filnavn+".xml")

        except:
            sys.exit("Oops! Har du riktig IOF utvekslingsfil (.xml) i katalogen? ")

        root = tree.getroot()

        scale = (float(root[2][0].text))/1000 # koordinater i Purple pen er mm???

        map=[] #Kartinfo [Målestokk, Venstre, Topp]
        ctrl=[] #Kontrolpost [UTM Vest, UTM Nord, Venstre, Topp]
        start=[] #Starpost [UTM Vest, UTM Nord, Venstre, Topp]

         #Henter inn skala og koordinater for øvre venstre hjørne
        for mapinfo in root.iter('Map'):
            map.append(float(mapinfo[0].text))
            map.append(float(mapinfo[1].attrib.get('x')))
            map.append(float(mapinfo[1].attrib.get('y')))

        for control in root.iter('Control'):
            for controlcode in control.iter('ControlCode'):
                #Henter inn posisjon for "Dummypost i øverste venstre hjørne
                if controlcode.text=='999':
                    for i in range(1, 3):
                        ctrl.append(float(control[i].attrib.get('x')))
                        ctrl.append(float(control[i].attrib.get('y')))

            # Du må lage en sjekk på om kontrollposten finnes. Eller om det er gitt riktig kode 999. Eventuelt så kan du lage en rutine som sjekker om det er en post i øverste venstre hjørne

        for startpoint in root.iter('StartPoint'):
            for startpointcode in startpoint.iter('StartPointCode'):
                #henter in posisojn til starten
                if startpointcode.text=='STA1':
                     for i in range(1, 3):
                        start.append(float(startpoint[i].attrib.get('x')))
                        start.append(float(startpoint[i].attrib.get('y')))

        grid = []
        # Snutt tatt fra koder.py
        for course in root.iter('Course'):
            row = []
            row.append(course[0].text)
            for coursecontrol in course.iter('CourseControl'):
                row.append(coursecontrol[1].text)
            row.append('100')
            #    print(row)
            print
            " ".join(row)
            grid.append(row)


class PurplePen:

    def __init__(self, filename):

        self.read_ppen(filename)
        self.set_courses()


    def read_ppen(self,filename):

        #Henter inn data fra Purple Pen
        try:
            tree = ET.parse(filename)
        except:
            sys.exit("Oops! Har du riktig Purple Pen-fil (.ppen) i katalogen? ")

        root = tree.getroot()

        #Henter data fra Purple Pen fila
        #ctrl = []
        self.controls = []
        #crs = []
        #chain = []
        self.courses = []
        self.order = []
        self.variations = []

        for event in root.iter('event'):
            for map in event.iter('map'):
                self.scale = map.attrib.get('scale')

        #Leser inn alle postene
        for ctrl in root.iter('control'):
            x = None
            y = None
            for loc in ctrl.iter('location'):
                x = loc.attrib.get('x')
                y = loc.attrib.get('y')
            self.controls.append(Control((ctrl.attrib.get('id'), ctrl[0].text, x, y, ctrl.attrib.get('kind'))))

            #controls = sorted(controls, key=lambda x: x.id)
        # Leser inn løypene
        for crs in root.iter('course'): # Mulig at jeg bør legge inn dette i en loop

            self.courses.append(Course((crs.attrib.get('id'), crs[0].text, crs.attrib.get('kind'), crs.attrib.get('order'), \
                            crs[1].attrib.get('label-kind'), crs[2].attrib.get('course-control'))))

        for cc in root.iter('course-control'):
            #variation = []
            vr = []
            next = None
            #Finner neste post
            for nxt in cc.iter('next'):
                next = (nxt.get('course-control'))
            for var in cc.iter('variation'):
                vr.append(var.get('course-control')) # Sjekker om det er en variation

            if vr:
                vr = tuple(vr)
                self.variations.append(Variation((cc.attrib.get('variation'), cc.attrib.get('variation-end'), vr)))

            self.order.append((cc.attrib.get('id'), next, cc.attrib.get('control'), cc.attrib.get('variation')))

    def set_courses(self):

        for course in self.courses:
            course.set_order(self.order)
            course.set_codes(self.controls)
            course.set_leg_length(self.controls)





class Variation:

    def __init__(self, var):

        self.type = var[0]
        self.end = var[1]
        #self.end = var[]
        self.var = []
        for vr in var[2][1:]:
            self.var.append(vr)






class Course:

    def __init__(self, crs):
        self.id = crs[0] #.zfill(2)
        self.name = crs[1]
        self.kind = crs[2]
        self.first_ctrl = crs[5]
        self.codes = []
        self.order = []
        self.x = []
        self.y = []


    def set_order(self, order):
        next_ctrl = self.first_ctrl
        loop = False
        n = 1
        while next_ctrl:
            for control in order:
                if control[0] == next_ctrl:
                    if control[3] == 'loop'and not loop:  # Nå er vi igang med en loop hvordan skal jeg klare å få den til å sjekke begge runder
                        # Sett inn variation

                        if n < len(control[3][2]): # Denne er feil. *Må sjekke variations med riktig loop og riktig endpost
                            next_ctrl = control[3][2][n] # Her henter jeg første variasjon, men jeg må også hente 2 og 3 versjon slik at jeg får alle sløyfene
                            n += 1

                        else:
                            n = 1
                        loop = True
                        break
                    else:
                        self.order.append(control[2])
                        next_ctrl = control[1]
                        loop = False
                        break

    def set_codes(self, controls):

        for code in self.order:
            for ctrl in controls:
                if ctrl.id == code:
                    self.codes.append(ctrl.code)
                    self.x.append(float(ctrl.x))
                    self.y.append(float(ctrl.y))

                    break
        del self.codes[0]
        self.codes[-1] = 100
        self.codes = [int(x) for x in self.codes]

    def set_leg_length(self,controls):
        self.dl = []
        scale = 10
        for i in range(0, len(self.x)-1):
            dx = (self.x[i] - self.x[i+1])
            dy = (self.y[i] - self.y[i+1])

            self.dl.append(np.sqrt(dx**2 + dy**2)*scale)

    def leg_length(self):
        return self.dl

    def code_list(self):
        return self.codes

        print('hello')


class Control:

    def __init__(self, ctrl):
        self.id = ctrl[0]  #.zfill(2)
        self.code = ctrl[1]
        self.x = ctrl[2]
        self.y = ctrl[3]
        self.kind = ctrl[4]
        #self.variation =


def code_list(order,controls):
    codes = []
    for o in order:
        codes.append(controls[0])


# sette samme løype
# Lage Kodeliste legge på 100 som målpost i lista
# Finne lendge mellom hver post for å beregne km/tid


# Videre arbeid.

        # Mulighet til å lese inn XML
        # Flere løyper
        # Gaffling og sommerfugl pluss fandens oldemor

        print('helle')


        #
        # if name.text == filename:
        #     for printarea in course.iter('print-area'):
        #         #Utskriftsdata
        #         ppen.append(float(printarea.attrib.get('left')))
        #         ppen.append(float(printarea.attrib.get('top')))
        #         ppen.append(float(printarea.attrib.get('right')))
        #         ppen.append(float(printarea.attrib.get('bottom')))
        #         ppen.append(float(printarea.attrib.get('page-margins')))
        #         ppen.append(float(printarea.attrib.get('page-width')))
        #         ppen.append(float(printarea.attrib.get('page-height')))

# def main():
#
#     map = PurplePen('course.ppen')
#
# main()

#------------------------Gammelt grums --------------------------
# Her ligger data for Melhuskartene
##Kart=[Øst,Nord,vinkel,pixel_per_meter]
#Anemarka=[561000, 7017000, 0.077672,0.635 ]
#Gimse=[561000, 7017000, 0.077672, 0.635]
#Oyberga=[562000, 7021000, -2.4, 0.8466666667 ]
#Skjetnemarka=[560320, 7012550, -1.4, 0.8466666667]
#Vassfjellet=[567000, 7016500, 0.0, 1.27 ]
## Andre kart
#Fremo=[569000, 7009000, 0.0, 0.8466666667]

#if mapname== "Anemarka":
#    omap=Anemarka
#elif mapname== "Gimse":
#    omap=Gimse
#elif  mapname=="Oyberga":
#    omap=Oyberga
#elif  mapname== "Skjetnemarka":
#    omap=Skjetnemarka
#elif  mapname== "Vassfjellet":
#    omap=Vassfjellet
#elif  mapname== "Fremo":
#    omap=Fremo
#


#        
#    if args.pdf:
#        dpi=150
##        with Image(filename=filnavn+'.pdf', resolution=dpi) as img:
##            img.background_color = Color("white")
##            img.alpha_channel = False
##            img.trim(Color("WHITE"))
##            img.save(filename=filnavn+'.png')
#            
#        #Henter inn fra purple pen filen
#        tree = ET.parse(filnavn+".ppen")
#        root = tree.getroot()
#        
#        #Hent data fra Purple Pen fila
#        for printarea in root.iter('print-area'):
#            #Utskriftsdata
#            ppen.append(float(printarea.attrib.get('left')))
#            ppen.append(float(printarea.attrib.get('top')))
#            ppen.append(float(printarea.attrib.get('page-margins')))
#            ppen.append(float(printarea.attrib.get('page-width')))
#            ppen.append(float(printarea.attrib.get('page-height')))
#            
#        # Hent data for "dummy-post i øverste hjørne av utskriftområdet. Er dette nødvendig?
#        for control in root.iter('control'):
#            control.attrib
#            for code in control.iter('code'):
#                if code.text =='999':
#                    for location in control.iter('location'):
#                        ppen.append(float(location.attrib.get('x')))
#                        ppen.append(float(location.attrib.get('y')))
#                
#        # Finner venstre topp hjørne på kartet
#        map_x=[ppen[0]-ppen[2]*dpi/100]#-omap[3]*5]
#        map_y=[ppen[1]+ppen[2]*dpi/100]#+omap[3]*5]
#        
#        
##    for ControlPosition in root.iter('ControlPosition'):
##        pos_x.append(ControlPosition.attrib.get('x'))
##        pos_y.append(ControlPosition.attrib.get('y'))
#
#        
    #omap.append(float(map_x[0]))
    #omap.append(float(map_y[0]))
