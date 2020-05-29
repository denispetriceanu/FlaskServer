from app import app
from flask import request, render_template, request, redirect, url_for, session, make_response
from flask_mysqldb import MySQL
from flask import jsonify
import app.models as models

mysql = MySQL(app)

@app.route("/hranire_post", methods=['POST'])
def hranire_post():
    if request.method == "POST":
        try:
            receive = request.get_json()

            id_stup = receive["id_stup"]
            data_hranire = receive["data_hranire"]
            tip_hrana = receive["tip_hrana"]
            tip_hranire = receive["tip_hranire"]
            produs = receive["produs"]
            producator = receive["producator"]
            cantitate = receive["cantitate"]
            nota = receive["nota"]

            print("ce am primit", id_stup, data_hranire, tip_hrana, tip_hranire, produs, producator, cantitate, nota)
            
            query1 = "select * from hranire order by id_hranire desc;"
            conn = mysql.connect
            cursor = conn.cursor()
            cursor.execute(query1)
            data = cursor.fetchone()
            
            try:
                id_hranire = data[0] + 1
            except:
                id_hranire = 1

            print(id_hranire)    
            cursor.execute("INSERT INTO hranire VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (id_hranire, id_stup, data_hranire, tip_hranire, 
                tip_hrana, produs, producator, cantitate, nota))

            mesaj = "Succes"
            return jsonify(mesaj)
        except Exception as e:
            print("Eroare: ", e)
        finally:
            conn.commit()
            cursor.close
            conn.close
            print("Close the connection!")

# de vazut ce trebuie facut in tabela hranire cu id-ul in cazul functiei get dupa id
@app.route("/hranire/<id>", methods=['GET', 'PUT', 'DELETE'])
def modify_data_hranire(id):
    if request.method == 'GET':
        try:
            conn = mysql.connect
            cursor = conn.cursor()
            query = "select * from hranire where id_hranire = " + id + " order by id_hranire desc;"
            cursor.execute(query)
            data = cursor.fetchall()
            items = []
            for row in range(cursor.rowcount):
                items.append(
                    models.hranire_model(
                        data[row][0], data[row][1], data[row][2], data[row][3], data[row][4], data[row][5], data[row][6], data[row][7], data[row][7]
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

    elif request.method == 'DELETE':
        try:
            query = "delete from hranire where id_hranire =" + id
            conn = mysql.connect
            cursor = conn.cursor()
            cursor.execute(query)
            return jsonify({'S-a sters cu success!'})
        except Exception as e:
            print("Eroare: ", e)
        finally:
            conn.commit()
            cursor.close
            conn.close
            print("Close the connection!")

    elif request.method == "PUT":
        try:
            receive = request.get_json()
            
            id_hranire = id
            id_stup = receive['id_stup']
            data_hranire = receive["data_hranire"]
            tip_hranire = receive["tip_hranire"]
            tip_hrana = receive["tip_hrana"]
            produs = receive["produs"]
            producator = receive["producator"]
            cantitate = receive["cantitate"]
            nota = receive["nota"]

            query = (
                "update stup set id_stup = '" + id_stup 
                + "', data_hranire ='" + data_hranire + "', tip_hranire = '" 
                + tip_hranire + "', tip_hrana = '" + tip_hrana + "', produs = '" 
                + produs + "', producator = '"  + producator + "', cantitate = " + cantitate + ", nota = '" + nota 
                + "' where id_hranire = " + id_hranire
            )
            conn = mysql.connect
            cursor = conn.cursor()
            cursor.execute(query)
            return "Success"
        except Exception as e:
            print("Eroare: ", e)
        finally:
            conn.commit()
            cursor.close
            conn.close
            print("Close the connection!")
    else:
        return "Sunteti aici pentru a modifica."


# pentru a prelua toate inregistrarile din tabela hranire
@app.route('/data_hranire/<id_user>', methods=['GET'])
def get_data_hranire(id_user):
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        query = "select * from hranire where id_stup in (select id_stup from stup where id_stupina in (select id_stupina from listastupine where id_user =" + id_user + " ))order by id_hranire desc"
        cursor.execute(query)
        data = cursor.fetchall()
        items = []
        for row in range(cursor.rowcount):
            items.append(
                models.hranire_model(
                    data[row][0], data[row][1], data[row][2], data[row][3], data[row][4], data[row][5], data[row][6], data[row][7], data[row][7]
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