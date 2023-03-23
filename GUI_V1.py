import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.uix.popup import Popup

import time
kivy.require('1.11.1')


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        # Create the label for date and time
        self.datetime_label = Label(text='', size_hint=(1, 0.1), pos_hint={'top': 1, 'left':1}, color = (0, 0, 0, 1), bold = True)
        self.datetime_label.bind(size=self.datetime_label.setter('text_size'))
        self.add_widget(self.datetime_label)
        
        # Update the label every second
        Clock.schedule_interval(self.update_datetime_label, 1)
   
    
    def update_datetime_label(self, *args):
        # Update the label with the current date and time
        self.datetime_label.text = time.strftime('%Y-%m-%d %H:%M:%S')

        # Add the logo to the top left of the screen
        self.logo = Image(source='novo_logo.png', allow_stretch=False, keep_ratio=True)
        self.logo.bind(size=self.logo.setter('size'), pos=self.logo.setter('pos'))
        #self.logo.opacity = 1
        self.logo.size_hint = (0.3 , 0.3)
        self.logo.pos_hint = {'right': 1, 'top': 1}
        self.add_widget(self.logo)
        Window.clearcolor = (1, 1, 1, 1)

        dropdown = DropDown()
        for i in range(1, 17):
            btn = Button(text='Buffer Mix ' + str(i), size_hint_y=None, height=34, background_color = (.1, .9, 1, 1))
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

        main_button = Button(text='Select Buffer Mix', size_hint=(1, 0.1), font_size = 24, pos_hint={'center_x': 0.5, 'center_y': 0.6}, bold = True, background_color = (0, 0.01, 1, 1))
        main_button.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(main_button, 'text', x))
        self.add_widget(main_button)
        
        #Create the Button Box
        button_box1 = BoxLayout(orientation='horizontal', size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.45})
        button_box1.add_widget(Button(text='Stop', font_size = 20, background_color = (0, 0.09, 1, 1), size_hint=(0.25, 1)))
        self.add_widget(button_box1)

        # Create Start button
        start_button = Button(text='Start', font_size = 20, background_color = (0, 0.09, 1, 1), size_hint=(0.25, 1))
        start_button.bind(on_release=self.on_start_button_press)
        button_box1.add_widget(start_button)
            
        #Create the Button Box
        button_box2 = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), pos_hint={'y': 0})
        self.add_widget(button_box2)

        # Create Next Page button
        self.next_page_button = Button(text='Admin', font_size = 16, background_color = (0, 0.09, 1, 1), size_hint=(0.25, 1))
        self.next_page_button.bind(on_release=self.on_admin_page)
        button_box2.add_widget(self.next_page_button)

        # Create Next Page button
        self.next_page_button = Button(text='Flush Pumps', font_size = 16, background_color = (0, 0.09, 1, 1), size_hint=(0.25, 1))
        self.next_page_button.bind(on_release=self.on_next_page)
        button_box2.add_widget(self.next_page_button)

        #Create the Reset Scale button
        reset_scale_button = Button(text='Reset Scale', font_size = 16, background_color = (0, 0.09, 1, 1), size_hint=(0.25, 1))
        reset_scale_button.bind(on_release=self.on_reset_scale_button_press)
        button_box2.add_widget(reset_scale_button)
        
        # Create Next Page button
        self.next_page_button = Button(text='Next Page', font_size = 16, background_color = (0, 0.09, 1, 1), size_hint=(0.25, 1))
        self.next_page_button.bind(on_release=self.on_next_page)
        button_box2.add_widget(self.next_page_button)

    def on_admin_page(self, *args):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'fourth'

    def on_next_page(self, *args):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'second'

    def on_reset_scale_button_press(self, *args):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'third'

    def on_start_button_press(self, *args):
        # Create popup with loading bar
        popup = Popup(title='Buffer in preparation', size_hint=(None, None), size=(600, 200), background_color = (0, 0.09, 1, 1), title_size = 26)
        progress_bar = ProgressBar(max=100)
        popup.content = progress_bar
        popup.open()

        # Update progress bar value using Clock.schedule_interval
        def update_progress_bar(dt):
            if progress_bar.value >= progress_bar.max:
                # Remove popup and cancel Clock.schedule_interval
                popup.dismiss()
                Clock.unschedule(update_progress_bar)
            else:
                progress_bar.value += 20


