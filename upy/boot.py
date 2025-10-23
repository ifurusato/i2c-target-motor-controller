# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal
import pyb

pyb.country('US') # ISO 3166-1 Alpha-2 code, eg US, GB, DE, AU
#pyb.usb_mode('CDC')
pyb.usb_mode('VCP+MSC') # temporarily restore default USB config
#pyb.main('main.py') # main script to run after this one
