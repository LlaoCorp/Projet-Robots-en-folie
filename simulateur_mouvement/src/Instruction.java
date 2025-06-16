import java.util.ArrayList;

public class Instruction {
    private String refId;
    private ArrayList<Integer> numCube;
    private String status;

    public Instruction(String refId, ArrayList<Integer> numCube, String status) {
        this.refId = refId;
        this.numCube = numCube;
        this.status = status;
    }

    public String getRefId() {
        return refId;
    }

    public ArrayList<Integer> getNumCube() {
        return numCube;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}
