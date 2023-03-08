# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 09:19:16 2023

@author: 송강
"""

import time

from SRT import SRT
srt = SRT("01083878003","dksthd1@3")
dep = '동대구'
arr = '수서'
date = '20230228'
timee = '090000'

# [[SRT] 09월 30일, 수서~부산(15:00~17:34) 특실 예약가능, 일반실 예약가능,
# [SRT] 09월 30일, 수서~부산(15:30~18:06) 특실 예약가능, 일반실 예약가능,
# [SRT] 09월 30일, 수서~부산(16:00~18:24) 특실 매진, 일반실 예약가능,
# [SRT] 09월 30일, 수서~부산(16:25~18:45) 특실 예약가능, 일반실 예약가능, ...]
reservation = None
for j in range(10000):
    trains = srt.search_train(dep, arr, date, timee)
    for train in trains:
        if train.dep_time in "142300":
            print("ok")
            reservation = srt.reserve(train)
            break
    if reservation is not None:
        break
    time.sleep(1)