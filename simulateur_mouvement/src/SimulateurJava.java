import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class SimulateurJava {

    public static void envoyerMessage(String refId, String contenu) {
        try {
            URL url = new URL("http://localhost:8000/envoyer/");
            HttpURLConnection con = (HttpURLConnection) url.openConnection();

            con.setRequestMethod("POST");
            con.setRequestProperty("Content-Type", "application/json; utf-8");
            con.setDoOutput(true);

            String jsonInputString = String.format("{\"ref_id\": \"%s\", \"contenu\": \"%s\"}", refId, contenu);

            try (OutputStream os = con.getOutputStream()) {
                byte[] input = jsonInputString.getBytes("utf-8");
                os.write(input, 0, input.length);
            }

            int code = con.getResponseCode();
            System.out.println("Code réponse : " + code);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        envoyerMessage("robot-simu-001", "test");
    }
}
