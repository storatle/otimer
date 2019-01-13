#!/usr/bin/env python3
# coding: utf8 e


import sys
from datetime import datetime, timedelta
import itertools
import argparse
import serial

# from subprocess import call
# import glob
# import os


# parser = argparse.ArgumentParser(description='Tidtagersystem for EMit og Rasberry pi')
# #parser.add_argument('a', help="Initier løpet. Legg inn poster og løyper")
# #parser.add_argument('b',  help="tekst som skal byttes inn")
# parser.add_argument('-i',   "--init", action="store_true",  help="Initier løpet. Legg inn poster og løyper")
# parser.add_argument('-s',   "--start", action="store_true",  help="Start å lese inn brikker")
# parser.add_argument('-r',   "--results", action="store_true",  help="lag resultatlister")
# #parser.add_argument('-ap',   "--partartist", action="store_true",  help="bytte ut sjanger på artist. Søker etter deler av navnet flactag.py -a artist sjanger")
# args = parser.parse_args()

br222072 = bytearray(
    b'\xff\xff\xff\xff\xe6M\x10<\x12\x0c\x0b\x0f\x1e:\x00\x00\xe4\x1a\xe7\xffxc\x03\x1f\x0f\xf4\x00\x00\x00\xfa\xe1\x14\xfa\xfd\xe1\xfam\x00\xfa\x9a1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Emit EPT V5.00                          S0034P0012L0022 P\x00')

br211421 = bytearray(
    b'\xff\xff\xff\xff\xe6M\x10<\x12\x0c\x0b\x0f\x1f\x0f\x00\x00\xe5\x1a\xe7\xff\xdd9\x03\x07\x0f\xd1\x00\x00\x00d\x01\x00\xfa\xd1\x14\xfa\xa7 \xfa\xfa\x05\xfa\x00\x00\xfa\xc01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Emit EPT V4.20                          S0041P0009L0031 \x1c\x00')

br211419 = bytearray(
    b'\xff\xff\xff\xff\xe6M\x10<\x12\x0c\x0b\x0f\x1f3\x00\x00\xe7\x1a\xe7\xff\xdb9\x03\x07\x0f\xd3\x00\x00\x00\x97\xc7\x02\x91\xae\x03\xa8s\x04\x8f\x12\x07\x9dV\x07\x94\xb3\x08\x95\xa7\t\xaa|\n'
    b'\x96\xb7\n'
    b'\xaf\xe3\n'
    b'\xfa\xef\n'
    b'\xfa\x00\x00c\x01\x00\xfa"\x01c"\x01\xfa\xfa\xb5\x0c\xfaH\x14\xfa\x00\xfa\x0c\xfa\xad\x07\xfa\x00\x00\xfa\x8c1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Emit EPT V4.20                          S0035P0014L0020 \xe5\x00')

br215066 = bytearray(b'\xff\xff\xff\xff\xe6M\x10<\x12\x0c\x0b\x0f&\x05\x00\x00\xec\x1a\xe7\xff\x1aH\x03\n'
                     b"\x0f\x82\x00\x00\x00|b\x00cx\x01\x83\xed\x01e\x9d\x03\x81F\x04\x84\x1d\x05&\xa3\x05%\xfe\x05\x85I\x06'\x13\x07{L\x08}9\t\x82\xce\t~\t\x0bd7\x0b\xfa\x8f\x0b\xfag#\xfa\x06\x8d\xfa\x00\x00\xfa\xa0\xdd\xfa\x00\x00\xfa\x0c3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Emit EPT V5.00                          S0121P0018L0103 O\x00")


# filename = '211421.txt'
# filename = '211419.txt'
# filename = '215066.txt' # Denne fila har et hopp midt i koderekken
# filename = '222072.txt'
#
# class course:
#     def __init__(self,input):
#         y=input.split(' ', 1)
#         self.navn = y[0]
#
#
# class eCard:
#     def __init_(self, data):
#         self.number = data


