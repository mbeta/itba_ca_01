
-- Tabla critic_reviews
CREATE TABLE critic_reviews (
    reviewId BIGINT PRIMARY KEY,
    creationDate DATE,
    criticName VARCHAR(255),
    criticPageUrl VARCHAR(255),
    reviewState VARCHAR(50),
    isFresh BOOLEAN,
    isRotten BOOLEAN,
    isRtUrl BOOLEAN,
    isTopCritic BOOLEAN,
    publicationUrl VARCHAR(255),
    publicationName VARCHAR(255),
    reviewUrl TEXT,
    quote TEXT,
    scoreSentiment VARCHAR(50),
    originalScore VARCHAR(50),
    movieId UUID
);

-- Tabla movies
CREATE TABLE movies (
    movieId UUID PRIMARY KEY,
    movieTitle TEXT,
    movieYear INTEGER, 
    movieURL TEXT,
    movieRank INTEGER,
    critic_score VARCHAR(10),
    audience_score VARCHAR(10)
);

-- Tabla user_reviews
CREATE TABLE user_reviews (
    movieId UUID,
    rating DECIMAL(2,1),
    quote TEXT,
    reviewId VARCHAR(50),
    isVerified BOOLEAN,
    isSuperReviewer BOOLEAN,
    hasSpoilers BOOLEAN,
    hasProfanity BOOLEAN,
    score DECIMAL(2,1),
    creationDate DATE,
    userDisplayName VARCHAR(255),
    userRealm VARCHAR(50),
    userId BIGINT
);
