"""
ProductFormDialog — modal dialog for creating or editing a product.
"""
from __future__ import annotations

from typing import Optional

from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QSpinBox,
    QVBoxLayout,
)

from src.models.product import Product


class ProductFormDialog(QDialog):
    """
    Reusable form dialog.
    Pass `product` to pre-fill fields (edit mode); omit it for creation mode.
    """

    def __init__(self, parent=None, product: Optional[Product] = None):
        super().__init__(parent)
        self._product = product
        self.setWindowTitle("Modifier le produit" if product else "Ajouter un produit")
        self.setMinimumWidth(400)
        self._build_ui()
        if product:
            self._populate(product)

    # ------------------------------------------------------------------ #
    #  UI construction                                                     #
    # ------------------------------------------------------------------ #

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        form = QFormLayout()
        form.setSpacing(10)

        self.nom_input = QLineEdit()
        self.nom_input.setPlaceholderText("Ex. : Ordinateur portable")
        form.addRow(QLabel("Nom *"), self.nom_input)

        self.ref_input = QLineEdit()
        self.ref_input.setPlaceholderText("Ex. : REF-001")
        form.addRow(QLabel("Référence *"), self.ref_input)

        self.qty_input = QSpinBox()
        self.qty_input.setRange(0, 999_999)
        form.addRow(QLabel("Quantité *"), self.qty_input)

        self.prix_input = QDoubleSpinBox()
        self.prix_input.setRange(0.0, 10_000_000.0)
        self.prix_input.setDecimals(2)
        self.prix_input.setSuffix(" €")
        form.addRow(QLabel("Prix *"), self.prix_input)

        self.seuil_input = QSpinBox()
        self.seuil_input.setRange(0, 999_999)
        self.seuil_input.setValue(5)
        form.addRow(QLabel("Seuil d'alerte"), self.seuil_input)

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Ex. : Informatique (optionnel)")
        form.addRow(QLabel("Catégorie"), self.category_input)

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    # ------------------------------------------------------------------ #
    #  Pre-fill for edit mode                                              #
    # ------------------------------------------------------------------ #

    def _populate(self, product: Product) -> None:
        self.nom_input.setText(product.nom)
        self.ref_input.setText(product.reference)
        self.qty_input.setValue(product.quantite)
        self.prix_input.setValue(product.prix)
        self.seuil_input.setValue(product.seuil_alerte)
        if product.category:
            self.category_input.setText(product.category.nom)

    # ------------------------------------------------------------------ #
    #  Validation                                                          #
    # ------------------------------------------------------------------ #

    def _validate_and_accept(self) -> None:
        if not self.nom_input.text().strip():
            QMessageBox.warning(self, "Champ requis", "Le nom est obligatoire.")
            return
        if not self.ref_input.text().strip():
            QMessageBox.warning(self, "Champ requis", "La référence est obligatoire.")
            return
        self.accept()

    # ------------------------------------------------------------------ #
    #  Data extraction                                                     #
    # ------------------------------------------------------------------ #

    def get_data(self) -> dict:
        """Return form values as a plain dict, ready for the controller."""
        return {
            "nom": self.nom_input.text().strip(),
            "reference": self.ref_input.text().strip(),
            "quantite": self.qty_input.value(),
            "prix": self.prix_input.value(),
            "seuil_alerte": self.seuil_input.value(),
            "category_nom": self.category_input.text().strip() or None,
        }
