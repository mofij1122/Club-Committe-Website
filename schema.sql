CREATE DATABASE IF NOT EXISTS college_clubs;
USE college_clubs;

CREATE TABLE clubs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT,
    full_description TEXT,
    logo VARCHAR(255),
    meeting_time VARCHAR(100),
    meeting_location VARCHAR(100),
    contact_email VARCHAR(100),
    contact_phone VARCHAR(20),
    president_name VARCHAR(100),
    founded_year INT,
    member_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE members (
    id INT PRIMARY KEY AUTO_INCREMENT,
    club_id INT,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(50),
    photo VARCHAR(255) DEFAULT 'default-avatar.png',
    bio TEXT,
    year VARCHAR(20),
    department VARCHAR(100),
    email VARCHAR(100),
    joined_date DATE,
    FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE CASCADE
);

CREATE TABLE events (
    id INT PRIMARY KEY AUTO_INCREMENT,
    club_id INT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    event_date DATE,
    event_time VARCHAR(50),
    location VARCHAR(100),
    image VARCHAR(255),
    status VARCHAR(20) DEFAULT 'upcoming',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE CASCADE
);

CREATE TABLE event_gallery (
    id INT PRIMARY KEY AUTO_INCREMENT,
    event_id INT,
    image_path VARCHAR(255) NOT NULL,
    caption TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);

CREATE TABLE join_requests (
    id INT PRIMARY KEY AUTO_INCREMENT,
    club_id INT,
    student_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    year VARCHAR(20),
    department VARCHAR(100),
    reason TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE CASCADE
);

-- Sample Data
INSERT INTO clubs (name, category, description, full_description, logo, meeting_time, meeting_location, contact_email, president_name, founded_year, member_count) VALUES
('Tech Innovators Club', 'Technology', 'Explore cutting-edge technology and innovation', 'The Tech Innovators Club is a vibrant community of students passionate about technology and innovation. We organize hackathons, coding workshops, tech talks with industry leaders, and collaborative projects. Members gain hands-on experience with emerging technologies including AI, blockchain, cloud computing, and web development. Join us to build, learn, and innovate together!', 'tech_logo.png', 'Every Friday, 4:00 PM - 6:00 PM', 'Computer Lab A-305', 'tech.innovators@college.edu', 'Rahul Sharma', 2018, 85),

('Lens & Shutter Photography', 'Arts & Media', 'Capture life through creative lenses', 'Lens & Shutter is where photography enthusiasts come together to explore visual storytelling. We conduct photo walks, workshops on composition and editing, exhibitions, and inter-college competitions. Whether you\'re a beginner with a smartphone or an advanced DSLR user, we welcome all who see the world through a creative lens. Learn techniques, share your work, and grow your portfolio with us.', 'photo_logo.png', 'Every Wednesday, 3:30 PM - 5:30 PM', 'Art Studio, 2nd Floor', 'lensshutter@college.edu', 'Priya Desai', 2015, 62),

('Drama & Theatre Society', 'Performing Arts', 'Unleash your theatrical potential', 'The Drama & Theatre Society is your stage to express, perform, and create magic. We produce full-length plays, street plays, skits, and participate in inter-college festivals. Our members learn acting techniques, stage management, scriptwriting, direction, and production. Beyond performances, we build confidence, teamwork, and creative expression. All are welcome - actors, backstage crew, and theatre lovers!', 'drama_logo.png', 'Monday & Thursday, 5:00 PM - 7:00 PM', 'Main Auditorium', 'drama.society@college.edu', 'Arjun Patel', 2012, 74),

('Green Earth Environmental Club', 'Social & Environment', 'Creating a sustainable campus future', 'Green Earth is dedicated to environmental awareness and sustainable practices. We organize tree plantation drives, campus clean-up campaigns, waste segregation initiatives, workshops on climate change, and eco-friendly competitions. Our mission is to create an environmentally conscious community and make our campus greener. Join us to make a real difference for our planet - every small action counts toward a sustainable future.', 'env_logo.png', 'Every Saturday, 9:00 AM - 12:00 PM', 'Campus Garden & Eco Center', 'greenearth@college.edu', 'Sneha Kulkarni', 2016, 93),

('Literary Circle', 'Literature & Writing', 'Words that inspire and transform', 'The Literary Circle celebrates the power of words through poetry, prose, creative writing, and literary discussions. We host open mic nights, book club meetings, writing workshops, and publish an annual literary magazine. Members explore diverse genres, sharpen their writing skills, and engage in meaningful discussions about literature and life. Whether you write, read, or simply love stories, you belong here.', 'lit_logo.png', 'Every Tuesday, 4:30 PM - 6:00 PM', 'Library Reading Room', 'litcircle@college.edu', 'Kavya Menon', 2017, 56),

('Robotics & Automation Lab', 'Engineering & Innovation', 'Building the future with robotics', 'The Robotics & Automation Lab brings together engineering minds to design, build, and program robots. We participate in national-level robotics competitions, conduct workshops on Arduino, Raspberry Pi, and IoT, and work on innovative automation projects. From beginners to advanced builders, we provide resources, mentorship, and a collaborative space to turn ideas into working prototypes.', 'robo_logo.png', 'Wednesday & Friday, 3:00 PM - 6:00 PM', 'Engineering Workshop Lab', 'robotics.lab@college.edu', 'Vikram Joshi', 2019, 48);

