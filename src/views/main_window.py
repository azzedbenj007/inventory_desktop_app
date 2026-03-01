"""
MainWindow — the application's primary window.

Layout
------
  ┌─ Toolbar ────────────────────────────────────────────────────┐
  │  [+ Ajouter]  [✎ Modifier]  [✕ Supprimer]  [Search...]       │
  ├──────────────────────────────────────────────────────────────┤
  │                                                              │
  │   QTableWidget  (list of products)                           │
  │                                                              │
  ├──────────────────────────────────────────────────────────────┤
  │  Status bar                                                  │
  └──────────────────────────────────────────────────────────────┘
"""
from __future__ import annotations

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from src.controllers.inventory_controller import InventoryController
from src.models.product import Product
from src.views.product_form import ProductFormDialog


# Colours used for low-stock highlighting
_LOW_STOCK_BG = QColor("#FFDDC1")
_LOW_STOCK_FG = QColor("#8B2000")


class MainWindow(QMainWindow):
    """Application main window (MVC — View layer)."""

    COLUMNS = ["ID", "Nom", "Référence", "Catégorie", "Quantité", "Prix (€)", "Seuil alerte"]

    def __init__(self, controller: InventoryController) -> None:
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Gestion de Stock — Inventaire")
        self.resize(1100, 650)
        self._build_ui()
        self._load_products()

    # ------------------------------------------------------------------ #
    #  UI construction                                                     #
    # ------------------------------------------------------------------ #

    def _build_ui(self) -> None:
        # Central widget & root layout
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setSpacing(0)
        root.setContentsMargins(0, 0, 0, 0)

        # --- Toolbar ---
        toolbar = self._build_toolbar()
        root.addWidget(toolbar)

        # --- Search bar ---
        search_row = QHBoxLayout()
        search_row.setContentsMargins(8, 6, 8, 6)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher par nom ou référence…")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.textChanged.connect(self._on_search)
        search_row.addWidget(QLabel("Recherche :"))
        search_row.addWidget(self.search_input)
        root.addLayout(search_row)

        # --- Table ---
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.COLUMNS))
        self.table.setHorizontalHeaderLabels(self.COLUMNS)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setVisible(False)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Nom column
        self.table.doubleClicked.connect(self._on_edit)
        root.addWidget(self.table)

        # --- Status bar ---
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def _build_toolbar(self) -> QToolBar:
        toolbar = QToolBar("Actions")
        toolbar.setMovable(False)

        btn_add = QPushButton("＋  Ajouter")
        btn_add.setToolTip("Ajouter un nouveau produit (Ctrl+N)")
        btn_add.setShortcut("Ctrl+N")
        btn_add.clicked.connect(self._on_add)
        toolbar.addWidget(btn_add)

        toolbar.addSeparator()

        btn_edit = QPushButton("✎  Modifier")
        btn_edit.setToolTip("Modifier le produit sélectionné (Ctrl+E)")
        btn_edit.setShortcut("Ctrl+E")
        btn_edit.clicked.connect(self._on_edit)
        toolbar.addWidget(btn_edit)

        toolbar.addSeparator()

        btn_delete = QPushButton("✕  Supprimer")
        btn_delete.setToolTip("Supprimer le produit sélectionné (Del)")
        btn_delete.setShortcut("Del")
        btn_delete.clicked.connect(self._on_delete)
        toolbar.addWidget(btn_delete)

        toolbar.addSeparator()

        btn_refresh = QPushButton("↻  Actualiser")
        btn_refresh.setToolTip("Recharger la liste (F5)")
        btn_refresh.setShortcut("F5")
        btn_refresh.clicked.connect(self._load_products)
        toolbar.addWidget(btn_refresh)

        # Low-stock filter toggle
        toolbar.addSeparator()
        self.btn_low_stock = QPushButton("⚠  Stock faible")
        self.btn_low_stock.setToolTip("Afficher uniquement les produits en stock faible")
        self.btn_low_stock.setCheckable(True)
        self.btn_low_stock.toggled.connect(self._load_products)
        toolbar.addWidget(self.btn_low_stock)

        return toolbar

    # ------------------------------------------------------------------ #
    #  Data loading                                                        #
    # ------------------------------------------------------------------ #

    def _load_products(self) -> None:
        """Fetch products from the controller and populate the table."""
        search_text = self.search_input.text().strip() if hasattr(self, "search_input") else ""
        low_stock_only = self.btn_low_stock.isChecked() if hasattr(self, "btn_low_stock") else False

        if low_stock_only:
            products = self.controller.get_low_stock_products()
        elif search_text:
            products = self.controller.search_products(search_text)
        else:
            products = self.controller.get_all_products()

        self._populate_table(products)
        self._update_status(products)

    def _populate_table(self, products: list[Product]) -> None:
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)

        for row_idx, product in enumerate(products):
            self.table.insertRow(row_idx)
            values = [
                str(product.id),
                product.nom,
                product.reference,
                product.category.nom if product.category else "—",
                str(product.quantite),
                f"{product.prix:.2f}",
                str(product.seuil_alerte),
            ]
            for col_idx, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                # Numeric columns — right-align
                if col_idx in (0, 4, 5, 6):
                    item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
                # Store the product id on the first column for retrieval
                if col_idx == 0:
                    item.setData(Qt.ItemDataRole.UserRole, product.id)
                # Highlight low-stock rows
                if product.is_low_stock:
                    item.setBackground(_LOW_STOCK_BG)
                    item.setForeground(_LOW_STOCK_FG)
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)
                self.table.setItem(row_idx, col_idx, item)

        self.table.setSortingEnabled(True)
        self.table.resizeColumnsToContents()

    def _update_status(self, products: list[Product]) -> None:
        low = sum(1 for p in products if p.is_low_stock)
        msg = f"{len(products)} produit(s) affiché(s)"
        if low:
            msg += f"  |  ⚠ {low} en stock faible"
        self.status_bar.showMessage(msg)

    # ------------------------------------------------------------------ #
    #  Event handlers                                                      #
    # ------------------------------------------------------------------ #

    def _get_selected_product_id(self) -> int | None:
        selected = self.table.selectedItems()
        if not selected:
            return None
        row = self.table.currentRow()
        id_item = self.table.item(row, 0)
        return id_item.data(Qt.ItemDataRole.UserRole) if id_item else None

    def _on_search(self) -> None:
        # Debounce: wait 300 ms before refreshing to avoid hammering the DB
        if not hasattr(self, "_search_timer"):
            self._search_timer = QTimer(self)
            self._search_timer.setSingleShot(True)
            self._search_timer.timeout.connect(self._load_products)
        self._search_timer.start(300)

    def _on_add(self) -> None:
        dialog = ProductFormDialog(parent=self)
        if dialog.exec() == ProductFormDialog.DialogCode.Accepted:
            data = dialog.get_data()
            try:
                self.controller.add_product(**data)
                self._load_products()
                self.status_bar.showMessage("Produit ajouté avec succès.", 3000)
            except ValueError as exc:
                QMessageBox.warning(self, "Erreur", str(exc))

    def _on_edit(self) -> None:
        product_id = self._get_selected_product_id()
        if product_id is None:
            QMessageBox.information(self, "Sélection requise", "Veuillez sélectionner un produit.")
            return
        product = self.controller.get_product_by_id(product_id)
        if product is None:
            QMessageBox.warning(self, "Erreur", "Produit introuvable.")
            return

        dialog = ProductFormDialog(parent=self, product=product)
        if dialog.exec() == ProductFormDialog.DialogCode.Accepted:
            data = dialog.get_data()
            try:
                self.controller.update_product(product_id=product_id, **data)
                self._load_products()
                self.status_bar.showMessage("Produit mis à jour avec succès.", 3000)
            except ValueError as exc:
                QMessageBox.warning(self, "Erreur", str(exc))

    def _on_delete(self) -> None:
        product_id = self._get_selected_product_id()
        if product_id is None:
            QMessageBox.information(self, "Sélection requise", "Veuillez sélectionner un produit.")
            return

        confirm = QMessageBox.question(
            self,
            "Confirmer la suppression",
            "Voulez-vous vraiment supprimer ce produit ? Cette action est irréversible.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                self.controller.delete_product(product_id)
                self._load_products()
                self.status_bar.showMessage("Produit supprimé.", 3000)
            except ValueError as exc:
                QMessageBox.warning(self, "Erreur", str(exc))
