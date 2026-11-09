-- Demo accounts for local development. Password for each account: password123
-- The stored value is a bcrypt hash; never store demo passwords in plain text.
INSERT OR IGNORE INTO users (email, password_hash, display_name, role) VALUES
    ('admin@example.com', '$2b$12$z5IXvHRRNP3lPhZyty/zOO.xtUSc5HId5geSsDxo1kJkYn7.BxTY2', 'Quản trị', 'admin'),
    ('priya@example.com', '$2b$12$z5IXvHRRNP3lPhZyty/zOO.xtUSc5HId5geSsDxo1kJkYn7.BxTY2', 'Priya Nair', 'user'),
    ('dan@example.com', '$2b$12$z5IXvHRRNP3lPhZyty/zOO.xtUSc5HId5geSsDxo1kJkYn7.BxTY2', 'Dan Okafor', 'user'),
    ('marisol@example.com', '$2b$12$z5IXvHRRNP3lPhZyty/zOO.xtUSc5HId5geSsDxo1kJkYn7.BxTY2', 'Marisol Vega', 'user'),
    ('wen@example.com', '$2b$12$z5IXvHRRNP3lPhZyty/zOO.xtUSc5HId5geSsDxo1kJkYn7.BxTY2', 'Wen Zhao', 'user');
