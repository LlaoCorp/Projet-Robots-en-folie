import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;
import java.io.*;
import java.net.*;

public class SimpleJavaServer {
    public static void main(String[] args) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);

        // Route pour /process
        server.createContext("/process", new HttpHandler() {
            public void handle(HttpExchange exchange) throws IOException {
                if ("POST".equals(exchange.getRequestMethod())) {
                    // Lire le JSON d'entrée
                    InputStream input = exchange.getRequestBody();
                    String requestBody = new String(input.readAllBytes());

                    // Réponse simple
                    String response = "{\"message\":\"Processed by Java\",\"original\":\"" + requestBody + "\"}";

                    exchange.getResponseHeaders().set("Content-Type", "application/json");
                    exchange.sendResponseHeaders(200, response.length());
                    OutputStream os = exchange.getResponseBody();
                    os.write(response.getBytes());
                    os.close();
                }
            }
        });

        server.start();
        System.out.println("Serveur Java démarré sur port 8080");
    }
}