#!/usr/bin/env python3
# coding: utf8 e

import serial

import map as mp
import ecard as ec
import pymysql

br215066 = bytearray(b'\xff\xff\xff\xff\xe6M\x10<\x12\x0c\x0b\x0f&\x05\x00\x00\xec\x1a\xe7\xff\x1aH\x03\n'
                     b"\x0f\x82\x00\x00\x00|b\x00cx\x01\x83\xed\x01e\x9d\x03\x81F\x04\x84\x1d\x05&\xa3\x05%\xfe\x05\x85I\x06'\x13\x07{L\x08}9\t\x82\xce\t~\t\x0bd7\x0b\xfa\x8f\x0b\xfag#\xfa\x06\x8d\xfa\x00\x00\xfa\xa0\xdd\xfa\x00\x00\xfa\x0c3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Emit EPT V5.00                          S0121P0018L0103 O\x00")


# Lese inn fra brikke kontinuerlig
# Lag ny brikke

# brikke = ec.Ecard()


# Henter inn løyper fra kartet. Denne inneholder alle løyper

# kart = mp.fromPurplePen('course.ppen')
# kart = mp.fromXml('course.xml')


def print_all_codes(kart):
    for course in kart.courses:
        for var in course.variations:
            s = (str(var.codes).strip('[]'))
            s = s.replace(',', '')
            if not var.name:
                var.name = ''
            s = course.name + ' ' + var.name + ': ' + s
            print(s)

    # codes_mp = kart.courses[0].code_list()


class Runner:

    def __init__(self, filname, bytearray):
        # filnavn = 'Treningsløp_uke01.xml'
        self.brikke = ec.Ecard(bytearray)
        self.kart = mp.fromXml(filname)
        self.name = ''
        self.find_name(self.brikke.e_num)
        self.sluttid = ec.set_time(self.brikke.times[-1])


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
                        ind = ind + codes_ec[ind:].index(code) + 1
                        self.chk.append(code)

                if self.chk == codes:
                    correct = True

        # print(chk)
        # print(codes_ec)
        # print(codes)

        return correct

    def find_name(self, num):

        # Henter navn fra database

        names = read_from_database()

        for name in names:
            if name[6] == self.brikke.e_num:
                self.name = name[2]
                break


    def print(self):
        num_ctrl = 0
        print('Brikkenummer ' + str(self.brikke.e_num))
        print('Navn: ' + self.name)
        print('Sluttid ' + ec.set_time(self.brikke.times[-1]))
        i = 1
        output = list(zip(self.brikke.codes, self.brikke.legs, self.brikke.times))
        for item in output[:-2]:
            print(
                'Post ' + str(i).zfill(2) + ':  ' + ec.set_time(item[2]) + '  ' + ec.set_time(item[1]) + '  ' + str(
                    item[0]))
            i += 1

        item = output[-2]
        print('Post ' + 'F ' + ':  ' + ec.set_time(item[2]) + '  ' + ec.set_time(item[1]) + '  ' + str(item[0]))


def read_from_database():
    # Legge inn ny mysql-database lokalt
    # mysql - u atle - p  resultatdatabase < brikkesys.sql

    db = pymysql.connect(host="localhost", user="atle", passwd="password", db="resultatdatabase")
    names = None
    cursor = db.cursor()

    # Henter alle løp
    sql = " SELECT * FROM names"

    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        names = cursor.fetchall()

    except:
        print("Error: unable to fecth data")

    return names

def main():
    runners = []
    # serialport = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)
    read = True

    #read_database()

    while read:
        # command = serialport.read()

        command = br215066
        print(str(command))

        kartfil = 'course.xml'
        # filnavn = 'Treningsløp_uke01.xml'

        runners.append(Runner(kartfil, command))

        print_all_codes(runners[-1].kart)

        if runners[-1].check_codes():
            print('ok')
            runners[-1].print()

        else:
            print('Løper mangler poster')

        read = False


main()

# Her skal du lage en snutt som sjekker lest ecard mot koder fra map
