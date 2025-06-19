/**
 * @file ClientAPI.java
 * @brief Classe permettant de communiquer avec le serveur FastAPI pour les robots virtuels.
 */

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;

/**
 * Classe responsable des échanges HTTP entre le robot et le serveur :
 * récupération des instructions, envoi de la télémétrie et des résumés.
 */
public class ClientAPI {

    private final String apiHost = "10.7.5.148";

    /**
     * Méthode générique pour envoyer une requête POST à une route de l’API.
     * @param endpoint chemin de l’API
     * @param jsonPayload corps de la requête JSON
     */
    private void envoyer(String endpoint, String jsonPayload) {
        try {
            URL url = new URL("http://" + apiHost + ":8000" + endpoint);
            HttpURLConnection con = (HttpURLConnection) url.openConnection();
            con.setRequestMethod("POST");
            con.setRequestProperty("Content-Type", "application/json");
            con.setDoOutput(true);

            OutputStream os = con.getOutputStream();
            byte[] input = jsonPayload.getBytes("utf-8");
            os.write(input, 0, input.length);
            os.close();

            int responseCode = con.getResponseCode();
            System.out.println("Requête vers " + endpoint + " - Code : " + responseCode);
            con.disconnect();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * Récupère l’instruction en cours pour un robot donné.
     * @param refId identifiant du robot
     * @return une instance de Instruction si trouvée, sinon null
     */
    public Instruction recupererInstruction(String refId) {
        try {
            URL url = new URL("http://localhost:8000/instructions?robot_id=" + refId);
            HttpURLConnection con = (HttpURLConnection) url.openConnection();
            con.setRequestMethod("GET");
            con.setRequestProperty("Accept", "application/json");

            int responseCode = con.getResponseCode();
            if (responseCode == 200) {
                BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
                StringBuilder content = new StringBuilder();
                String line;
                while ((line = in.readLine()) != null) {
                    content.append(line);
                }
                in.close();

                JSONObject json = new JSONObject(content.toString());
                JSONArray blocksArray = json.getJSONArray("blocks");

                ArrayList<Integer> cubes = new ArrayList<>();
                for (int i = 0; i < blocksArray.length(); i++) {
                    cubes.add(blocksArray.getInt(i));
                }

                String status = "current";
                modifierStatusInstruction(refId, "current");
                return new Instruction(refId, cubes, status);
            } else {
                System.out.println("Erreur récupération instruction (code " + responseCode + ")");
                return null;
            }
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    /**
     * Modifie le statut d'une instruction dans l’API.
     * @param refId identifiant du robot
     * @param status nouveau statut (ex : \"new\", \"current\", \"finish\")
     */
    public void modifierStatusInstruction(String refId, String status) {
        JSONObject payload = new JSONObject();
        payload.put("robot_id", refId);
        payload.put("status", status);
        envoyer("/instructions/change_status/" + refId, payload.toString());
    }

    /**
     * Envoie une mesure de télémétrie au serveur.
     * @param refId identifiant du robot
     * @param vitesse_instant vitesse actuelle du robot
     * @param ds_ultrasons distance mesurée par les ultrasons
     * @param status_deplacement statut du mouvement (ex : \"avancer\")
     * @param ligne position actuelle du robot
     * @param status_pince état de la pince (true = fermée)
     */
    public void envoyerTelemetry(String refId, float vitesse_instant, float ds_ultrasons,
                                 String status_deplacement, Integer ligne, boolean status_pince) {
        JSONObject payload = new JSONObject();
        payload.put("robot_id", refId);
        payload.put("vitesse_instant", vitesse_instant);
        payload.put("ds_ultrasons", ds_ultrasons);
        payload.put("statut_deplacement", status_deplacement);
        payload.put("ligne", ligne);
        payload.put("statut_pince", status_pince);
        envoyer("/telemetry", payload.toString());
    }

    /**
     * Envoie un résumé de mission (summary) et met le statut à \"finish\".
     * @param refId identifiant du robot
     */
    public void envoyerSummary(String refId) {
        JSONObject payload = new JSONObject();
        payload.put("robot_id", refId);
        modifierStatusInstruction(refId, "finish");
        envoyer("/summary", payload.toString());
    }
}
