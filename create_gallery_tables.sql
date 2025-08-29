-- Create Gallery tables manually

CREATE TABLE IF NOT EXISTS college_website_gallery (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(50) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(20) NOT NULL,
    cover_image VARCHAR(100) NOT NULL,
    is_featured BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    ordering INTEGER NOT NULL,
    meta_description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS college_website_galleryphoto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    image VARCHAR(100) NOT NULL,
    title VARCHAR(200) NOT NULL,
    caption TEXT NOT NULL,
    photographer VARCHAR(100) NOT NULL,
    date_taken DATE,
    ordering INTEGER NOT NULL,
    is_active BOOLEAN NOT NULL,
    gallery_id INTEGER NOT NULL,
    FOREIGN KEY (gallery_id) REFERENCES college_website_gallery (id)
);

-- Insert migration record
INSERT OR IGNORE INTO django_migrations (app, name, applied) 
VALUES ('college_website', '0003_gallery_galleryphoto', datetime('now'));
