import netscape.javascript.JSObject;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class ClientAPI {

    public JsonObject getMission(String uuid){
        return null;
    }

    public void envoyerEtat(JSONObject message){

    }

    public JSONArray lireMessage(){
        return null;
    }

    public static void recupererMessages() {
        try {
            URL url = new URL("http://localhost:8000/messages/");
            HttpURLConnection con = (HttpURLConnection) url.openConnection();
            con.setRequestMethod("GET");

            BufferedReader in = new BufferedReader(
                    new InputStreamReader(con.getInputStream()));
            String inputLine;
            StringBuilder contenu = new StringBuilder();

            while ((inputLine = in.readLine()) != null) {
                contenu.append(inputLine);
            }
            in.close();

            System.out.println("Réponse du serveur : " + contenu.toString());

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

