# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 10:23:09 2023

@author: 송강
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET = "django-insecure-s)y)i5n*2ci53l1kr8u-@dwhkgp7qv_#_m2xh7^b(ma&k5nni6"
# 꼭 변수명이 SECRET일 필요는 없으나, SECRET_KEY에 대한 내용이니 통일성을 유지하자

DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# 마찬가지로 변수명이 database일 필요는 없으나 통일성 유지!