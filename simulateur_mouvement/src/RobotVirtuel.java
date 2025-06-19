import org.json.JSONArray;
import org.json.JSONObject;

import javax.swing.*;
import java.util.ArrayList;

public class RobotVirtuel {

    private String refId = "REF-25-20-0506";
    private ClientAPI api = new ClientAPI();
    private Instruction instruction = null;
    private Boolean hasBox = false;
    private int position = 1;
    private int[] zonesDepot = {4,5,8,9};
    private SimulateurJava simulateur;

    public void avancer(int positionCible) {
        log("Avance vers position " + position);
        if (position < positionCible) {
            position++;
        } else if (position > positionCible) {
            position--;
        }

        float vitesse = 1.0f;
        float distanceUltrasons = 20.0f;
        String statusDeplacement = "avancer";
        int ligne = position;
        boolean pinceActive = hasBox;

        api.envoyerTelemetry(refId, vitesse, distanceUltrasons, statusDeplacement, ligne, pinceActive);
    }

    public void prendreCube() {
        hasBox = true;
        log("Cube récupéré !");
        System.out.println("Cube récupéré en position " + position);
    }

    public void deposerCube() {
        hasBox = false;
        log("Dépose cube en zone " + position);
        System.out.println("Cube déposé en position " + position);
    }

    public boolean hasBox() {
        return this.hasBox;
    }

    public String getRefId() {
        return refId;
    }

    public int getZoneDepotPlusProche() {
        int minDistance = Integer.MAX_VALUE;
        int meilleureZone = zonesDepot[0];

        for (int zone : zonesDepot) {
            int distance = Math.abs(zone - this.position);
            if (distance < minDistance) {
                minDistance = distance;
                meilleureZone = zone;
            }
        }
        return meilleureZone;
    }

    public ClientAPI getApi() {
        return api;
    }

    public void deplacerVers(int cible, ZonePanel panel) throws InterruptedException {
        while (position != cible) {
            System.out.println(position);
            System.out.println(cible);
            avancer(cible);
            panel.setPositionRobot(position);
            Thread.sleep(600);
        }
    }

    public void executerInstruction(ZonePanel panel) throws InterruptedException {
        instruction = api.recupererInstruction(refId);
        ArrayList<Integer> blocks = instruction.getNumCube();
        System.out.println(blocks);
        if (instruction == null || blocks == null || blocks.isEmpty()) {
            System.out.println("Aucune instruction trouvée.");
            return;
        }

        for (int i = 0; i < blocks.size(); i++) {
            System.out.println(blocks.get(i));
            int cible = instruction.getNumCube().get(i);

            deplacerVers(cible, panel);
            prendreCube();

            int zoneDepot = getZoneDepotPlusProche();
            deplacerVers(zoneDepot, panel);
            deposerCube();
        }
        api.envoyerSummary(refId);
    }


    public void setSimulateur(SimulateurJava simulateur) {
        this.simulateur = simulateur;
    }

    private void log(String message) {
        if (simulateur != null) simulateur.ajouterInstruction(message);
    }
}