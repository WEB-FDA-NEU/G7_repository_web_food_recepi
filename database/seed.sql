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

-- Refresh the descriptive seed content on reruns without changing demo ratings.
UPDATE recipes SET summary = 'Chewy chocolate cookies with nutty browned butter, savoury white miso, and crisp edges around soft centers.', notes = 'Chill the dough at least 30 minutes for thicker cookies. Refrigerate scooped dough for up to 3 days, or freeze for up to 2 months and bake from frozen with 1–2 extra minutes.' WHERE id = 1;
UPDATE recipes SET summary = 'A cozy one-pan dinner of tender chickpeas simmered in garlicky tomato sauce, finished with herbs and an optional fried egg.', notes = 'Use the chickpea liquid if you want a thicker, silkier sauce. Serve with toasted sourdough, rice, or warm flatbread.' WHERE id = 2;
UPDATE recipes SET summary = 'Smoky sweet corn, creamy avocado, salty feta, and crunchy greens tossed in a bright lime-chili dressing.', notes = 'Char the corn in a very hot, dry pan for the best colour. Keep the dressing and avocado separate until just before serving.' WHERE id = 3;
UPDATE recipes SET summary = 'Springy noodles tossed in a quick ginger-scallion oil with soy, sesame, and a little chili for a savoury weeknight bowl.', notes = 'The oil should be hot enough to sizzle the scallions but not smoke. Add a splash of noodle water if the sauce needs loosening.' WHERE id = 4;
UPDATE recipes SET summary = 'Juicy harissa-spiced chicken thighs roast on one tray with chickpeas, red onion, and lemon until crisp and caramelized.', notes = 'Pat the chicken dry before seasoning for crisp skin. Swap in cauliflower florets for a vegetable-forward tray bake.' WHERE id = 5;
UPDATE recipes SET summary = 'A rustic pear galette with buttery flaky pastry, ripe fruit, cardamom, and a golden sugared crust.', notes = 'Keep the pastry cold and patch small cracks as you fold. Let the galette rest 20 minutes after baking so the fruit juices settle.' WHERE id = 6;
UPDATE recipes SET summary = 'Roasted squash blended with white miso, browned butter, and stock into a deeply savoury, velvety autumn soup.', notes = 'Roast the squash until the edges are browned for the sweetest flavour. Blend in batches and vent the lid carefully while the soup is hot.' WHERE id = 7;
UPDATE recipes SET summary = 'Creamy coconut rice pudding topped with ripe mango, lime zest, and toasted coconut for a make-ahead breakfast or dessert.', notes = 'Stir often as the rice thickens to prevent sticking. It will firm up in the fridge; loosen with a splash of coconut milk before serving.' WHERE id = 8;
UPDATE recipes SET summary = 'Crispy-edged potatoes with fluffy centers, tossed with garlic, smoked paprika, and herbs for an easy sheet-pan breakfast.', notes = 'Space the potatoes out and leave them untouched for the first 20 minutes of roasting. Crowding the pan will steam them instead of crisping.' WHERE id = 9;

-- These tables do not have a uniqueness constraint on (recipe_id, position),
-- so remove the demo recipes' detail rows before reseeding them. This keeps
-- rerunning the seed script from duplicating their ingredients and steps.
DELETE FROM ingredients WHERE recipe_id BETWEEN 1 AND 9;
DELETE FROM steps WHERE recipe_id BETWEEN 1 AND 9;

INSERT INTO ingredients (recipe_id, position, qty, item) VALUES
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

