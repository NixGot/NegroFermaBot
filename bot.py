import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import negro
import threading
import traceback
import time


T = 'your token'
bot = telebot.TeleBot(T)
last_response = {}
page = {}
room = {}
top = negro.getTop()

def topUpdate():
    threading.Timer(600, topUpdate).start()
    global top 
    top = negro.getTop()
topUpdate()

def marketUpdate(message, rs):
    mark = negro.marketGet(page[f'{message.chat.id}'] - 1).copy()
    res = []
    for i in range(len(mark)):
        res.append(f"""{i + 1 + 10*(page[f'{message.chat.id}'] - 1)}. {mark[i][0]}: {negro.formatedNum(mark[i][2])} шт. {negro.formatedNum(mark[i][1])}$/шт.""")
        rs = '\n'.join(res)
    if rs != '':
        bot.send_message(message.chat.id, f"""
        {rs}
        """)
    else:
        bot.send_message(message.chat.id, f"""Лотов пока нет""")

def Keyboard(room):
    if room == 'В усадьбу':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = KeyboardButton('Чёрный рынок')
        b2 = KeyboardButton('Создать работу')
        b3 = KeyboardButton('Земельный рынок')
        b4 = KeyboardButton('Рабочая статистика')
        keyboard.row(b1, b2, b3, b4)
        b5 = KeyboardButton('Собрать дань')
        b6 = KeyboardButton('↺')
        b7 = KeyboardButton('Промокод')
        keyboard.row(b5, b6, b7)
        b8 = KeyboardButton('Топ')
        b9 = KeyboardButton('Переводы')
        keyboard.row(b8, b9)
        b10 = KeyboardButton('Рынок')
        b11 = KeyboardButton('Странные фрукты')
        keyboard.row(b10, b11)
        return keyboard
    elif room in ['Чёрный рынок', 'Создать работу', 'Промокод', 'Топ', 'Переводы', '']:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = KeyboardButton('В усадьбу')
        keyboard.row(b1)
        return keyboard
    elif room == 'Рабочая статистика':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = KeyboardButton('В усадьбу')
        b2 = KeyboardButton('Ускорить чёрных')
        keyboard.row(b1, b2)
        return keyboard
    elif room in ['Земельный рынок']:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = KeyboardButton('В усадьбу')
        b2 = KeyboardButton('Расширить территорию')
        keyboard.row(b1, b2)
        return keyboard
    elif room in ['Выбор']:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = KeyboardButton('Да')
        b2 = KeyboardButton('Нет')
        keyboard.row(b1, b2)
        return keyboard
    elif room in ['Рынок']:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = KeyboardButton('<-')
        b2 = KeyboardButton('В усадьбу')
        b3 = KeyboardButton('Создать лот')
        b4 = KeyboardButton('->')
        b5 = KeyboardButton('Удалить лот')
        keyboard.row(b1, b2, b4)
        keyboard.row(b3, b5)
        return keyboard
    elif room == 'Странные фрукты 1':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = KeyboardButton('В усадьбу')
        b2 = KeyboardButton('Купить дерево')
        keyboard.row(b1, b2)
        return keyboard
    elif room == 'Странные фрукты 2':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = KeyboardButton('В усадьбу')
        keyboard.row(b1)
        return keyboard
    elif room == 'Странные фрукты 3':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = KeyboardButton('В усадьбу')
        b2 = KeyboardButton('Отправить негров')
        keyboard.row(b1, b2)
        return keyboard


@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        room[f'{message.chat.id}']
        last_response[f'{message.chat.id}']
    except KeyError:
        room[f'{message.chat.id}'] = ''
        last_response[f'{message.chat.id}'] = ''
    last_response[f'{message.chat.id}'] = message.text
    bot.send_message(message.chat.id,"""
    Преветствую вас в этом рабовладельческом мире
    Для участия в этом мире зароботка на черных рабах вам надо зарегестрировать себя
    для этого напишите название своей компании
    """)

