[app]
title = GestorMasterS.ILMVC
package.name = gestormastersilmvc
package.domain = com.scorpiomaster066
source.dir =.
source.include_exts = py,png,jpg,kv,atlas,db,json,txt
version = 1.0.0
requirements = python3,kivy==2.3.0,kivymd,requests,urllib3,chardet,certifi,idna,pillow,plyer
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license_agreements = True
p4a.bootstrap = sdl2
p4a.whitelist = lib-dynload,sqlite3

[buildozer]
log_level = 2
warn_on_root = 0