-- Members Data
INSERT INTO members (club_id, name, role, year, department, email, joined_date) VALUES
(1, 'Rahul Sharma', 'President', 'Final Year', 'Computer Science', 'rahul.s@college.edu', '2023-08-01'),
(1, 'Amit Kumar', 'Vice President', 'Third Year', 'Information Technology', 'amit.k@college.edu', '2023-08-15'),
(1, 'Neha Singh', 'Technical Lead', 'Third Year', 'Computer Science', 'neha.s@college.edu', '2023-09-01'),
(1, 'Rohan Verma', 'Event Coordinator', 'Second Year', 'Computer Science', 'rohan.v@college.edu', '2024-01-10'),

(2, 'Priya Desai', 'President', 'Final Year', 'Fine Arts', 'priya.d@college.edu', '2023-07-20'),
(2, 'Rohan Mehta', 'Photography Head', 'Second Year', 'Media Studies', 'rohan.m@college.edu', '2024-08-05'),
(2, 'Ananya Roy', 'Social Media Manager', 'Third Year', 'Mass Communication', 'ananya.r@college.edu', '2023-09-10'),

(3, 'Arjun Patel', 'President', 'Final Year', 'English Literature', 'arjun.p@college.edu', '2022-08-01'),
(3, 'Kavya Nair', 'Director', 'Third Year', 'Performing Arts', 'kavya.n@college.edu', '2023-08-01'),
(3, 'Siddharth Rao', 'Stage Manager', 'Second Year', 'Theatre Arts', 'siddharth.r@college.edu', '2024-07-15'),

(4, 'Sneha Kulkarni', 'President', 'Final Year', 'Environmental Science', 'sneha.k@college.edu', '2023-06-15'),
(4, 'Vikram Joshi', 'Event Coordinator', 'Second Year', 'Biology', 'vikram.j@college.edu', '2024-08-20'),
(4, 'Diya Sharma', 'Volunteer Head', 'Third Year', 'Environmental Studies', 'diya.s@college.edu', '2023-10-01'),

(5, 'Kavya Menon', 'President', 'Final Year', 'English Literature', 'kavya.m@college.edu', '2023-07-01'),
(5, 'Aditya Singh', 'Editor-in-Chief', 'Third Year', 'Journalism', 'aditya.s@college.edu', '2023-09-15'),

(6, 'Vikram Joshi', 'President', 'Final Year', 'Electronics Engineering', 'vikram.joshi@college.edu', '2023-08-10'),
(6, 'Tanvi Patel', 'Technical Head', 'Third Year', 'Mechatronics', 'tanvi.p@college.edu', '2023-09-20');

-- Events Data
INSERT INTO events (club_id, title, description, event_date, event_time, location, status) VALUES
(1, 'HackFest 2026', '24-hour coding marathon with exciting prizes and mentorship from industry experts', '2026-02-15', '9:00 AM - Next Day 9:00 AM', 'Main Auditorium', 'upcoming'),
(1, 'AI/ML Workshop Series', 'Introduction to Machine Learning with Python - hands-on session', '2026-01-25', '2:00 PM - 5:00 PM', 'Computer Lab B-204', 'upcoming'),
(1, 'Tech Talk: Cloud Computing', 'Industry expert session on AWS and cloud architecture', '2026-01-18', '4:00 PM - 6:00 PM', 'Seminar Hall', 'upcoming'),

(2, 'Moments in Frame Exhibition', 'Annual showcase of best student photographs from the year', '2026-02-01', '10:00 AM - 6:00 PM', 'College Art Gallery', 'upcoming'),
(2, 'Night Photography Workshop', 'Learn long exposure and night sky photography techniques', '2026-01-20', '7:00 PM - 10:00 PM', 'Campus Grounds', 'upcoming'),

(3, 'Annual Play: Romeo & Juliet', 'Classic Shakespearean performance with modern direction', '2026-03-10', '6:00 PM - 9:00 PM', 'Main Auditorium', 'upcoming'),
(3, 'Street Play Festival', 'Social awareness through street theatre performances', '2026-02-05', '3:00 PM - 6:00 PM', 'Campus Quadrangle', 'upcoming'),

(4, 'Green Campus Drive', 'Plant 500 trees across campus - volunteers needed!', '2026-01-20', '7:00 AM - 12:00 PM', 'Campus Grounds', 'upcoming'),
(4, 'Zero Waste Workshop', 'Learn composting, upcycling, and sustainable living practices', '2026-01-28', '10:00 AM - 1:00 PM', 'Eco Center', 'upcoming'),

(5, 'Open Mic Night', 'Poetry, storytelling, and spoken word performances', '2026-01-22', '6:00 PM - 9:00 PM', 'Library Auditorium', 'upcoming'),
(5, 'Author Meet: Bestselling Novelist', 'Interactive session with renowned author', '2026-02-10', '4:00 PM - 6:00 PM', 'Seminar Hall', 'upcoming'),

(6, 'Robo Wars Competition', 'Battle of the bots - build and compete!', '2026-02-20', '9:00 AM - 5:00 PM', 'Engineering Workshop', 'upcoming');
