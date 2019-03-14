#!/usr/bin/env python3

import map as mp
import os
import argparse



# Format på codes.txt
# Klasse;Løype;Lengde;S1;Lengde;kode;lengde:kode;lengde;kode



dir_path = 'C:\\Users\\atlep\\Desktop\\'
dir_path = './'

def print_all_codes(kart,f_out):
    s = ''
    with open(dir_path+f_out, 'w') as the_file:
        for course in kart.courses:
            for var in course.variations:
                # course.name;var.name;0;Total_lengde;0;Startkode;lengde;kode....
                s = course.name + ';'+ course.name +'-'+ var.id + ';0;'+str('%.3f' % var.length())+';0;'+'S1;' # Når jeg gjør dette så kan jeg bare ha en start
                for i in range(0, len(var.codes)):
                    
                    s = s + str("%.3f" % var.dl[i]) +';'
                    s = s + str(var.codes[i]) +';'
                s = s[:-1]
                print(course.name + ' ' + course.name + '-' + var.id + ' ' + str(var.codes))
                the_file.write(s+'\n')

def main():
    parser = argparse.ArgumentParser(description='Leser løypa i IOF xml-format og lager en OCAD textfil som kan importeres i Brikkesys')
    parser.add_argument('input', help="Løypefil i IOF xml format")
    parser.add_argument('output', help="Tekstfil for kodeliste,  (koder.txt)",  nargs='*')
    args = parser.parse_args()

    if args.input:
        print(args.input)
        f_in = args.input
        has_inputfile=True
    else:
        if os.path.exists('./course.xml'):
            f_in = 'course.xml'
        else:
            sys.exit('Du må skrive inn et filenavn')

    if args.output:
        f_out = args.output[0]
    else:
        f_out = 'koder.txt'


    kartfil = dir_path+f_in
    map = mp.fromXml(kartfil)
    print_all_codes(map,f_out)


if __name__ == '__main__':
    main()
