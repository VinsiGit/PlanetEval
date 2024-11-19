DROP TABLE IF EXISTS missing_planet CASCADE;

CREATE TABLE IF NOT EXISTS missing_planet (
    hostname TEXT,
    pl_letter TEXT,
    pl_orbper DOUBLE PRECISION NULL,
    pl_orbsmax DOUBLE PRECISION NULL,
    pl_rade DOUBLE PRECISION NULL,
    pl_bmasse DOUBLE PRECISION NULL,
    pl_eqt DOUBLE PRECISION NULL,
    pl_dens DOUBLE PRECISION NULL,
    pl_esi_estimation DOUBLE PRECISION NULL,
    PRIMARY KEY (hostname, pl_letter),
    FOREIGN KEY (hostname) REFERENCES system(hostname) ON DELETE CASCADE
);