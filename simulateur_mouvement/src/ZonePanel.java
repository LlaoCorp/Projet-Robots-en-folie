import javax.swing.*;
import java.awt.*;

class ZonePanel extends JPanel {
    private static final int NB_ZONES = 10;
    private static final int NB_COLONNES = 5;
    private static final int NB_LIGNES = 2;
    private static final int RAYON_ZONE = 50;
    private static final int MARGE = 40;

    private int positionRobot = 1;

    public void setPositionRobot(int pos) {
        this.positionRobot = pos;
        repaint();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

        int startX = (getWidth() - (NB_COLONNES * (RAYON_ZONE + MARGE))) / 2;
        int startY = (getHeight() - (NB_LIGNES * (RAYON_ZONE + MARGE))) / 2;

        for (int i = 1; i <= NB_ZONES; i++) {
            int index = i-1;
            int row = index / NB_COLONNES;
            int col = index % NB_COLONNES;

            int x = startX + col * (RAYON_ZONE + MARGE);
            int y = startY + row * (RAYON_ZONE + MARGE);

            if (i == positionRobot) {
                g2.setColor(Color.GREEN);
            } else if (i == 4 || i == 5 || i == 8 || i == 9) {
                g2.setColor(new Color(173, 216, 230));
            } else {
                g2.setColor(Color.LIGHT_GRAY); // Zone vide
            }

            g2.fillOval(x, y, RAYON_ZONE, RAYON_ZONE);
            g2.setColor(Color.LIGHT_GRAY);
            g2.setColor(Color.BLACK);
            g2.drawOval(x, y, RAYON_ZONE, RAYON_ZONE);

            String num = String.valueOf(i);
            FontMetrics fm = g2.getFontMetrics();
            int tx = x + (RAYON_ZONE - fm.stringWidth(num)) / 2;
            int ty = y + ((RAYON_ZONE - fm.getHeight()) / 2) + fm.getAscent();
            g2.drawString(num, tx, ty);

            String label = getLabel(i);
            int labelY = y + RAYON_ZONE + 15;
            int labelX = x + (RAYON_ZONE - fm.stringWidth(label)) / 2;
            g2.drawString(label, labelX, labelY);
        }
    }

    private String getLabel(int position){
        String label = switch (position) {
            case 1 -> "Départ";
            case 2 -> "Cube Jaune";
            case 3 -> "Cube Rouge";
            case 4 -> "Entrée Dépôt 1";
            case 5 -> "Sortie Dépôt 1";
            case 6 -> "Cube Rose";
            case 7 -> "Cube Violet";
            case 8 -> "Entrée Dépôt 2";
            case 9 -> "Sortie Dépôt 2";
            case 10 -> "Cube Vert";
            default -> "Zone vide";
        };
        return label;
    }
}