INSERT INTO ingredients (recipe_id, position, qty, item) VALUES
    (2, 0, '2 tbsp', 'olive oil'), (2, 1, '1', 'small yellow onion, diced'),
    (2, 2, '3 cloves', 'garlic, minced'), (2, 3, '1 tbsp', 'tomato paste'),
    (2, 4, '2 cans (400 g each)', 'chickpeas, drained and rinsed'),
    (2, 5, '1 can (400 g)', 'crushed tomatoes'), (2, 6, '1/2 cup', 'vegetable stock'),
    (2, 7, '1 tsp', 'smoked paprika'), (2, 8, '1/2 tsp', 'ground cumin'),
    (2, 9, '1/2 tsp', 'fine salt'), (2, 10, '2 tbsp', 'chopped parsley'),
    (2, 11, '4', 'eggs, optional'),
    (3, 0, '4 ears', 'sweet corn, husked'), (3, 1, '1 tbsp', 'olive oil'),
    (3, 2, '1', 'ripe avocado, diced'), (3, 3, '100 g', 'feta, crumbled'),
    (3, 4, '4 cups', 'baby spinach or rocket'), (3, 5, '1', 'lime, juiced and zested'),
    (3, 6, '2 tbsp', 'extra-virgin olive oil'), (3, 7, '1 tsp', 'honey'),
    (3, 8, '1/4 tsp', 'chili flakes'), (3, 9, '1/4 tsp', 'fine salt'),
    (4, 0, '200 g', 'dried wheat noodles'), (4, 1, '4', 'scallions, thinly sliced'),
    (4, 2, '1 tbsp', 'fresh ginger, finely grated'), (4, 3, '3 tbsp', 'neutral oil'),
    (4, 4, '2 tbsp', 'soy sauce'), (4, 5, '1 tbsp', 'rice vinegar'),
    (4, 6, '1 tsp', 'toasted sesame oil'), (4, 7, '1 tsp', 'chili crisp, optional'),
    (4, 8, '1 tsp', 'toasted sesame seeds'),
    (5, 0, '700 g', 'bone-in chicken thighs, skin on'), (5, 1, '2 tbsp', 'harissa paste'),
    (5, 2, '1 tbsp', 'olive oil'), (5, 3, '1 can (400 g)', 'chickpeas, drained'),
    (5, 4, '1', 'red onion, cut into wedges'), (5, 5, '1', 'lemon, cut into wedges'),
    (5, 6, '1 tsp', 'ground cumin'), (5, 7, '1/2 tsp', 'fine salt'),
    (5, 8, '2 tbsp', 'chopped cilantro'),
    (6, 0, '250 g', 'all-purpose flour'), (6, 1, '170 g', 'cold unsalted butter, cubed'),
    (6, 2, '3 tbsp', 'granulated sugar, divided'), (6, 3, '1/2 tsp', 'fine salt'),
    (6, 4, '5 tbsp', 'ice water'), (6, 5, '4', 'ripe but firm pears, thinly sliced'),
    (6, 6, '1 tbsp', 'lemon juice'), (6, 7, '1 tbsp', 'cornstarch'),
    (6, 8, '1/2 tsp', 'ground cardamom'), (6, 9, '1', 'egg, beaten'),
    (7, 0, '1.2 kg', 'butternut squash, peeled and cubed'), (7, 1, '2 tbsp', 'olive oil'),
    (7, 2, '1', 'yellow onion, diced'), (7, 3, '2 tbsp', 'unsalted butter'),
    (7, 4, '2 tbsp', 'white miso paste'), (7, 5, '750 ml', 'vegetable stock'),
    (7, 6, '1/4 tsp', 'ground nutmeg'), (7, 7, '1/2 tsp', 'fine salt'),
    (7, 8, '2 tbsp', 'pumpkin seeds, toasted'),
    (8, 0, '200 g', 'short-grain rice'), (8, 1, '400 ml', 'coconut milk'),
    (8, 2, '500 ml', 'whole milk'), (8, 3, '60 g', 'sugar'),
    (8, 4, '1', 'pinch fine salt'), (8, 5, '1 tsp', 'vanilla extract'),
    (8, 6, '1', 'ripe mango, diced'), (8, 7, '2 tbsp', 'toasted coconut flakes'),
    (8, 8, '1', 'lime, zested'),
    (9, 0, '1 kg', 'waxy potatoes, cut into 3 cm cubes'), (9, 1, '2 tbsp', 'olive oil'),
    (9, 2, '1 tsp', 'smoked paprika'), (9, 3, '1/2 tsp', 'garlic powder'),
    (9, 4, '1/2 tsp', 'fine salt'), (9, 5, '1/4 tsp', 'black pepper'),
    (9, 6, '2 tbsp', 'chopped parsley'), (9, 7, '1 tbsp', 'apple cider vinegar');

INSERT INTO steps (recipe_id, position, title, text, timer_minutes) VALUES
    (1, 0, 'Brown the butter', 'Melt the butter in a light-colored pan over medium heat. Keep swirling until it turns amber and smells nutty, about 5 minutes. Whisk in the miso off the heat until smooth, then let cool for 10 minutes.', NULL),
    (1, 1, 'Mix the wet ingredients', 'Whisk the brown butter mixture with both sugars until glossy. Add the egg, egg yolk, and vanilla, and whisk until the mixture lightens slightly.', NULL),
    (1, 2, 'Bring in the dry ingredients', 'Fold in the flour, baking soda, and salt just until no dry streaks remain. Fold in the chopped chocolate.', NULL),
    (1, 3, 'Chill the dough', 'Cover and chill for at least 30 minutes — this keeps the cookies from spreading too thin.', 30),
    (1, 4, 'Bake', 'Scoop into 14 balls on a lined sheet, spaced well apart. Bake at 190°C (375°F) for 11–13 minutes, until the edges are set but the centers still look soft.', 12),
    (1, 5, 'Finish', 'Sprinkle with flaky salt the moment they come out of the oven. Cool on the tray for 5 minutes before moving.', NULL);

