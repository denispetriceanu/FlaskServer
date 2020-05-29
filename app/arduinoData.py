from app import app
from flask import request, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask import jsonify, render_template
import app.models as models
import random
from datetime import date, datetime
from flask_mail import Mail, Message


mysql = MySQL(app)
# @app.route("/autocomplete", methods=['GET'])
# def autocompleteData():
#     if request.method == 'GET':
#         try:
#             conn = mysql.connect
#             cursor = conn.cursor()
#             temperatura = 30;
#             vizibilitate = 15000
#             greutate = 50000
#             umiditate = 65
#             presiune = 70
#             for i in range(100):
#                 greutate = greutate + 100
#                 dateIns = datetime.now()
#                 dateIns = dateIns.strftime("%m.%d.%Y")
#                 temperatura = random.randint(temperatura - 2, temperatura + 2)
#                 temp_ex = random.randint(temperatura - 14, temperatura - 10)
#                 vizibilitate = random.randint(vizibilitate - 2000, vizibilitate + 2000)
#                 umiditate = random.randint(umiditate - 10, umiditate + 10)
#                 if umiditate < 50:
#                     umiditate = 60
#                 if umiditate > 100:
#                     umiditate = 70
#                 presiune = random.randint(presiune - 10, presiune + 10)
#                 if i > 60:
#                     cursor.execute("INSERT INTO datafromarduino VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ('1a', 12, 3, dateIns, greutate,
#                                                                 temperatura, temp_ex, vizibilitate, umiditate, presiune))
#                 else:
#                     cursor.execute("INSERT INTO datafromarduino VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ('1a', 10, 3, dateIns, greutate,
#                                                                 temperatura, temp_ex, vizibilitate, umiditate, presiune))
#             mesaj = "Succes"
#             return jsonify(mesaj)
#         except Exception as e:
#             print(e)
#         finally:
#             conn.commit()
#             cursor.close
#             conn.close
#             print("Close the connection!")
# pentru a ma conecta la gmail si pentru a configura serverul

mail_settings = {
    "MAIL_SERVER": "smtp.gmail.com",
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "denispetriceanu@gmail.com",
    "MAIL_PASSWORD": models.someText(),
}

app.config.update(mail_settings)
mail = Mail(app)


def antifurt_send(id_stup):
    try:
        print("Am fost apelat!")
        mesaj = (
            "<p>Alerta,</p>"
            + "<p>Stupul dumneavoastra a fost miscat."
            + "Daca aceasta este o eroare va rugam sa ne contactati."
            + "<p>albinuta_ta@albina.net</p>"
        )
        conn = mysql.connect
        cursor = conn.cursor()
        qwery = (
            "select email from users where id_user in (select id_user from listastupine where id_stupina in (select id_stupina from stup where id_stup = '"
            + id_stup
            + "'));"
        )
        cursor.execute(qwery)
        data = cursor.fetchall()
        items = []
        username = "test"
        link = "google.ro"
        try:
            with app.app_context():
                msg = Message(
                    subject="ALERTA",
                    sender="denispetriceanu@gmail.com",
                    recipients=[
                        "denispetriceanu@gmail.com"
                    ],  # replace with your email for testing,
                    html=mesaj,
                )
                mail.send(msg)
                return jsonify("Success")
        except:
            return jsonify("Failure")
    except Exception as e:
        print(e)
    finally:
        cursor.close
        conn.close
        print("Close connection")


@app.route("/save_data/<id_stup_par>", methods=["POST", "GET"])
def save_data(id_stup_par):
    if request.method == "POST":
        try:
            receive = request.get_json()
            conn = mysql.connect
            cursor = conn.cursor()

            dateIns = datetime.now()
            dateIns = dateIns.strftime("%m.%d.%Y, %H:%M")
            problem = receive["antifurt"]

            temperatura = receive["temperatura"]
            presiune = receive["presiune"]
            id_stup = receive["id_stup"]
            nr_rame = receive["nr_rame"]
            id_stupina = receive["id_stupina"]
            vizibilitate = receive["lumina"]
            umiditate = receive["precipitatii"]

            if not problem:
                print("TRUE")
                # send email
                # antifurt_send(id_stup)
            else:
                print("FALSE")
            # qwery1 este pentru a verifica daca id-ul respectiv exista in tabela stupWith
            qwery1 = "select * from stupiwitharduino where id_stup = '" + id_stup + "';"
            cursor.execute(qwery1)
            if cursor.rowcount < 1:
                # interogare pentru aflarea id_ului potrivit din tabel
                qwery1 = "select * from stupiwitharduino;"
                cursor.execute(qwery1)
                data1 = cursor.fetchall()
                if cursor.rowcount < 1:
                    id = 1
                else:
                    id = data1[1] + 1
                # executam codul pentru adaugarea in baze de date a id_ului care nu exista deja
                cursor.execute(
                    "INSERT INTO stupiwitharduino VALUES (%s, %s)", (id, id_stup)
                )

            temp_ex = random.randint(
                int(temperatura[:-2].replace(".", "")) - 20,
                int(temperatura[:-2].replace(".", "")) - 7,
            )
            greutate = random.randint(5000 - 500, 5000 + 500)

            cursor.execute(
                "INSERT INTO datafromarduino VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    id_stup,
                    nr_rame,
                    id_stupina,
                    dateIns,
                    greutate,
                    temperatura,
                    temp_ex,
                    vizibilitate,
                    umiditate,
                    presiune,
                ),
            )

            mesaj = "Succes"
            return jsonify(mesaj)
        except Exception as e:
            print(e)
        finally:
            conn.commit()
            cursor.close
            conn.close
            print("Close the connection!")
    if request.method == "GET":
        try:
            conn = mysql.connect
            cursor = conn.cursor()
            cursor.execute(
                "select * from datafromarduino where id_stup='"
                + id_stup_par
                + "' order by data_insert;"
            )
            data = cursor.fetchall()
            items = []
            nr_oferit = cursor.rowcount
            if nr_oferit > 24:
                nr_oferit = 24

            for row in range(nr_oferit):
                items.append(
                    models.receive_data_arduino(
                        data[row][0],
                        data[row][2],
                        data[row][1],
                        data[row][3],
                        data[row][4],
                        data[row][5],
                        data[row][6],
                        data[row][7],
                        data[row][8],
                        data[row][9],
                    )
                )
            send = jsonify(items)
            return send
        except Exception as e:
            print(e)
        finally:
            conn.commit()
            cursor.close
            conn.close
            print("Close the connection!")
    else:
        return "FAILURE"


