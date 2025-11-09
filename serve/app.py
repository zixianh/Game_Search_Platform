from flask import Flask, request, jsonify
import pymysql
from pymysql.cursors import DictCursor
from mysql.connector import connect, Error
from flask_cors import CORS
#from allFunctions import searchbyplatform,searchbyname,searchbytag,addUser,favourite,unFavourite,retrieveAllFavGames
from matching import addUser,favor, unFavor,retrieveAllFavGames,SearchName,SearchPlatform,SearchTag, insertGame, deleteGame, deleteUser, updateGame,updateUser
from flask_cors import cross_origin

app = Flask(__name__)
CORS(app)
def get_db_connection(DB):
    try:
        if DB == 1:
            db_name = 'GDB1'
        elif DB == 2:
            db_name = 'GDB2'
        else:
            raise ValueError("Invalid database selection")

        connection = connect(
            host='localhost',
            user='root',
            password='frank990808',
            database=db_name
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
    
    
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/insertgame/<string:gameid>/<string:gamename>/<string:gametag>/<string:gameplatform>/<string:favorablerate>/<string:price>', methods=['GET'])
def add_game(gameid, gamename, gametag, gameplatform, favorablerate, price):
    # Convert "null" values to None
    gameid = None if gameid == "null" else gameid
    gamename = None if gamename == "null" else gamename
    gametag = None if gametag == "null" else gametag
    gameplatform = None if gameplatform == "null" else gameplatform
    favorablerate = None if favorablerate == "null" else favorablerate
    price = None if price == "null" else float(price)

    print([gameid, gamename, gametag, gameplatform, favorablerate, price])
    response = insertGame([gameid, gamename, gametag, gameplatform, favorablerate, price])
    print(response)
    return jsonify({"result": response}), 200

   
@app.route('/deletegame/<string:gameid>', methods=['GET'])
def delete_game(gameid):
    response = deleteGame(gameid)
    print(response)
    return jsonify({"result": response}), 200

@app.route('/deleteuser/<string:userid>', methods=['GET'])
def delete_user(userid):
    response = deleteUser(userid)
    print(response)
    return jsonify({"result": response}), 200

@app.route('/updateuser/<string:userid>/<string:username>', methods=['GET'])
def update_User(userid,username):
    response = updateUser(userid, username)
    print(response)
    return jsonify({"result": response}), 200


@app.route('/updategame/<gameid>', methods=['GET'])
def update_game(gameid):

    update_data = {}

    # List of possible parameters
    possible_params = ['gamename', 'gametag', 'gameplatform', 'favorablerate', 'price']

    # Iterate through possible parameters and add them to the dictionary if provided
    for param in possible_params:
        value = request.args.get(param)
        if value is not None:
            update_data[param] = value

    response = updateGame(gameid, update_data)
    print(response)
    return jsonify({"result": response}), 200

'''
@app.route('/game/<int:id>', methods=['DELETE'])
def delete_game(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Check if the game exists
    cursor.execute('SELECT * FROM Game WHERE Id = %s', (id,))
    game = cursor.fetchone()
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    
    # Delete the game if it exists
    cursor.execute('DELETE FROM Game WHERE Id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': 'Game deleted successfully'}), 200
'''


# Search games by name
@app.route('/games/searchname/<string:name>', methods=['GET'])
def search_games_by_name(name):
    if not name:
        return jsonify({'error': 'Name parameter is required'}), 400
    
    matching_games = SearchName(name)
    print(type(matching_games))
    result = jsonify(matching_games)
    return result 



# Search games by tag
@app.route('/games/searchtag/<string:tag>', methods=['GET'])
def search_games_by_tag(tag):

    if not tag:
        return jsonify({'error': 'Tag parameter is required'}), 400
    
    matching_games = SearchTag(tag)
    return jsonify(matching_games), 200

# Search games by platform
@app.route('/games/searchplatform/<string:platform>', methods=['GET'])
def search_games_by_platform(platform):

    if not platform:
        return jsonify({'error': 'platform parameter is required'}), 400
    
    matching_games = SearchPlatform(platform)
    return jsonify(matching_games), 200


@app.route('/favourite/<string:user_id>/<string:game_id>', methods=['GET'])
def add_favourite(user_id, game_id):
    #print("fav page")
    response = favor(game_id, user_id)
    print(response)
    return jsonify({"result": response}), 200

@app.route('/unfavourite/<string:user_id>/<string:game_id>', methods=['GET'])
def remove_favourite(user_id, game_id):
    response = unFavor(game_id, user_id)
    return jsonify({"result": response}), 200



@app.route('/adduser/<int:user_id>/<string:user_name>', methods=['GET'])
def add_user(user_id, user_name):
    response = addUser(user_id, user_name)
    return jsonify({"result": response}), 200



@app.route('/allfavgames/<string:user_id>', methods=['GET'])
def get_favorite_games(user_id):
    try:
        favorite_games = retrieveAllFavGames(user_id)
        return favorite_games, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
