"""Nạp dữ liệu mẫu.  Chạy:  python seed.py

BẮT BUỘC có. Trang trống thì không demo được, và không kiểm tra được empty state.

Dữ liệu mẫu ở đây CỐ Ý trùng với frontend/mock/*.json (cùng tên món, cùng tác
giả) — để khi frontend chuyển từ đọc mock sang gọi API thật, giao diện demo
trông vẫn quen thuộc.
"""
from database import Base, SessionLocal, engine
from models import Ingredient, Recipe, Step, User
from security import hash_password

AUTHORS = [
    dict(email="priya@example.com", display_name="Priya Nair"),
    dict(email="dan@example.com", display_name="Dan Okafor"),
    dict(email="marisol@example.com", display_name="Marisol Vega"),
    dict(email="wen@example.com", display_name="Wen Zhao"),
]

RECIPES = [
    dict(
        title="Brown Butter Miso Cookies",
        category="baking", minutes=35, servings=14, difficulty="Easy",
        author="Priya Nair", rating=4.8, rating_count=212,
        summary="Chewy cookies with nutty browned butter and a savoury edge from white miso.",
        tags=["dessert", "cookies", "make-ahead"],
        notes="Dough keeps in the fridge for up to 3 days, or freeze the scooped balls and bake straight from frozen — add a minute or two to the bake time.",
        ingredients=[
            ("170 g", "unsalted butter"), ("3 tbsp", "white miso paste"),
            ("200 g", "brown sugar"), ("50 g", "granulated sugar"),
            ("1", "large egg, plus 1 yolk"), ("2 tsp", "vanilla extract"),
            ("260 g", "all-purpose flour"), ("1 tsp", "baking soda"),
            ("1/2 tsp", "flaky salt, plus extra for topping"), ("150 g", "chopped dark chocolate"),
        ],
        steps=[
            ("Brown the butter", "Melt the butter in a light-colored pan over medium heat. Keep swirling until it turns amber and smells nutty, about 5 minutes. Whisk in the miso off the heat until smooth, then let cool for 10 minutes.", None),
            ("Mix the wet ingredients", "Whisk the brown butter mixture with both sugars until glossy. Add the egg, egg yolk, and vanilla, and whisk until the mixture lightens slightly.", None),
            ("Bring in the dry ingredients", "Fold in the flour, baking soda, and salt just until no dry streaks remain. Fold in the chopped chocolate.", None),
            ("Chill the dough", "Cover and chill for at least 30 minutes — this keeps the cookies from spreading too thin.", 30),
            ("Bake", "Scoop into 14 balls on a lined sheet, spaced well apart. Bake at 190°C (375°F) for 11–13 minutes, until the edges are set but the centers still look soft.", 12),
            ("Finish", "Sprinkle with flaky salt the moment they come out of the oven. Cool on the tray for 5 minutes before moving.", None),
        ],
    ),
    dict(
        title="Weeknight Tomato-Braised Chickpeas",
        category="mains", minutes=25, servings=4, difficulty="Easy",
        author="Dan Okafor", rating=4.6, rating_count=158,
        summary="One pan, pantry staples, and a fried egg on top if you're feeling it.",
        tags=["vegetarian", "one-pan", "budget"], notes="",
        ingredients=[
            ("2 tbsp", "olive oil"), ("1", "yellow onion, diced"), ("3 cloves", "garlic, sliced"),
            ("2 x 400 g", "canned chickpeas, drained"), ("400 g", "canned crushed tomatoes"),
            ("1 tsp", "smoked paprika"), ("to taste", "salt and pepper"),
        ],
        steps=[
            ("Soften the aromatics", "Heat the oil in a wide pan over medium heat. Cook the onion until soft, about 6 minutes, then add the garlic for 1 minute more.", None),
            ("Braise", "Add the chickpeas, tomatoes, and paprika. Simmer uncovered for 15 minutes, mashing a few chickpeas against the pan to thicken the sauce.", 15),
            ("Season and serve", "Taste and adjust salt and pepper. Serve as is, over rice, or with a fried egg on top.", None),
        ],
    ),
    dict(
        title="Charred Corn and Feta Salad",
        category="salads", minutes=20, servings=4, difficulty="Easy",
        author="Marisol Vega", rating=4.7, rating_count=94,
        summary="Sweet charred corn, salty feta, and a lime-chili dressing that ties it together.",
        tags=["summer", "gluten-free"], notes="",
        ingredients=[
            ("4 ears", "corn, husked"), ("100 g", "feta, crumbled"), ("1", "jalapeño, thinly sliced"),
            ("2 tbsp", "lime juice"), ("3 tbsp", "olive oil"), ("handful", "cilantro leaves"),
        ],
        steps=[
            ("Char the corn", "Grill or dry-sear the corn on all sides until charred in spots, about 8 minutes. Let cool, then cut kernels from the cob.", 8),
            ("Dress", "Whisk the lime juice and olive oil, and season with salt.", None),
            ("Toss and finish", "Toss the corn with the feta, jalapeño, and dressing. Top with cilantro just before serving.", None),
        ],
    ),
    dict(
        title="Ginger Scallion Noodles",
        category="mains", minutes=15, servings=2, difficulty="Easy",
        author="Wen Zhao", rating=4.9, rating_count=301,
        summary="A five-ingredient sauce that turns dried noodles into something worth craving.",
        tags=["vegetarian", "quick"], notes="",
        ingredients=[
            ("200 g", "dried wheat noodles"), ("4", "scallions, finely sliced"),
            ("1 tbsp", "fresh ginger, minced"), ("3 tbsp", "neutral oil"),
            ("2 tbsp", "soy sauce"), ("1 tsp", "sugar"),
        ],
        steps=[
            ("Boil the noodles", "Cook the noodles according to the package, then drain well.", None),
            ("Make the sizzle", "Pile the scallions and ginger in a heatproof bowl. Heat the oil until just smoking and pour it over — it should sizzle loudly.", None),
            ("Toss", "Stir in the soy sauce and sugar, then toss with the hot noodles until coated.", None),
        ],
    ),
    dict(
        title="Sheet-Pan Harissa Chicken",
        category="mains", minutes=45, servings=4, difficulty="Medium",
        author="Dan Okafor", rating=4.5, rating_count=122,
        summary="Chicken thighs and chickpeas roast together under a spicy harissa glaze.",
        tags=["one-pan", "dinner"], notes="",
        ingredients=[
            ("8", "bone-in chicken thighs"), ("400 g", "canned chickpeas, drained"),
            ("3 tbsp", "harissa paste"), ("2 tbsp", "olive oil"), ("1", "lemon, sliced"),
        ],
        steps=[
            ("Marinate", "Toss the chicken with harissa and half the oil. Marinate 15 minutes at room temperature if you have time.", 15),
            ("Arrange the pan", "Spread the chickpeas and lemon slices on a sheet pan, toss with the remaining oil, and nestle the chicken on top.", None),
            ("Roast", "Roast at 220°C (425°F) for 30–35 minutes, until the chicken skin is deeply browned and cooked through.", 32),
        ],
    ),
    dict(
        title="Cardamom Pear Galette",
        category="desserts", minutes=70, servings=8, difficulty="Medium",
        author="Priya Nair", rating=4.9, rating_count=87,
        summary="A free-form tart that forgives a messy fold and rewards it with flaky pastry.",
        tags=["dessert", "fruit", "baking"], notes="",
        ingredients=[
            ("1", "disc pie dough, chilled"), ("4", "ripe pears, thinly sliced"),
            ("60 g", "sugar, plus extra for the crust"), ("1/2 tsp", "ground cardamom"),
            ("1 tbsp", "cornstarch"), ("1", "egg, beaten, for egg wash"),
        ],
        steps=[
            ("Roll the dough", "Roll the chilled dough into a rough circle on parchment and transfer to a sheet pan.", None),
            ("Fill", "Toss the pears with sugar, cardamom, and cornstarch. Pile onto the dough, leaving a 5cm border.", None),
            ("Fold and chill", "Fold the border over the fruit, pleating as you go. Chill 15 minutes so it holds its shape in the oven.", 15),
            ("Bake", "Brush with egg wash, sprinkle with sugar, and bake at 200°C (400°F) for 40–45 minutes until deeply golden.", 42),
        ],
    ),
    dict(
        title="Miso-Butter Roasted Squash Soup",
        category="soups", minutes=40, servings=4, difficulty="Easy",
        author="Marisol Vega", rating=4.6, rating_count=76,
        summary="Roasting the squash first is the whole trick — deep flavour, no cream needed.",
        tags=["vegetarian", "fall"], notes="",
        ingredients=[
            ("1 large", "butternut squash, cubed"), ("2 tbsp", "butter, melted"),
            ("2 tbsp", "white miso paste"), ("1 L", "vegetable stock"), ("1", "onion, chopped"),
        ],
        steps=[
            ("Roast the squash", "Toss the squash with the melted butter and roast at 200°C (400°F) for 25 minutes, until tender and browned at the edges.", 25),
            ("Simmer", "Sauté the onion until soft, then add the roasted squash, miso, and stock. Simmer 10 minutes.", 10),
            ("Blend", "Blend until smooth, thinning with extra stock if needed. Taste and adjust salt.", None),
        ],
    ),
    dict(
        title="Coconut Rice Pudding with Mango",
        category="breakfast", minutes=30, servings=4, difficulty="Easy",
        author="Wen Zhao", rating=4.7, rating_count=143,
        summary="Make it the night before — it's better cold, straight from the fridge.",
        tags=["make-ahead", "breakfast"], notes="",
        ingredients=[
            ("200 g", "short-grain rice, rinsed"), ("400 ml", "coconut milk"),
            ("400 ml", "whole milk"), ("60 g", "sugar"), ("2", "ripe mangoes, sliced"),
        ],
        steps=[
            ("Simmer", "Combine the rice, coconut milk, milk, and sugar in a pot. Simmer gently, stirring often, for 20–25 minutes until thick and creamy.", 22),
            ("Cool", "Cool to room temperature, then chill at least 2 hours (or overnight).", None),
            ("Serve", "Spoon into bowls and top with sliced mango.", None),
        ],
    ),
    dict(
        title="Crispy Sheet-Pan Home Fries",
        category="breakfast", minutes=35, servings=4, difficulty="Easy",
        author="Dan Okafor", rating=4.4, rating_count=61,
        summary="Parboil, then roast hot and undisturbed. That's the entire secret.",
        tags=["breakfast", "budget"], notes="",
        ingredients=[
            ("1 kg", "waxy potatoes, cubed"), ("3 tbsp", "olive oil"),
            ("1 tsp", "smoked paprika"), ("to taste", "salt and pepper"),
        ],
        steps=[
            ("Parboil", "Boil the potatoes in salted water for 5 minutes, then drain well and let steam-dry for a few minutes.", 5),
            ("Season", "Toss with the oil, paprika, salt, and pepper on a sheet pan, spreading into a single layer.", None),
            ("Roast undisturbed", "Roast at 220°C (425°F) for 25 minutes without stirring, so a real crust forms on one side.", 25),
        ],
    ),
]


