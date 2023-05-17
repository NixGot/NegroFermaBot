import sqlite3
import time
import json


# conn = sqlite3.connect(r'profiles_data.db', check_same_thread=False)
# cur = conn.cursor()
# cur.execute("""CREATE TABLE IF NOT EXISTS users(
# userid INT PRIMARY KEY,
# userName TEXT,
# baks float,
# negro int,
# baraks int,
# timeout int,
# sovietRubles float,
# eat int,
# negroAct int,
# promocode int,
# fruitFerma int);
# """)
# conn.commit()               
# cur.close()
# conn.close()
#создание таблицы

# conn = sqlite3.connect(r'profiles_data.db', check_same_thread=False)
# cur = conn.cursor()
# cur.execute("""CREATE TABLE IF NOT EXISTS market(
# userid INT PRIMARY KEY,
# userName text,
# price float,
# count int);
# """)
# conn.commit()               
# cur.close()
# conn.close()
#создание рынка


def create_profile(id, name):
    conn = sqlite3.connect(r'profiles_data.db', check_same_thread=False)
    cur = conn.cursor()
    data = (id, name, 300, 0, 1, 0, 0, 0, 0, 0, 0)
    cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", data)
    conn.commit()
    cur.close()
    conn.close()


def getDB(id, name):
    conn = sqlite3.connect(r'profiles_data.db', check_same_thread=False)
    cur = conn.cursor()
    cur.execute(f"""
        SELECT {name}
        FROM users
        WHERE userid = {id};
    """)
    res = cur.fetchone()
    if res is not None:
        res = res[0]
    try:
        return res
    finally:
        cur.close()
        conn.close()
# userid timeout baks sovietRubles baraks userName

def putDB(id, name, val):
    conn = sqlite3.connect(r'profiles_data.db', check_same_thread=False)
    cur = conn.cursor()
    cur.execute(f"""
    UPDATE users
    SET {name} = {val}
    WHERE userid = {id}; 
    """)
    conn.commit()
    cur.close()
    conn.close()

