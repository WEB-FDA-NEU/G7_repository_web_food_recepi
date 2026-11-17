-- Demo accounts for local development. Password for each account: password
-- The stored value is a bcrypt hash; never store demo passwords in plain text.
BEGIN;
INSERT OR IGNORE INTO users (email, username, password_hash, display_name, role) VALUES
    ('admin@example.com', 'admin', '$2b$12$x7H097vVUrsrYPu5T1QaIeqrvzf.adhJ/ieisXkDeKyDlPRdWK3p.', 'admin', 'admin'),
    ('priya@example.com', 'priya', '$2b$12$x7H097vVUrsrYPu5T1QaIeqrvzf.adhJ/ieisXkDeKyDlPRdWK3p.', 'Priya Nair', 'user'),
    ('dan@example.com', 'dan', '$2b$12$x7H097vVUrsrYPu5T1QaIeqrvzf.adhJ/ieisXkDeKyDlPRdWK3p.', 'Dan Okafor', 'user'),
    ('marisol@example.com', 'marisol', '$2b$12$x7H097vVUrsrYPu5T1QaIeqrvzf.adhJ/ieisXkDeKyDlPRdWK3p.', 'Marisol Vega', 'user'),
    ('wen@example.com', 'wen', '$2b$12$x7H097vVUrsrYPu5T1QaIeqrvzf.adhJ/ieisXkDeKyDlPRdWK3p.', 'Wen Zhao', 'user');

UPDATE users
SET password_hash = '$2b$12$x7H097vVUrsrYPu5T1QaIeqrvzf.adhJ/ieisXkDeKyDlPRdWK3p.'
WHERE email IN (
    'admin@example.com', 'priya@example.com', 'dan@example.com',
    'marisol@example.com', 'wen@example.com'
);

INSERT OR IGNORE INTO recipes
    (id, title, summary, notes, category, minutes, servings, difficulty, tags,
     rating, rating_count, owner_id)
VALUES
    (1, 'Brown Butter Miso Cookies', 'Chewy cookies with nutty browned butter and a savoury edge from white miso.', 'Dough keeps in the fridge for up to 3 days, or freeze the scooped balls and bake straight from frozen — add a minute or two to the bake time.', 'baking', 35, 14, 'Easy', 'dessert,cookies,make-ahead', 4.8, 212, (SELECT id FROM users WHERE email = 'priya@example.com')),
    (2, 'Weeknight Tomato-Braised Chickpeas', 'One pan, pantry staples, and a fried egg on top if you’re feeling it.', '', 'mains', 25, 4, 'Easy', 'vegetarian,one-pan,budget', 4.6, 158, (SELECT id FROM users WHERE email = 'dan@example.com')),
    (3, 'Charred Corn and Feta Salad', 'Sweet charred corn, salty feta, and a lime-chili dressing that ties it together.', '', 'salads', 20, 4, 'Easy', 'summer,gluten-free', 4.7, 94, (SELECT id FROM users WHERE email = 'marisol@example.com')),
    (4, 'Ginger Scallion Noodles', 'A five-ingredient sauce that turns dried noodles into something worth craving.', '', 'mains', 15, 2, 'Easy', 'vegetarian,quick', 4.9, 301, (SELECT id FROM users WHERE email = 'wen@example.com')),
    (5, 'Sheet-Pan Harissa Chicken', 'Chicken thighs and chickpeas roast together under a spicy harissa glaze.', '', 'mains', 45, 4, 'Medium', 'one-pan,dinner', 4.5, 122, (SELECT id FROM users WHERE email = 'dan@example.com')),
    (6, 'Cardamom Pear Galette', 'A free-form tart that forgives a messy fold and rewards it with flaky pastry.', '', 'desserts', 70, 8, 'Medium', 'dessert,fruit,baking', 4.9, 87, (SELECT id FROM users WHERE email = 'priya@example.com')),
    (7, 'Miso-Butter Roasted Squash Soup', 'Roasting the squash first is the whole trick — deep flavour, no cream needed.', '', 'soups', 40, 4, 'Easy', 'vegetarian,fall', 4.6, 76, (SELECT id FROM users WHERE email = 'marisol@example.com')),
    (8, 'Coconut Rice Pudding with Mango', 'Make it the night before — it’s better cold, straight from the fridge.', '', 'breakfast', 30, 4, 'Easy', 'make-ahead,breakfast', 4.7, 143, (SELECT id FROM users WHERE email = 'wen@example.com')),
    (9, 'Crispy Sheet-Pan Home Fries', 'Parboil, then roast hot and undisturbed. That’s the entire secret.', '', 'breakfast', 35, 4, 'Easy', 'breakfast,budget', 4.4, 61, (SELECT id FROM users WHERE email = 'dan@example.com'));

INSERT OR IGNORE INTO ingredients (recipe_id, position, qty, item) VALUES
    (1, 0, '170 g', 'unsalted butter'),
    (1, 1, '3 tbsp', 'white miso paste'),
    (1, 2, '200 g', 'brown sugar'),
    (1, 3, '50 g', 'granulated sugar'),
    (1, 4, '1', 'large egg, plus 1 yolk'),
    (1, 5, '2 tsp', 'vanilla extract'),
    (1, 6, '260 g', 'all-purpose flour'),
    (1, 7, '1 tsp', 'baking soda'),
    (1, 8, '1/2 tsp', 'flaky salt, plus extra for topping'),
    (1, 9, '150 g', 'chopped dark chocolate');

INSERT OR IGNORE INTO steps (recipe_id, position, title, text, timer_minutes) VALUES
    (1, 0, 'Brown the butter', 'Melt the butter in a light-colored pan over medium heat. Keep swirling until it turns amber and smells nutty, about 5 minutes. Whisk in the miso off the heat until smooth, then let cool for 10 minutes.', NULL),
    (1, 1, 'Mix the wet ingredients', 'Whisk the brown butter mixture with both sugars until glossy. Add the egg, egg yolk, and vanilla, and whisk until the mixture lightens slightly.', NULL),
    (1, 2, 'Bring in the dry ingredients', 'Fold in the flour, baking soda, and salt just until no dry streaks remain. Fold in the chopped chocolate.', NULL),
    (1, 3, 'Chill the dough', 'Cover and chill for at least 30 minutes — this keeps the cookies from spreading too thin.', 30),
    (1, 4, 'Bake', 'Scoop into 14 balls on a lined sheet, spaced well apart. Bake at 190°C (375°F) for 11–13 minutes, until the edges are set but the centers still look soft.', 12),
    (1, 5, 'Finish', 'Sprinkle with flaky salt the moment they come out of the oven. Cool on the tray for 5 minutes before moving.', NULL);

COMMIT;
