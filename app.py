from flask import Flask, render_template, request, redirect, url_for
import mariadb
import redis
from pymongo import MongoClient, ASCENDING, DESCENDING
mongo_client = MongoClient("mongodb://34.85.203.59:27017")

app = Flask(__name__)

"""This is the main page of the website that displays all characters in the database and their details"""
@app.route("/", methods=["GET", "POST"])
def mainpage():
    if "element" and "weapon" in request.args:
        element = request.args["element"]
        weapon = request.args["weapon"]
        characters = getCharacters(element, weapon)
        elements = getElements()
        weapons = getWeapons()
        mondstadt = getMondstadt()
        liyue = getLiyue()
        inazuma = getInazuma()
        sumeru = getSumeru()
        booksAdd = addBooks()
        booksRemove = removeBooks()
        books = getBooks()
        monThurs = getMonThurs()
        tuesFri = getTuesFri()
        wedSat = getWedSat()
        sunday = getSun()
        return render_template("mainpage.html", characters=characters, elements=elements, weapons=weapons, mondstadt=mondstadt, liyue=liyue, inazuma=inazuma, sumeru=sumeru, booksAdd=booksAdd, booksRemove=booksRemove, books=books, monThurs=monThurs, tuesFri=tuesFri, wedSat=wedSat, sunday=sunday)
    elif "addBook" in request.args:
        r = redis.StrictRedis(password="genshin", charset="utf-8", decode_responses=True, host="34.85.203.59", port=6379)
        book = request.args["addBook"]
        for day in getDays():
            if r.hget("mondstadt", day) == book:
                r.sadd(day, book)
            elif r.hget("liyue", day) == book:
                r.sadd(day, book)
            elif r.hget("inazuma", day) == book:
                r.sadd(day, book)
            elif r.hget("sumeru", day) == book:
                r.sadd(day, book)
        r.close()
        conn = mariadb.connect(user="guest", password="guest", host="34.85.203.59", port=3306, database="genshin")
        cur = conn.cursor()
        cur.execute("SELECT * FROM characters NATURAL JOIN ascensionStats LIMIT 10")
        characters = cur.fetchall()
        elements = getElements()
        weapons = getWeapons()
        conn.close()
        mondstadt = getMondstadt()
        liyue = getLiyue()
        inazuma = getInazuma()
        sumeru = getSumeru()
        booksAdd = addBooks()
        booksRemove = removeBooks()
        books = getBooks()
        monThurs = getMonThurs()
        tuesFri = getTuesFri()
        wedSat = getWedSat()
        sunday = getSun()
        return render_template("mainpage.html", characters=characters, elements=elements, weapons=weapons, mondstadt=mondstadt, liyue=liyue, inazuma=inazuma, sumeru=sumeru, booksAdd=booksAdd, booksRemove=booksRemove, books=books, monThurs=monThurs, tuesFri=tuesFri, wedSat=wedSat, sunday=sunday)
    elif "removeBook" in request.args:
        r = redis.StrictRedis(password="genshin", charset="utf-8", decode_responses=True, host="34.85.203.59", port=6379)
        book = request.args["removeBook"]
        for day in getDays():
            if r.hget("mondstadt", day) == book:
                r.srem(day, book)
            elif r.hget("liyue", day) == book:
                r.srem(day, book)
            elif r.hget("inazuma", day) == book:
                r.srem(day, book)
            elif r.hget("sumeru", day) == book:
                r.srem(day, book)
        r.close()
        conn = mariadb.connect(user="guest", password="guest", host="34.85.203.59", port=3306, database="genshin")
        cur = conn.cursor()
        cur.execute("SELECT * FROM characters NATURAL JOIN ascensionStats LIMIT 10")
        characters = cur.fetchall()
        elements = getElements()
        weapons = getWeapons()
        conn.close()
        mondstadt = getMondstadt()
        liyue = getLiyue()
        inazuma = getInazuma()
        sumeru = getSumeru()
        booksAdd = addBooks()
        booksRemove = removeBooks()
        books = getBooks()
        monThurs = getMonThurs()
        tuesFri = getTuesFri()
        wedSat = getWedSat()
        sunday = getSun()
        return render_template("mainpage.html", characters=characters, elements=elements, weapons=weapons, mondstadt=mondstadt, liyue=liyue, inazuma=inazuma, sumeru=sumeru, booksAdd=booksAdd, booksRemove=booksRemove, books=books, monThurs=monThurs, tuesFri=tuesFri, wedSat=wedSat, sunday=sunday)
    elif request.method == "POST":
        #if "add character link is clicked", go to "add character" page
        return redirect(url_for("addCharacter"))
    else:
        # if the user is visiting the main page for the first time, then display all characters
        conn = mariadb.connect(user="guest", password="guest", host="34.85.203.59", port=3306, database="genshin")
        cur = conn.cursor()
        cur.execute("SELECT * FROM characters NATURAL JOIN ascensionStats LIMIT 10")
        characters = cur.fetchall()
        elements = getElements()
        weapons = getWeapons()
        conn.close()
        mondstadt = getMondstadt()
        liyue = getLiyue()
        inazuma = getInazuma()
        sumeru = getSumeru()
        booksAdd = addBooks()
        booksRemove = removeBooks()
        books = getBooks()
        monThurs = getMonThurs()
        tuesFri = getTuesFri()
        wedSat = getWedSat()
        sunday = getSun()
        return render_template("mainpage.html", characters=characters, elements=elements, weapons=weapons, mondstadt=mondstadt, liyue=liyue, inazuma=inazuma, sumeru=sumeru, booksAdd=booksAdd, booksRemove=booksRemove, books=books, monThurs=monThurs, tuesFri=tuesFri, wedSat=wedSat, sunday=sunday)

