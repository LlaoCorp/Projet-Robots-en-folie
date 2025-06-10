import org.json.JSONArray;
import org.json.JSONObject;

public class RobotVirtuel {

    private String refId = "REF-25-20-0506";
    private ClientAPI api = new ClientAPI();
    private Boolean hasBox = false;
    private int position = 0;
    private int[] zonesDepot = {3, 6};

    public void avancer(int positionCible) {
        if (position < positionCible) {
            position++;
            api.envoyerAction(refId, "avance", position);
        } else if (position > positionCible) {
            position--;
            api.envoyerAction(refId, "recule", position);
        }
        String objectif = hasBox ? "Déposer un cube" : "Chercher un cube";
        api.envoyerEtat(refId, position, hasBox, objectif);
    }

    public int getPosition() {
        return this.position;
    }

    public int getPositionFromCube(String cubeName) {
        switch (cubeName) {
            case "Cube 1":
                return 1;
            case "Cube 2":
                return 2;
            case "Cube 3":
                return 4;
            case "Cube 4":
                return 5;
            case "Cube 5":
                return 7;
            default:
                return 0;
        }
    }

    public void setHasBox(boolean hasBox) {
        this.hasBox = hasBox;
        if (hasBox) {
            api.envoyerEtat(refId, position, hasBox,"Cube récupéré en position " + position);
            api.envoyerEtat(refId, position, hasBox, "Robot a désormais un cube");
        }else{
            api.envoyerEtat(refId, position, hasBox, "Cube déposé en zone " + position);
        }
    }

    public void prendreCube() {
        hasBox = true;
        api.envoyerAction(refId, "prend un cube", position);
        api.envoyerEtat(refId, position, hasBox, "Déposer un cube");
    }

    public void deposerCube() {
        hasBox = false;
        api.envoyerAction(refId, "dépose un cube", position);
        api.envoyerEtat(refId, position, hasBox, "Aucun objectif");
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
            avancer(cible);
            panel.setPositionRobot(position);
            Thread.sleep(600);
        }
    }
}