class Ecard:


    def __init__(self, array):
        #array = br215066
        self.dump = []
        self.e_num = 0

        self.codes = []
        self.times = []
        self.legs = []
        self.read_ecard(array)
        self.get_ecard_number()
        #self.get_codes()
        self.get_codes_and_times()

        #self.print()

    def read_ecard(self, array):
        # Denne her må sette opp slik at jeg leser direkte fra serieport
        # Bruk read line

        # brikkenr = br211419
        #brikkenr = br215066
        # brikkenr = br222072

        # brikkenr = br211421
        for byte in array:
            self.dump.append(byte)
            # print(byte)
            #print(hex(byte))

    def read_port(self):
        # Denne må undersøker i branch serial
        ser = serial.Serial()
        ser.baudrate = 9600
        ser.bytesize = serial.EIGHTBITS
        ser.parity = serial.PARITY_NONE
        ser.stopbits = serial.STOPBITS_ONE
        # ser.xonxoff=1
        # ser.rtscts=1
        ser.timeout = 1
        ser.port = "/dev/ttyUSB0"

        ser.open()
        count = 0
        stack = []
        f = open("brikkenummer.txt", "w+")

        while 1:
            x = ser.readline()
            print(x)
            f.write(str((x)) + '\n')

        for byte in x:
            self.dump.append(byte)
            # print(byte)
            print(hex(byte))

        # while count < 200:  # Her må du definere end of line
        #
        #     # p1_raw = str(ser.readline())
        #
        #     # with open('test.txt', 'a') as file:
        #
        #     p1_raw = ser.read()
        #
        #     # print(int.from_bytes(p1_raw, byteorder='big'))
        #
        #     # file.write(p1_raw)
        #
        #     print((p1_raw))
        #     f.write(str((p1_raw)) + '\n')
        #     # print(ord(p1_raw))
        #     # a = ord(p1_raw)
        #     # print(chr(a))
        #     count = count + 1
        # bytes
        ser.close()
        f.close()

    def get_ecard_number(self):

        # Find brikkenummer
        a = hex(self.dump[20])
        b = hex(self.dump[21])
        c = hex(self.dump[22])
        self.e_num = int((c + b[2:] + a[2:]), 16)

    def get_codes_and_times(self):
        code_num = []
        i = 0
        # Finner der hvor vi har 3 nuller på rad.
        for byte in self.dump:  # Mulig jeg burde bruke while sløyfe
            # info.append(int(byte))
            if int(byte) == 0:
                j += 1
                zero = True
                if j == 3:
                    code_num.append(i)
                    break
            else:
                zero = False
                j = 0

            # print(int(byte))
            i += 1

        # Finn koder og tid
        j = code_num[0] + 1
        i = 1
        time = 0

        last_time = timedelta(0)
        while self.dump[j] > 0:
            time = (calc_time(self.dump[j + 1], self.dump[j + 2]))
            self.times.append(time)
            self.legs.append(time - last_time)
            self.codes.append(self.dump[j])
            # print('Post ' + str(i) + ':  ' +str(time - last_time) +'  ' + str(time) + '  ' + str(info[j]))
            last_time = time

            if self.dump[j] == 250:
                #num_ctrl = i - 2
                break
            i += 1
            j = j + 3

    # def print(self):
    #     num_ctrl = 0
    #     print('Brikkenummer ' + str(self.e_num))
    #     print('Sluttid ' + set_time(self.times[-1]))
    #     i = 1
    #     output = list(zip(self.codes, self.legs, self.times))
    #     for item in output[:-2]:
    #         print('Post ' + str(i).zfill(2) + ':  ' + set_time(item[2]) + '  ' + set_time(item[1]) + '  ' + str(item[0]))
    #         i += 1
    #
    #     item = output[-2]
    #     print('Post ' + 'F ' + ':  ' + set_time(item[2]) + '  ' + set_time(item[1]) + '  ' + str(item[0]))

    def codes(self):
        return self.codes()




# def main():
#     brikke = Ecard()


def set_time(td):
    m = int(td.seconds / 60)
    s = int(td.seconds - (m * 60))
    return str(m).zfill(2) + ':' + str(s).zfill(2)


def calc_time(byte1, byte2):
    a = hex(byte1)
    if len(a) < 4:
        a = insert_null(a)
    b = hex(byte2)
    if len(b) < 4:
        b = insert_null(b)
    num = int(b + a[2:], 16)
    sec = timedelta(seconds=num)
    return sec


def insert_null(byte):
    return byte[:2] + '0' + byte[2:]

    # finn første kode
    # Tell till du finner 3 nuller på rad
    # Sjekk første kode

    # int((c+b[2:]+a[2:]),16)
    # 211419
    # c=hex(3)
    # b = hex(99)
    # a = hex(120)

    # 222072

    # int((c+b[2:]+a[2:]),16)


#main()

# if  (args.start):
#     cont =1
#     courses=[]
#     while (cont):
#         input=raw_input("Skriv inn løypene: løypenavn og postkoder (rød 123 145 ...): ")
#         if input:
#             courses.append(course(input))
#         else:
#             cont =0
#
#
