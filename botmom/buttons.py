from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardRemove


class InlineButtons:
    def __init__(self, buttons, callbacks=None):
        if type(buttons) == dict:
            self.buttons_dict = buttons
        elif len(buttons) == len(callbacks):
            self.buttons_dict = dict(buttons, callbacks)
        else:
            raise ValueError(f"Неверные аргументы для InlineButtons!")
        
        
        self.buttons = InlineKeyboardBuilder()
        for button, callback in self.buttons_dict.items():
            self.buttons.add(InlineKeyboardButton(text=button, callback_data=callback))
    
    
    def as_markup(self):
        return self.buttons.as_markup()



class ReplyButtons:
    def __init__(self, buttons: list = []):
        self.buttons_list = buttons
        
        if self.buttons_list == []:
            self.buttons = ReplyKeyboardRemove()
        else:
            self.buttons = ReplyKeyboardBuilder()
            for button in self.buttons_list:
                self.buttons.add(KeyboardButton(text=button))
    
    
    def as_markup(self):
        if isinstance(self.buttons, ReplyKeyboardRemove):
            return self.buttons
    
        return self.buttons.as_markup()
        
        
        