
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types


class TelBot:
    def __init__(self, token: str):
        self.bot = Bot(token=token)
        self.users_time = {}
        self.users_nick = {}
        self.users_previous_command = {}
        self.buttons = [
            "Узнать счет",
            "Изменить счет"
        ]

    async def start(self):
        dp = Dispatcher(self.bot, storage=MemoryStorage())
        dp.register_message_handler(self._message_handler, content_types=['text'])
        print("start_polling")
        await dp.start_polling()

    async def _message_handler(self, message: types.Message):
        """
        логика работы с ботом на телеграмме
        """
        text = message.text
        user_id = message.from_user.id
        try:
            if not self.users_nick.__contains__(user_id):
                if "nick:" in text:
                    self.users_nick[user_id] = text[5::]
                    self.users_time[user_id] = 0
                    self.users_previous_command[user_id] = None
                    await self.create_bottom_keyboard(user_id, self.buttons, "Вам доступны следующие команды.")
                    return
                await self.send_message_to_user(message.from_user.id,
                    "Введите свой ник в форме: 'nick:your_nick'. "
                    "Он будет виден другим участникам при совершении вами каких либо операций со своим счетом")
                return
            if text == "Узнать счет":
                self.users_previous_command[user_id] = text
                await self.send_message_to_user(user_id, "Ваш счет: " + str(self.users_time[user_id]))
                return
            if text == "Изменить счет":
                self.users_previous_command[user_id] = text
                await self.send_message_to_user(user_id, "Введите число, для изменения счета. Отрицательное число уменьшит счет, положительное увеличит")
                return
            if self.users_previous_command[user_id] == "Изменить счет":
                try:
                    delta = int(text)
                    self.users_time[user_id] += delta
                    self.users_previous_command[user_id] = None
                    await self.create_bottom_keyboard(user_id, self.buttons, "Счет успешно изменен")
                    for other_user_id in self.users_nick:
                        if user_id != other_user_id:
                            await self.send_message_to_user(other_user_id,
                                self.users_nick[user_id] + " Изменил счет на " + str(delta))
                except:
                    await self.send_message_to_user(user_id, "Не удалось преобразовать в целое число")
                return
            await self.create_bottom_keyboard(user_id, self.buttons, "Команда неизвестна")
        except:
            await self.send_message_to_user(user_id,
                        "Что то пошло не так, и прога чуть не легла, осторожней, пожалуйста)")


    async def send_message_to_user(self, user_id, message: str):
        await self.bot.send_message(chat_id=user_id, text=message)

    async def create_bottom_keyboard(self, user_id, buttons: list, message: str):
        """
        Создает обычную клавиатуру
        :param message:
        :param buttons:
        :param answer:
        :return:
        """
        bottom_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                    row_width=2)
        bottom_keyboard.add(
            *[types.KeyboardButton(text=button) for button in buttons])
        await self.bot.send_message(chat_id=user_id, text=message,
                                      reply_markup=bottom_keyboard)
