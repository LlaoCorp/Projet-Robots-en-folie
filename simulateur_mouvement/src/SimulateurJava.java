import javax.swing.*;
import java.awt.*;

public class SimulateurJava extends JFrame {

    private JComboBox<String> cubeSelector;
    private ZonePanel zonePanel;
    private RobotVirtuel robot;

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            SimulateurJava frame = new SimulateurJava();
            frame.setVisible(true);
        });
    }

    public SimulateurJava() {
        robot = new RobotVirtuel();
        zonePanel = new ZonePanel();

        setTitle("Simulateur REF");
        setSize(600, 450);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setLayout(new BorderLayout());

        add(zonePanel, BorderLayout.CENTER);

        String[] cubes = {"Cube 1", "Cube 2", "Cube 3", "Cube 4", "Cube 5"};
        cubeSelector = new JComboBox<>(cubes);
        cubeSelector.setFont(new Font("Arial", Font.PLAIN, 14));

        JButton bouton = new JButton("Aller chercher un cube");
        bouton.setFont(new Font("Arial", Font.BOLD, 16));
        bouton.addActionListener(e -> {
            String selectedCube = (String) cubeSelector.getSelectedItem();
            robot.getApi().envoyerMission(robot.getRefId(), selectedCube);
            this.robotAction(robot);
        });

        JPanel topPanel = new JPanel(new FlowLayout());
        topPanel.add(new JLabel("Choisir un cube :"));
        topPanel.add(cubeSelector);
        topPanel.add(bouton);

        add(topPanel, BorderLayout.NORTH);
    }

    public void robotActionTest(RobotVirtuel robot, String selectedCube) {
        int cible = robot.getPositionFromCube(selectedCube);
        robot.getApi().envoyerAction(robot.getRefId(), "démarre une mission", robot.getPosition());
        robot.getApi().envoyerEtat(robot.getRefId(), robot.getPosition(), robot.hasBox(), "Chercher un cube");

        new Thread(() -> {
            try {
                robot.deplacerVers(cible, zonePanel);
                JOptionPane.showMessageDialog(this, "Cube atteint en position " + cible + " !");
                robot.prendreCube();

                int zoneDepot = robot.getZoneDepotPlusProche();
                robot.deplacerVers(zoneDepot, zonePanel);
                robot.deposerCube();
                JOptionPane.showMessageDialog(this, "Cube déposé en zone " + zoneDepot + " !");

            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }).start();
    }

    public void robotAction(RobotVirtuel robot) {
        new Thread(() -> {
            try {
                robot.executerMission(zonePanel);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }).start();
    }
}