"""This is the page that allows users to add characters to the database"""
@app.route("/addCharacter", methods=["GET", "POST"])
def addCharacter():
    if request.method == "POST":
        # if the user is submitting a new character, then add it to the database
        name = request.form.get("name")
        element = request.form.get("element")
        weapon = request.form.get("weapon")
        rarity = request.form.get("rarity")
        nation = request.form.get("nation")
        stat = request.form.get("stat")
        talentBook = request.form.get("talentBook")
        conn = mariadb.connect(user="guest", password="guest", host="34.85.203.59", port=3306, database="genshin")
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM characters where name=? LIMIT 1", (name,))
        exists = cur.fetchone()
        if exists == None:
            # if the character doesn't exist, then add it to the database
            cur.execute("INSERT INTO characters (name, element, weapon, rarity, nation, stat, talentBook) VALUES (?, ?, ?, ?, ?, ?, ?)", (name, element, weapon, rarity, nation, stat, talentBook))
            conn.commit()
        else:
            # if the character already exists, then reload the page and tell the user that the character already exists
            msg = "Sorry, that character already exists!"
            elements = getElements()
            weapons = getWeapons()
            rarities = getRarities()
            stats = getStats()
            talentBooks = getBooks()
            conn.close()
            return render_template("addCharacter.html", msg=msg, elements=elements, weapons=weapons, rarities=rarities, stats=stats, talentBooks=talentBooks)
        conn.close()
        return redirect(url_for("mainpage"))
    else:
        # if the user is visiting the add character page for the first time, then display the form
        elements = getElements()
        weapons = getWeapons()
        rarities = getRarities()
        stats = getStats()
        talentBooks = getBooks()
        return render_template("addCharacter.html", elements=elements, weapons=weapons, rarities=rarities, stats=stats, talentBooks=talentBooks)

