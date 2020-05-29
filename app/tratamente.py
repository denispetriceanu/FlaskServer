from app import app
from flask import request, render_template, request, redirect, url_for, session, make_response
from flask_mysqldb import MySQL
from flask import jsonify
from app.models import tratamente_model

mysql = MySQL(app)

@app.route("/tratament/post", methods=['POST'])
def addtratament():
     if request.method == "POST":
        try:
            receive = request.get_json()
            id_stup = receive['id_stup']
            data_receive = receive['data_tratament']
            afectiune = receive['afectiune']
            produs = receive['produs']
            mod_admin = receive['mod_administrare']
            familii_albine = receive['familii_albine']
            doza = receive['doza']
            cantitate = receive['cantitate']
            observatii = receive['observatii']
            
            query = "select * from licenta.tratamente order by id_tratament desc"
            conn = mysql.connect
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchone()

            try:
                id_tratament = data[0]
                id_tratament = id_tratament + 1
            except Exception:
                id_tratament = 1

            cursor.execute("INSERT INTO tratamente VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ((id_tratament), id_stup, data_receive, afectiune,  produs, mod_admin, familii_albine, int(doza), int(cantitate), observatii))
            mesaj = "Succes"
            return jsonify(mesaj)
        except Exception as e:
            print("Eroare: ", e, "Asta e")
        finally:
            conn.commit()
            cursor.close
            conn.close
            print("Close the connection!")


@app.route("/tratamente/<id>", methods=['GET', 'DELETE'])
def modify_data_tratamente(id):
    if request.method == 'GET':
        try:
            query = "select * from tratamente where id_tratament =" + id
            conn = mysql.connect
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            print(data)
            items = []
            for row in range(cursor.rowcount):
                items.append(
                    tratamente_model(
                        data[row][0], data[row][1], data[row][2], data[row][3], data[row][4], 
                        data[row][5], data[row][6], data[row][7], data[row][8], data[row][9])
                )
            if not items:
                return "Resources not found!"

            return jsonify(items)
        except Exception as e:
            print("Eroare: ", e)
        finally:
            cursor.close
            conn.close
            print("Close the connection!")
    elif request.method == 'DELETE':
        try:
            query = "delete from tratamente where id_tratament =" + id
            conn = mysql.connect
            cursor = conn.cursor()
            cursor.execute(query)
            res = make_response(jsonify({"It's ok!"}), 200)
            return res
        except Exception as e:
            print("Eroare: ", e)
        finally:
            conn.commit()
            cursor.close
            conn.close
    else:
        return "Ai gresit metoda!"


# pentru a prelua toate inregistrarile din tabela data
@app.route('/tratamentefacute/<id_user>', methods=['GET'])
def get_data_tratamente(id_user):
    if request.method == 'GET':
        try:
            query = "select * from tratamente where id_stup in (select id_stup from stup where id_stupina in (select id_stupina from listastupine where id_user =" + id_user + " ))order by id_tratament desc"
            conn = mysql.connect
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            print(data)
            items = []
            for row in range(cursor.rowcount):
                items.append(
                    tratamente_model(
                        data[row][0], data[row][1], data[row][2], data[row][3], data[row][4], 
                        data[row][5], data[row][6], data[row][7], data[row][8], data[row][9])
                )
            return jsonify(items)
        except Exception as e:
            print("Eroare: ", e)
        finally:
            cursor.close
            conn.close
            print("Close the connection!")