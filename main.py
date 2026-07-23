import os
from pathlib import Path
from kivymd.app import MDApp
from kivy.lang import Builder

KV = '''
ScreenManager:
    MDScreen:
        md_bg_color: 0,0,0,1
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(20)
            MDLabel:
                text: 'GestorMasterS NEGRA OK #32'
                halign: 'center'
                text_color: 1,1,1,1
'''

class GestorMasterSApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

GestorMasterSApp().run()