# primim date AI
@app.route("/set_data_ai", methods=["POST", "GET", "PUT"])
def set_data_ai():
    if request.method == "POST":
        try:
            receive = request.get_json
            # print(receive)
            rezultat = request.values.get("rezultat")
            id_stup = request.values.get("id_stup")
            conn = mysql.connect
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO rezultate_ai (id_stup, rezultat ) VALUES (%s, %s)",
                (id_stup, rezultat),
            )

            mesaj = rezultat
            print(mesaj)
            # return "success"
            return jsonify("Success")
        except Exception as e:
            print(e)
        finally:
            conn.commit()
            cursor.close
            conn.close
            print("Close the connection!")
    if request.method == "GET":
        try:
            conn = mysql.connect
            cursor = conn.cursor()
            cursor.execute("select * from rezultate_ai")
            data = cursor.fetchone()
            items = []
            items.append(models.ai(data[1], data[2]))

            print(items[0])

            send = jsonify(items)
            return send
        except Exception as e:
            print(e)
        finally:
            conn.commit()
            cursor.close
            conn.close
            print("Close the connection!")
    if request.method == "PUT":
        try:
            conn = mysql.connect
            cursor = conn.cursor()
            cursor.execute("SELECT * from rezultate_ai")
            data = cursor.fetchone()
            # nr_row = data[0]
            # print(nr_row)
            # print(type(nr_row))
            # print(type(str(nr_row)))
            cursor.execute("UPDATE rezultate_ai set rezultat=1 where id=" + str(data[0]))
            
            # send = jsonify("Success")
            return "Success"
        except Exception as e:
            print(e)
        finally:
            conn.commit()
            cursor.close
            conn.close
            print("Close the connection!")

# preluam date dupa idul stupinei
@app.route("/get_data_stupina/<id_stupina_par>", methods=["GET"])
def get_data(id_stupina_par):
    if request.method == "GET":
        try:
            conn = mysql.connect
            cursor = conn.cursor()
            cursor.execute(
                "select * from datafromarduino where id_stupina='"
                + id_stupina_par
                + "' order by data_insert;"
            )
            data = cursor.fetchall()
            items = []
            nr_oferit = cursor.rowcount
            if nr_oferit > 24:
                nr_oferit = 24

            for row in range(nr_oferit):
                items.append(
                    models.receive_data_arduino(
                        data[row][0],
                        data[row][2],
                        data[row][1],
                        data[row][3],
                        data[row][4],
                        data[row][5],
                        data[row][6],
                        data[row][7],
                        data[row][8],
                        data[row][9],
                    )
                )
            send = jsonify(items)
            return send
        except Exception as e:
            print(e)
        finally:
            conn.commit()
            cursor.close
            conn.close
            print("Close the connection!")


@app.route("/data_ML", methods=["GET"])
def send_data_to_ML():
    try:
        if request.method == "GET":
            conn = mysql.connect
            cursor = conn.cursor()
            print("test")
            print(cursor)
            query = "select * from datafromarduino"
            cursor.execute(query)
            data = cursor.fetchall()
            items = []
            for row in range(cursor.rowcount):
                query = (
                    "select data_tratament, produs from tratamente where id_stup = '"
                    + data[row][0]
                    + "' order by data_tratament asc;"
                )
                cursor.execute(query)
                tratament = cursor.fetchone()
                query = (
                    "select data_hranire, produs from hranire where id_stup = '"
                    + data[row][0]
                    + "' order by data_hranire asc;"
                )
                cursor.execute(query)
                hranire = cursor.fetchone()
                items.append(
                    models.info_for_ML(
                        data[row][6],  # temp_ex
                        data[row][5],  # temp_stup
                        data[row][4],  # greutate
                        data[row][9],  # vant
                        data[row][8],  # umidit_stup
                        data[row][8],  # umiditate_ext
                        data[row][9],  # presiune_stup
                        data[row][0].replace("a", "1"),  # "id_stup"
                        data[row][3]
                        .replace(".", "")
                        .replace(":", "")
                        .replace(",", "")
                        .replace(" ", ""),  # data
                        tratament[0][0],  # data_tratament
                        tratament[0][1],  # substanta
                        hranire[0][0],  # data_hranire
                        hranire[0][1],  # cantitate
                        data[row][1],  # rame_puie
                        data[row][1],  # mancare
                        data[row][1],  # goale
                        random.randint(0, 1),
                    )
                )
            send = jsonify(items)
            return send
    except Exception as e:
        print(e)
    finally:
        cursor.close
        conn.close
        print("Close connection")

