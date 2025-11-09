#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
import os.path
import sys

import numpy as np
from sqlalchemy import create_engine


my_path = os.path.abspath("__file__")
dir = os.path.dirname(my_path)
dir = dir.replace('SteamMatch', 'data')
os.chdir(dir)


connection1 = sqlite3.connect('database1.db')
cursor1 = connection1.cursor()

connection2 = sqlite3.connect('database2.db')
cursor2 = connection2.cursor()
'''
import re
import mysql.connector
from mysql.connector import Error
import pandas as pd
from fuzzywuzzy import fuzz
from json import loads, dumps
import warnings
import json

#ignore UserWarning
warnings.filterwarnings('ignore')
# ignore SettingWithCopyWarning
pd.options.mode.chained_assignment = None  # default='warn'

# maximum return rows in json
maxrow=51



def connect_fetch(i):
    """ Connect to MySQL database and fetch data """
    conn = None
    try:
        if i == 1:
            conn = mysql.connector.connect(
                host='localhost',
                database='GDB1',
                user='root',
                passwd='frank990808',
                port='3306'  # Optional: default is 3306
            )
        else:
            conn = mysql.connector.connect(
                host='localhost',
                database='GDB2',
                user='root',
                passwd='frank990808',
                port='3306'  # Optional: default is 3306
            )
        if conn.is_connected():
            # print('Connected to MySQL database')

            cursor = conn.cursor()
            return conn, cursor

    except Error as e:
        print('connect_fetch_error:', e)



def addUser(user_id, user_name):
    """
    user_id is int, user_name is string, 
    return if user is already in database, or add user to user table
    """
    sql_query = f"SELECT 1 FROM table_user1 WHERE user_id = {user_id}"
    conn1, cursor1 = connect_fetch(1)
    conn2, cursor2 = connect_fetch(2)
    cursor1.execute(sql_query)
    result = cursor1.fetchall()

    if result:
        conn1.commit()
        conn1.close()
        conn2.commit()
        conn2.close()
    else:
        sql_query1 = f"INSERT INTO table_user1 (user_id, user_name) VALUES ({user_id}, '{user_name}');"
        cursor1.execute(sql_query1)
        sql_query2 = f"INSERT INTO table_user2 (user_id, user_name) VALUES ({user_id}, '{user_name}');"
        cursor2.execute(sql_query2)

        cursor1.close()
        conn1.commit()
        conn1.close()
        cursor2.close()
        conn2.commit()
        conn2.close()
        return True



# to improve
def retrieveAllFavGames(user_id):
    """
    user_id is int,
    if user not exist in table_user1 and table_user1,
    return 'user non-existent',
    else return a json array, 
    json array is empty if the user dosen't have faverate game,
    """
    conn1, cursor1 = connect_fetch(1)
    conn2, cursor2 = connect_fetch(2)

    try:
        # check if user exists in table_user1 and table_favourite
        sql_query0 = f"SELECT 1 FROM table_user1 WHERE user_id = {user_id}"
        sql_query1 = f"SELECT 1 FROM table_favourite1 WHERE user_id = {user_id};"
        sql_query2 = f"SELECT 1 FROM table_favourite2 WHERE user_id = {user_id};"

        cursor1.execute(sql_query0)
        result0 = cursor1.fetchall()

        if not result0:
            return ('user non-existent')

        conn1, cursor1 = connect_fetch(1)
        conn2, cursor2 = connect_fetch(2)

        # check if user exists in 2 table_favourites
        cursor1.execute(sql_query1)
        result1 = cursor1.fetchall()
        cursor2.execute(sql_query2)
        result2 = cursor2.fetchall()

        fav_games = []
        if result1:
            sql_query3 = (f"SELECT g.gamename, g.price "
                          f"FROM table_favourite1 AS f "
                          f"JOIN table_game1 AS g ON f.user_favorite_game_id = g.gameid "
                          f"WHERE f.user_id = {user_id};")
            cursor1.execute(sql_query3)
            fav_games += cursor1.fetchall()

        if result2:
            sql_query4 = (f"SELECT g.gamename, g.price "
                          f"FROM table_favourite2 AS f "
                          f"JOIN table_game2 AS g ON f.user_favorite_game_id = g.gameid "
                          f"WHERE f.user_id = {user_id};")
            cursor2.execute(sql_query4)
            fav_games += cursor2.fetchall()

    finally:
        if cursor1:
            cursor1.close()
        if cursor2:
            cursor2.close()
        if conn1:
            conn1.commit()
            conn1.close()
        if conn2:
            conn2.commit()
            conn2.close()

    #print([i for i in fav_games])
    flat_list = [(item[0],item[1]) for item in fav_games]
    return flat_list
    
    # df = pd.concat([df1, df2], axis=0)
    # df.to_json(f'AllFavGames{user_id}.json', orient = 'split', compression = 'infer')
    


def favor(gameid, user_id):
    """
    gameid is string, user_id is int,
    gameid has to be informat "G001" to "G999", "G1000" to "G4839"
    if not added yet,
    add gameid to favourite table under the corresponding database, return success
    else return fail
    """

    pattern1 = r'^G(0{0,2}[1-9]|0?[1-9][0-9]|[1-9][0-9]{2})'
    pattern2 = r'^G(100[0-9]|10[1-9][0-9]|1[1-9][0-9]{2}|2[0-4][0-9]{2}|2500)'
    pattern3 = r'^G(250[1-9]|25[1-9][0-9]|2[6-9][0-9]{2}|[3-9][0-9]{3})'

    if re.match(pattern1, gameid) and len(gameid) == 4:
        inx = 1
        conn, cursor = connect_fetch(1)

    elif re.match(pattern2, gameid) and len(gameid) == 5:
        inx = 1
        conn, cursor = connect_fetch(1)

    elif re.match(pattern3, gameid) and len(gameid) == 5:
        inx = 2
        conn, cursor = connect_fetch(2)
    else:
        return ('game id non-existent')       
    
    '''
    gamei = int(gameid[1:])
    if gamei <= 2500:
        inx = 1
        conn, cursor = connect_fetch(1)
    elif 2500 < gamei <= 4839:
        inx = 2
        conn, cursor = connect_fetch(2)
    else:
        return ('game non-existent')
    '''

    sql_query1 = f"SELECT 1 FROM table_favourite{inx} WHERE user_id = {user_id} AND user_favorite_game_id = '{gameid}';"
    sql_query2 = f"SELECT 1 FROM table_user{inx} WHERE user_id = {user_id}"

    cursor.execute(sql_query1)
    result1 = cursor.fetchall()
    cursor.execute(sql_query2)
    result2 = cursor.fetchall()

    if result1:
        cursor.close()
        conn.commit()
        conn.close()
        return ('Game added to collection')
    
    elif not result2:
        cursor.close()
        conn.commit()
        conn.close()
        return ('User non-existent')
    
    else:
        sql_query = f"INSERT INTO table_favourite{inx} (user_favorite_game_id, user_id) VALUES ('{gameid}', {user_id});"
        cursor.execute(sql_query)

        cursor.close()
        conn.commit()
        conn.close()
        return ('Game added to collection')



def unFavor(gameid, user_id):
    """
    gameid is string, user_id is int,
    if not deleted yet,
    delete gameid in the favourite table under the corresponding database, return success
    else return fail
    """
    gamei = int(gameid[1:])
    if gamei <= 2500:
        inx = 1
        conn, cursor = connect_fetch(1)
    elif 2500 < gamei <= 4839:
        inx = 2
        conn, cursor = connect_fetch(2)
    else:
        return ('This game is not favorited or game does not exist')

    sql_query1 = f"SELECT 1 FROM table_favourite{inx} WHERE user_id = {user_id} AND user_favorite_game_id = '{gameid}';"
    sql_query2 = f"SELECT 1 FROM table_user{inx} WHERE user_id = {user_id}"

    cursor.execute(sql_query1)
    result1 = cursor.fetchall()
    cursor.execute(sql_query2)
    result2 = cursor.fetchall()

    if result1:
        sql_query1 = f"DELETE FROM table_favourite{inx} WHERE user_favorite_game_id = '{gameid}' AND user_id = {user_id};"
        cursor.execute(sql_query1)
        conn.commit()
        conn.close()
        return ('Game removed from collection')
    
    elif not result2:
        conn.commit()
        conn.close()
        return ('User does not exist')
    
    else:
        conn.commit()
        conn.close()
        return ('This game is not favorited or game does not exist')



def SearchName(name):
    """
    ignore letter case
    ignore stopwords
    first do sql query on GameName in table_game1 and table_game2
    load games with name include the search name to dataframe

    then search by name by match over 60% or inclusion,
    max return are first 50 GameName, base on match score
    default sort by match score

    input name(string)
    if input name(string) is '', match all game
    input kind(string: Match, GameName, PositiveReviewRate, Price)
    input order(string: asc, desc)

    return a json file call SearchName{name}.json
    includes gameid, gamename, gametag, gameplatform, PositiveReviewRate, price, match
    """
    name_clean = name.replace(',', ' ')
    name_list = name_clean.split()
    stopwords = ['a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for',
             'if', 'in', 'is', 'it', 'no', 'of', 'on', 'or', 'such', 'that', 'the', 'to']
    name_l = [i for i in name_list if i not in stopwords]

    ss = ''
    for n in name_l:
        s = f' LOWER(gamename) LIKE LOWER("%{n}%")'
        ss = ss + s + ' OR'
    statement1 = ('SELECT * FROM table_game1 WHERE' + ss)[:-3]
    statement2 = ('SELECT * FROM table_game2 WHERE' + ss)[:-3]

    conn1, cursor1 = connect_fetch(1)
    conn2, cursor2 = connect_fetch(2)

    df1 = pd.read_sql(statement1, conn1)
    df2 = pd.read_sql(statement2, conn2)
    
    cursor1.close()
    conn1.commit()
    conn1.close()
    cursor2.close()
    conn2.commit()
    conn2.close()
    
    df = pd.concat([df1, df2], axis=0)
    # df = merged_df.drop_duplicates()


    # further delicate filtering by python
    # set up match score for each game name fetched
    def condition(x):
        if fuzz.token_set_ratio(x, name) > 60:
            return True
        elif name in x:
            return True
        else:
            return False

    dfMatched = df[df['gamename'].apply(condition)]

    
    if len(dfMatched) == 0:
        return ('no match')
    
    dfMatched['match'] = dfMatched['gamename'].apply(lambda x: fuzz.token_set_ratio(x, name))
    dfMatched = dfMatched.sort_values(by='match', ascending=False)
    dfMatched = dfMatched.reset_index(drop=True)
    dfMatched = dfMatched.drop(dfMatched.index[maxrow:])
    

    # return json object
    #js = dfMatched.to_json(orient="split")
    return dfMatched.to_dict(orient='records')
    #js_array = convert(js)
    #return js


def SearchTag(tag):
    """
    ignore letter case
    search by tag by match 85% or inclusion
    defualt sort by match score

    input tag(string ignore letter case)
    seperate by "," if input multiple tags

    return a json file call SearchTag{tag}.json
    includes gameid, gamename, gametag, gameplatform, PositiveReviewRate, price, match
    """
    # clean input string
    tag_l = tag.split(',')
    tag_l = [j.strip() for j in tag_l]
    tag_t = ' '.join(tag_l)

    # generate sql query
    ss = ''
    for t in tag_l:
        s = f' LOWER(gametag) LIKE LOWER("%{t}%")'
        ss = ss + s + ' OR'

    # connect to sql server and fetch desired data based on user input
    statement1 = ('SELECT * FROM table_game1 WHERE' + ss)[:-3]
    statement2 = ('SELECT * FROM table_game2 WHERE' + ss)[:-3]

    conn1, cursor1 = connect_fetch(1)
    conn2, cursor2 = connect_fetch(2)

    df1 = pd.read_sql(statement1, conn1)
    df2 = pd.read_sql(statement2, conn2)
    
    cursor1.close()
    conn1.commit()
    conn1.close()
    cursor2.close()
    conn2.commit()
    conn2.close()
    
    df = pd.concat([df1, df2], axis=0)
    # df = merged_df.drop_duplicates()
    
    def condition(x):
        if type(x) != str:
            return False
        l = list(x.split(', '))
        for ele in l:
            if fuzz.token_set_ratio(ele, i) >= 85:
                return True
            elif tag in ele:
                return True
        
        return False

    frames = []
    for i in tag_l:
        frames.append(df[df['gametag'].apply(condition)])

    # dfMatched = pd.concat(frames, axis=1, join="inner").iloc[:,:5]
    dfMatched = pd.concat(frames, axis=0)
    dfMatched = dfMatched.drop_duplicates()


    if len(dfMatched) == 0:
        return ('no match')


    dfMatched['match'] = dfMatched['gametag'].apply(lambda x: fuzz.token_set_ratio(x, tag_t))
    dfMatched = dfMatched.sort_values(by='match', ascending=False)
    dfMatched = dfMatched.reset_index(drop=True)
    dfMatched = dfMatched.drop(dfMatched.index[maxrow:])

    return dfMatched.to_dict(orient='records')
    #js = dfMatched.to_json(orient="split")
    #return js



def SearchPlatform(platform):
    """
    ignore letter case
    search by platform by match over 75% or inclusion
    sort by match score

    if no match, print "no match", return nothing
    if match, return a json file call SearchPlatform{platform}.json
    includes gameid, gamename, gametag, gameplatform, PositiveReviewRate, price, match
    """
    pf_l = platform.split(',')
    pf_l = [j.strip() for j in pf_l]
    pf_t = ' '.join(pf_l)

    ss = ''
    for pf in pf_l:
        if 'win' in pf.lower():
            pf = 'win'
        s = f' LOWER(gameplatform) LIKE LOWER("%{pf}%")'
        ss = ss + s + ' OR'
    statement1 = ('SELECT * FROM table_game1 WHERE' + ss)[:-3] + ';'
    statement2 = ('SELECT * FROM table_game2 WHERE' + ss)[:-3] + ';'
    
    conn1, cursor1 = connect_fetch(1)
    conn2, cursor2 = connect_fetch(2)

    df1 = pd.read_sql(statement1, conn1)
    df2 = pd.read_sql(statement2, conn2)
    
    cursor1.close()
    conn1.commit()
    conn1.close()
    cursor2.close()
    conn2.commit()
    conn2.close()
    
    dfMatched = pd.concat([df1, df2], axis=0)
    # df = merged_df.drop_duplicates()


    if len(dfMatched) == 0:
        return ('no match')

    dfMatched['match'] = dfMatched['gameplatform'].apply(lambda x: fuzz.token_set_ratio(x, pf_t))
    dfMatched = dfMatched.sort_values(by='match', ascending=False)
    dfMatched = dfMatched.reset_index(drop=True)
    dfMatched = dfMatched.drop(dfMatched.index[maxrow:])
    dfMatched = dfMatched.reset_index(drop=True)

    #js = dfMatched.to_json(orient="split")
    #return js
    return dfMatched.to_dict(orient='records')

'''
def convert(json_input):
    # Load the JSON string into a Python dictionary
    data = json.loads(json_input)
    
    # Extract the columns and data from the dictionary
    columns = data['columns']
    rows = data['data']
    
    # Create a new list to hold the JSON array
    json_array = []
    
    # Iterate over each row in the data
    for row in rows:
        # Create a dictionary for each row, mapping column names to row values
        row_dict = {columns[i]: row[i] for i in range(len(columns))}
        # Add the dictionary to the JSON array list
        json_array.append(row_dict)
    
    # Convert the list of dictionaries back into JSON formatted string
    return json.dumps(json_array, indent=4)