"""This method returns 10 characters from mariadb based on the element and weapon"""
def getCharacters(element, weapon):
    conn = mariadb.connect(user="guest", password="guest", host="34.85.203.59", port=3306, database="genshin")
    cur = conn.cursor()
    if element == "all" and weapon == "all":
        # if both element and weapon are "all", then display all characters
        cur.execute("SELECT * FROM characters NATURAL JOIN ascensionStats LIMIT 10")
    elif element == "all":
        # if element is "all", then we filter only by weapon
        cur.execute("SELECT * FROM characters NATURAL JOIN ascensionStats WHERE weapon = ? LIMIT 10", (weapon,))
    elif weapon == "all":
        # if weapon is "all", then filter only by element
        cur.execute("SELECT * FROM characters NATURAL JOIN ascensionStats WHERE element = ? LIMIT 10", (element,))
    else:
        # if both are not "all", then filter by both
        cur.execute("SELECT * FROM characters NATURAL JOIN ascensionStats WHERE element = ? AND weapon = ? LIMIT 10", (element, weapon))
    characters = cur.fetchall()
    conn.close()
    return characters

"""This method gets all unique elements from mariadb"""
def getElements():
    conn = mariadb.connect(user="guest", password="guest", host="34.85.203.59", port=3306, database="genshin")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT element FROM characters ORDER BY element")
    elements = cur.fetchall()
    conn.close()
    return elements

"""This method gets all unique weapon types from mariadb"""
def getWeapons():
    conn = mariadb.connect(user="guest", password="guest", host="34.85.203.59", port=3306, database="genshin")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT weapon FROM characters ORDER BY weapon")
    weapons = cur.fetchall()
    conn.close()
    return weapons

"""This method gets all unique rarities from the mariadb"""
def getRarities():
    conn = mariadb.connect(user="guest", password="guest", host="34.85.203.59", port=3306, database="genshin")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT rarity FROM characters ORDER BY rarity")
    rarities = cur.fetchall()
    conn.close()
    return rarities

"""This method gets all unique ascension stats from mariadb"""
def getStats():
    conn = mariadb.connect(user="guest", password="guest", host="34.85.203.59", port=3306, database="genshin")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT stat FROM ascensionStats ORDER BY stat")
    stats = cur.fetchall()
    conn.close()
    return stats

"""This method gets all unique mondstadt talent books from mariadb"""
def getMondstadt():
    r = redis.StrictRedis(password="genshin", charset="utf-8", decode_responses=True, host="34.85.203.59", port=6379)
    mondstadt = r.hgetall("mondstadt")
    mondstadt["Monday/Thursday"] = mondstadt["Monday"]
    mondstadt["Tuesday/Friday"] = mondstadt["Tuesday"]
    mondstadt["Wednesday/Saturday"] = mondstadt["Wednesday"]
    mondstadt.pop("Monday")
    mondstadt.pop("Tuesday")
    mondstadt.pop("Wednesday")
    mondstadt.pop("Thursday")
    mondstadt.pop("Friday")
    mondstadt.pop("Saturday")
    r.close()
    return mondstadt

"""This method gets all unique liyue talent books from mariadb"""
def getLiyue():
    r = redis.StrictRedis(password="genshin", charset="utf-8", decode_responses=True, host="34.85.203.59", port=6379)
    liyue = r.hgetall("liyue")
    liyue["Monday/Thursday"] = liyue["Monday"]
    liyue["Tuesday/Friday"] = liyue["Tuesday"]
    liyue["Wednesday/Saturday"] = liyue["Wednesday"]
    liyue.pop("Monday")
    liyue.pop("Tuesday")
    liyue.pop("Wednesday")
    liyue.pop("Thursday")
    liyue.pop("Friday")
    liyue.pop("Saturday")
    r.close()
    return liyue

