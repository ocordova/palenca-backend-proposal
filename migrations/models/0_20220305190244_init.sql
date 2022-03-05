-- upgrade --
CREATE TABLE IF NOT EXISTS "clients" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "cuid" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "api_key" TEXT NOT NULL,
    "company_name" TEXT NOT NULL,
    "logo_name" TEXT NOT NULL,
    "list_apps" JSONB NOT NULL,
    "webhook_url" TEXT NOT NULL,
    "extra_data" JSONB,
    "list_of_countries" JSONB NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "platforms" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "code" TEXT NOT NULL,
    "status" TEXT NOT NULL,
    "available_countries" JSONB NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "cuid" TEXT NOT NULL,
    "extra_data" JSONB,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "client_id" INT NOT NULL REFERENCES "clients" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "app_logins" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "country" TEXT NOT NULL,
    "platform" TEXT NOT NULL,
    "login" TEXT NOT NULL,
    "status" TEXT NOT NULL,
    "password" TEXT,
    "source" TEXT,
    "worker_id" TEXT,
    "access_token" TEXT,
    "refresh_token" TEXT,
    "expiration_date" TIMESTAMPTZ,
    "failed_reason" TEXT,
    "extra_data" JSONB,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "client_id" INT NOT NULL REFERENCES "clients" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
