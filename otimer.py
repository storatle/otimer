#!/usr/bin/env python3
# coding: utf8 e

import serial

import map as mp
import ecard as ec

# Lese inn fra brikke kontinuerlig
# Lag ny brikke

brikke = ec.Ecard()


# Henter inn løyper fra kartet. Denne inneholder alle løyper

#kart = mp.fromPurplePen('course.ppen')
kart = mp.fromXml('trening.xml')


def check_codes(brikke, kart):

    codes_ec = brikke.codes
    ind = 0
    chk = []
    correct = False
    for course in kart.courses:
        for var in course.variations:
            codes = var.codes
            for code in codes:
                if code in codes_ec[ind:]:
                    ind = ind + codes_ec[ind:].index(code)+1
                    chk.append(code)

            if chk == codes:
                correct = True

    print(chk)
    print(codes_ec)
    print(codes)

    return correct



    #codes_mp = kart.courses[0].code_list()



def main():
    if check_codes(brikke, kart):
        brikke.print()
    else:
        print('Feil')


main()





# Her skal du lage en snutt som sjekker lest ecard mot koder fra map

