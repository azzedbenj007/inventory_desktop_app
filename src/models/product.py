"""
SQLAlchemy ORM models: Category and Product.
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.models.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), nullable=False, unique=True)

    products = relationship(
        "Product",
        back_populates="category",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Category id={self.id} nom={self.nom!r}>"


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(200), nullable=False)
    reference = Column(String(100), nullable=False, unique=True)
    quantite = Column(Integer, nullable=False, default=0)
    prix = Column(Float, nullable=False, default=0.0)
    seuil_alerte = Column(Integer, nullable=False, default=5)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    category = relationship("Category", back_populates="products")

    @property
    def is_low_stock(self) -> bool:
        return self.quantite <= self.seuil_alerte

    def __repr__(self) -> str:
        return (
            f"<Product id={self.id} ref={self.reference!r} "
            f"nom={self.nom!r} qty={self.quantite}>"
        )
