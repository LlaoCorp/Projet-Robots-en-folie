public class RobotVirtuel {
    protected String uuid;
    protected int x,y;
    protected String etat;
    protected String objectif;

    public RobotVirtuel(String uuid, int x, int y, String etat, String objectif) {
        this.uuid = uuid;
        this.x = x;
        this.y = y;
        this.etat = etat;
        this.objectif = objectif;
    }

    public void deplacerVers(int cibleX, int cibleY) {
    }

    public <JSONObject> JSONObject genererMessageEtat(){
        return null;
    }

    public boolean estMissionTerminee(){
        return false;
    }
}
