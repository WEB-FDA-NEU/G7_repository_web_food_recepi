"""
Hình dạng JSON đi vào và đi ra.

QUY TẮC: field ở đây phải khớp với những gì frontend/js/render.js và
frontend/mock/*.json mong đợi. Sai một tên trường là frontend vỡ.

VÌ SAO TÁCH KHỎI models.py: bảng users có cột password_hash, nhưng JSON trả ra
internet KHÔNG được có nó. Model nằm trong DB, schema đi ra ngoài.
"""
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator

Category = Literal["breakfast", "mains", "salads", "soups", "baking", "desserts"]
Difficulty = Literal["Easy", "Medium", "Hard"]


# ══════════ Nguyên liệu & các bước — con của Recipe ══════════

class IngredientOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    qty: str
    item: str


class IngredientIn(BaseModel):
    qty: str = Field(min_length=1, max_length=40)
    item: str = Field(min_length=1, max_length=160)


class StepOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    text: str
    timer_minutes: int | None = None


class StepIn(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    text: str = Field(min_length=1)
    timer_minutes: int | None = Field(default=None, ge=1, le=600)


# ══════════ Recipe — thực thể chính ══════════

class RecipeCard(BaseModel):
    """Dữ liệu hiển thị trên một thẻ trong danh sách (trang chủ, trang browse)."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    category: Category
    minutes: int
    servings: int
    difficulty: Difficulty
    cover_url: str
    summary: str
    tags: list[str]
    rating: float
    rating_count: int
    owner_name: str
    created_at: datetime

    # DB lưu tags dạng "a,b,c" (xem models.Recipe.tags) — tách thành list ở đây
    # thay vì thêm bảng many-to-many, đủ dùng cho quy mô đồ án.
    @field_validator("tags", mode="before")
    @classmethod
    def split_tags(cls, v):
        if isinstance(v, str):
            return [t for t in v.split(",") if t]
        return v


class RecipeDetail(RecipeCard):
    """Thẻ + các trường chỉ có ở trang chi tiết."""
    notes: str
    ingredients: list[IngredientOut]
    steps: list[StepOut]


class RecipePage(BaseModel):
    """Quy ước phân trang thống nhất cả lớp."""
    items: list[RecipeCard]
    total: int
    page: int
    page_size: int


class RecipeCreate(BaseModel):
    # Ràng buộc tối thiểu để demo — đổi/thêm theo Business Rules thật của đề tài
    # nếu nhóm có quy định riêng (vd. giá, số bước tối thiểu...).
    title: str = Field(min_length=6, max_length=160)
    summary: str = Field(min_length=20)
    category: Category
    minutes: int = Field(ge=1, le=600)
    servings: int = Field(ge=1, le=50)
    difficulty: Difficulty = "Easy"
    tags: list[str] = Field(default_factory=list)
    notes: str = ""
    ingredients: list[IngredientIn] = Field(min_length=1)
    steps: list[StepIn] = Field(min_length=1)


# ══════════ Tài khoản — dùng chung mọi đề tài, ít khi phải sửa ══════════

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    display_name: str
    role: str


class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    display_name: str = Field(min_length=2, max_length=80)
    phone: str = ""


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
