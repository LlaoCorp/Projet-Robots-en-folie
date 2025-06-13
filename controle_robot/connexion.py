import sys, json, network, time, urequests, ubinascii

## Configuration de la connexion Wi-Fis
ssid = 'IMERIR Fablab'
password = 'imerir66'

# #  @return Réponse du serveur à la requête POST.
# async def request():
#     try:
#         data = {
#                 "ref_id": "robotTest",
#                 "contenu": "test"
#             }
#         json_str = json.dumps(data)
#         print(json_str)
#         res = urequests.post(url='http://10.7.5.148:8000/envoyer/', json=json_str, headers={'content-type': 'application/json'})
#         return res
#     except Exception as exc:
#         print("erreur",exc)
#     time.sleep(2)

def init_connexion():
    wlan = network.WLAN(network.STA_IF)
    print(ubinascii.hexlify(wlan.config('mac')).decode())
    wlan.active(True)
    if not wlan.isconnected():
        print(f"Try connect to SSID : {ssid}")
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            print('.', end = " ")
            time.sleep_ms(500)
    print("\nWi-Fi Config:", wlan.ifconfig())
    print("{} initialized".format(sys.platform))