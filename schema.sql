DROP TABLE IF EXISTS list_items CASCADE;
DROP TABLE IF EXISTS lists CASCADE;
DROP TABLE IF EXISTS topics CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- USERS table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- TOPICS table
CREATE TABLE topics (
  id SERIAL PRIMARY KEY,
  owner INT NOT NULL REFERENCES users(id),
  title VARCHAR(100) NOT NULL,
  description TEXT,
  category TEXT CHECK (
    category IN ('anime','movies','music','tv','video games')
  ),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- LISTS table
CREATE TABLE lists (
  id SERIAL PRIMARY KEY,
  topic_id INT NOT NULL REFERENCES topics(id),
  author_id INT NOT NULL REFERENCES users(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE (topic_id, author_id)
);

-- LIST ITEMS table
CREATE TABLE list_items (
  id SERIAL PRIMARY KEY,
  list_id INT NOT NULL REFERENCES lists(id) ON DELETE CASCADE,
  rank INT NOT NULL CHECK (rank BETWEEN 1 AND 5),
  ext_id TEXT NOT NULL,
  notes TEXT,
  UNIQUE (list_id, rank)           
);
