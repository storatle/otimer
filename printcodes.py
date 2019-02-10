#!/usr/bin/env python3

import map as mp


def print_all_codes(kart):
    with open('somefile.txt', 'w') as the_file:
        for course in kart.courses:
            for var in course.variations:
                s = (str(var.codes).strip('[]'))
                s = s.replace(',', '')
                if not var.name:
                    var.name = ''
                s = course.name + ' ' + var.name + ': ' + s
                print(s)
                the_file.write(s+'\n')

def main():
    kartfil = 'course.xml'
    kartfil = 'trening.xml'

    map = mp.fromXml(kartfil)
    print_all_codes(map)


main()
