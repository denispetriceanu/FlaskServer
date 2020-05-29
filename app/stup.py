from app import app
from flask import request, render_template, request, redirect, url_for, session, make_response
from flask_mysqldb import MySQL
from flask import jsonify
import app.models as models

mysql = MySQL(app)


@app.route("/stup_post", methods=['POST'])
def stup_post():
    if request.method == "POST":
        try:
            receive = request.get_json()
            id_stupina = receive['id_stupina']
            tip_stup = receive['tip_stup']
            culoare_stup = receive['culoare_stup']
            numarRame = receive['numarRame']
            rasa_albine = receive['rasa_albine']
            varsta_matca = receive['varsta_matca']
            mod_constituire = receive['mod_constituire']
            rame_puiet = receive['rame_puiet']
            rame_hrana = receive['rame_hrana']
            query = "select * from licenta.stup order by id_stup desc"
            conn = mysql.connect
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchone()
            id_stup = data[0]
            print(str((int(id_stup[:-1]) + 1))+"a")
            cursor.execute("INSERT INTO stup VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ((str((int(id_stup[:-1]) + 1))+"a"), id_stupina, tip_stup, culoare_stup,
                                                                                        numarRame, rasa_albine, varsta_matca, mod_constituire, rame_puiet, rame_hrana))
            mesaj = "Succes"
            return jsonify(mesaj)
        except Exception as e:
            print("Eroare: ", e)
        finally:
            conn.commit()
            cursor.close
            conn.close
            print("Close the connection!")

@app.route("/stup/usstupina/<id>/<id_user>", methods=["GET"])
def getStupina(id, id_user):
    if request.method == 'GET':
        try:
            conn = mysql.connect
            cursor = conn.cursor()
            query = "select * from stup where id_stupina in (select id_stupina from listastupine where id_user =" + id_user + " and id_stupina =" + id + " ) order by id_stup desc;"
            cursor.execute(query)
            data = cursor.fetchall()
            items = []
            for row in range(cursor.rowcount):
                items.append(
                    models.stup_model(
                        data[row][0], data[row][1], data[row][2], data[row][3], data[row][4], data[row][5], data[row][6], data[row][7], data[row][8], data[row][9]
                    )
                )
            send = make_response(jsonify(items), 200)
            return send
        except Exception as e:
            print("Error: ", e)
        finally:
            cursor.close
            conn.close
            print("Close the connection")

@app.route("/stup/<id>/<tip>", methods=['GET', 'POST', 'PUT', 'DELETE'])
def modify_data_stup(id, tip):
    if request.method == 'GET':
        try:
            conn = mysql.connect

            if tip == 'more':
                cursor = conn.cursor()
                query = "select * from stup where id_stup = '" + id + "';"        
                query2 = "select * from hranire where id_stup = '" + id + "' order by id_hranire limit 1;"
                query3 = "select * from tratamente where id_stup = '" + id + "' order by id_tratament limit 1;"
                
                cursor.execute(query2)
                data2 = cursor.fetchall()
                print(data2)
                cursor.execute(query3)
                data3 = cursor.fetchall()
                print(data3)
                cursor.execute(query)
                data = cursor.fetchall()
                print(data)
                items = []
                if not data2 or not data3:    
                    for row in range(cursor.rowcount):
                        items.append(
                            models.stup_model(
                                data[row][0], data[row][1], 
                                data[row][2], data[row][3], 
                                data[row][4], data[row][5], 
                                data[row][6], data[row][7],
                                data[row][8], data[row][9]
                            )
                        )
                else:
                    for row in range(cursor.rowcount):
                        items.append(
                            models.stup_model_complex(
                                data[row][0], data[row][1], 
                                data[row][2], data[row][3], 
                                data[row][4], data[row][5], 
                                data[row][6], data[row][7],
                                data[row][8], data[row][9],
                                data2[0][2], data2[0][3], 
                                data2[0][8], data3[0][2], 
                                data3[0][3], data3[0][8]
                            )
                        )
                send = make_response(jsonify(items), 200)
            else:
                cursor = conn.cursor()
                query = "select * from stup where id_stup = '" + id + "';"        
                cursor.execute(query)   
                data = cursor.fetchall()
                items = []
                for row in range(cursor.rowcount):
                    items.append(
                        models.stup_model(
                            data[row][0], data[row][1], data[row][2], data[row][3], data[row][4], data[row][5], data[row][6], data[row][7], data[row][8], data[row][9]
                        )
                    )
                send = make_response(jsonify(items), 200)            
            return send
        except Exception as e:
            print("Error: ", e)
        finally:
            cursor.close
            conn.close
            print("Close the connection")
    elif request.method == 'PUT':
        try:
            receive = request.get_json()
            print(receive)
            id_stup = id
            id_stupina = receive['id_stupina']
            tip_stup = receive['tip_stup']
            culoare_stup = receive['culoare_stup']
            
            numarRame = receive['numarRame']
            rasa_albine = receive['rasa_albine']
            varsta_matca = receive['varsta_matca']
            mod_constituire = receive['mod_constituire']
            rame_puiet = receive['rame_puiet']
            rame_hrana = receive['rame_hrana']

            print("Am primit:")
            print(id_stup, rasa_albine, varsta_matca)
            query = (
                "update stup set rasa_albine = '" + rasa_albine
                + "', id_stupina =" + id_stupina + ", tip_stup = '"
                + tip_stup + "', culoare_stup = '" + culoare_stup + "', numarRame = '"
                + numarRame + "', varsta_matca = " + varsta_matca +
                ", mod_constituire = '" + mod_constituire + "', rame_puiet = " + rame_puiet + ", rame_hrana = " + rame_hrana  
                + " where id_stup = '" + id + "'"
            )
            conn = mysql.connect
            cursor = conn.cursor()
            cursor.execute(query)
            print(query)
            return "Success"
        except Exception as e:
            print("Eroare: ", e)
        finally:
            conn.commit()
            cursor.close
            conn.close
            print("Close the connection!")
    elif request.method == 'DELETE':
        try:
            print(id)
            query = "delete from stup where id_stup ='" + id + "'"
            print(query)
            conn = mysql.connect
            cursor = conn.cursor()
            cursor.execute(query)
            return "Succes"
        except Exception as e:
            print("Eroare: ", e)
        finally:
            conn.commit()
            cursor.close
            conn.close
            print("Close the connection!")
    else:
        return "Wrong link!"


@app.route('/data_stup/<id_user>', methods=['GET'])
def get_data_stup(id_user):
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        query = "select  * from licenta.stup where id_stupina in (select id_stupina from listastupine where id_user = " + id_user + " ) order by id_stup desc;"
        cursor.execute(query)
        data = cursor.fetchall()
        items = []
        for row in range(cursor.rowcount):
            items.append(
                models.stup_model(
                    data[row][0], data[row][1], data[row][2], data[row][3], data[row][4], data[row][5], data[row][6], data[row][7], data[row][8], data[row][9]
                )
            )
        send = make_response(jsonify(items), 200)
        return send
    except Exception as e:
        print("Error: ", e)
    finally:
        cursor.close
        conn.close
        print("Close the connection")
