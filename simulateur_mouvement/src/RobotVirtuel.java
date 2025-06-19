/**
 * @file RobotVirtuel.java
 * @brief Classe représentant un robot virtuel capable d'exécuter des instructions.
 */

import java.util.ArrayList;

/**
 * Classe représentant un robot virtuel qui interagit avec une API,
 * se déplace dans un environnement simulé, et effectue des actions sur des blocs.
 */
public class RobotVirtuel {

    private String refId = "REF-25-20-0506";
    private ClientAPI api = new ClientAPI();
    private Instruction instruction = null;
    private Boolean hasBox = false;
    private int position = 1;
    private int[] zonesDepot = {4, 5, 8, 9};
    private SimulateurJava simulateur;

    /**
     * Déplace le robot d'une case vers la position cible et envoie la télémétrie.
     * @param positionCible la position cible à atteindre
     */
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

    /**
     * Active la pince virtuelle pour simuler la prise d’un cube.
     */
    public void prendreCube() {
        hasBox = true;
        log("Cube récupéré !");
        System.out.println("Cube récupéré en position " + position);
    }

    /**
     * Désactive la pince virtuelle pour simuler le dépôt du cube.
     */
    public void deposerCube() {
        hasBox = false;
        log("Dépose cube en zone " + position);
        System.out.println("Cube déposé en position " + position);
    }

    /**
     * Retourne l’état de la pince (si elle contient un cube).
     * @return true si un cube est transporté
     */
    public boolean hasBox() {
        return this.hasBox;
    }

    /**
     * Retourne l'identifiant du robot.
     * @return l'ID unique du robot
     */
    public String getRefId() {
        return refId;
    }

    /**
     * Calcule la zone de dépôt la plus proche de la position actuelle.
     * @return l'identifiant de la zone de dépôt la plus proche
     */
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

    /**
     * Retourne l’instance de l’API utilisée.
     * @return instance de ClientAPI
     */
    public ClientAPI getApi() {
        return api;
    }

    /**
     * Déplace progressivement le robot jusqu’à la cible tout en mettant à jour l’interface.
     * @param cible position cible
     * @param panel panneau graphique à mettre à jour
     * @throws InterruptedException si le thread est interrompu
     */
    public void deplacerVers(int cible, ZonePanel panel) throws InterruptedException {
        while (position != cible) {
            System.out.println(position);
            System.out.println(cible);
            avancer(cible);
            panel.setPositionRobot(position);
            Thread.sleep(600);
        }
    }

    /**
     * Exécute l’instruction reçue : va chercher chaque cube, le dépose, puis envoie un résumé.
     * @param panel panneau graphique à mettre à jour
     * @throws InterruptedException si le thread est interrompu
     */
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

    /**
     * Associe le simulateur actuel à ce robot (pour afficher les logs).
     * @param simulateur instance du simulateur
     */
    public void setSimulateur(SimulateurJava simulateur) {
        this.simulateur = simulateur;
    }

    /**
     * Enregistre une action dans le journal du simulateur.
     * @param message texte à afficher dans le log
     */
    private void log(String message) {
        if (simulateur != null) simulateur.ajouterInstruction(message);
    }
}
