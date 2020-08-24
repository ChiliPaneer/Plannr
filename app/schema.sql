-- The user table which contains information about each user
CREATE TABLE user (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  profile_pic TEXT NOT NULL
);

-- The calendar table which contains the ids of each google calendar
-- and the id and email of the user that created the calendar
CREATE TABLE calendar (
    calendar_id TEXT PRIMARY KEY,
    email TEXT NOT NULL,
    user_id TEXT NOT NULL
);

CREATE TABLE group (
  group_id TEXT PRIMARY KEY,
  email TEXT NOT NULL,
  user_id TEXT NOT NULL
)