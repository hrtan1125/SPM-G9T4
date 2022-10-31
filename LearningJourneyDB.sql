create table Learning_Journey
(lj_id int(11) NOT NULL auto_increment,
title VARCHAR(50) DEFAULT NULL,
role_id int NOT NULL,
staff_id int NOT NULL,
CONSTRAINT PRIMARY KEY(lj_id));

create table Learning_Journey_Courses
(row_id int(11) NOT NULL auto_increment,
lj_id int NOT NULL,
skill_code VARCHAR(20) DEFAULT NULL,
course_id VARCHAR(20) NOT NULL,
CONSTRAINT PRIMARY KEY(row_id));

INSERT INTO Learning_Journey (title, role_id, staff_id) VALUES
('LJ1', 123, 321),
('LJ2', 123, 321),
('LJ3', 345, 321),
('LJ4', 345, 321),
('LJ5', 345, 321);

INSERT INTO Learning_Journey_Courses (lj_id, skill_code, course_id) VALUES
(123, 'French', 'merci bercoup'),
(123, 'German', 'danke sehr'),
(345, 'Chinese', 'xie xie'),
(345, 'Malay', 'terima kaseh'),
(345, 'English', 'thank you');

