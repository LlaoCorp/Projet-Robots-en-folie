import org.json.JSONArray;
import org.json.JSONObject;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;

public class ClientAPI {

    private void envoyer(String endpoint, String jsonPayload) {
        try {
            URL url = new URL("http://localhost:8000" + endpoint);
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

    public void envoyerEtat(String refId, int position, boolean hasBox, String objectif) {
        JSONObject payload = new JSONObject();
        payload.put("ref_id", refId);
        payload.put("position", position);
        payload.put("has_box", hasBox);
        payload.put("objectif", objectif);
        envoyer("/etat", payload.toString());
    }

    public void envoyerAction(String refId, String action, int position) {
        JSONObject payload = new JSONObject();
        payload.put("ref_id", refId);
        payload.put("action", action);
        payload.put("position", position);
        envoyer("/action", payload.toString());
    }

    public void envoyerMission(String refId, String numCube) {
        JSONObject payload = new JSONObject();
        payload.put("ref_id", refId);
        payload.put("num_cube", numCube);
        payload.put("statut", "new");

        envoyer("/mission", payload.toString());
    }

    public Mission recupererMission(String refId) {
        try {
            URL url = new URL("http://localhost:8000/mission/" + refId);
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
                String numCube = json.getString("num_cube");
                String statut = json.getString("statut");

                return new Mission(refId, numCube, statut);
            } else {
                System.out.println("Aucune mission récupérée (code " + responseCode + ")");
                return null;
            }
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    public void modifierStatusMission(String refId, Mission mission){
        JSONObject payload = new JSONObject();
        payload.put("ref_id", refId);
        payload.put("statut", mission.getStatut());
        envoyer("/mission/change_statut/"+refId, payload.toString());
    }

}
