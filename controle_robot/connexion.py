import sys, json, network, time, urequests, ubinascii

## Configuration de la connexion Wi-Fis
ssid = 'IMERIR Fablab'
password = 'imerir66'
wlan = network.WLAN(network.STA_IF)

def get_adr_mac():
    return ubinascii.hexlify(wlan.config('mac')).decode()

def init_connexion():
    wlan.active(True)
    if not wlan.isconnected():
        print(f"Try connect to SSID : {ssid}")
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            print('.', end = " ")
            time.sleep_ms(500)
    print("\nWi-Fi Config:", wlan.ifconfig())
    print("{} initialized".format(sys.platform))