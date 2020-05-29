def stupina_model(
    id_stupina, locatie, nr_stupi, data_plasare, latitudinea, longitudinea
):
    return {
        "id_stupina": id_stupina,
        "locatie": locatie,
        "nr_stupi": nr_stupi,
        "data_plasare": data_plasare,
        "latitudine": latitudinea,
        "longitudine": longitudinea,
    }


def stup_model(
    id_stup,
    id_stupina,
    tip_stup,
    culoare_stup,
    numarRame,
    rasa_albine,
    varsta_matca,
    mod_constituire,
    rame_puiet,
    rame_hrana,
):
    return {
        "id_stup": id_stup,
        "id_stupina": id_stupina,
        "tip_stup": tip_stup,
        "culoare_stup": culoare_stup,
        "numarRame": numarRame,
        "rasa_albine": rasa_albine,
        "varsta_matca": varsta_matca,
        "mod_constituire": mod_constituire,
        "rame_puiet": rame_puiet,
        "rame_hrana": rame_hrana
    }


def stup_model_complex(
    id_stup,
    id_stupina,
    tip_stup,
    culoare_stup,
    numarRame,
    rasa_albine,
    varsta_matca,
    mod_constituire,
    rame_puiet,
    rame_hrana,
    data_hranire,
    tip_hrana,
    nota_hramire,
    data_tratamente,
    afectiune,
    observatii,
):
    return {
        "id_stup": id_stup,
        "id_stupina": id_stupina,
        "tip_stup": tip_stup,
        "culoare_stup": culoare_stup,
        "numarRame": numarRame,
        "rasa_albine": rasa_albine,
        "varsta_matca": varsta_matca,
        "mod_constituire": mod_constituire,
        "rame_puiet": rame_puiet,
        "rame_hrana": rame_hrana,
        "data_hranire": data_hranire,
        "tip_hrana": tip_hrana,
        "nota_hranire": nota_hramire,
        "data_tratament": data_tratamente,
        "afectiune": afectiune,
        "observatii": observatii,
    }


def hranire_model(
    id_hranire,
    id_stup,
    tip_hranire,
    data_hranire,
    tip_hrana,
    produs,
    producator,
    cantitate,
    nota,
):
    return {
        "id_hranire": id_hranire,
        "id_stup": id_stup,
        "data_hranire": data_hranire,
        "tip_hranire": tip_hranire,
        "tip_hrana": tip_hrana,
        "produs": produs,
        "producator": producator,
        "cantitate": cantitate,
        "nota": nota,
    }


def control_veterinar_model(
    id_control,
    id_stupina,
    data_control,
    examinare,
    stare,
    proba,
    concluzii,
    veterinar,
    observatii,
):
    return {
        "id_control": id_control,
        "id_stupina": id_stupina,
        "data_control": data_control,
        "examinare": examinare,
        "stare": stare,
        "proba": proba,
        "concluzii": concluzii,
        "veterinar": veterinar,
        "observatii": observatii,
    }


def tratamente_model(
    id_tratament,
    id_stup,
    data_tratament,
    afectiune,
    produs,
    mod_administrare,
    familii_albine,
    doza,
    cantitate,
    observatii,
):
    return {
        "id_tratament": id_tratament,
        "id_stup": id_stup,
        "data_tratament": data_tratament,
        "afectiune": afectiune,
        "produs": produs,
        "mod_administrare": mod_administrare,
        "familii_albine": familii_albine,
        "doza": doza,
        "cantitate": cantitate,
        "observatii": observatii,
    }


def user_model(id_user, parola, nume, prenume, adresa, email, telefon):
    return {
        "parola": parola,
        "id_user": id_user,
        "nume": nume,
        "prenume": prenume,
        "adresa": adresa,
        "email": email,
        "telefon": telefon,
    }


def user_response(message):
    return {"mesaj": message}


def receive_data_arduino(
    id_stup,
    id_stupina,
    nr_rame,
    data_insert,
    greutate,
    temperatura,
    temp_ex,
    vizibilitate,
    umiditate,
    presiune,
):
    return {
        "id_stup": id_stup,
        "id_stupina": id_stupina,
        "nr_rame": nr_rame,
        "data_insert": data_insert,
        "greutate": greutate,
        "temperatura": temperatura,
        "temp_ex": temp_ex,
        "vizibilitate": vizibilitate,
        "umiditate": umiditate,
        "presiune": presiune,
    }


def someText():
    nume = "Denis"
    an = "98."
    hobby = "fotbal"
    returning = hobby + nume + an
    return returning

def ai(id, rezultat):
    return {
    "id": id,
    "rezultat": rezultat
    }
    

def info_for_ML(
    temp_ex,
    temp_stup,
    greutate,
    vant,
    umiditate_stup,
    umiditate_ex,
    presiune_stup,
    id_stup,
    data_ora,
    data_tratamente,
    substanta_tratament,
    data_hranire,
    cantitate_hrana,
    rame_puiet,
    rame_mancare,
    rame_goale,
    stare
):
    return {
        "temperatura_exterior": temp_ex,
        "temperatura_stup": temp_stup,
        "greutate": greutate,
        "vant": vant,
        "umiditate_stup": umiditate_stup,
        "umiditate_exterior": umiditate_ex,
        "presiune_stup": presiune_stup,
        "id_stup": id_stup,
        "data_ora": data_ora,
        "data_tratament": data_tratamente,
        "substanta_tratament": substanta_tratament,
        "data_hranire": data_hranire,
        "cantitate_hrana": cantitate_hrana,
        "rame_puiet": rame_puiet,
        "rame_mancare": rame_mancare,
        "rame_goale": rame_goale,
        "stare": stare
    }

