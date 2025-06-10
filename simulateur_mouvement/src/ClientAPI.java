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
}