'''

def insertGame(glist):
# check if gameid valid
    gameid = glist[0]
    pattern1 = r'^G(0{0,2}[1-9]|0?[1-9][0-9]|[1-9][0-9]{2})'
    pattern2 = r'^G(100[0-9]|10[1-9][0-9]|1[1-9][0-9]{2}|2[0-4][0-9]{2}|2500)'
    pattern3 = r'^G(250[1-9]|25[1-9][0-9]|2[6-9][0-9]{2}|[3-9][0-9]{3})'

    if re.match(pattern1, gameid) and len(gameid) == 4:
        inx = 1
        conn, cursor = connect_fetch(1)

    elif re.match(pattern2, gameid) and len(gameid) == 5:
        inx = 1
        conn, cursor = connect_fetch(1)

    elif re.match(pattern3, gameid) and len(gameid) == 5:
        inx = 2
        conn, cursor = connect_fetch(2)
    else:
        return ('game id invalid')

    # check if gameid exists
    sql_query1 = f"SELECT 1 FROM table_game{inx} WHERE gameid = '{gameid}';"
    cursor.execute(sql_query1)
    result1 = cursor.fetchall()
    if result1:
        cursor.close()
        conn.commit()
        conn.close()
        return ('game id taken')
    
    else:
        # replace empty string with 'NULL'
        values = ''
        
        for i in glist:
            if not i:
                print("null", i)
                values = values + ", NULL"
            elif (type(i) == float) or (type(i) == int):
                values = values + f", {i}"
            else:
                values = values + f", '{i}'"
        print(values)
        sql_query2 = (f"INSERT INTO table_game{inx} "
                      f"(gameid, gamename, gametag, gameplatform, favorablerate, price) "
                      f"VALUES ({values[2:]});")
        cursor.execute(sql_query2)

        cursor.close()
        conn.commit()
        conn.close()
        return ('success')

def deleteGame(gameid):
    pattern1 = r'^G(0{0,2}[1-9]|0?[1-9][0-9]|[1-9][0-9]{2})'
    pattern2 = r'^G(100[0-9]|10[1-9][0-9]|1[1-9][0-9]{2}|2[0-4][0-9]{2}|2500)'
    pattern3 = r'^G(250[1-9]|25[1-9][0-9]|2[6-9][0-9]{2}|[3-9][0-9]{3})'

    if re.match(pattern1, gameid) and len(gameid) == 4:
        inx = 1
        conn, cursor = connect_fetch(1)

    elif re.match(pattern2, gameid) and len(gameid) == 5:
        inx = 1
        conn, cursor = connect_fetch(1)

    elif re.match(pattern3, gameid) and len(gameid) == 5:
        inx = 2
        conn, cursor = connect_fetch(2)
    else:
        return ('game id invalid')
    
    # check if gameid exists
    sql_query1 = f"SELECT 1 FROM table_game{inx} WHERE gameid = '{gameid}';"
    cursor.execute(sql_query1)
    result1 = cursor.fetchall()

    if result1:
        sql_query2 = f"DELETE FROM table_game{inx} WHERE gameid = '{gameid}';"
        cursor.execute(sql_query2)
        conn.commit()
        conn.close()
        return ('game deleted')
    
    else:
        cursor.close()
        conn.commit()
        conn.close()
        return ('game non-existent')

def deleteUser(user_id):
    '''
    deleteUser(int: userid)
    return meesage
    - user deleted
    - user non-existent
    '''
    # check if user exists
    sql_query = f"SELECT 1 FROM table_user1 WHERE user_id = {user_id}"
    conn1, cursor1 = connect_fetch(1)
    conn2, cursor2 = connect_fetch(2)
    cursor1.execute(sql_query)
    result = cursor1.fetchall()

    if result:
        sql_query1 = f"DELETE FROM table_user1 WHERE user_id = {user_id};"
        cursor1.execute(sql_query1)
        sql_query2 = f"DELETE FROM table_user2 WHERE user_id = {user_id};"
        cursor2.execute(sql_query2)

        cursor1.close()
        conn1.commit()
        conn1.close()
        cursor2.close()
        conn2.commit()
        conn2.close()
        return ('user deleted')
    
    else:
        cursor1.close()
        conn1.commit()
        conn1.close()
        cursor2.close()
        conn2.commit()
        conn2.close()
        return ('user non-existent')

def updateGame(gameid, gdict):
    
    gamei = int(gameid[1:])
    if gamei <= 2500:
        inx = 1
        conn, cursor = connect_fetch(1)
    elif 2500 < gamei <= 9999:
        inx = 2
        conn, cursor = connect_fetch(2)
    else:
        return ('game non-existent')

    # check if gameid exists
    sql_query1 = f"SELECT 1 FROM table_game{inx} WHERE gameid = '{gameid}';"
    cursor.execute(sql_query1)
    result1 = cursor.fetchall()

    if result1:
        for key, value in gdict.items():
            if key == 'gameid':
                break
            if value == 'null':
                sql_query2 = f"UPDATE table_game{inx} SET {key} = NULL WHERE gameid = '{gameid}';"
            elif key == 'price':
                sql_query2 = f"UPDATE table_game{inx} SET {key} = {value} WHERE gameid = '{gameid}';"
            else:
                sql_query2 = f"UPDATE table_game{inx} SET {key} = '{value}' WHERE gameid = '{gameid}';"
            cursor.execute(sql_query2)
        cursor.close()
        conn.commit()
        conn.close()
        return ('success')
    
    else:
        cursor.close()
        conn.commit()
        conn.close()
        return ('gameid non-existent')

def updateUser(user_id, newname):
    '''
    updateUser(user_id, string: "newusername")
        - success
        - user_id non-existent
    '''
    # check if user exists
    sql_query = f"SELECT 1 FROM table_user1 WHERE user_id = {user_id}"
    conn1, cursor1 = connect_fetch(1)
    conn2, cursor2 = connect_fetch(2)
    cursor1.execute(sql_query)
    result = cursor1.fetchall()

    if result:
        sql_query1 = f"UPDATE table_user1 SET user_name = '{newname}' WHERE user_id = {user_id};"
        cursor1.execute(sql_query1)
        sql_query2 = f"UPDATE table_user2 SET user_name = '{newname}' WHERE user_id = {user_id};"
        cursor2.execute(sql_query2)

        cursor1.close()
        conn1.commit()
        conn1.close()
        cursor2.close()
        conn2.commit()
        conn2.close()
        return ('User Updated')
    
    else:
        cursor1.close()
        conn1.commit()
        conn1.close()
        cursor2.close()
        conn2.commit()
        conn2.close()
        return ('User Does Not Exist')



if __name__ == '__main__':
    #addUser(1, "Austin")
    #print(favor("G001", 1))
    #print(SearchName("Battlefleet"))
    #print(favor("G204", 1))
    #retrieveAllFavGames(1)
    #print(unFavor("G013", 1))
    #print(deleteGame("G2078"))
    pass
    