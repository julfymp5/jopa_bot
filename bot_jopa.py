import time
import telebot
import sqlite3
import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, types
import random
bot = Bot('5297518467:AAEE3w0C1znuNM12_JgDSEyUHps9MPOS5FQ')
bot1 = telebot.TeleBot("5297518467:AAEE3w0C1znuNM12_JgDSEyUHps9MPOS5FQ")
dp = Dispatcher(bot)

CHAT_ID = "756834690"


@dp.message_handler(commands=['help_jopa'])
async def send_help(message):
     await bot.send_message(chat_id=message.chat.id, text="/jopa_reg: register_new_jopa\n/jopa_delete: end your jopa\n/jopa: make your jopa bigger\n/jopa_size: size of your jopa")


class Database:

    def __init__(self, db_file):
         self.connection = sqlite3.connect(db_file)
         self.cursor = self.connection.cursor()

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def set_nickname(self, user_id, nickname):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `nickname` = ? WHERE `user_id` = ?", (nickname, user_id,))

    def get_signup(self, user_id):
        with self.connection as connection:
            with connection.cursor() as cursor:
                result = cursor.execute("SELECT `signup` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
                for row in result:
                    signup = str(row[0])
                return signup

    def set_signup(self, user_id, signup):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `signup` = ? WHERE `user_id` = ?", (signup, user_id,)).fetchall()

    def get_nickname(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `nickname` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                nickname = str(row[0])
            return nickname

    def delete_user_id(self, user_id):
        with self.connection:
            res = self.cursor.execute("DELETE FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return res

    def delete_nickname(self, nickname):
        with self.connection:
            r = self.cursor.execute("DELETE FROM `users` WHERE `nickname` = ?", (nickname,)).fetchall()
            return r

    def set_jopa(self, user_id, razmer_jopi: int):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `razmer_jopi` = ? WHERE `user_id` = ?", (razmer_jopi, user_id,))

    def delete_time(self, time):
        with self.connection:
            return self.cursor.execute("DELETE FROM `users` WHERE `time` = ?", (time,)).fetchall()

    def get_jopa(self, user_id):
        with self.connection:
            razmer1 = self.cursor.execute("SELECT `razmer_jopi` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchone()
            for i in razmer1:
                return i

    def get_time(self, user_id):
        with self.connection:
            time = self.cursor.execute("SELECT `time` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchone()
            for b in time:
                return b

    def set_time(self, user_id, time_left):
        return self.cursor.execute("UPDATE `users` SET `time` = ? WHERE `user_id` = ?", (time_left, user_id,))

    def get_statistic(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT `nickname`, `razmer_jopi` FROM `users` ").fetchall()

    def get_all_jopa(self):
        with self.connection:
            stata = self.cursor.execute("SELECT `razmer_jopi` FROM `users`").fetchall()
            print(type(stata))
            return stata

    def find_nickname_by_jopa(self, jopa):
        with self.connection:
            nick = self.cursor.execute("SELECT `nickname` FROM `users` WHERE `razmer_jopi` = ?", (jopa,)).fetchone()
            for n in nick:
                return n


db = Database('users.db')


@dp.message_handler(commands=['jopa_reg'])
async def jopa_register(message: types.Message):
    if(not db.user_exists(message.from_user.id)):
        db.add_user(message.from_user.id)
        db.set_nickname(message.from_user.id, message.from_user.first_name)
        user_nick = db.get_nickname(message.from_user.id)
        if(db.user_exists(message.from_user.id)):
            user_jopa = db.get_jopa(message.from_user.id)
            await bot.send_message(chat_id=message.chat.id, text=f"Привет {user_nick}! Твоя jopa = {user_jopa} см")
        if (not db.user_exists(message.from_user.id)):
            await bot.send_message(chat_id=message.chat.id, text=f"Привет {user_nick}!")
    else:
        user_nick = db.get_nickname(message.from_user.id)
        await bot.send_message(chat_id=message.chat.id, text=f"Привет {user_nick}, вы уже зареганы")


@dp.message_handler(commands=['jopa'])
async def jopa(message):
    global time_left
    jopka = db.get_jopa(message.from_user.id)
    time_left = db.get_time(message.from_user.id)
    if time_left == 10800:
        user_nick = db.get_nickname(message.from_user.id)
        a = random.randint(-1, 4)
        jopka = jopka + a
        await bot.send_message(chat_id=message.chat.id, text=f"{user_nick}, твоя jopka выросла на {a} см, теперь она {jopka} см")
        db.set_jopa(message.from_user.id, jopka)
        while time_left != 0:
            await asyncio.sleep(1)
            time_left = time_left - 1
            db.set_time(message.from_user.id, time_left)
            if time_left == 0:
                db.set_time(message.from_user.id, 10800)
                break
    else:
        time_left = db.get_time(message.from_user.id)
        nick = db.get_nickname(message.from_user.id)
        await bot.send_message(chat_id=message.chat.id, text=f'{nick}, подождите ещё {time_left} секунд')


@dp.message_handler(commands=['jopa_delete'])
async def jopa(message):
    db.delete_nickname(message.from_user.id)
    db.delete_user_id(message.from_user.id)
    db.delete_time(message.from_user.id)
    await bot.send_message(chat_id=message.chat.id, text="your jopa deleted(((((")


@dp.message_handler(commands=['jopa_size'])
async def jopa_size(message):
    user_nick = db.get_nickname(message.from_user.id)
    user_jopa = db.get_jopa(message.from_user.id)
    await bot.send_message(chat_id=message.chat.id, text=f"{user_nick}, твоя jopa = {user_jopa} см")


@dp.message_handler(commands=['jopa_statistcis'])
async def jopa_statistics(message):
    global i, b
    lst = []
    jop = db.get_all_jopa()
    for i in jop:
        for b in i:
            lst.append(b)
            print(type(b))
    lst.sort(reverse=True)
    print(lst)
    await bot.send_message(chat_id=message.chat.id, text="Статистика игроков\n")
    b = 0
    for d in lst:
        user_nick = db.find_nickname_by_jopa(d)
        b = b + 1
        await bot.send_message(chat_id=message.chat.id, text=f"{b} Место: {user_nick} с jopoy: {d} см\n")


if __name__ == '__main__':
    executor.start_polling(dp)