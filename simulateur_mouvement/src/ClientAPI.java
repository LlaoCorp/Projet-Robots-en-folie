import org.json.JSONArray;
import org.json.JSONObject;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

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

//    public void envoyerEtat(String refId, int position, boolean hasBox, String objectif) {
//        JSONObject payload = new JSONObject();
//        payload.put("ref_id", refId);
//        payload.put("position", position);
//        payload.put("has_box", hasBox);
//        payload.put("objectif", objectif);
//        envoyer("/etat", payload.toString());
//    }

//    public void envoyerAction(String refId, String action, int position) {
//        JSONObject payload = new JSONObject();
//        payload.put("ref_id", refId);
//        payload.put("action", action);
//        payload.put("position", position);
//        envoyer("/action", payload.toString());
//    }

    public void envoyerInstruction(String refId, ArrayList<Integer> blocks) {
        JSONObject payload = new JSONObject();
        payload.put("robot_id", refId);
        payload.put("blocks", blocks);
        payload.put("statut", "new");
        envoyer("/instructions", payload.toString());
    }

    public Instruction recupererInstruction(String refId) {
        try {
            URL url = new URL("http://localhost:8000/instructions/" + refId);
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
                JSONArray blocksArray = new JSONArray(json.getString("blocks"));
                String statut = json.getString("statut");

                ArrayList<Integer> cubes = new ArrayList<>();
                for (int i = 0; i < blocksArray.length(); i++) {
                    cubes.add(blocksArray.getInt(i));
                }

                modifierStatusInstruction(refId, "current");
                return new Instruction(refId, cubes, statut);
            } else {
                System.out.println("Erreur récupération instruction (code " + responseCode + ")");
                return null;
            }
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    public void modifierStatusInstruction(String refId, String statut) {
        JSONObject payload = new JSONObject();
        payload.put("robot_id", refId);
        payload.put("statut", statut);
        envoyer("/mission/change_statut/"+refId, payload.toString());
    }

    public void envoyerTelemetry(String refId, float vitesse_instant, float ds_ultrasons, String status_deplacement, Integer ligne, boolean status_pince){
        JSONObject payload = new JSONObject();
        payload.put("robot_id", refId);
        payload.put("vitesse_instant", vitesse_instant);
        payload.put("ds_ultrasons", ds_ultrasons);
        payload.put("status_deplacement", status_deplacement);
        payload.put("ligne", ligne);
        payload.put("status_pince", status_pince);
        envoyer("/telemetry", payload.toString());
    }

    public void envoyerSummary(String refId, float viesse_moy){
        JSONObject payload = new JSONObject();
        payload.put("robot_id", refId);
        payload.put("viesse_moy", viesse_moy);
        envoyer("/summary", payload.toString());
    }
}
