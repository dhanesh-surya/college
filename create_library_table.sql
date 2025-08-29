-- Create LibraryResource table manually
CREATE TABLE IF NOT EXISTS "college_website_libraryresource" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "created_at" datetime NOT NULL,
    "updated_at" datetime NOT NULL,
    "title" varchar(300) NOT NULL,
    "slug" varchar(50) NOT NULL UNIQUE,
    "resource_type" varchar(20) NOT NULL,
    "author" varchar(200) NOT NULL,
    "isbn" varchar(20) NOT NULL,
    "publisher" varchar(200) NOT NULL,
    "publication_year" integer unsigned NULL,
    "description" text NOT NULL,
    "subject_category" varchar(100) NOT NULL,
    "location" varchar(100) NOT NULL,
    "availability_status" varchar(20) NOT NULL,
    "digital_copy" varchar(100) NOT NULL,
    "external_link" varchar(200) NOT NULL,
    "cover_image" varchar(100) NOT NULL,
    "is_featured" bool NOT NULL
);

-- Mark migration as applied
INSERT OR IGNORE INTO django_migrations (app, name, applied) 
VALUES ('college_website', '0006_admissioninfo_alumniprofile_elearningcourse_and_more', datetime('now'));
