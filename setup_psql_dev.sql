CREATE DATABASE goodreads_clone_dev_db;

CREATE USER goodreads_clone_dev WITH PASSWORD 'Goodreads_clone_dev_pwd123';

GRANT ALL PRIVILEGES ON DATABASE goodreads_clone_dev_db TO goodreads_clone_dev;

-- Reset the sequence to the maximum value in the communities_community table
SELECT setval('communities_community_id_seq', (SELECT MAX(id) FROM communities_community));

-- Create a function to update the sequence
CREATE OR REPLACE FUNCTION update_community_id_seq()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM setval('communities_community_id_seq', MAX(id)) FROM communities_community;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create a trigger to call the function after insert
CREATE TRIGGER update_community_id_seq_trigger
AFTER INSERT ON communities_community
FOR EACH STATEMENT
EXECUTE FUNCTION update_community_id_seq();

-- Sample INSERT statement for the communities_community table
INSERT INTO communities_community (name, description, date_added, owner_id, image)
VALUES ('Sample Community', 'This is a sample community description.', NOW(), 1, 'sample_image.jpg');
