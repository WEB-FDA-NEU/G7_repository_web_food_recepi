from fastapi import APIRouter, Depends, HTTPException, Response, status
from pathlib import Path

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session, joinedload, selectinload

from ..database import engine, get_db
from ..deps import get_admin
from ..models import Recipe, RecipeReview, SavedRecipe, User
from ..schemas import AdminReviewOut, AdminUserOut, RecipeCard

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/stats")
def get_stats(
    _: User = Depends(get_admin),
    db: Session = Depends(get_db),
):
    """Return admin dashboard counts and the current SQLite file size."""
    user_count = db.scalar(select(func.count()).select_from(User)) or 0
    database_size_bytes = None
    if engine.dialect.name == "sqlite":
        database_path = engine.url.database
        if database_path and database_path != ":memory:":
            try:
                database_size_bytes = Path(database_path).stat().st_size
            except OSError:
                pass
    return {
        "user_count": user_count,
        "database_size_bytes": database_size_bytes,
    }


@router.get("/users", response_model=list[AdminUserOut])
def list_users(
    _: User = Depends(get_admin),
    db: Session = Depends(get_db),
):
    return db.scalars(select(User).order_by(User.created_at.desc())).all()


@router.get("/recipes", response_model=list[RecipeCard])
def list_recipes(_: User = Depends(get_admin), db: Session = Depends(get_db)):
    return db.scalars(
        select(Recipe).options(selectinload(Recipe.owner)).order_by(Recipe.created_at.desc())
    ).all()


@router.delete("/recipes/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(
    recipe_id: int,
    _: User = Depends(get_admin),
    db: Session = Depends(get_db),
):
    recipe = db.get(Recipe, recipe_id)
    if recipe is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "We couldn't find that recipe.")
    db.execute(delete(SavedRecipe).where(SavedRecipe.recipe_id == recipe_id))
    db.delete(recipe)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/comments", response_model=list[AdminReviewOut])
def list_comments(_: User = Depends(get_admin), db: Session = Depends(get_db)):
    return db.scalars(
        select(RecipeReview)
        .options(joinedload(RecipeReview.user), joinedload(RecipeReview.recipe))
        .order_by(RecipeReview.created_at.desc())
    ).all()


@router.delete("/comments/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    review_id: int,
    _: User = Depends(get_admin),
    db: Session = Depends(get_db),
):
    review = db.get(RecipeReview, review_id)
    if review is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "We couldn't find that comment.")
    recipe = db.get(Recipe, review.recipe_id)
    db.delete(review)
    db.flush()
    if recipe is not None:
        average, count = db.query(
            func.avg(RecipeReview.rating), func.count(RecipeReview.id)
        ).filter(RecipeReview.recipe_id == recipe.id).one()
        recipe.rating = float(average or 0)
        recipe.rating_count = count
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