def createWork(id, name, niggers):
    if niggers > 0:
        open(f'individual_profile_stat\{id}.json', 'a', encoding='utf-8')
        with open(f'individual_profile_stat\{id}.json', 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.decoder.JSONDecodeError:
                data = {'works':{}, 'BizzareFarm': {}}
        if name in data['works'].keys():
            return 'такая работа уже есть'
        elif getDB(id, 'negroAct') + niggers <= getDB(id, 'negro'):
            data['works'][f'{name}'] = {'time': int(round(time.time())), 'maxMoney': niggers * 240, 'niggers': niggers, 'money/h': niggers * 240 / 8, 'boost': 0}
            with open(f'individual_profile_stat\{id}.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False)
            putDB(id, 'negroAct', niggers + getDB(id, 'negroAct'))
            return 'работа успешно создана'
        else:
            return "недостаточно 'свобоных' негров"
    else:
        return 'работы без негров не бывает'

def getWorksList(id):
    with open(f'individual_profile_stat\{id}.json', 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
        except json.decoder.JSONDecodeError:
            data = {}
        return data
    
def moneyGet(id):
    if getDB(id, 'timeout') <= int(round(time.time())):
        k = getWorksList(id).copy()
        money = 0
        del_k = []
        for i in k['works'].keys():
            if (int(round(time.time())) - k['works'][f'{i}']['time']) * k['works'][f'{i}']['money/h'] / 3600 < k['works'][f'{i}']['maxMoney']:
                money += round((int(round(time.time())) - k['works'][f'{i}']['time']) * k['works'][f'{i}']['money/h'] / 3600, 2)
                k['works'][f'{i}']['maxMoney'] -= round((int(round(time.time())) - k['works'][f'{i}']['time']) * k['works'][f'{i}']['money/h'] / 3600, 2)
                k['works'][f'{i}']['time'] = int(round(time.time()))
            else:
                money += k['works'][f'{i}']['maxMoney']
                putDB(id, 'negro', (getDB(id, 'negro') - k['works'][f'{i}']['niggers']))
                putDB(id, 'negroAct', (getDB(id, 'negroAct') - k['works'][f'{i}']['niggers']))
                del_k.append(i)
        for i in del_k:
            del k['works'][f'{i}']
        putDB(id, 'baks', (getDB(id, 'baks') + money))
        putDB(id, 'timeout', int(round(time.time())) + 5 * 60)
        with open(f'individual_profile_stat\{id}.json', 'w', encoding='utf-8') as file:
            json.dump(k, file, ensure_ascii=False)
        return f'Вы собрали {money} $'
    else:
        return 'Отчёты о зароботке ещё не получены'

def marketGet(page):
    conn = sqlite3.connect(r'profiles_data.db', check_same_thread=False)
    cur = conn.cursor()
    cur.execute(f"""
        SELECT userName, price, count, userid
        FROM market
        WHERE count > 0
        ORDER BY price limit 10 offset {(page - 1)*10};
    """)
    res = cur.fetchmany(10)
    return res

def marketGetCount(id):
  conn = sqlite3.connect(r'profiles_data.db', check_same_thread=False)
  cur = conn.cursor()
  cur.execute(f"""
        SELECT count
        FROM market
        WHERE userid = {id};
    """)
  res = cur.fetchone()
  if res is None:
    return 0
  else:
    return res

def marketPut(id, name, val, count):
    conn = sqlite3.connect(r'profiles_data.db', check_same_thread=False)
    cur = conn.cursor()
    data = (id, name, val, count)
    cur.execute("INSERT INTO market VALUES(?, ?, ?, ?);", data)
    conn.commit()
    cur.close()
    conn.close()

def marketMaxPage():
    conn = sqlite3.connect(r'profiles_data.db', check_same_thread=False)
    cur = conn.cursor()
    cur.execute(f"""
        SELECT Count(*)
        FROM market
    """)
    res = cur.fetchone()
    cur.close()
    conn.close()
    return res[0]

def marketDel(id):
    conn = sqlite3.connect(r'profiles_data.db', check_same_thread=False)
    cur = conn.cursor()
    cur.execute(f"""
        DELETE FROM market
        WHERE userid = {id};
    """)
    conn.commit()
    cur.close()
    conn.close()

def marketEdit(id, count):
    conn = sqlite3.connect(r'profiles_data.db', check_same_thread=False)
    cur = conn.cursor()
    cur.execute(f"""
    UPDATE market
    SET count = {count}
    WHERE userid = {id}; 
    """)
    conn.commit()
    cur.close()
    conn.close()

def checkLots(id):
    conn = sqlite3.connect(r'profiles_data.db', check_same_thread=False)
    cur = conn.cursor()
    cur.execute(f"""
        SELECT userid
        FROM market
        WHERE userid = {id};
    """)
    res = cur.fetchone()
    if res is not None:
        res = res[0]
    try:
        return res
    finally:
        cur.close()
        conn.close()

def boostNegro(id, workName, fruit):
    k = getWorksList(id).copy()
    if fruit >= k['works'][f'{workName}']['niggers'] + marketGetCount(id)[0] and k['works'][f'{workName}']['boost'] == 0:
        k['works'][f'{workName}']['money/h'] *= 2
        k['works'][f'{workName}']['maxMoney'] *= 2
        k['works'][f'{workName}']['boost'] = 1
        with open(f'individual_profile_stat\{id}.json', 'w', encoding='utf-8') as file:
            json.dump(k, file, ensure_ascii=False)
        return True
    else:
        return False
    
def createBizzare(id, niggers):
    if niggers > 0:
        if getDB(id, 'negro') - getDB(id, 'negroAct') >= niggers:
            with open(f'individual_profile_stat\{id}.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                data['BizzareFarm'] = {'time': int(round(time.time()) + 24*60*60), 'fruit': niggers * 9, 'niggers': niggers}
                with open(f'individual_profile_stat\{id}.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False)
                putDB(id, 'negroAct', niggers + getDB(id, 'negroAct'))
                return 'Негры на ферме'
        else:
            return "недостаточно 'свобоных' негров"
    else:
        return 'работы без негров не бывает'
    
def getBizzare(id):
    with open(f'individual_profile_stat\{id}.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        try:
           data['BizzareFarm'] 
        except KeyError:
            data['BizzareFarm'] = {}
    return data['BizzareFarm']

def delBizzare(id):
    with open(f'individual_profile_stat\{id}.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        putDB(id, 'eat', data['BizzareFarm']['niggers'] * 9)
        putDB(id, 'negro', getDB(id, 'negro') - data['BizzareFarm']['niggers'])
        putDB(id, 'negroAct', getDB(id, 'negroAct') - data['BizzareFarm']['niggers'])
        data['BizzareFarm'] = {}
        with open(f'individual_profile_stat\{id}.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)

def getPayment(id):
    pay = 0
    with open(f'individual_profile_stat\{id}.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        for i in data['works'].keys():
            pay += data['works'][f'{i}']['money/h']
    return pay

# conn = sqlite3.connect(r'profiles_data.db', check_same_thread=False)
# cur = conn.cursor()
# cur.execute(f"""
# UPDATE users
# SET promocode = 0; 
# """)
# conn.commit()
# cur.close()
# conn.close()
#ресет промокодов

# conn = sqlite3.connect(r'profiles_data.db', check_same_thread=False)
# cur = conn.cursor()
# cur.execute(f"""
# ALTER TABLE users
# ADD fruitFerma INT; 
# """)
# conn.commit()
# cur.close()
# conn.close()
# добавление столбца

def getTop():
    conn = sqlite3.connect(r'profiles_data.db', check_same_thread=False)
    cur = conn.cursor()
    cur.execute(f"""
        SELECT userName, baks
        FROM users
        WHERE userid != '928393988'
        ORDER BY baks desc limit 10;
    """)
    res = cur.fetchmany(10)
    return res
