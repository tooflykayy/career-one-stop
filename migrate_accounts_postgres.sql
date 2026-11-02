BEGIN;

SET LOCAL lock_timeout = '5s';

CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    email VARCHAR(254) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

ALTER TABLE skill
    ADD COLUMN IF NOT EXISTS user_id INTEGER
    REFERENCES "user"(id);

ALTER TABLE application
    ADD COLUMN IF NOT EXISTS user_id INTEGER
    REFERENCES "user"(id);

ALTER TABLE learning_activity
    ADD COLUMN IF NOT EXISTS user_id INTEGER
    REFERENCES "user"(id);

CREATE INDEX IF NOT EXISTS ix_skill_user_id
    ON skill(user_id);

CREATE INDEX IF NOT EXISTS ix_application_user_id
    ON application(user_id);

CREATE INDEX IF NOT EXISTS ix_learning_activity_user_id
    ON learning_activity(user_id);

COMMIT;