DROP TABLE IF EXISTS planet CASCADE;

CREATE TABLE IF NOT EXISTS planet (
    hostname TEXT,
    pl_letter TEXT,
    pl_orbper DOUBLE PRECISION,
    pl_orbsmax DOUBLE PRECISION,
    pl_rade DOUBLE PRECISION,
    pl_bmasse DOUBLE PRECISION,
    pl_eqt DOUBLE PRECISION,
    pl_dens DOUBLE PRECISION,
    pl_esi DOUBLE PRECISION,
    PRIMARY KEY (hostname, pl_letter),
    FOREIGN KEY (hostname) REFERENCES system(hostname) ON DELETE CASCADE
);