@bot.message_handler(commands=['help'])
def send_help(message):
    try:
        room[f'{message.chat.id}']
        last_response[f'{message.chat.id}']
    except KeyError:
        room[f'{message.chat.id}'] = ''
        last_response[f'{message.chat.id}'] = ''
    last_response[f'{message.chat.id}'] = message.text
    bot.send_message(message.chat.id,"""
* При первом входе в игру обязательно зарегестрируйтесь (напишите /start потом название своей компании)
* Желательно осуществлять все переходы по кнопкам
* Если вы ввели некоректные данные бот просто не ответит
* Также заходите в наш телеграмм канал где будут вывешиваться новости, промокоды и устраиваться розыгрыши
https://t.me/negroferma
* Для открытия клавиатуры нажимайте на квадратик с 4 точками
    """, reply_markup=Keyboard(''))

@bot.message_handler(content_types=['text'])
def create_profile(message):
    try:    
        try:
            room[f'{message.chat.id}']
            last_response[f'{message.chat.id}']
        except KeyError:
            room[f'{message.chat.id}'] = ''
            last_response[f'{message.chat.id}'] = ''
        u = 'userName'
        b = 'baks'
        n = 'negro'
        na = 'negroAct'
        bar = 'baraks'
        an = 'negroAct'
        pr = 'promocode'
        if message.text == 'Чёрный рынок':
            room[f'{message.chat.id}'] = 'Чёрный рынок'
            last_response[f'{message.chat.id}'] = ''
            bot.send_message(message.chat.id, f"""
            {negro.getDB(message.chat.id, u)}, приветствуем на рынке
    1 негр стоит 120 $
    Сколько негров вы хотите купить?
    Ваш счёт: {negro.formatedNum(round(negro.getDB(message.chat.id, b), 2))} $
    Всего негров: {negro.getDB(message.chat.id, n)}/{negro.getDB(message.chat.id, bar) * 10}
            """, reply_markup=Keyboard('Чёрный рынок'))
        elif message.text == 'Создать работу':
            room[f'{message.chat.id}'] = 'Создать работу'
            last_response[f'{message.chat.id}'] = ''
            bot.send_message(message.chat.id, "Введите название работы", reply_markup=Keyboard('Создать работу'))
        elif message.text in ['В усадьбу', '↺']:
            room[f'{message.chat.id}'] = 'В усадьбу'
            last_response[f'{message.chat.id}'] = ''
            bot.send_message(message.chat.id, f"""{negro.getDB(message.chat.id, u)}, добро пожаловать домой
    Денег: {negro.formatedNum(negro.getDB(message.chat.id, b))} $
    Всего негров: {negro.getDB(message.chat.id, n)}/{negro.getDB(message.chat.id, bar)*10}
    странных фруктов: {negro.getDB(message.chat.id, 'eat')}
    Общий заработок: {negro.formatedNum(negro.getPayment(message.chat.id))} $/час""", reply_markup=Keyboard('В усадьбу'))
        elif message.text == 'Земельный рынок':
            room[f'{message.chat.id}'] = 'Земельный рынок'
            last_response[f'{message.chat.id}'] = ''
            bot.send_message(message.chat.id, f"""
Вы уверены что хотите расширить территорию
Бараков всего: {negro.getDB(message.chat.id, bar)}
Денег: {negro.formatedNum(negro.getDB(message.chat.id, b))} $
Барак стоит: {round((4800 * negro.getDB(message.chat.id, bar)) * 1.001 ** (negro.getDB(message.chat.id, bar) - 1), 2)} $
            """, reply_markup=Keyboard('Земельный рынок'))
        elif message.text == 'Рабочая статистика':
            room[f'{message.chat.id}'] = 'Рабочая статистика'
            p = []
            lis = negro.getWorksList(message.chat.id)['works']
            for i in negro.getWorksList(message.chat.id)['works'].keys():
                tim = lis[i]['maxMoney'] / lis[i]['money/h'] * 3600 - (time.time() - lis[i]['time'])
                p.append(f"""{i}: {lis[i]['niggers']} негров принесут ещё {lis[i]['maxMoney']} $. Осталось {int(tim // 3600)} ч. {round((tim / 3600 - tim // 3600) * 60)} мин.""")
            room[f'{message.chat.id}'] = 'Рабочая статистика'
            last_response[f'{message.chat.id}'] = ''
            me = '\n'.join(p)
            if me == '': me = 'Рабочих негров ещё нет'
            bot.send_message(message.chat.id, f"""{me}""", reply_markup=Keyboard('Рабочая статистика'))
        elif message.text == 'Промокод':
            room[f'{message.chat.id}'] = 'Промокод'
            last_response[f'{message.chat.id}'] = ''
            bot.send_message(message.chat.id, f"{negro.getDB(message.chat.id, u)}, введите промокод", reply_markup=Keyboard('Промокод'))
        elif message.text == 'Топ':
            bot.send_message(message.chat.id, f"""
---------------Топ---------------
🏆{top[0][0]}: {negro.formatedNum(top[0][1])} $
🥇{top[1][0]}: {negro.formatedNum(top[1][1])} $
🥈{top[2][0]}: {negro.formatedNum(top[2][1])} $
🥉{top[3][0]}: {negro.formatedNum(top[3][1])} $
😇{top[4][0]}: {negro.formatedNum(top[4][1])} $
👳{top[5][0]}: {negro.formatedNum(top[5][1])} $
🐷{top[6][0]}: {negro.formatedNum(top[6][1])} $
👨🏿{top[7][0]}: {negro.formatedNum(top[7][1])} $
👨🏿‍🦽{top[8][0]}: {negro.formatedNum(top[8][1])} $
🗑️{top[9][0]}: {negro.formatedNum(top[9][1])} $
---------------------------------
Топ обновляется каждые 10 мин
""", reply_markup=Keyboard('Топ'))
        elif message.text == 'Переводы':
            room[f'{message.chat.id}'] = 'Переводы'
            last_response[f'{message.chat.id}'] = ''
            bot.send_message(message.chat.id, f"""Ваш id {message.chat.id}
Для перевода другому человеку введите его id - сумму перевода
За транзакции банк возьмёт комиссию 5%
Деньги из банка будут разыгрываться""", reply_markup=Keyboard('Переводы'))
        elif message.text == 'Рынок':
            room[f'{message.chat.id}'] = 'Рынок'
            last_response[f'{message.chat.id}'] = ''
            bot.send_message(message.chat.id, f"""
Для покупки странных фруктов введите номер лота, а после количество фруктов
Комиссия на покупку состовляет 5% и её платит покупатель""", reply_markup=Keyboard('Рынок'))
            page[f'{message.chat.id}'] = 1
            mark = negro.marketGet(page[f'{message.chat.id}'] - 1).copy()
            res = []
            for i in range(len(mark)):
                res.append(f"""{i + 1 + 10*(page[f'{message.chat.id}'] - 1)}. {mark[i][0]}: {mark[i][2]} шт. {mark[i][1]}$/шт.""")
                r = '\n'.join(res)
            if res == []:
                bot.send_message(message.chat.id, f"""
Лотов пока нет
                """)
            else:
                bot.send_message(message.chat.id, f"""
    {r}
                """)
        elif message.text == 'Странные фрукты':
            room[f'{message.chat.id}'] = 'Странные фрукты'
            if negro.getDB(message.chat.id, 'fruitFerma') == 0:
                bot.send_message(message.chat.id, f"""
Для работы ферму купите дерево фруктов за 40 000 $""", reply_markup=Keyboard('Странные фрукты 1'))
            else:
                bizzareData = negro.getBizzare(message.chat.id).copy()
                try:
                    if bizzareData['time'] > round(time.time()):
                        tim = bizzareData['time'] - round(time.time())
                        bot.send_message(message.chat.id, f"""
    Фрукты ещё не выросли
    Осталось: {tim // 3600}ч. {tim % 3600 // 60}мин.
    Вы получите {bizzareData['niggers'] * 9} странных фруктов""", reply_markup=Keyboard('Странные фрукты 2'))
                    else:
                        negro.delBizzare(message.chat.id)
                        bot.send_message(message.chat.id, f"""
Вы собрали {bizzareData['niggers'] * 9} странных фруктов""", reply_markup=Keyboard('Странные фрукты 3'))
                except KeyError:
                    bot.send_message(message.chat.id, f"Ферма пустует", reply_markup=Keyboard('Странные фрукты 3'))

        if room[f'{message.chat.id}'] == 'В усадьбу':
            if message.text == 'Собрать дань':
                n = (' ' + negro.moneyGet(message.chat.id))[1:]
                bot.send_message(message.chat.id, f'{n}')
        elif room[f'{message.chat.id}'] == 'Создать работу':
            if message.text != 'Создать работу' and last_response[f'{message.chat.id}'] == '':
                bot.send_message(message.chat.id, f"""Сколько негров вы хотите отправить
    негров доступно: {negro.getDB(message.chat.id, n) - negro.getDB(message.chat.id, na)}""")
                last_response[f'{message.chat.id}'] = message.text
            elif message.text != 'Создать работу' and message.text.isdigit() and last_response[f'{message.chat.id}'] != '':
                n = (' ' + negro.createWork(message.chat.id, last_response[f'{message.chat.id}'], int(message.text)))[1:]
                if n == 'такая работа уже есть':
                    bot.send_message(message.chat.id, 'Такая работа уже есть')
                elif n == "недостаточно 'свобоных' негров":
                    bot.send_message(message.chat.id, "Недостаточно 'свобоных' негров")
                elif n == 'работы без негров не бывает':
                    bot.send_message(message.chat.id, 'работы без негров не бывает')
                elif n == 'работа успешно создана':
                    bot.send_message(message.chat.id, 'Работа успешно создана')
        elif room[f'{message.chat.id}'] == 'Чёрный рынок':
            try:
                if negro.getDB(message.chat.id, n) + int(message.text) > negro.getDB(message.chat.id, bar) * 10:
                    bot.send_message(message.chat.id, 'В бараках мало места')
                elif negro.getDB(message.chat.id, b) < int(message.text) * 120:
                    bot.send_message(message.chat.id, 'Вам не хватает денег')
                else:
                    baks = negro.getDB(message.chat.id, b) - int(message.text) * 120
                    nig = negro.getDB(message.chat.id, n) + int(message.text)
                    negro.putDB(message.chat.id, 'baks', round(baks, 2))
                    negro.putDB(message.chat.id, 'negro', nig)
                    bot.send_message(message.chat.id, f"""
    Покупка успешно совершена
    негров: {negro.getDB(message.chat.id, n)}/{negro.getDB(message.chat.id, bar)*10}
    денег: {negro.formatedNum(negro.getDB(message.chat.id, b))} $
                """)
            except BaseException:
                pass
        elif room[f'{message.chat.id}'] == 'Земельный рынок':
            if message.text == 'Расширить территорию':
                try:
                    if (4800 * negro.getDB(message.chat.id, bar)) * 1.001 ** (negro.getDB(message.chat.id, bar) - 1) > negro.getDB(message.chat.id, b):
                        bot.send_message(message.chat.id, 'Вам не хватает денег')
                    else:
                        baks = negro.getDB(message.chat.id, b) - (4800 * negro.getDB(message.chat.id, bar)) * 1.001 ** (negro.getDB(message.chat.id, bar) - 1)
                        barak = negro.getDB(message.chat.id, bar) + 1
                        negro.putDB(message.chat.id, 'baks', round(baks, 2))
                        negro.putDB(message.chat.id, 'baraks', barak)
                        bot.send_message(message.chat.id, f"""Покупка успешно совершена
    Бараков всего: {negro.getDB(message.chat.id, bar)}
    Денег: {negro.formatedNum(negro.getDB(message.chat.id, b))} $
    Следующий барак стоит: {negro.formatedNum(round((4800 * negro.getDB(message.chat.id, bar)) * 1.001 ** (negro.getDB(message.chat.id, bar) - 1), 2))} $""")
                except BaseException:
                    pass
        elif room[f'{message.chat.id}'] == 'Рабочая статистика':
            if message.text == 'Ускорить чёрных':
                bot.send_message(message.chat.id, 'Введите работу для ускорения')
                last_response[f'{message.chat.id}'] = 'Ускорить чёрных'
            elif last_response[f'{message.chat.id}'] == 'Ускорить чёрных':
                if message.text in negro.getWorksList(message.chat.id)['works'].keys():
                    if negro.boostNegro(message.chat.id, message.text, negro.getDB(message.chat.id, 'eat')):
                        negro.putDB(message.chat.id, 'eat', negro.getDB(message.chat.id, 'eat') - negro.getWorksList(message.chat.id)['works'][f'{message.text}']['niggers'])
                        bot.send_message(message.chat.id, 'Негры работают быстрее')
                    else:
                        bot.send_message(message.chat.id, 'Вам не хватает странных фруктов / Негры уже под бустами / часть странных фруктов зарезервированна под лот')
                else:
                    bot.send_message(message.chat.id, 'Такой работы нет')
        elif room[f'{message.chat.id}'] == 'Промокод':
            if message.text == 'BizzareFruit':
                if negro.getDB(message.chat.id, pr) == 0:
                    negro.putDB(message.chat.id, 'promocode', 1)
                    negro.putDB(message.chat.id, 'baks', negro.getDB(message.chat.id, 'baks') + 10000)
                    bot.send_message(message.chat.id, f"""Промокод успешно активирован
Вы получили 10 000 $""")
                else:
                    bot.send_message(message.chat.id, 'Вы уже активировали')
            elif message.text in ['Промокод', 'Топ']:
                pass
            elif message.text != 'BizzareFruit':
                bot.send_message(message.chat.id, 'Неверный промокод')
        elif room[f'{message.chat.id}'] == 'Переводы':
            if last_response[f'{message.chat.id}'] == '' and message.text != 'Переводы':
                last_response[f'{message.chat.id}'] = list(message.text.split(' - '))
                bot.send_message(message.chat.id, f"""Будет отправленно: {negro.formatedNum(list(message.text.split(' - '))[1])} $
Вы заплатите: {negro.formatedNum(int(list(message.text.split(' - '))[1]) * 1.05)}
Вы уверены?""", reply_markup=Keyboard('Выбор'))
            elif last_response[f'{message.chat.id}'] != '':
                if message.text == 'Да':
                    negro.putDB(message.chat.id, 'baks', negro.getDB(message.chat.id, 'baks') - int(last_response[f'{message.chat.id}'][1]) * 1.05)
                    negro.putDB(int(last_response[f'{message.chat.id}'][0]), 'baks', negro.getDB(int(last_response[f'{message.chat.id}'][0]), 'baks') + int(last_response[f'{message.chat.id}'][1]))
                    negro.putDB(0, 'baks', negro.getDB(0, 'baks') + int(last_response[f'{message.chat.id}'][1]) * 0.05)
                    bot.send_message(message.chat.id, f"Перевод завершён", reply_markup=Keyboard('Переводы'))
                elif message.text == 'Нет':
                    bot.send_message(message.chat.id, f"Перевод отменён", reply_markup=Keyboard('Переводы'))
            else:
                pass
        elif room[f'{message.chat.id}'] == 'Рынок':
            if message.text == '->':
                if page[f'{message.chat.id}'] < negro.marketMaxPage():
                    page[f'{message.chat.id}'] += 1
            elif message.text == '<-':
                if page[f'{message.chat.id}'] > 1:
                    page[f'{message.chat.id}'] -= 1
            elif message.text == 'Создать лот':
                if negro.checkLots(message.chat.id) is None:
                    bot.send_message(message.chat.id, f"Ведите количество фруктов - цену")
                    last_response[f'{message.chat.id}'] = message.text
                else:
                    bot.send_message(message.chat.id, f"У вас уже есть активный лот")
            elif last_response[f'{message.chat.id}'] == 'Создать лот':
                try:
                    mes = message.text.split(' - ')
                    if int(mes[0]) <= negro.getDB(message.chat.id, 'eat'):
                        bot.send_message(message.chat.id, f"Лот успешно создан")
                        negro.marketPut(message.chat.id, negro.getDB(message.chat.id, 'userName'), int(mes[1]), int(mes[0]))
                        last_response[f'{message.chat.id}'] = ''
                    else:
                        bot.send_message(message.chat.id, f"У вас недостаточно фруктов")
                        last_response[f'{message.chat.id}'] = ''
                    marketUpdate(message, '')
                except BaseException:
                    last_response[f'{message.chat.id}'] = ''
            elif message.text == 'Удалить лот':
                if negro.checkLots(message.chat.id) is not None:
                    negro.marketDel(message.chat.id)
                    bot.send_message(message.chat.id, f"Лот успешно удалён")
                else:
                    bot.send_message(message.chat.id, f"У нет активных лотов")
                marketUpdate(message, '')
            if type(last_response[f'{message.chat.id}']) == int and message.text.isdigit():
                try:
                    spis = list(negro.marketGet(page[f'{message.chat.id}'])[last_response[f'{message.chat.id}'] - 1]).copy()
                    if negro.getDB(message.chat.id, 'baks') >= spis[1] * int(message.text):
                        if int(message.text) <= spis[2]:
                            negro.putDB(message.chat.id, 'baks', round(negro.getDB(message.chat.id, 'baks') - spis[1] * int(message.text) * 1.05, 2))
                            negro.putDB(message.chat.id, 'eat', round(negro.getDB(message.chat.id, 'eat') + int(message.text), 2))
                            negro.putDB(spis[3], 'eat', round(negro.getDB(spis[3], 'eat') - int(message.text), 2))
                            negro.putDB(spis[3], 'baks', round(negro.getDB(spis[3], 'baks') + spis[1] * int(message.text), 2))
                            negro.putDB(0, 'baks', round(negro.getDB(0, 'baks') + spis[1] * int(message.text) * 0.05, 2))
                            if int(message.text) < spis[2]:
                                negro.marketEdit(spis[3], spis[2] - int(message.text))
                            elif int(message.text) == spis[2]:
                                negro.marketDel(spis[3])
                                bot.send_message(message.chat.id, f"""Покупка успешна совершена""")
                        else:
                            bot.send_message(message.chat.id, f"Ваше значение превышает значение лота")
                    last_response[f'{message.chat.id}'] = ''
                except IndexError:
                    bot.send_message(message.chat.id, f"Неправильный номер лота")
                marketUpdate(message, '')     
            elif message.text.isdigit():
                last_response[f'{message.chat.id}'] = int(message.text) - 10 * (page[f'{message.chat.id}'] - 1)
                bot.send_message(message.chat.id, f"""
Введите количество фруктов
                """)
        elif room[f'{message.chat.id}'] == 'Странные фрукты':
            if message.text == 'Купить дерево':
                if negro.getDB(message.chat.id, 'baks') >= 40000:
                    negro.putDB(message.chat.id, 'baks', negro.getDB(message.chat.id, 'baks') - 40000)
                    negro.putDB(message.chat.id, 'fruitFerma', 1)
                    bot.send_message(message.chat.id, f"Дерево куплено", reply_markup=Keyboard('Странные фрукты 3'))
                else:
                    bot.send_message(message.chat.id, f"Вам не хватает денег")
            elif message.text == 'Отправить негров':
                bot.send_message(message.chat.id, f"""Сколько негров вы хотите отправить?
Свободно: {negro.getDB(message.chat.id, "negro") - negro.getDB(message.chat.id, "negroAct")}
!!! Они будут работать 24 часа и 1 негр = 9 фруктов !!!""")
                last_response[f'{message.chat.id}'] = 'Отправить негров'
            elif last_response[f'{message.chat.id}'] == 'Отправить негров':
                if int(message.text) > 0 and (negro.getDB(message.chat.id, 'negro') - negro.getDB(message.chat.id, 'negroAct')) >= int(message.text):
                    negro.createBizzare(message.chat.id, int(message.text))
                    bot.send_message(message.chat.id, f"Негры отправлены на работу", reply_markup=Keyboard('Странные фрукты 2'))
                else:
                    bot.send_message(message.chat.id, f"У вас не хватает негров")
        else:
            if negro.getDB(message.chat.id, 'userid') is None and last_response[f'{message.chat.id}'] == '/start':
                negro.create_profile(message.chat.id, message.text)
                bot.send_message(message.chat.id, f'{negro.getDB(message.chat.id, u)}, Вы успешно зарегестрированны', reply_markup=Keyboard('В усадьбу'))
            elif negro.getDB(message.chat.id, 'userid') is not None:
                bot.send_message(message.chat.id, f'{negro.getDB(message.chat.id, u)}, Вы уже зарегестрированны')
    except BaseException:
        traceback.print_exc()
        pass

bot.infinity_polling()

# Доделать ферму фруктов и отправить в релиз, пусть люди тестят за виртуальную валюту
