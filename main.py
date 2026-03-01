"""
main.py — point d'entrée de l'application Gestion de Stock.

Usage:
    python main.py

Ordre d'initialisation :
    1. Création des tables SQLite (si elles n'existent pas)
    2. Instanciation du contrôleur
    3. Instanciation de la vue principale
    4. Démarrage de la boucle d'événements PyQt6
"""
import sys

from PyQt6.QtWidgets import QApplication

from src.models.database import init_db
from src.controllers.inventory_controller import InventoryController
from src.views.main_window import MainWindow


def main() -> None:
    # --- 1. Initialise la base de données (crée le fichier SQLite + tables) ---
    init_db()

    # --- 2. Lance l'application Qt ---
    app = QApplication(sys.argv)
    app.setApplicationName("Gestion de Stock")
    app.setOrganizationName("MonEntreprise")

    # Feuille de style globale minimaliste
    app.setStyleSheet("""
        QMainWindow {
            background-color: #F5F5F5;
        }
        QToolBar {
            background-color: #2C3E50;
            spacing: 6px;
            padding: 4px;
        }
        QToolBar QPushButton {
            background-color: #3498DB;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 6px 12px;
            font-size: 13px;
        }
        QToolBar QPushButton:hover {
            background-color: #2980B9;
        }
        QToolBar QPushButton:checked {
            background-color: #E67E22;
        }
        QTableWidget {
            gridline-color: #DCDCDC;
            font-size: 13px;
        }
        QTableWidget QHeaderView::section {
            background-color: #2C3E50;
            color: white;
            padding: 6px;
            font-weight: bold;
            border: none;
        }
        QTableWidget::item:selected {
            background-color: #AED6F1;
            color: #1A252F;
        }
        QStatusBar {
            background-color: #ECF0F1;
            font-size: 12px;
        }
        QLineEdit {
            border: 1px solid #BDC3C7;
            border-radius: 4px;
            padding: 4px 8px;
            font-size: 13px;
        }
        QLineEdit:focus {
            border-color: #3498DB;
        }
        QPushButton {
            padding: 5px 10px;
        }
    """)

    # --- 3. Instancie le contrôleur et la fenêtre principale ---
    controller = InventoryController()
    window = MainWindow(controller=controller)
    window.show()

    # --- 4. Boucle d'événements ---
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
