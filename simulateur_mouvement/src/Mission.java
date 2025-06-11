public class Mission {
    private String refId;
    private String numCube;
    private String statut;

    public Mission(String refId, String numCube, String statut) {
        this.refId = refId;
        this.numCube = numCube;
        this.statut = statut;
    }

    public String getRefId() {
        return refId;
    }

    public String getNumCube() {
        return numCube;
    }

    public String getStatut() {
        return statut;
    }

    public void setStatut(String statut) {
        this.statut = statut;
    }
}
