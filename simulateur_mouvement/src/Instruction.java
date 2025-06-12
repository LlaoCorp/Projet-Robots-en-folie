import java.util.ArrayList;

public class Instruction {
    private String refId;
    private ArrayList<Integer> numCube;
    private String statut;

    public Instruction(String refId, ArrayList<Integer> numCube, String statut) {
        this.refId = refId;
        this.numCube = numCube;
        this.statut = statut;
    }

    public String getRefId() {
        return refId;
    }

    public ArrayList<Integer> getNumCube() {
        return numCube;
    }

    public String getStatut() {
        return statut;
    }

    public void setStatut(String statut) {
        this.statut = statut;
    }
}
