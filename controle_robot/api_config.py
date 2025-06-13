import ujson as json
import urequests, time

class ClientAPI:
    def __init__(self, server_ip, port=8000):
        self.base_url = f"http://{server_ip}:{port}"

    def envoyer(self, endpoint, payload):
        try:
            url = self.base_url + endpoint
            headers = {"Content-Type": "application/json"}
            res = urequests.post(url, data=json.dumps(payload), headers=headers)
            print(f"Requête POST vers {endpoint} - Code : {res.status_code}")
            res.close()
        except Exception as e:
            print("Erreur lors de l'envoi :", e)

    def envoyer_instruction(self, ref_id, blocks):
        payload = {
            "robot_id": ref_id,
            "blocks": blocks,
            "statut": "new"
        }
        self.envoyer("/instructions", payload)

    def recuperer_instruction(self, ref_id):
        try:
            url = self.base_url + f"/instructions/{ref_id}"
            res = urequests.get(url)
            if res.status_code == 200:
                data = res.json()
                blocks = data.get("blocks", [])
                statut = data.get("statut", "")
                print("Instruction reçue :", data)

                self.modifier_status_instruction(ref_id, "current")
                return {"ref_id": ref_id, "blocks": blocks, "statut": statut}
            else:
                print("Erreur récupération instruction - Code :", res.status_code)
            res.close()
        except Exception as e:
            print("Erreur GET instruction :", e)
        return None

    def modifier_status_instruction(self, ref_id, statut):
        payload = {
            "robot_id": ref_id,
            "statut": statut
        }
        self.envoyer(f"/mission/change_statut/{ref_id}", payload)

    def envoyer_telemetry(self, ref_id, ds_ultrasons, status_deplacement, ligne, status_pince):
        payload = {
            "robot_id": ref_id,
            "vitesse_instant": 1.0,
            "ds_ultrasons": ds_ultrasons,
            "status_deplacement": status_deplacement,
            "ligne": ligne,
            "status_pince": status_pince
        }
        self.envoyer("/telemetry", payload)
        time.sleep(1)

    def envoyer_summary(self, ref_id, vitesse_moy):
        payload = {
            "robot_id": ref_id,
            "viesse_moy": vitesse_moy
        }
        self.envoyer("/summary", payload)
