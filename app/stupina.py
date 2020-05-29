from app import app
from flask import (
    request,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,
    make_response,
    abort,
)
from flask_mysqldb import MySQL
import datetime
import json
import app.models as models
import ast

mysql = MySQL(app)
# function for split
@app.route("/stupina_split", methods=["POST"])
def stupina_split():
    if request.method == "POST":
        try:
            receive = request.get_json()
            print(receive)
            locatie = receive["locatie_stupina_noua"]
            nr_stupi = receive["nr_stupi"]
            data_plasare = receive["data_stupina_noua"]
            id_user = receive["id_user"]
            lon = receive["longitudinea"]
            lat = receive["latitudinea"]
            alti = receive["altitudinea"]
            nr_stupi = receive["nr_stupi"]
            listStupi = receive["lista_stupi"]
            # Convertim stringul in array
            listStupi = listStupi.replace('[', "")
            listStupi = listStupi.replace('a]', "")
            listStupi = listStupi.replace('a, ', "")
            listStupi = list(listStupi)

            # adaugam stupina
            query = "select * from licenta.listastupine order by id_stupina desc"
            conn = mysql.connect
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchone()
            try:
                id_stupina = data[0]
            except Exception:
                id_stupina = 0

            # print(id_stupina)
            # cursor.execute("INSERT INTO listastupine VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", ((id_stupina + 1), locatie, nr_stupi, data_plasare, id_user, lon, lat, alti))
            for i in range(len(listStupi)):
                query = "update stup set id_stupina = "+ str(id_stupina + 1) + " where id_stup = '" + listStupi[i] + "a';"
                # cursor.execute(query)
            return "Success"
        except Exception as e:
            print("Eroare: ", e)
        finally:
            conn.commit()
            cursor.close
            conn.close
            print("Close the connection!")


@app.route("/stupina_post/<id_user>", methods=["POST"])
def post_data_stupina(id_user):
    if request.method == "POST":
        try:
            receive = request.get_json()
            locatie = receive["locatie"]
            nr_stupi = receive["nr_stupi"]
            data_plasare = receive["data_plasare"]
            lon = receive["longitudinea"]
            lat = receive["latitudinea"]
            alti = receive["altitudinea"]
            # print(lon, alti, lan)
            # print("Printarea s-a facut:", locatie, data_plasare)
            query = "select * from licenta.listastupine order by id_stupina desc"
            conn = mysql.connect
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchone()
            try:
                id_stupina = data[0]
            except Exception:
                id_stupina = 0
            print(id_stupina)
            cursor.execute(
                "INSERT INTO listastupine VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    (id_stupina + 1),
                    locatie,
                    nr_stupi,
                    data_plasare,
                    id_user,
                    lon,
                    lat,
                    alti,
                ),
            )
            mesaj = "Succes"
            return jsonify(mesaj)
        except Exception as e:
            print("Eroare: ", e)
        finally:
            conn.commit()
            cursor.close
            conn.close
            print("Close the connection!")


@app.route("/stupina/<id>/<id_user>", methods=["GET", "PUT", "DELETE"])
def modify_data_Stupina(id, id_user):
    # Extragerea tuturor stupilor cu acelasi id de stupina
    if request.method == "GET":
        try:
            query = (
                "select * from stup where id_stupina in (select id_stupina from listastupine where id_user ="
                + id_user
                + " and id_stupina ="
                + id
                + " ) order by id_stup desc;"
            )
            conn = mysql.connect
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            items = []
            for row in range(cursor.rowcount):
                items.append(
                    models.stup_model(
                        data[row][0],
                        data[row][1],
                        data[row][2],
                        data[row][3],
                        data[row][4],
                        data[row][5],
                        data[row][6],
                        data[row][7],
                        data[row][8],
                        data[row][9]
                    )
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

    elif request.method == "DELETE":
        try:
            query = "delete from listastupine where id_stupina =" + id
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
            print("Close the connection!")

    elif request.method == "PUT":
        try:
            receive = request.get_json()
            print(receive)
            print(type(receive))
            locatie = receive["locatie"]
            nr_stupi = receive["nr_stupi"]
            data_plasare = receive["data_plasare"]
            id_stupina = id

            query = (
                "update listastupine set locatie = '"
                + locatie
                + "', nr_stupi ="
                + nr_stupi
                + ", data_plasare = '"
                + data_plasare
                + "' where id_stupina = "
                + id
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


# pentru a prelua toate inregistrarile din tabela listastupina
@app.route("/data/<id_user>", methods=["GET"])
def get_data_stupina(id_user):
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        qwery = (
            "select id_stupina, count(id_stup) from stup where id_stupina in (select id_stupina from listastupine where id_user = "
            + id_user
            + ") group by id_stupina order by id_stupina asc"
        )
        cursor.execute(qwery)
        nr_stupi = cursor.fetchall()
        qwery = (
            "select * from listastupine where id_user ="
            + id_user
            + " order by id_stupina"
        )
        cursor.execute(qwery)
        data = cursor.fetchall()

        items = []
        for row in range(cursor.rowcount):
            try:
                items.append(
                    models.stupina_model(
                        data[row][0],
                        data[row][1],
                        nr_stupi[row][1],
                        data[row][3],
                        data[row][6],
                        data[row][5],
                    )
                )
            except IndexError:
                items.append(
                    models.stupina_model(
                        data[row][0],
                        data[row][1],
                        data[row][2],
                        data[row][3],
                        data[row][6],
                        data[row][5],
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


@app.route("/stupina/one/<id>", methods=["GET"])
def giveOneStup(id):
    if request.method == "GET":
        try:
            conn = mysql.connect
            cursor = conn.cursor()
            query = "select * from listastupine where id_stupina = '" + id + "';"
            cursor.execute(query)
            data = cursor.fetchall()
            items = []
            items = models.stupina_model(
                data[0][0], data[0][1], data[0][2], data[0][3], data[0][5], data[0][6]
            )
            print(items)
            send = make_response(jsonify(items), 200)
            return send
        except Exception as e:
            print("Error: ", e)
        finally:
            cursor.close
            conn.close
            print("Close the connection")
    else:
        return "Something went wrong! "


# implementation join for stupine
# stupina 1 va fi cea care va prelua datele de la stupina 2
@app.route("/stupina_modify/<stupina1>/<stupina2>", methods=["GET"])
def make_modify(stupina1, stupina2):
    try:
        qwery = (
            "update stup set id_stupina = "
            + stupina1
            + " where id_stupina = "
            + stupina2
            + ";"
        )
        qweryDelete = "delete from listastupine where id_stupina =" + stupina2 + ";"
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute(qwery)
        cursor.execute(qweryDelete)
        print(qwery)
        return "Success"
    except Exception as e:
        print("Eroare: ", e)
    finally:
        conn.commit()
        cursor.close
        conn.close
        print("Close the connection!")