"""This method gets all unique inazuma talent books from mariadb"""
def getInazuma():
    r = redis.StrictRedis(password="genshin", charset="utf-8", decode_responses=True, host="34.85.203.59", port=6379)
    inazuma = r.hgetall("inazuma")
    inazuma["Monday/Thursday"] = inazuma["Monday"]
    inazuma["Tuesday/Friday"] = inazuma["Tuesday"]
    inazuma["Wednesday/Saturday"] = inazuma["Wednesday"]
    inazuma.pop("Monday")
    inazuma.pop("Tuesday")
    inazuma.pop("Wednesday")
    inazuma.pop("Thursday")
    inazuma.pop("Friday")
    inazuma.pop("Saturday")
    r.close()
    return inazuma

"""This method gets all unique sumeru talent books from mariadb"""
def getSumeru():
    r = redis.StrictRedis(password="genshin", charset="utf-8", decode_responses=True, host="34.85.203.59", port=6379)
    sumeru = r.hgetall("sumeru")
    sumeru["Monday/Thursday"] = sumeru["Monday"]
    sumeru["Tuesday/Friday"] = sumeru["Tuesday"]
    sumeru["Wednesday/Saturday"] = sumeru["Wednesday"]
    sumeru.pop("Monday")
    sumeru.pop("Tuesday")
    sumeru.pop("Wednesday")
    sumeru.pop("Thursday")
    sumeru.pop("Friday")
    sumeru.pop("Saturday")
    r.close()
    return sumeru

def addBooks():
    conn = mariadb.connect(user="guest", password="guest", host="34.85.203.59", port=3306, database="genshin")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT talentBook FROM characters ORDER BY talentBook")
    books = cur.fetchall()
    r = redis.StrictRedis(password="genshin", charset="utf-8", decode_responses=True, host="34.85.203.59", port=6379)
    addBooks = []
    days = ["Monday", "Tuesday", "Wednesday"]
    for book in books:
        if r.sismember(days[0], book[0]) == 0 and r.sismember(days[1], book[0]) == 0 and r.sismember(days[2], book[0]) == 0:
            addBooks.append(book[0])
    r.close()
    conn.close()
    return addBooks

def removeBooks():
    conn = mariadb.connect(user="guest", password="guest", host="34.85.203.59", port=3306, database="genshin")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT talentBook FROM characters ORDER BY talentBook")
    books = cur.fetchall()
    r = redis.StrictRedis(password="genshin", charset="utf-8", decode_responses=True, host="34.85.203.59", port=6379)
    removeBooks = []
    days = ["Monday", "Tuesday", "Wednesday"]
    for day in days:
        for book in books:
            if r.sismember(day, book[0]) == 1:
                removeBooks.append(book[0])
    r.close()
    conn.close()
    return removeBooks

def getDays():
    return ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

def getBooks():
    conn = mariadb.connect(user="guest", password="guest", host="34.85.203.59", port=3306, database="genshin")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT talentBook FROM characters ORDER BY talentBook")
    books = cur.fetchall()
    conn.close()
    return books

def getMonThurs():
    r = redis.StrictRedis(password="genshin", charset="utf-8", decode_responses=True, host="34.85.203.59", port=6379)
    monThurs = r.smembers("Monday")
    r.close()
    return monThurs

def getTuesFri():
    r = redis.StrictRedis(password="genshin", charset="utf-8", decode_responses=True, host="34.85.203.59", port=6379)
    tuesFri = r.smembers("Tuesday")
    r.close()
    return tuesFri

def getWedSat():
    r = redis.StrictRedis(password="genshin", charset="utf-8", decode_responses=True, host="34.85.203.59", port=6379)
    wedSat = r.smembers("Wednesday")
    r.close()
    return wedSat

def getSun():
    r = redis.StrictRedis(password="genshin", charset="utf-8", decode_responses=True, host="34.85.203.59", port=6379)
    monThurs = r.smembers("Monday")
    tuesFri = r.smembers("Tuesday")
    wedSat = r.smembers("Wednesday")
    sunday = monThurs.union(tuesFri, wedSat)
    r.close()
    return sunday

if __name__ == '__main__':
    app.run()