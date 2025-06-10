import javax.swing.*;
import java.awt.*;

class ZonePanel extends JPanel {
    private static final int NB_ZONES = 8;
    private static final int RAYON_ZONE = 60;
    private static final int MARGE = 40;

    private int positionRobot = 0;

    public void setPositionRobot(int pos) {
        this.positionRobot = pos;
        repaint();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

        int startX = (getWidth() - (4 * (RAYON_ZONE + MARGE))) / 2;
        int startY = (getHeight() - (2 * (RAYON_ZONE + MARGE))) / 2;

        for (int i = 0; i < NB_ZONES; i++) {
            int row = i / 4;
            int col = i % 4;

            int x = startX + col * (RAYON_ZONE + MARGE);
            int y = startY + row * (RAYON_ZONE + MARGE);

            if (i == positionRobot) {
                g2.setColor(Color.GREEN);
            } else if (i == 3 || i == 6) {
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
            case 0 -> "Départ";
            case 1 -> "Cube 1";
            case 2 -> "Cube 2";
            case 4 -> "Cube 3";
            case 5 -> "Cube 4";
            case 7 -> "Cube 5";
            default -> "Zone de dépôt";
        };
        return label;
    }
}