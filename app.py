import random
import string
from flask_api import FlaskAPI, status


from persistenc import Persitance
from Artikel import Artikel

from flask import request, jsonify

app = FlaskAPI(__name__)

def randomString(stringLength):
    """Generate a random string with the combination of lowercase and uppercase letters """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))
@app.before_first_request
def fillwithData():
    art1 = {"anzahl":200,"beschreibung":"Umwälzpumpe","bilder":[{"id":"361bb816-0e89-4271-9b65-a812436810af","titel":"Umwälzpumpe","url":"https://upload.wikimedia.org/wikipedia/commons/0/08/Sindelfingen_Haus_%26_Energie_2018_by-RaBoe_056.jpg"}],"code":"DE12345678","einfuehrungsdatum":"2020-03-30T22:00:00Z[UTC]","einkaufspreis":25.3,"verkaufspreis":77.9}
    art2 = {"anzahl": 10, "beschreibung": "Dingenskirchen2", "bilder": [{
        "id": "361bb8",
        "titel": "Dinegnskirchen2",
        "url": "https://upload.wikimedia.org/wikipedia/commons/0/08/Sindelfingen_Haus_%26_Energie_2018_by-RaBoe_056.jpg"
    }],
    "code": "DE888555",
    "einfuehrungsdatum": "2020-03-31T19:21:57.634Z[UTC]",
    "einkaufspreis": 8.5,
    "verkaufspreis": 96.2
    }
    Persitance.BD.append(Artikel(art1))
    Persitance.BD.append(Artikel(art2))
    print("vorbereitet")


@app.route('/ArtikelService/rest/artikel/', methods=['POST'])
def hinzufugen():
    try:
        print(request.get_json(force=True))
        st = status.HTTP_200_OK
        if request.get_json(force=True) is not None:
            json = request.get_json(force=True)

            artikle = Artikel(json)
            if(artikle.hatFehler()):
                print("OK hat Fheler ??????")
                st = status.HTTP_400_BAD_REQUEST
            else:
                print('hinzufügen(' + json['code'] + ')')
                ok = True
                for b in artikle.bilder:
                    ok = True
                    try:
                        if len(b['id']) == 0:
                            print("kein id")
                            b['id'] = randomString(20)
                    except:
                        ok = False
                        st = status.HTTP_500_INTERNAL_SERVER_ERROR
                if ok:
                    for art in Persitance.BD:
                        if(art.code == artikle.code):
                            ok = False
                    if ok:
                        Persitance.BD.append(artikle)
                    else:
                        st = status.HTTP_500_INTERNAL_SERVER_ERROR
                    for ar in Persitance.BD:
                        print(ar.code)
        else:
            print("hier??")
            st = status.HTTP_400_BAD_REQUEST
    except:
        st = status.HTTP_500_INTERNAL_SERVER_ERROR
    return '', st


@app.route('/ArtikelService/rest/artikel/<string:code>', methods=['PUT'])
def aendern(code):
    try:
        st = status.HTTP_200_OK
        if request.get_json(force=True) is not None:
            code = code.upper()
            json = request.get_json(force=True)
            print('äandere'+ code)
            json['code'] = code
            artikle = Artikel(json)
            if(artikle.hatFehler()):
               st = status.HTTP_400_BAD_REQUEST
            else:
                for b in artikle.bilder:
                    ok = True
                    try:
                        if len(b['id']) == 0:
                            print("kein id")
                            b['id'] = randomString(20)
                    except:
                        ok = False
                        st = status.HTTP_500_INTERNAL_SERVER_ERROR
                gefunde = False
                for ar in Persitance.BD:
                    print(ar.code)
                    print(artikle.code)
                    print('----------')
                    if ar.code == artikle.code and not gefunde:
                        Persitance.BD.remove(ar)
                        Persitance.BD.append(artikle)
                        gefunde = True
                if not gefunde:
                    st = status.HTTP_401_UNAUTHORIZED
        else:
            st = status.HTTP_400_BAD_REQUEST
    except:
        st = status.HTTP_500_INTERNAL_SERVER_ERROR
    return '', st


@app.route('/ArtikelService/rest/artikel/<string:code>', methods=['DELETE'])
def loeschen(code):
    st = status.HTTP_200_OK
    code = code.upper()
    print('löschen'+ code)
    gefunde = False
    for ar in Persitance.BD:
        print(ar.code)
        print(code)
        print('----------')
        if ar.code == code and not gefunde:
            Persitance.BD.remove(ar)
            gefunde = True
        if not gefunde:
            st = status.HTTP_401_UNAUTHORIZED
    return '', st


@app.route('/ArtikelService/rest/artikel/', methods=['DELETE'])
def alleLoeschen():
    print('alle Löschen')
    Persitance.BD.clear()
    return '', status.HTTP_200_OK

@app.route('/ArtikelService/rest/artikel/', methods=['GET'])
def getArtikleListe():
    ret = '['
    ret2 = list()
    Persitance.BD.sort(key=lambda art: art.code)
    firtst = True
    for artikel in Persitance.BD:
        if not firtst:
            ret += ','
        ret += str(artikel.json)
        firtst = False
        ret2.append(artikel.json)
    return ret2


@app.route('/ArtikelService/rest/artikel/<string:code>', methods=['GET'])
def getArtikle(code):
    ret = ""
    code = code.upper()
    print('hole' + code)
    for artikel in Persitance.BD:
        if artikel.code == code:
            ret = artikel.json
    return ret
if __name__ == '__main__':
    app.run(debug=True, port=8080)