def run():
    Base.metadata.create_all(engine)
    db = SessionLocal()

    if db.query(User).count() > 0:
        print("Database đã có dữ liệu, bỏ qua.")
        db.close()
        return

    admin = User(
        email="admin@example.com", password_hash=hash_password("password123"),
        display_name="Quản trị", role="admin",
    )
    db.add(admin)

    users_by_name = {}
    for a in AUTHORS:
        user = User(email=a["email"], password_hash=hash_password("password123"), display_name=a["display_name"])
        db.add(user)
        users_by_name[a["display_name"]] = user

    db.flush()  # để user.id có giá trị trước khi gán owner_id bên dưới

    for r in RECIPES:
        recipe = Recipe(
            title=r["title"], summary=r["summary"], notes=r["notes"],
            category=r["category"], minutes=r["minutes"], servings=r["servings"],
            difficulty=r["difficulty"], tags=",".join(r["tags"]),
            rating=r["rating"], rating_count=r["rating_count"],
            owner_id=users_by_name[r["author"]].id,
        )
        recipe.ingredients = [
            Ingredient(position=i, qty=qty, item=item) for i, (qty, item) in enumerate(r["ingredients"])
        ]
        recipe.steps = [
            Step(position=i, title=title, text=text, timer_minutes=timer)
            for i, (title, text, timer) in enumerate(r["steps"])
        ]
        db.add(recipe)

    db.commit()
    print("Đã nạp dữ liệu mẫu. Đăng nhập: priya@example.com / password123 (hoặc dan / marisol / wen, admin@example.com)")
    db.close()


if __name__ == "__main__":
    run()