INSERT INTO steps (recipe_id, position, title, text, timer_minutes) VALUES
    (2, 0, 'Soften the aromatics', 'Warm the olive oil in a deep skillet over medium heat. Add the onion and cook until soft, about 5 minutes. Stir in garlic, tomato paste, paprika, and cumin for 1 minute.', 6),
    (2, 1, 'Simmer the chickpeas', 'Add the chickpeas, crushed tomatoes, stock, and salt. Bring to a gentle simmer and cook uncovered, stirring occasionally, until thick and saucy.', 15),
    (2, 2, 'Finish and serve', 'Taste and adjust the seasoning. Scatter parsley over the chickpeas. If using eggs, fry them separately and place one on each serving.', NULL),
    (3, 0, 'Char the corn', 'Heat a heavy skillet until very hot. Brush the corn lightly with oil and turn it in the pan until charred in spots and tender. Cool slightly, then slice kernels from the cobs.', 10),
    (3, 1, 'Shake the dressing', 'Whisk lime juice and zest with olive oil, honey, chili flakes, and salt until glossy.', NULL),
    (3, 2, 'Toss the salad', 'Combine greens and corn with the dressing. Fold in avocado and feta gently, then finish with black pepper and serve right away.', NULL),
    (4, 0, 'Cook the noodles', 'Boil noodles in salted water according to the package directions. Reserve 1/4 cup cooking water, then drain.', 8),
    (4, 1, 'Make the scallion oil', 'Put scallions and ginger in a heatproof bowl. Warm neutral oil until shimmering, then carefully pour it over the aromatics and stir.', NULL),
    (4, 2, 'Toss and serve', 'Mix soy sauce, vinegar, sesame oil, and chili crisp into the scallion oil. Toss with hot noodles, loosening with reserved water as needed. Top with sesame seeds.', NULL),
    (5, 0, 'Heat the oven', 'Heat oven to 220°C (425°F). Pat chicken thighs dry. Mix harissa, olive oil, cumin, and salt, then coat the chicken.', NULL),
    (5, 1, 'Arrange the tray', 'Toss chickpeas and onion with a little oil on a rimmed sheet pan. Nestle chicken skin-side up among them and add lemon wedges.', NULL),
    (5, 2, 'Roast until crisp', 'Roast until chicken is deeply browned and reaches 74°C (165°F) at the thickest part. Scatter cilantro over the tray and serve with the pan juices.', 35),
    (6, 0, 'Make the pastry', 'Rub cold butter into flour, 1 tablespoon sugar, and salt until pea-sized pieces remain. Add ice water gradually, bring the dough together, flatten into a disc, and chill.', 30),
    (6, 1, 'Prepare the pears', 'Toss sliced pears with lemon juice, cornstarch, cardamom, and 1 tablespoon sugar.', NULL),
    (6, 2, 'Shape the galette', 'Roll dough into a rough 32 cm circle on parchment. Pile pears in the center, leaving a 5 cm border, then fold the pastry over the fruit in loose pleats.', NULL),
    (6, 3, 'Bake until golden', 'Brush pastry with beaten egg and sprinkle with the remaining sugar. Bake at 200°C (400°F) until the crust is golden and pear juices bubble.', 40),
    (7, 0, 'Roast the squash', 'Heat oven to 220°C (425°F). Toss squash with olive oil and salt. Roast on a sheet pan until tender and browned at the edges.', 30),
    (7, 1, 'Build the soup', 'Cook onion in butter over medium heat until soft. Stir in miso and nutmeg, then add roasted squash and stock. Simmer briefly.', 8),
    (7, 2, 'Blend and serve', 'Blend until smooth, adding stock to reach your preferred consistency. Taste for seasoning and serve with toasted pumpkin seeds.', NULL),
    (8, 0, 'Rinse and simmer the rice', 'Rinse rice until the water runs mostly clear. Add to a saucepan with coconut milk, whole milk, sugar, and salt.', NULL),
    (8, 1, 'Cook until creamy', 'Bring to a gentle simmer, then cook on low, stirring often, until the rice is tender and the pudding is creamy.', 25),
    (8, 2, 'Chill and top', 'Stir in vanilla. Serve warm or chill until cold, then top with mango, toasted coconut, and lime zest.', NULL),
    (9, 0, 'Parboil the potatoes', 'Place potatoes in well-salted cold water. Bring to a boil and cook until the outside is tender but the centers still hold their shape. Drain and let steam-dry.', 8),
    (9, 1, 'Season the tray', 'Heat oven to 230°C (450°F). Toss potatoes with olive oil, paprika, garlic powder, salt, and pepper. Spread in one layer with cut sides against the pan.', NULL),
    (9, 2, 'Roast until crisp', 'Roast without moving until the undersides are deeply golden. Turn once and continue roasting until crisp all over.', 25),
    (9, 3, 'Finish and serve', 'Toss hot potatoes with cider vinegar and parsley. Taste, add more salt if needed, and serve immediately.', NULL);

COMMIT;
