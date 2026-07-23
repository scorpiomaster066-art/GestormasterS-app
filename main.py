from kivy.metrics import dp
from kivymd.app import MDApp
from kivy.lang import Builder

KV = '''
ScreenManager:
    MDScreen:
        md_bg_color: 0,0,0,1
        MDBoxLayout:
            orientation: 'vertical'
            MDTopAppBar:
                title: "GestorMasterS"
                pos_hint: {"top": 1}
            ScrollView:
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: dp(15)
                    spacing: dp(15)
                    adaptive_height: True
                    MDLabel:
                        text: "GestorMasterS NEGRA OK FIJA"
                        halign: "center"
                        size_hint_y: None
                        height: self.texture_size[1]
                        text_color: 1,1,1,1
                    MDRaisedButton:
                        text: "Boton 1"
                        pos_hint: {"center_x":.5}
                    MDRaisedButton:
                        text: "Boton 2"
                        pos_hint: {"center_x":.5}
                    MDRaisedButton:
                        text: "Boton 3"
                        pos_hint: {"center_x":.5}
'''

class GestorMasterSApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

GestorMasterSApp().run()
