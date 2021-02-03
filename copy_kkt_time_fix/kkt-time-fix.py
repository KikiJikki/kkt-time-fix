# -*- coding: utf-8 -*-
import sys
import os
from libfptr10 import IFptr
from datetime import datetime
import logging

fptr_lib = IFptr(r"C:\Program Files (x86)\ATOL\Drivers10\KKT\bin\fptr10.dll")
fptr = IFptr("")

#---- Настройка логирования

_log_format = f"%(asctime)s - [%(levelname)s] - %(message)s"
logging.basicConfig(filename="c:\\transfert\\log\\kkt-time-fix-log.txt", level=logging.DEBUG, format=_log_format)


#---- Подключения через указания USB

fptr.setSingleSetting(IFptr.LIBFPTR_SETTING_PORT, str(IFptr.LIBFPTR_PORT_USB))

fptr.applySingleSettings()
fptr.open()
isOpened = fptr.isOpened()
if isOpened == 0:
        logging.error("Не удалось открыть соединение с ККМ!")
        f = open(os.path.join('c:\\transfert\\log\\','kkt-time-fix-status.txt'), 'w')
        f.write('Не удалось открыть соединение с ККМ!')
        f.close()
        sys.exit()
        
#------------------------------------------------


#---- Проверка времени на компьютере


#---- Проверка времени на ККМ

fptr.setParam(IFptr.LIBFPTR_PARAM_DATA_TYPE, IFptr.LIBFPTR_DT_DATE_TIME)
fptr.queryData()
dateTimeKKM = fptr.getParamDateTime(IFptr.LIBFPTR_PARAM_DATE_TIME)


#---- Проверка какое время первое

if datetime.now() > dateTimeKKM:
        delta = datetime.now() - dateTimeKKM
if datetime.now() < dateTimeKKM:
        delta = dateTimeKKM - datetime.now()

#---- Если время на ккм и компьютере отличается больше чем на час, значит ошибка времени на кассе

logging.info("Разница во времени %s секунд", delta)
if delta.seconds > 3600:
           logging.error ("Проблема времени на компьютере")
           f = open(os.path.join('c:\\transfert\\log\\','kkt-time-fix-status.txt'), 'w')
           f.write('Проблема времени на компьютере')
           f.close()
           fptr.close()
           del fptr
           sys.exit()

#---- Если время на ккм и компьютере отличается меньше чем на полторы минуты


if delta.seconds < 90:
        logging.info ("Все хорошо, синхронизация времени не требуется")
        f = open(os.path.join('c:\\transfert\\log\\','kkt-time-fix-status.txt'), 'w')
        f.write('Синхронизация не требуется')
        f.close()
        fptr.close()
        del fptr
        sys.exit()

#---- Синхронизация времени ккм и пк
        
if delta.seconds > 90:
        logging.warning ("Корректируем время на ккм")
        fptr.setParam(IFptr.LIBFPTR_PARAM_DATE_TIME, datetime.now())
        fptr.writeDateTime()
        f = open(os.path.join('c:\\transfert\\log\\','kkt-time-fix-status.txt'), 'w')
        f.write('Время ккм и пк синхронизировано ')
        f.close()



#-----------------------------------------
fptr.close()
del fptr






