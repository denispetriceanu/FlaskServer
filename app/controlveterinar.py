from app import app
from flask import request, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask import jsonify
from app.models import control_veterinar_model

mysql = MySQL(app)

@app.route("/controlveterinar_post", methods=['POST'])
def control_post():
    if request.method == "POST":
        try:
            receive = request.get_json()
            id_stupina = receive['id_stupina']
            data_control = receive['data_control']
            examinare = receive['examinare']
            stare = receive['stare']
            proba = receive['proba']
            concluzii = receive['concluzii']
            veterinar = receive['veterinar']
            observatii = receive['observatii']
            
            print("Ceea ce am primit: ", id_stupina, data_control, examinare, stare, proba, concluzii, veterinar, observatii)
            
            query = "select * from licenta.controlveterinar order by id_control desc"
            conn = mysql.connect
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchone()
            print("Data + ", type(data))

            try:
                id_control = data[0] + 1
            except:
                id_control = 1;
            
            cursor.execute("INSERT INTO controlveterinar VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (id_control, id_stupina, data_control, examinare,
                                                                                        stare, proba, concluzii, veterinar, observatii))
            mesaj = "Succes"
            return jsonify(mesaj)
        except Exception as e:
            print("Eroare: ", e)
        finally:
            conn.commit()
            cursor.close
            conn.close
            print("Close the connection!")

@app.route("/controlVeterinar/<id>", methods=['GET', 'PUT', 'DELETE'])
def modify_data_control(id):
    if request.method == 'GET':
        try:
            if request.method == 'GET':
                conn = mysql.connect
                cursor = conn.cursor()
                query = "SELECT * FROM controlveterinar where id_control = " + id + ";";
                cursor.execute(query)
                data = cursor.fetchall()
                items = []
                for row in range(cursor.rowcount):
                    items.append(
                        control_veterinar_model(data[row][0], data[row][1], data[row][2], data[row][3], data[row][4], data[row][5], data[row][6], 
                        data[row][7], data[row][8])
                    )
                send = jsonify(items)
                return send
        except Exception as e:
            print(e)
        finally:
            cursor.close
            conn.close
            print("Close connection")    
    elif request.method == 'DELETE':
        try:
            query = "delete from controlveterinar where id_control =" + id
            conn = mysql.connect
            cursor = conn.cursor()
            cursor.execute(query)
            mesaj = "succes"
            return mesaj
        except Exception as e:
            print("Eroare: ", e)
        finally:
            conn.commit()
            cursor.close
            conn.close
            print("Close the connection!")
    else:
        return "Sunteti aici pentru a modifica."


# pentru a prelua toate inregistrarile din tabela control_veterinar
@app.route('/data_controlVeterinar/<id_user>', methods=['GET'])
def get_data_controlVeterinar(id_user):
    try:
        if request.method == 'GET':
            conn = mysql.connect
            cursor = conn.cursor()
            cursor.execute("select * from licenta.controlveterinar where id_stupina in (select id_stupina from listastupine where id_user = " + id_user + " ) order by id_control desc;")
            data = cursor.fetchall()
            items = []
            for row in range(cursor.rowcount):
                items.append(
                    control_veterinar_model(data[row][0], data[row][1], data[row][2], data[row][3], data[row][4], data[row][5], data[row][6], 
                    data[row][7], data[row][8])
                )
            send = jsonify(items)
            return send
    except Exception as e:
        print(e)
    finally:
        cursor.close
        conn.close
        print("Close connection")    