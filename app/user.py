from app import app
from flask import request, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask import jsonify, render_template, Response
import app.models as models
from flask_mail import Mail, Message
import json
import os

mysql = MySQL(app)


@app.route("/user", methods=["GET", "POST", "PUT", "DELETE"])
def modify_data_user():
    if request.method == "PUT":
        try:
            receive = request.get_json()
            email = receive["email"]
            adresa = receive["adresa"]
            prenume = receive["prenume"]
            nume = receive["nume"]
            telefon = receive["telefon"]
            query = (
                "update users set nume ='"
                + nume
                + "', prenume = '"
                + prenume
                + "', telefon = '"
                + telefon
                + "', adresa = '"
                + adresa
                + "' where email = '"
                + email
                + "';"
            )
            conn = mysql.connect
            cursor = conn.cursor()
            cursor.execute(query)
            try:
                response = Response(status=333)
                return jsonify(response)
            except:
                return "false"
        except Exception as e:
            print(e)
        finally:
            conn.commit()
            cursor.close
            conn.close
            print("Close the connection!")
    elif request.method == "POST":
        try:
            receive = request.get_json()
            email = receive["email"]
            parola = receive["parola"]
            adresa = receive["adresa"]
            prenume = receive["prenume"]
            nume = receive["nume"]
            telefon = receive["telefon"]
            conn = mysql.connect
            cursor = conn.cursor()

            query = "Select * from users where email = '" + email + "';"
            cursor.execute(query)
            test = cursor.fetchone()
            try:
                test = test[4]
                response = Response(status=666)
                return response
            except:
                print("Error")

            queryForID = "Select * from users order by id_user desc;"
            cursor.execute(queryForID)
            data = cursor.fetchone()
            try:
                id = data[0] + 1
            except:
                id = 1
            cursor.execute(
                "INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (id, nume, prenume, adresa, email, telefon, parola),
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
        # metoda DELETE verifica daca datele cu care se incearca logarea sunt corecte
    elif request.method == "DELETE":
        try:
            receive = request.get_json()
            email = receive["email"]
            parola = receive["pass"]
            print(email + " " + parola)
            query = (
                "select * from users where parola = '"
                + parola
                + "' and email = '"
                + email
                + "';"
            )
            conn = mysql.connect
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            if not data:
                return jsonify("false")
            else:
                mesaj = data[0][0]
                return jsonify(mesaj)
        except Exception as e:
            print(e)
        finally:
            conn.commit()
            cursor.close
            conn.close
            print("Close the connection!")
    else:
        return "Sunteti aici pentru a modifica."


# pentru a prelua toate inregistrarile din tabela data
@app.route("/data_user/<id_user>", methods=["GET"])
def get_data_user(id_user):
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        # text = 'select * from licenta.stup'
        cursor.execute("select * from users where id_user = " + id_user)
        data = cursor.fetchall()
        items = []
        for row in range(cursor.rowcount):
            # id_user, parola, nume, prenume, adresa, email, telefon
            items.append(
                models.user_model(
                    data[row][0],
                    data[row][6],
                    data[row][1],
                    data[row][2],
                    data[row][3],
                    data[row][4],
                    data[row][5],
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


@app.route("/recover_pass", methods=["POST"])
def recover():
    try:
        
        receive = request.get_json()
        email = receive["email"]
        print("emaile: " + email)
        mesaj = (
            "<p>Buna,</p>"
            + "<p>Dumneavoastr sau altcineva a realizat o cerere de resetare a parolei."
            + "Daca tu ai facut aceasta cerere va rog dati click pe urmatorul link: "
            + "<a href={{link}}><strong>reset password</strong></a>. Daca nu ai facut aceasta cerere ignorati emailul.</p>"
            + "<p>Te saluta,</p><p>Albinuta Ta</p>"
            + "<p>albinuta_ta@albina.net</p>"
        )
        conn = mysql.connect
        cursor = conn.cursor()
        qwery = "select * from users where email = '" + email + "';"
        cursor.execute(qwery)
        data = cursor.fetchall()
        items = []
        username = "test"
        link = "google.ro"
        try:
            print(data[0][4])
            if email == data[0][4]:
                with app.app_context():
                    msg = Message(
                        subject="Resetare parola",
                        sender="denispetriceanu@gmail.com",
                        recipients=[
                            "denispetriceanu@gmail.com"
                        ],  # replace with your email for testing,
                        html=mesaj,
                    )
                    mail.send(msg)
                    print ("success")
                    return jsonify("Success")
        except:
            return jsonify("Failure")
    except Exception as e:
        print(e)
    finally:
        cursor.close
        conn.close
        print("Close connection")


