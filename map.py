#!/usr/bin/env python
#coding: utf8 e

import xml.etree.ElementTree as ET
import numpy as np
import argparse
import sys
#from wand.image import Image


class fromXml:

    def __init__(self, filename):
        self.controls = []
        self.courses = []
        self.variations = []
        self.read_xml(filename)

    # Denne er tatt fra worldfile.py
    def read_xml(self, filnavn):

        # Henter inn data fra IOF utveklsingsfil
        try:
            tree = ET.parse(filnavn)

        except:
            sys.exit("Oops! Har du riktig IOF utvekslingsfil (.xml) i katalogen? ")

        root = tree.getroot()

        scale = (float(root[2][0].text))/1000 # koordinater i Purple pen er mm???

        map=[] #Kartinfo [Målestokk, Venstre, Topp]


         #Henter inn skala og koordinater for øvre venstre hjørne
        for mapinfo in root.iter('Map'):
            map.append(float(mapinfo[0].text))
            map.append(float(mapinfo[1].attrib.get('x')))
            map.append(float(mapinfo[1].attrib.get('y')))

        #Her må jeg legge inn alle controller.

        for control in root.iter('Control'):
            self.controls.append(Control((int(control[0].text), float(control[2].attrib.get('x')), float(control[2].attrib.get('y')), 'normal')))
            self.controls[-1].set_utm(float(control[1].attrib.get('x')), float(control[1].attrib.get('y')))

        for control in root.iter('StartPoint'):
            self.controls.append(Control((control[0].text, float(control[2].attrib.get('x')), float(control[2].attrib.get('y')), 'start')))
            self.controls[-1].set_utm(float(control[1].attrib.get('x')), float(control[1].attrib.get('y')))

        for control in root.iter('FinishPoint'):
            self.controls.append(Control((control[0].text, float(control[2].attrib.get('x')), float(control[2].attrib.get('y')), 'finish')))
            self.controls[-1].set_utm(float(control[1].attrib.get('x')), float(control[1].attrib.get('y')))

        for course in root.iter('Course'):
            self.courses.append(Course((course[1].text, course[0].text)))
            self.variations = []
            for variation in course.iter('CourseVariation'):
                self.variations.append(Variation((course[0].text, variation[0].text)))
                for name in variation.iter('Name'):
                    self.variations[-1].set_name(name.text)

                for name in variation.iter('StartPointCode'):
                    self.variations[-1].set_startpoint(name.text)

                for control in variation.iter('CourseControl'):
                    self.variations[-1].set_code(control[1].text)

                self.variations[-1].set_code('100')
                self.variations[-1].set_controls(self.controls)
                self.variations[-1].set_leg_length()
                self.variations[-1].check_name()

            self.courses[-1].set_variations(self.variations)

class Variation:

    def __init__(self, var):
        self.course_id = var[0]
        self.id = var[1] # Variation id
        self.name = None
        self.startpoint = None
        self.codes = []
        self.order = []
        self.controls = []
        self.dl = []

    def check_name(self):
        if not self.name:
            self.name = self.course_id

    def set_name(self, name):

        self.name = name

    def set_startpoint(self, name):
        self.startpoint = name

    def set_code(self,code):
        self.codes.append(int(code))

    def set_order(self, order):
        self.order = order

    def set_controls(self, controls):
        # Finne startkode først
        for ctrl in controls:
            if ctrl.kind == 'start':
                self.controls.append(ctrl)
                break
        for code in self.codes:
            for control in controls:
                if code == int(control.code):
                    self.controls.append(control)
                    break

    def set_leg_length(self):
        self.dl = []
        scale = 0.01
        for i in range(0, len(self.controls)-1):
            dx = (self.controls[i].x - self.controls[i+1].x)
            dy = (self.controls[i].y - self.controls[i+1].y)

            self.dl.append(np.sqrt(dx**2 + dy**2)*scale)

    def length(self):
        return sum(self.dl)


