from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from database import get_db
from deps import get_current_user
from models import Ingredient, Recipe, SavedRecipe, Step, User
from schemas import RecipeCard, RecipeCreate, RecipeDetail, RecipePage

router = APIRouter(prefix="/api/recipes", tags=["recipes"])
me_router = APIRouter(prefix="/me", tags=["me"])


def _with_relations(stmt):
    """selectinload tránh N+1 query — mỗi recipe không phải tự bắn thêm một
    câu SELECT để lấy owner/ingredients/steps của riêng nó."""
    return stmt.options(
        selectinload(Recipe.owner),
        selectinload(Recipe.ingredients),
        selectinload(Recipe.steps),
    )


@router.get("", response_model=RecipePage)
def list_recipes(
    category: str | None = None,
    q: str | None = Query(default=None, description="Tìm theo tên món hoặc theo tag"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=12, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """Danh sách công thức đã đăng, lọc theo danh mục / từ khóa, có phân trang.

    Lọc và phân trang làm ở SQL (WHERE/OFFSET/LIMIT), không tải hết bảng rồi
    lọc bằng Python — cách đó tốn bộ nhớ và chậm dần khi dữ liệu lớn lên."""
    stmt = select(Recipe).where(Recipe.status == "published")

    if category and category != "all":
        stmt = stmt.where(Recipe.category == category)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(or_(Recipe.title.ilike(like), Recipe.tags.ilike(like)))

    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0

    stmt = stmt.order_by(Recipe.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    recipes = db.scalars(_with_relations(stmt)).unique().all()

    return RecipePage(items=recipes, total=total, page=page, page_size=page_size)


@router.get("/{recipe_id}", response_model=RecipeDetail)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    stmt = _with_relations(select(Recipe).where(Recipe.id == recipe_id))
    recipe = db.scalars(stmt).unique().first()
    if recipe is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Không tìm thấy công thức này.")
    return recipe


@router.post("", response_model=RecipeDetail, status_code=status.HTTP_201_CREATED)
def create_recipe(
    payload: RecipeCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Đăng công thức mới. Ingredients/Steps được lưu kèm vị trí (position) để
    giữ đúng thứ tự hiển thị — thứ tự trong JSON gửi lên là thứ tự hiển thị."""
    recipe = Recipe(
        title=payload.title,
        summary=payload.summary,
        notes=payload.notes,
        category=payload.category,
        minutes=payload.minutes,
        servings=payload.servings,
        difficulty=payload.difficulty,
        tags=",".join(t.strip() for t in payload.tags if t.strip()),
        owner_id=user.id,
    )
    recipe.ingredients = [
        Ingredient(position=i, qty=ing.qty, item=ing.item) for i, ing in enumerate(payload.ingredients)
    ]
    recipe.steps = [
        Step(position=i, title=s.title, text=s.text, timer_minutes=s.timer_minutes)
        for i, s in enumerate(payload.steps)
    ]

    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe


@me_router.get("/recipes", response_model=list[RecipeCard])
def my_recipes(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Công thức của chính người dùng đang đăng nhập — bao gồm cả bản draft,
    khác với /api/recipes vốn chỉ trả về những bài đã published."""
    stmt = _with_relations(
        select(Recipe).where(Recipe.owner_id == user.id).order_by(Recipe.created_at.desc())
    )
    return db.scalars(stmt).unique().all()


@me_router.get("/saved", response_model=list[RecipeCard])
def list_saved(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    stmt = _with_relations(
        select(Recipe)
        .join(SavedRecipe, SavedRecipe.recipe_id == Recipe.id)
        .where(SavedRecipe.user_id == user.id)
        .order_by(SavedRecipe.created_at.desc())
    )
    return db.scalars(stmt).unique().all()


@me_router.post("/saved/{recipe_id}", status_code=status.HTTP_201_CREATED)
def save_recipe(recipe_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Nút 'Save recipe' ở trang chi tiết. Bấm lại lần nữa vẫn trả về 201 —
    idempotent — thay vì báo lỗi trùng, vì với người dùng thì bấm Save hai lần
    và Save một lần nên có kết quả giống nhau."""
    if db.get(Recipe, recipe_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Không tìm thấy công thức này.")

    try:
        db.add(SavedRecipe(user_id=user.id, recipe_id=recipe_id))
        db.commit()
    except IntegrityError:
        # Đã lưu từ trước (hoặc một request khác vừa lưu cùng lúc) — ràng buộc
        # unique(user_id, recipe_id) ở database là thứ chặn việc này, không
        # phải một câu `if not exists` viết trước bằng Python.
        db.rollback()

    return {"saved": True}


@me_router.delete("/saved/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def unsave_recipe(recipe_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.scalar(
        select(SavedRecipe).where(SavedRecipe.user_id == user.id, SavedRecipe.recipe_id == recipe_id)
    )
    if row:
        db.delete(row)
        db.commit()
    return None
