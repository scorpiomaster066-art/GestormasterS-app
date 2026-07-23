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
                title: "GestorMasterS #32 BOTONES OK"
                pos_hint: {"top": 1}
            ScrollView:
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: dp(20)
                    spacing: dp(20)
                    adaptive_height: True
                    MDLabel:
                        text: "GestorMasterS NEGRA OK #32 BOTONES FIX"
                        halign: "center"
                        size_hint_y: None
                        height: self.texture_size[1]
                        theme_text_color: "Custom"
                        text_color: 1,1,1,1
                    MDRaisedButton:
                        text: "Boton 1 - YA NO ENCIMADO"
                        pos_hint: {"center_x":.5}
                        size_hint_x:.8
                    MDRaisedButton:
                        text: "Boton 2"
                        pos_hint: {"center_x":.5}
                        size_hint_x:.8
                    MDRaisedButton:
                        text: "Boton 3"
                        pos_hint: {"center_x":.5}
                        size_hint_x:.8
                    MDRaisedButton:
                        text: "Boton 4 PRUEBA SCROLL"
                        pos_hint: {"center_x":.5}
                        size_hint_x:.8
'''

class GestorMasterSApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

GestorMasterSApp().run()
