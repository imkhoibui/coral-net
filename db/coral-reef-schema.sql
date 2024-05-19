CREATE TABLE species (
    species_id SERIAL PRIMARY KEY,
    species_name TEXT,
)

CREATE TABLE species_images (
    image_id TEXT PRIMARY KEY,
    species_id INTEGER REFERENCES species(species_id),
    image_data BYTEA NOT NULL,
)

CREATE TABLE species_annotations (
    annotation_id SERIAL PRIMARY KEY,
    image_id INTEGER REFERENCES species_images(image_id),
    file_name TEXT,
    boxes FLOAT[4],
    labels INT,
    areas FLOAT,
    iscrowd INT,
)