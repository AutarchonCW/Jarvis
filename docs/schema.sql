-- JARVIS database schema — single source of truth.
-- SQLite. Apply with:  sqlite3 jarvis.db < docs/schema.sql
--
-- Design notes:
--  * One device table with a status column, NOT separate "registered" and
--    "discovered" tables. A device is discovered first and registered later;
--    two tables would mean moving rows and losing history.
--  * Surrogate integer id as primary key, MAC as a UNIQUE natural key. Foreign
--    keys reference the small id, and a mis-read MAC can be corrected without
--    orphaning history.
--  * Sightings are frequent and worthless individually, so they are NOT stored
--    per observation: last_seen is updated in place, and device_event records
--    only transitions (first appearance, reconnect, IP change).
--  * alert.acknowledged_at is the evidence that the HOMEOWNER acted, not the
--    system — the core human-in-the-loop claim depends on this column.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS device (
    id          INTEGER PRIMARY KEY,
    mac         TEXT NOT NULL UNIQUE,
    vendor      TEXT,
    name        TEXT,
    status      TEXT NOT NULL DEFAULT 'unknown'
                CHECK (status IN ('registered', 'unknown', 'ignored')),
    randomised  INTEGER NOT NULL DEFAULT 0,   -- 1 = locally-administered MAC
    first_seen  TEXT NOT NULL,                -- ISO 8601 UTC
    last_seen   TEXT NOT NULL,
    last_ip     TEXT
);

CREATE TABLE IF NOT EXISTS device_event (
    id          INTEGER PRIMARY KEY,
    device_id   INTEGER NOT NULL REFERENCES device(id),
    event_type  TEXT NOT NULL
                CHECK (event_type IN ('first_seen', 'reconnected',
                                      'ip_changed', 'disconnected')),
    occurred_at TEXT NOT NULL,
    detail      TEXT
);

CREATE TABLE IF NOT EXISTS alert (
    id              INTEGER PRIMARY KEY,
    event_id        INTEGER NOT NULL REFERENCES device_event(id),
    raised_at       TEXT NOT NULL,
    acknowledged_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_event_device ON device_event(device_id, occurred_at);
CREATE INDEX IF NOT EXISTS idx_alert_unack  ON alert(acknowledged_at);
