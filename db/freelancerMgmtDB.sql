PRAGMA foreign_keys = OFF;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS workHistory;
DROP TABLE IF EXISTS assignments;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS organizations;
DROP TABLE IF EXISTS freelancerSkills;
DROP TABLE IF EXISTS skills;
DROP TABLE IF EXISTS profiles;
PRAGMA foreign_keys = ON;

-- Freelancer Profiles table
CREATE TABLE IF NOT EXISTS profiles (
    flID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    rate REAL NOT NULL,
    availability TEXT NOT NULL
);

INSERT OR IGNORE INTO profiles (name, rate, availability) VALUES
('Adrian Smith', 50, '2025-01-10'),
('Dung Long', 45, '2025-01-22'),
('David Hong', 60, '2025-01-10'),
('Mike Brom', 45, '2025-02-01'),
('Andrew Kumar', 55, '2025-02-22');


-- Skills table
CREATE TABLE IF NOT EXISTS skills (
    skillID INTEGER PRIMARY KEY AUTOINCREMENT,
    skillName TEXT NOT NULL
);

INSERT OR IGNORE INTO skills (skillName) VALUES
('Web Development'),
('Graphic Design'),
('Content Writing'),
('Data Analysis'),
('Digital Marketing'),
('Software Development');

-- Freelancer Skills Table (N:N relation between profiles and skills)
CREATE TABLE IF NOT EXISTS freelancerSkills (
    flID INTEGER NOT NULL, -- profiles table PK
    skillID INTEGER NOT NULL, -- skills table PK
    PRIMARY KEY (flID, skillID), -- composite primary key
    FOREIGN KEY (flID) REFERENCES profiles(flID),
    FOREIGN KEY (skillID) REFERENCES skills(skillID)
);

INSERT OR IGNORE INTO freelancerSkills (flID, skillID) VALUES
(1, 1), (1, 2),
(2, 3), (2, 4),         
(3, 3), (3, 4), (3, 5),
(4, 4), (4, 5),
(5, 1), (5, 6); 					

-- Organizations table
CREATE TABLE IF NOT EXISTS organizations (
    organizationID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

INSERT OR IGNORE INTO organizations (name) VALUES
('Alpha Techs'),
('IREP Inc'),
('Nokia Inc');

-- Projects table
CREATE TABLE IF NOT EXISTS projects (
    projectID INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    budget REAL NOT NULL,
    organizationID INTEGER NOT NULL, -- Organizations table Foreign key
    FOREIGN KEY (organizationID) REFERENCES organizations(organizationID)
);

INSERT OR IGNORE INTO projects (title, budget, organizationID) VALUES
('Website Redesign', 10000, 1),
('Content Creation', 5000, 2),
('Marketing Materials', 7000, 3);

-- assignments (N:N between profiles and projects)
CREATE TABLE IF NOT EXISTS assignments (
    flID INTEGER NOT NULL,
    projectID INTEGER NOT NULL,
    PRIMARY KEY (flID, projectID), -- composite key
    FOREIGN KEY (flID) REFERENCES profiles(flID),
    FOREIGN KEY (projectID) REFERENCES projects(projectID)
);

-- assginment of freelancers to projects based on need
INSERT OR IGNORE INTO assignments (flID, projectID) VALUES
(1, 1),                              -- Adrian Smith assigned to  Website redesign project for Alpha Techs
(2, 2),                              -- Dung Long assigned to  content creation project for IREP Inc
(3, 3),                              -- David Hong assigned to Marketing Materials project for Nokia Inc
(4, 3),                              -- Mike Brom assigned to Marketing Materials project for Nokia Inc.
(5, 1);                              -- Andrew Kumar assigned to Alpha Techs Website Redesign project

-- work history tab
CREATE TABLE IF NOT EXISTS workHistory (
    historyID INTEGER PRIMARY KEY AUTOINCREMENT,
    comments TEXT,
    role TEXT,
    flID INTEGER NOT NULL,
    projectID INTEGER NOT NULL,
    FOREIGN KEY (flID) REFERENCES profiles(flID),
    FOREIGN KEY (projectID) REFERENCES projects(projectID)
);

INSERT OR IGNORE INTO workHistory (comments, role, flID, projectID) VALUES
('Great Work', 'UI/UX Designer', 1, 1),
('Good Work', 'Content Writer', 2, 2),
('No Complaints', 'Data Analyst', 3, 3),
('Excellent Work', 'Marketing Lead', 4, 3),
('Top-notch Work', 'Software Developer', 5, 1);

-- reviews
CREATE TABLE IF NOT EXISTS reviews (
    reviewID INTEGER PRIMARY KEY AUTOINCREMENT,
    rating REAL NOT NULL,
    flID INTEGER NOT NULL,
    projectID INTEGER NOT NULL,
    FOREIGN KEY (flID) REFERENCES profiles(flID),
    FOREIGN KEY (projectID) REFERENCES projects(projectID)
);

INSERT OR IGNORE INTO reviews (rating, flID, projectID) VALUES
(4.8, 1, 1),
(4.5, 2, 2),
(4.9, 3, 3),
(4.7, 4, 3),
(4.3, 5, 1);



