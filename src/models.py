"""
Bảng trong database.

Thực thể chính của đề tài này là Recipe (công thức nấu ăn), thay cho Item
trong bản mẫu gốc. Mọi router đều import từ đây.
"""

from datetime import UTC, datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


def utcnow() -> datetime:
    return datetime.now(UTC)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    # unique=True là thứ THẬT SỰ chặn email trùng khi 2 request đến cùng lúc.
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    display_name: Mapped[str] = mapped_column(String(80))
    phone: Mapped[str] = mapped_column(String(20), default="")
    role: Mapped[str] = mapped_column(String(20), default="user")  # user | admin
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )

    recipes: Mapped[list["Recipe"]] = relationship(back_populates="owner")
    saved: Mapped[list["SavedRecipe"]] = relationship(back_populates="user")


class Recipe(Base):
    __tablename__ = "recipes"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(160), index=True)
    summary: Mapped[str] = mapped_column(Text, default="")
    notes: Mapped[str] = mapped_column(Text, default="")

    # Danh mục khớp với CATEGORIES trong frontend/js/config.js — nếu thêm danh
    # mục mới thì sửa cả hai chỗ, và sửa Literal[...] trong schemas.RecipeCreate.
    category: Mapped[str] = mapped_column(String(20), index=True)
    minutes: Mapped[int] = mapped_column(Integer, default=0)
    servings: Mapped[int] = mapped_column(Integer, default=4)
    difficulty: Mapped[str] = mapped_column(
        String(20), default="Easy"
    )  # Easy | Medium | Hard

    # Lưu tags dạng "a,b,c" cho đơn giản thay vì bảng many-to-many riêng.
    # Đủ dùng cho quy mô đồ án; chuyển sang bảng Tag riêng nếu cần lọc phức tạp hơn.
    tags: Mapped[str] = mapped_column(String(200), default="")

    cover_url: Mapped[str] = mapped_column(String(255), default="")

    rating: Mapped[float] = mapped_column(Float, default=0)
    rating_count: Mapped[int] = mapped_column(Integer, default=0)

    # draft | published — cho phép người dùng lưu nháp trước khi đăng.
    status: Mapped[str] = mapped_column(String(20), default="published", index=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, index=True
    )
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner: Mapped["User"] = relationship(back_populates="recipes")
    ingredients: Mapped[list["Ingredient"]] = relationship(
        back_populates="recipe",
        order_by="Ingredient.position",
        cascade="all, delete-orphan",
    )
    steps: Mapped[list["Step"]] = relationship(
        back_populates="recipe", order_by="Step.position", cascade="all, delete-orphan"
    )

    @property
    def owner_name(self) -> str:
        """Tiện cho schemas.RecipeCard hiển thị tên tác giả mà không cần JOIN thủ công."""
        return self.owner.display_name if self.owner else ""


class Ingredient(Base):
    """Một dòng nguyên liệu. Tách bảng riêng (thay vì nhét JSON vào Recipe) để
    giữ đúng nguyên tắc chuẩn hóa — và để sau này có thể lọc/tính toán theo
    từng nguyên liệu nếu đề tài mở rộng (vd. tính calo)."""

    __tablename__ = "ingredients"
    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"))
    position: Mapped[int] = mapped_column(
        Integer, default=0
    )  # giữ đúng thứ tự hiển thị
    qty: Mapped[str] = mapped_column(String(40))
    item: Mapped[str] = mapped_column(String(160))

    recipe: Mapped["Recipe"] = relationship(back_populates="ingredients")


class Step(Base):
    """Một bước trong công thức."""

    __tablename__ = "steps"
    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"))
    position: Mapped[int] = mapped_column(Integer, default=0)
    title: Mapped[str] = mapped_column(String(80))
    text: Mapped[str] = mapped_column(Text)
    timer_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)

    recipe: Mapped["Recipe"] = relationship(back_populates="steps")


class SavedRecipe(Base):
    """Người dùng lưu (bookmark) một công thức — nút 'Save recipe' ở frontend.

    Ràng buộc chống lưu trùng PHẢI đặt ở database (UniqueConstraint dưới đây),
    không phải câu if trong Python: nếu người dùng bấm nút Save hai lần liền
    (double-click, mất mạng rồi bấm lại...), hai request có thể đến gần như
    cùng lúc và cả hai đều vượt qua một câu `if not exists` viết bằng Python.
    """

    __tablename__ = "saved_recipes"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )

    user: Mapped["User"] = relationship(back_populates="saved")
    recipe: Mapped["Recipe"] = relationship()

    __table_args__ = (UniqueConstraint("user_id", "recipe_id", name="uq_saved_recipe"),)
