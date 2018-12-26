#!/usr/bin/env python3
# coding: utf8 e

import serial

import map as mp
import ecard as ec

# Lese inn fra brikke kontinuerlig
# Lag ny brikke

#brikke = ec.Ecard()


# Henter inn løyper fra kartet. Denne inneholder alle løyper

#kart = mp.fromPurplePen('course.ppen')
#kart = mp.fromXml('course.xml')


def print_all_codes(kart):

    for course in kart.courses:
        for var in course.variations:
            s = (str(var.codes).strip('[]'))
            s= s.replace(',', '')
            if not var.name:
                var.name = ''
            s = course.name + ' ' + var.name + ': ' + s
            print(s)




    #codes_mp = kart.courses[0].code_list()

class runner:

    def __init__(self, filname):
        #filnavn = 'Treningsløp_uke01.xml'
        self.brikke = ec.Ecard()
        self.kart = mp.fromXml(filname)
        self.name = ''
        self.find_name(self.brikke.e_num)


    def check_codes(self):

        codes_ec = self.brikke.codes
        ind = 0
        self.chk = []
        correct = False
        for course in self.kart.courses:
            for var in course.variations:
                codes = var.codes
                for code in codes:
                    if code in codes_ec[ind:]:
                        ind = ind + codes_ec[ind:].index(code)+1
                        self.chk.append(code)

                if self.chk == codes:
                    correct = True

        #print(chk)
        #print(codes_ec)
        #print(codes)

        return correct

    def find_name(self, num):

        if num == 215066:
            self.name = 'Oskar Storler'
        # henter navn fra database

    def print(self):
        num_ctrl = 0
        print('Brikkenummer ' + str(self.brikke.e_num))
        print('Navn: ' + self.name)
        print('Sluttid ' + ec.set_time(self.brikke.times[-1]))
        i = 1
        output = list(zip(self.brikke.codes, self.brikke.legs, self.brikke.times))
        for item in output[:-2]:
            print(
                'Post ' + str(i).zfill(2) + ':  ' + ec.set_time(item[2]) + '  ' + ec.set_time(item[1]) + '  ' + str(item[0]))
            i += 1

        item = output[-2]
        print('Post ' + 'F ' + ':  ' + ec.set_time(item[2]) + '  ' + ec.set_time(item[1]) + '  ' + str(item[0]))

def main():
    filnavn = 'course.xml'
    #filnavn = 'Treningsløp_uke01.xml'

    oskar = runner(filnavn)

    print_all_codes(oskar.kart)

    if oskar.check_codes():
        print('ok')
        oskar.print()

    else:
        print('Løper mangler poster')


main()





# Her skal du lage en snutt som sjekker lest ecard mot koder fra map

