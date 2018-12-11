#!/usr/bin/env python3
# coding: utf8 e

import serial

import map as mp
import ecard as ec


brikke = ec.Ecard()

codes_ec = brikke.codes

kart = mp.PurplePen('course.ppen')

codes_mp = kart.courses[0].code_list()


print(codes_ec)
print(codes_mp)




# Her skal du lage en snutt som sjekker lest ecard mot koder fra map

