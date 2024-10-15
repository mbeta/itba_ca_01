-- Crear la tabla para los títulos básicos
CREATE TABLE title_basics (
    tconst VARCHAR(255) PRIMARY KEY,
    titleType VARCHAR(50),
    primaryTitle TEXT,
    originalTitle TEXT,
    isAdult BOOLEAN,
    startYear INT,
    endYear INT,
    runtimeMinutes INT,
    genres TEXT[]
);

-- Crear la tabla para los nombres de personas
CREATE TABLE name_basics (
    nconst VARCHAR(255) PRIMARY KEY,
    primaryName TEXT,
    birthYear INT,
    deathYear INT,
    primaryProfession TEXT[],
    knownForTitles TEXT[]
);

-- Crear la tabla para los títulos alternativos
CREATE TABLE title_akas (
    titleId VARCHAR(255),
    ordering INT,
    title TEXT,
    region VARCHAR(50),
    language VARCHAR(50),
    types TEXT[],
    attributes TEXT[],
    isOriginalTitle BOOLEAN,
    PRIMARY KEY (titleId, ordering),
    FOREIGN KEY (titleId) REFERENCES title_basics(tconst)
);

-- Crear la tabla para el elenco y el equipo principal
CREATE TABLE title_principals (
    tconst VARCHAR(255),
    ordering INT,
    nconst VARCHAR(255),
    category VARCHAR(50),
    job TEXT,
    characters TEXT,
    PRIMARY KEY (tconst, ordering, nconst),
    FOREIGN KEY (tconst) REFERENCES title_basics(tconst),
    FOREIGN KEY (nconst) REFERENCES name_basics(nconst)
);

-- Crear la tabla para las calificaciones de los títulos
CREATE TABLE title_ratings (
    tconst VARCHAR(255) PRIMARY KEY,
    averageRating FLOAT,
    numVotes INT,
    FOREIGN KEY (tconst) REFERENCES title_basics(tconst)
);