class Course:

    def __init__(self, crs):
        self.id = crs[0]
        self.name = crs[1]
        self.codes = []
        self.order = []
        self.x = []
        self.y = []
        self.var_id = 0
        self.kind = None
        self.first_ctrl = 0
        self.variations = []
        self.numvar = 0
        self.loops = []

    def set_kind(self, kind):
        self.kind = kind

    def set_first_ctrl(self, code):
        self.first_ctrl = code

    def set_variations(self, var):
        self.variations = var
        self.numvar = len(var)

    def set_loops(self, var):
        self.loops.append(var)

    # Setter rekkefølgen fra purple pen fila. Her må jeg sjekke om det er variasjoner
    # Flytt denne til variasjoner

    def set_order(self, order):
        next_ctrl = self.first_ctrl
        loop = False
        n = 1
        i = 1
        while next_ctrl:
            for control in order:
                if control[0] == next_ctrl:
                    if control[3] == 'loop'and not loop:# Nå er vi igang med en loop hvordan skal jeg klare å få den til å sjekke begge runder

                        if i == 1:
                            course_id = 0
                            variation_id = 0
                            self.variations.append(Variation((course_id, variation_id)))
                            self.variations[-1].set_name('A')
                            self.variations[-1].set_order(self.order[:])

                            next_ctrl = self.loops[0][i]
                        elif i >= len(self.loops[0]):
                            loop = False
                            next_ctrl = control[1]
                            self.order.append(control[2])
                            i = 1
                            break
                        else:
                            next_ctrl = self.loops[0][i]
                        # control = list(control)
                        # control[0] = self.loops[0][i]
                        i += 1
                        loop = True
                    else:
                        self.order.append(control[2])
                        next_ctrl = control[1]
                        loop = False
                        break

        self.variations[-1] # Her må jeg lage ny variasjon 'Bæ' How the hell?

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
    # Denne bør være i Variations

    def set_leg_length(self, controls): # Flyttet til vriations
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

        self.code = ctrl[0] # Her burde jeg endre koden fra string til int
        self.x = ctrl[1]
        self.y = ctrl[2]
        self.kind = ctrl[3]
        self.x_utm = 0
        self.y_utm = 0
        self.id = 0  # .zfill(2)
        self.name = None
        self.set_name()

    def set_name(self):
        if self.kind == 'start':
            self.name = self.code.replace("TA","")
            self.code = '0'
        if self.kind == 'finish':
            self.name = self.code
            self.code = '100'

    def set_utm(self, x, y):
        self.x_utm = x
        self.y_utm = y


def code_list(order,controls):
    codes = []
    for o in order:
        codes.append(controls[0])

        class fromPurplePen:

            def __init__(self, filename):

                self.controls = []
                self.courses = []
                self.variations = []

                self.read_ppen(filename)
                self.set_courses()

            def read_ppen(self, filename):

                # Henter inn data fra Purple Pen
                try:
                    tree = ET.parse(filename)
                except:
                    sys.exit("Oops! Har du riktig Purple Pen-fil (.ppen) i katalogen? ")

                root = tree.getroot()

                # Henter data fra Purple Pen fila
                for event in root.iter('event'):
                    for map in event.iter('map'):
                        self.scale = map.attrib.get('scale')

                # Leser inn alle postene
                for ctrl in root.iter('control'):
                    x = None
                    y = None
                    for loc in ctrl.iter('location'):
                        x = loc.attrib.get('x')
                        y = loc.attrib.get('y')
                    self.controls.append(Control((ctrl.attrib.get('id'), ctrl[0].text, x, y, ctrl.attrib.get('kind'))))

                # Leser inn løypene
                for crs in root.iter('course'):  # Mulig at jeg bør legge inn dette i en loop

                    self.courses.append(Course((crs.attrib.get('id'), crs[0].text)))
                    self.courses[-1].set_first_ctrl(crs[2].attrib.get('course-control'))

                    # , crs.attrib.get('kind'), crs.attrib.get('order'), crs[1].attrib.get('label-kind'), crs[2].attrib.get('course-control'))))
                order = []
                for cc in root.iter('course-control'):
                    # variation = []
                    vr = []
                    next = None
                    # Finner neste post
                    for nxt in cc.iter('next'):
                        next = (nxt.get('course-control'))
                    for var in cc.iter('variation'):
                        vr.append(var.get('course-control'))  # Sjekker om det er en variation

                    if vr:
                        vr = tuple(vr)
                        self.courses[-1].set_loops(vr)

                    order.append((cc.attrib.get('id'), next, cc.attrib.get('control'), cc.attrib.get('variation')))

                self.courses[-1].set_order(order)

            def set_courses(self):

                for course in self.courses:
                    # course.set_order(self.order)
                    course.set_codes(self.controls)
                    course.set_leg_length(self.controls)

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
