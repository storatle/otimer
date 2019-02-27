#!/usr/bin/env python3

import map as mp
import os
# Format på codes.txt
# Klasse;Løype;Lengde;S1;Lengde;kode;lengde:kode;lengde;kode

dir_path = 'C:\\Users\\atlep\\Desktop\\'
dir_path = './'
def print_all_codes(kart):
    s = ''
    with open(dir_path+'codes.txt', 'w') as the_file:
        for course in kart.courses:
            for var in course.variations:
                for i in range(0, len(var.codes)):
                    s = s + str("%.3f" % var.dl[i]) +';'
                    s = s + str(var.codes[i]) +';'

                    #s = (str(var.codes).strip('[]'))
                #s = s.replace(',', '')
                if not var.name:
                    var.name = ''
                s = course.name + ';' + var.name + ';' + s
                print(s)
                the_file.write(s+'\n')

def main():
    #dir_path = os.path.dirname(os.path.realpath(__file__))
    #print(dir_path)

    kartfil = dir_path+'course.xml'
    #kartfil = 'trening.xml'

    map = mp.fromXml(kartfil)
    print_all_codes(map)


main()
