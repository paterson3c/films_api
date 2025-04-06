-- Añadir columnas de género, idioma y país directamente a la tabla imdb_movies
ALTER TABLE imdb_movies
ADD COLUMN genres TEXT,
ADD COLUMN languages TEXT,
ADD COLUMN countries TEXT;

-- Insertar los géneros en la tabla imdb_movies
DO $$
DECLARE
    movie_record RECORD;
    genre_text TEXT;
    genres_array TEXT[];
BEGIN
    FOR movie_record IN SELECT movieid, genre FROM imdb_moviegenres
    LOOP
        genres_array := string_to_array(movie_record.genre, ',');

        FOREACH genre_text IN ARRAY genres_array
        LOOP
            UPDATE imdb_movies
            SET genres = COALESCE(genres, '') || CASE WHEN genres IS NOT NULL AND genres <> '' THEN ',' ELSE '' END || TRIM(genre_text)
            WHERE movieid = movie_record.movieid;
        END LOOP;
    END LOOP;
END $$;

-- Insertar los idiomas en la tabla imdb_movies
DO $$
DECLARE
    movie_record RECORD;
    language_text TEXT;
    languages_array TEXT[];
BEGIN
    FOR movie_record IN SELECT movieid, language FROM imdb_movielanguages
    LOOP
        languages_array := string_to_array(movie_record.language, ',');

        FOREACH language_text IN ARRAY languages_array
        LOOP
            UPDATE imdb_movies
            SET languages = COALESCE(languages, '') || CASE WHEN languages IS NOT NULL AND languages <> '' THEN ',' ELSE '' END || TRIM(language_text)
            WHERE movieid = movie_record.movieid;
        END LOOP;
    END LOOP;
END $$;

-- Insertar los países en la tabla imdb_movies
DO $$
DECLARE
    movie_record RECORD;
    country_text TEXT;
    countries_array TEXT[];
BEGIN
    FOR movie_record IN SELECT movieid, country FROM imdb_moviecountries
    LOOP
        countries_array := string_to_array(movie_record.country, ',');

        FOREACH country_text IN ARRAY countries_array
        LOOP
            UPDATE imdb_movies
            SET countries = COALESCE(countries, '') || CASE WHEN countries IS NOT NULL AND countries <> '' THEN ',' ELSE '' END || TRIM(country_text)
            WHERE movieid = movie_record.movieid;
        END LOOP;
    END LOOP;
END $$;

-- Modificar la tabla imdb_actormovies para mejorar la estructura
ALTER TABLE imdb_actormovies ADD PRIMARY KEY (actorid, movieid);
CREATE INDEX IF NOT EXISTS idx_imdb_actormovies_actorid_movieid ON imdb_actormovies (actorid, movieid);

-- Mantener las columnas de imdb_actormovies como SMALLINT
ALTER TABLE imdb_actormovies
    ALTER COLUMN isvoice SET DATA TYPE SMALLINT,
    ALTER COLUMN isarchivefootage SET DATA TYPE SMALLINT,
    ALTER COLUMN isuncredited SET DATA TYPE SMALLINT;

-- Modificar la tabla imdb_directormovies para mejorar la estructura
ALTER TABLE imdb_directormovies DROP CONSTRAINT IF EXISTS imdb_directormovies_pkey;
ALTER TABLE imdb_directormovies ADD PRIMARY KEY (directorid, movieid);
CREATE INDEX IF NOT EXISTS idx_imdb_directormovies_directorid_movieid ON imdb_directormovies (directorid, movieid);

-- Mantener las columnas de imdb_directormovies como SMALLINT
ALTER TABLE imdb_directormovies
    ALTER COLUMN isarchivefootage SET DATA TYPE SMALLINT,
    ALTER COLUMN isuncredited SET DATA TYPE SMALLINT,
    ALTER COLUMN iscodirector SET DATA TYPE SMALLINT,
    ALTER COLUMN ispilot SET DATA TYPE SMALLINT,
    ALTER COLUMN ischief SET DATA TYPE SMALLINT,
    ALTER COLUMN ishead SET DATA TYPE SMALLINT;

-- Eliminar las columnas antiguas y tablas no necesarias
DROP TABLE IF EXISTS imdb_moviegenres;
DROP TABLE IF EXISTS imdb_movielanguages;
DROP TABLE IF EXISTS imdb_moviecountries;
