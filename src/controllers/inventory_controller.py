"""
InventoryController — business logic layer between the DB and the UI.

All public methods open their own session via the get_session() context manager
so that sessions are always properly closed, preventing SQLite lock issues.
"""
from __future__ import annotations

from contextlib import contextmanager
from typing import Optional

from src.models.database import get_session
from src.models.product import Category, Product


class InventoryController:
    """CRUD operations for Product and Category entities."""

    # ------------------------------------------------------------------ #
    #  Internal helpers                                                    #
    # ------------------------------------------------------------------ #

    @contextmanager
    def _session(self):
        """Thin wrapper so controller methods can write `with self._session() as s:`."""
        yield from get_session()

    # ------------------------------------------------------------------ #
    #  Category methods                                                    #
    # ------------------------------------------------------------------ #

    def get_all_categories(self) -> list[Category]:
        with self._session() as session:
            return session.query(Category).order_by(Category.nom).all()

    def get_or_create_category(self, nom: str) -> Category:
        with self._session() as session:
            cat = session.query(Category).filter_by(nom=nom.strip()).first()
            if cat is None:
                cat = Category(nom=nom.strip())
                session.add(cat)
                session.flush()   # get the auto-generated id
            return cat

    # ------------------------------------------------------------------ #
    #  Product — Read                                                      #
    # ------------------------------------------------------------------ #

    def get_all_products(self) -> list[Product]:
        """Return all products, eager-loading their category."""
        with self._session() as session:
            return (
                session.query(Product)
                .order_by(Product.nom)
                .all()
            )

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        with self._session() as session:
            return session.get(Product, product_id)

    def search_products(self, query: str) -> list[Product]:
        """Case-insensitive search on nom or reference."""
        q = f"%{query.strip()}%"
        with self._session() as session:
            return (
                session.query(Product)
                .filter(
                    Product.nom.ilike(q) | Product.reference.ilike(q)
                )
                .order_by(Product.nom)
                .all()
            )

    def get_low_stock_products(self) -> list[Product]:
        """Return products whose quantity is at or below their alert threshold."""
        with self._session() as session:
            return (
                session.query(Product)
                .filter(Product.quantite <= Product.seuil_alerte)
                .order_by(Product.nom)
                .all()
            )

    # ------------------------------------------------------------------ #
    #  Product — Create                                                    #
    # ------------------------------------------------------------------ #

    def add_product(
        self,
        nom: str,
        reference: str,
        quantite: int,
        prix: float,
        seuil_alerte: int,
        category_nom: Optional[str] = None,
    ) -> Product:
        """
        Create and persist a new product.

        Raises:
            ValueError: if the reference already exists.
        """
        with self._session() as session:
            existing = session.query(Product).filter_by(reference=reference.strip()).first()
            if existing is not None:
                raise ValueError(f"Un produit avec la référence '{reference}' existe déjà.")

            category = None
            if category_nom and category_nom.strip():
                category = session.query(Category).filter_by(nom=category_nom.strip()).first()
                if category is None:
                    category = Category(nom=category_nom.strip())
                    session.add(category)
                    session.flush()

            product = Product(
                nom=nom.strip(),
                reference=reference.strip(),
                quantite=int(quantite),
                prix=float(prix),
                seuil_alerte=int(seuil_alerte),
                category_id=category.id if category else None,
            )
            session.add(product)
            session.flush()
            return product

    # ------------------------------------------------------------------ #
    #  Product — Update                                                    #
    # ------------------------------------------------------------------ #

    def update_product(
        self,
        product_id: int,
        nom: Optional[str] = None,
        reference: Optional[str] = None,
        quantite: Optional[int] = None,
        prix: Optional[float] = None,
        seuil_alerte: Optional[int] = None,
        category_nom: Optional[str] = None,
    ) -> Product:
        """
        Update an existing product by its id.

        Raises:
            ValueError: if no product is found for the given id.
        """
        with self._session() as session:
            product = session.get(Product, product_id)
            if product is None:
                raise ValueError(f"Aucun produit trouvé avec l'id {product_id}.")

            if nom is not None:
                product.nom = nom.strip()
            if reference is not None:
                product.reference = reference.strip()
            if quantite is not None:
                product.quantite = int(quantite)
            if prix is not None:
                product.prix = float(prix)
            if seuil_alerte is not None:
                product.seuil_alerte = int(seuil_alerte)
            if category_nom is not None:
                if category_nom.strip() == "":
                    product.category_id = None
                else:
                    cat = session.query(Category).filter_by(nom=category_nom.strip()).first()
                    if cat is None:
                        cat = Category(nom=category_nom.strip())
                        session.add(cat)
                        session.flush()
                    product.category_id = cat.id

            return product

    # ------------------------------------------------------------------ #
    #  Product — Delete                                                    #
    # ------------------------------------------------------------------ #

    def delete_product(self, product_id: int) -> None:
        """
        Delete a product by its id.

        Raises:
            ValueError: if no product is found for the given id.
        """
        with self._session() as session:
            product = session.get(Product, product_id)
            if product is None:
                raise ValueError(f"Aucun produit trouvé avec l'id {product_id}.")
            session.delete(product)
