/**
 * @file Instruction.java
 * @brief Structure représentant une mission contenant une liste de cubes.
 */

import java.util.ArrayList;

/**
 * Classe contenant les informations d’une instruction pour un robot.
 */
public class Instruction {
    private String refId;
    private ArrayList<Integer> numCube;
    private String status;

    /**
     * Constructeur.
     * @param refId identifiant du robot
     * @param numCube liste des blocs à traiter
     * @param status statut de la mission
     */
    public Instruction(String refId, ArrayList<Integer> numCube, String status) {
        this.refId = refId;
        this.numCube = numCube;
        this.status = status;
    }

    /** @return l’identifiant du robot */
    public String getRefId() {
        return refId;
    }

    /** @return la liste des blocs à traiter */
    public ArrayList<Integer> getNumCube() {
        return numCube;
    }

    /** @return le statut de la mission */
    public String getStatus() {
        return status;
    }

    /**
     * Met à jour le statut de l’instruction.
     * @param status nouveau statut
     */
    public void setStatus(String status) {
        this.status = status;
    }
}
