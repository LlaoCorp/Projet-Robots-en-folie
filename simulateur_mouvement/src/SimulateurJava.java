/**
 * @file SimulateurJava.java
 * @brief Interface graphique principale du simulateur de robot virtuel.
 */

import javax.swing.*;
import java.awt.*;

/**
 * Classe représentant l'interface graphique du simulateur de robot.
 * Elle permet de démarrer la simulation et d’afficher les logs des actions.
 */
public class SimulateurJava extends JFrame {

    private JTextArea logArea;
    private ZonePanel zonePanel;
    private RobotVirtuel robot;

    /**
     * Point d’entrée principal de l’application.
     * @param args arguments de ligne de commande
     */
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            SimulateurJava frame = new SimulateurJava();
            frame.setVisible(true);
        });
    }

    /**
     * Constructeur : initialise les composants graphiques.
     */
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

        JButton bouton = new JButton("Commencer");
        bouton.setFont(new Font("Arial", Font.BOLD, 16));
        bouton.addActionListener(e -> this.robotAction(robot));

        JPanel topPanel = new JPanel(new FlowLayout());
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

    /**
     * Lance l’exécution de la mission du robot dans un thread.
     * @param robot le robot à utiliser
     */
    public void robotAction(RobotVirtuel robot) {
        new Thread(() -> {
            try {
                robot.executerInstruction(zonePanel);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }).start();
    }

    /**
     * Ajoute un message à la zone de log.
     * @param texte texte à afficher
     */
    public void ajouterInstruction(String texte) {
        SwingUtilities.invokeLater(() -> {
            logArea.append(texte + "\n");
            logArea.setCaretPosition(logArea.getDocument().getLength());
        });
    }
}