class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)

        # Add the logo to the top left of the screen
        self.logo = Image(source='novo_logo.png', allow_stretch=False, keep_ratio=True)
        self.logo.bind(size=self.logo.setter('size'), pos=self.logo.setter('pos'))
        #self.logo.opacity = 1
        #self.logo.size_hint = (0.3 , 0.3)
        #self.logo.pos_hint = {'right': 1, 'top': 1}
        self.add_widget(self.logo)

       # Create Main Screen button
        self.main_screen_button = Button(text='Go Back', size_hint=(1, 0.1))
        self.main_screen_button.bind(on_release=self.on_main_screen_button_press)
        self.add_widget(self.main_screen_button)

    def on_main_screen_button_press(self, *args):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'main'
        

class ThirdScreen(Screen):
    def __init__(self, **kwargs):
        super(ThirdScreen, self).__init__(**kwargs)

        # Add the logo to the top left of the screen
        self.logo = Image(source='novo_logo.png', allow_stretch=False, keep_ratio=True)
        self.logo.bind(size=self.logo.setter('size'), pos=self.logo.setter('pos'))
        #self.logo.opacity = 1
        #self.logo.size_hint = (0.3 , 0.3)
        #self.logo.pos_hint = {'right': 1, 'top': 1}
        self.add_widget(self.logo)

        # Create Main Screen button
        self.main_screen_button = Button(text='Go Back', size_hint=(1, 0.1))
        self.main_screen_button.bind(on_release=self.on_main_screen_button_press)
        self.add_widget(self.main_screen_button)

    def on_main_screen_button_press(self, *args):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'main'

class FourthScreen(Screen):
    def __init__(self, **kwargs):
        super(FourthScreen, self).__init__(**kwargs)

        # Add the logo to the top left of the screen
        #self.logo = Image(source='novo_logo.png', allow_stretch=False, keep_ratio=True)
        #self.logo.bind(size=self.logo.setter('size'), pos=self.logo.setter('pos'))
        #self.logo.opacity = 1
        #self.logo.size_hint = (0.3 , 0.3)
        #self.logo.pos_hint = {'right': 1, 'top': 1}
        #self.add_widget(self.logo)
      
        # Create "Add stock solution" button
        self.add_stock_solution_button = Button(text='Add stock solution', size_hint=(0.3, 0.1), pos_hint={'center_x': 0.3, 'center_y': 0.5})
        self.add_stock_solution_button.bind(on_release=self.on_main_screen_button_press)
        self.add_widget(self.add_stock_solution_button)

        # Create "Create new Buffer mix" button
        self.create_new_buffer_mix_button = Button(text='Create new Buffer mix', size_hint=(0.3, 0.1), pos_hint={'center_x': 0.7, 'center_y': 0.5})
        self.create_new_buffer_mix_button.bind(on_release=self.on_main_screen_button_press)
        self.add_widget(self.create_new_buffer_mix_button)

    def on_main_screen_button_press(self, *args):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'main'


class MyScreenManager(ScreenManager):
    pass


class MyApp(App):
    def build(self):
        sm = MyScreenManager()
        main_screen = MainScreen(name='main')
        second_screen = SecondScreen(name='second')
        third_screen = ThirdScreen(name='third')
        fourth_screen = FourthScreen(name='fourth')
        sm.add_widget(main_screen)
        sm.add_widget(second_screen)
        sm.add_widget(third_screen)
        sm.add_widget(fourth_screen)

        return sm

    def on_select_buffer_mix(self, buffer_mix):
        second_screen = self.root.get_screen('second')
        second_screen.set_buffer_mix(buffer_mix)
        self.root.current = 'second'


if __name__ == '__main__':
    MyApp().run()
