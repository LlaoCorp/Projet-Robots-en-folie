import javax.swing.*;
import java.awt.*;
import java.util.ArrayList;

public class SimulateurJava extends JFrame {

    private JComboBox<String> cubeSelector;
    private JTextArea logArea;
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

        robot.setSimulateur(this);

        setTitle("Simulateur REF");
        setSize(600, 450);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setLayout(new BorderLayout());

        add(zonePanel, BorderLayout.CENTER);

        Integer[] cubes = {1, 2, 3, 4, 5};
        JComboBox<Integer> cubeSelector = new JComboBox<>(cubes);
        cubeSelector.setFont(new Font("Arial", Font.PLAIN, 14));

        JButton bouton = new JButton("Aller chercher un cube");
        bouton.setFont(new Font("Arial", Font.BOLD, 16));
        bouton.addActionListener(e -> {
            Integer selectedCube = (Integer) cubeSelector.getSelectedItem();
            ArrayList<Integer> blocks = new ArrayList<>();
            blocks.add(selectedCube);
            robot.getApi().envoyerInstruction(robot.getRefId(), blocks);
            this.robotAction(robot);
        });

        JPanel topPanel = new JPanel(new FlowLayout());
        topPanel.add(new JLabel("Choisir un cube :"));
        topPanel.add(cubeSelector);
        topPanel.add(bouton);

        add(topPanel, BorderLayout.NORTH);

        logArea = new JTextArea(15, 20);
        logArea.setEditable(false);
        JScrollPane scrollPane = new JScrollPane(logArea);

        JPanel rightPanel = new JPanel(new BorderLayout());
        rightPanel.setBorder(BorderFactory.createTitledBorder("Instructions du robot"));
        rightPanel.add(scrollPane, BorderLayout.CENTER);

        add(rightPanel, BorderLayout.EAST);

    }

    public void robotActionTest(RobotVirtuel robot, String selectedCube) {
        int cible = robot.getPositionFromCube(selectedCube);
//        robot.getApi().envoyerAction(robot.getRefId(), "démarre une mission", robot.getPosition());
//        robot.getApi().envoyerEtat(robot.getRefId(), robot.getPosition(), robot.hasBox(), "Chercher un cube");

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
                robot.executerInstruction(zonePanel);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }).start();
    }

    public void ajouterInstruction(String texte) {
        SwingUtilities.invokeLater(() -> {
            logArea.append(texte + "\n");
            logArea.setCaretPosition(logArea.getDocument().getLength());
        });
    }
}
