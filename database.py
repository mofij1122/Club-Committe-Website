import sqlite3
from contextlib import contextmanager
import os

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), 'college_clubs.db')

# ═══════════════════════════════════════════════════════
# CONNECTION MANAGEMENT
# ═══════════════════════════════════════════════════════

def get_connection():
    """Create and return a database connection"""
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row  # Return rows as dictionaries
        return connection
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return None

@contextmanager
def get_db():
    """Context manager for database connections"""
    conn = get_connection()
    if not conn:
        raise Exception("Database connection failed")
    
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# ═══════════════════════════════════════════════════════
# DATABASE INITIALIZATION
# ═══════════════════════════════════════════════════════

def init_database():
    """Create tables and insert sample data"""
    conn = get_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clubs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            full_description TEXT,
            logo TEXT,
            meeting_time TEXT,
            meeting_location TEXT,
            contact_email TEXT,
            contact_phone TEXT,
            president_name TEXT,
            founded_year INTEGER,
            member_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            club_id INTEGER,
            name TEXT NOT NULL,
            role TEXT,
            photo TEXT DEFAULT 'default-avatar.png',
            bio TEXT,
            year TEXT,
            department TEXT,
            email TEXT,
            joined_date DATE,
            FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE CASCADE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            club_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            event_date DATE,
            event_time TEXT,
            location TEXT,
            image TEXT,
            status TEXT DEFAULT 'upcoming',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE CASCADE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS event_gallery (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER,
            image_path TEXT NOT NULL,
            caption TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS join_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            club_id INTEGER,
            student_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            year TEXT,
            department TEXT,
            reason TEXT,
            status TEXT DEFAULT 'pending',
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE CASCADE
        )
    """)
    
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM clubs")
    if cursor.fetchone()[0] == 0:
        # Insert sample clubs
        clubs_data = [
            ('Tech Innovators Club', 'Technology', 'Explore cutting-edge technology and innovation', 
             'The Tech Innovators Club is a vibrant community of students passionate about technology and innovation. We organize hackathons, coding workshops, tech talks with industry experts, and collaborative projects. Members gain hands-on experience with emerging technologies including AI, blockchain, cloud computing, and web development. Join us to build, learn, and innovate together!',
             'tech_logo.png', 'Every Friday, 4:00 PM - 6:00 PM', 'Computer Lab A-305', 'tech.innovators@college.edu', None, 'Rahul Sharma', 2018, 85),
            
            ('Lens & Shutter Photography', 'Arts & Media', 'Capture life through creative lenses',
             'Lens & Shutter is where photography enthusiasts come together to explore visual storytelling. We conduct photo walks, workshops on composition and editing, exhibitions, and inter-college competitions. Whether you\'re a beginner with a smartphone or an advanced DSLR user, we welcome all who see the world through a creative lens.',
             'photo_logo.png', 'Every Wednesday, 3:30 PM - 5:30 PM', 'Art Studio, 2nd Floor', 'lensshutter@college.edu', None, 'Priya Desai', 2015, 62),
            
            ('Drama & Theatre Society', 'Performing Arts', 'Unleash your theatrical potential',
             'The Drama & Theatre Society is your stage to shine! We produce full-length plays, skits, and performances throughout the year. Develop acting skills, stage management, and production expertise while building confidence and creativity.',
             'drama_logo.png', 'Monday & Thursday, 5:00 PM - 7:00 PM', 'Main Auditorium', 'drama.society@college.edu', None, 'Arjun Patel', 2012, 74),
            
            ('Green Earth Environmental Club', 'Social & Environment', 'Creating a sustainable campus future',
             'Green Earth is dedicated to environmental awareness and sustainable practices. We organize tree plantation drives, campus clean-up campaigns, waste segregation initiatives, workshops on climate change, and eco-friendly competitions.',
             'env_logo.png', 'Every Saturday, 9:00 AM - 12:00 PM', 'Campus Garden & Eco Center', 'greenearth@college.edu', None, 'Sneha Kulkarni', 2016, 93),
            
            ('Literary Circle', 'Literature & Writing', 'Words that inspire and transform',
             'The Literary Circle celebrates the power of words through poetry, prose, creative writing, and literary discussions. We host open mic nights, book club meetings, writing workshops, and publish an annual literary magazine.',
             'lit_logo.png', 'Every Tuesday, 4:30 PM - 6:00 PM', 'Library Reading Room', 'litcircle@college.edu', None, 'Kavya Menon', 2017, 56),
            
            ('Robotics & Automation Lab', 'Engineering & Innovation', 'Building the future with robotics',
             'The Robotics & Automation Lab brings together engineering minds to design, build, and program robots. We participate in national-level robotics competitions, conduct workshops on Arduino, Raspberry Pi, and IoT.',
             'robo_logo.png', 'Wednesday & Friday, 3:00 PM - 6:00 PM', 'Engineering Workshop Lab', 'robotics.lab@college.edu', None, 'Vikram Joshi', 2019, 48)
        ]
        
        cursor.executemany("""
            INSERT INTO clubs (name, category, description, full_description, logo, meeting_time, 
                             meeting_location, contact_email, contact_phone, president_name, founded_year, member_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, clubs_data)
        
        # Insert sample members
        members_data = [
            (1, 'Rahul Sharma', 'President', 'Final Year', 'Computer Science', 'rahul.s@college.edu', '2023-08-01'),
            (1, 'Amit Kumar', 'Vice President', 'Third Year', 'Information Technology', 'amit.k@college.edu', '2023-08-15'),
            (1, 'Neha Singh', 'Technical Lead', 'Third Year', 'Computer Science', 'neha.s@college.edu', '2023-09-01'),
            (2, 'Priya Desai', 'President', 'Final Year', 'Fine Arts', 'priya.d@college.edu', '2023-07-20'),
            (2, 'Rohan Mehta', 'Photography Head', 'Second Year', 'Media Studies', 'rohan.m@college.edu', '2024-08-05'),
            (3, 'Arjun Patel', 'President', 'Final Year', 'English Literature', 'arjun.p@college.edu', '2022-08-01'),
            (3, 'Kavya Nair', 'Director', 'Third Year', 'Performing Arts', 'kavya.n@college.edu', '2023-08-01'),
            (4, 'Sneha Kulkarni', 'President', 'Final Year', 'Environmental Science', 'sneha.k@college.edu', '2023-06-15'),
            (4, 'Vikram Joshi', 'Event Coordinator', 'Second Year', 'Biology', 'vikram.j@college.edu', '2024-08-20'),
            (5, 'Kavya Menon', 'President', 'Final Year', 'English Literature', 'kavya.m@college.edu', '2023-07-01'),
            (6, 'Vikram Joshi', 'President', 'Final Year', 'Electronics Engineering', 'vikram.joshi@college.edu', '2023-08-10')
        ]
        
        cursor.executemany("""
            INSERT INTO members (club_id, name, role, year, department, email, joined_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, members_data)
        
        # Insert sample events
        events_data = [
            (1, 'HackFest 2026', '24-hour coding marathon with exciting prizes', '2026-02-15', '9:00 AM', 'Main Auditorium', 'upcoming'),
            (1, 'AI/ML Workshop Series', 'Introduction to Machine Learning with Python', '2026-01-25', '2:00 PM', 'Computer Lab B-204', 'upcoming'),
            (2, 'Moments in Frame Exhibition', 'Annual showcase of best student photographs', '2026-02-01', '10:00 AM', 'College Art Gallery', 'upcoming'),
            (3, 'Annual Play: Romeo & Juliet', 'Classic Shakespearean performance', '2026-03-10', '6:00 PM', 'Main Auditorium', 'upcoming'),
            (4, 'Green Campus Drive', 'Plant 500 trees across campus', '2026-01-20', '7:00 AM', 'Campus Grounds', 'upcoming'),
            (5, 'Open Mic Night', 'Poetry, storytelling, and spoken word performances', '2026-01-22', '6:00 PM', 'Library Auditorium', 'upcoming'),
            (6, 'Robo Wars Competition', 'Battle of the bots - build and compete!', '2026-02-20', '9:00 AM', 'Engineering Workshop', 'upcoming')
        ]
        
        cursor.executemany("""
            INSERT INTO events (club_id, title, description, event_date, event_time, location, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, events_data)
        
        conn.commit()
        print("✅ Database initialized with sample data!")
    
    cursor.close()
    conn.close()
    return True

# ═══════════════════════════════════════════════════════
# CLUB QUERIES
# ═══════════════════════════════════════════════════════

def get_all_clubs():
    """Get all clubs with member count"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.*, COUNT(DISTINCT m.id) as actual_member_count
                FROM clubs c
                LEFT JOIN members m ON c.id = m.club_id
                GROUP BY c.id
                ORDER BY c.name
            """)
            clubs = [dict(row) for row in cursor.fetchall()]
            return clubs
    except Exception as e:
        print(f"Error in get_all_clubs: {e}")
        return []

def get_clubs_by_category(category):
    """Get clubs filtered by category"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.*, COUNT(DISTINCT m.id) as member_count
                FROM clubs c
                LEFT JOIN members m ON c.id = m.club_id
                WHERE c.category = ?
                GROUP BY c.id
                ORDER BY c.name
            """, (category,))
            clubs = [dict(row) for row in cursor.fetchall()]
            return clubs
    except Exception as e:
        print(f"Error in get_clubs_by_category: {e}")
        return []

def get_club_by_id(club_id):
    """Get single club by ID"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clubs WHERE id = ?", (club_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    except Exception as e:
        print(f"Error in get_club_by_id: {e}")
        return None

def get_all_categories():
    """Get all unique club categories"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT category FROM clubs ORDER BY category")
            categories = [row[0] for row in cursor.fetchall()]
            return categories
    except Exception as e:
        print(f"Error in get_all_categories: {e}")
        return []

def get_club_stats():
    """Get overall statistics"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) as total FROM clubs")
            total_clubs = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) as total FROM members")
            total_members = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) as total FROM events WHERE status = 'upcoming'")
            upcoming_events = cursor.fetchone()[0]
            
            return {
                'total_clubs': total_clubs,
                'total_members': total_members,
                'upcoming_events': upcoming_events
            }
    except Exception as e:
        print(f"Error in get_club_stats: {e}")
        return {'total_clubs': 0, 'total_members': 0, 'upcoming_events': 0}

# ═══════════════════════════════════════════════════════
# MEMBER QUERIES
# ═══════════════════════════════════════════════════════

def get_club_members(club_id):
    """Get all members of a club"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM members 
                WHERE club_id = ?
                ORDER BY 
                    CASE role
                        WHEN 'President' THEN 1
                        WHEN 'Vice President' THEN 2
                        WHEN 'Secretary' THEN 3
                        WHEN 'Treasurer' THEN 4
                        ELSE 5
                    END, name
            """, (club_id,))
            members = [dict(row) for row in cursor.fetchall()]
            return members
    except Exception as e:
        print(f"Error in get_club_members: {e}")
        return []

# ═══════════════════════════════════════════════════════
# EVENT QUERIES
# ═══════════════════════════════════════════════════════

def get_all_upcoming_events():
    """Get all upcoming events with club information"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.*, c.name as club_name, c.category
                FROM events e
                JOIN clubs c ON e.club_id = c.id
                WHERE e.status = 'upcoming'
                ORDER BY e.event_date, e.event_time
            """)
            events = [dict(row) for row in cursor.fetchall()]
            return events
    except Exception as e:
        print(f"Error in get_all_upcoming_events: {e}")
        return []

def get_club_events(club_id, limit=5):
    """Get upcoming events for a specific club"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM events 
                WHERE club_id = ? AND status = 'upcoming'
                ORDER BY event_date
                LIMIT ?
            """, (club_id, limit))
            events = [dict(row) for row in cursor.fetchall()]
            return events
    except Exception as e:
        print(f"Error in get_club_events: {e}")
        return []

# ═══════════════════════════════════════════════════════
# GALLERY QUERIES
# ═══════════════════════════════════════════════════════

def get_club_gallery(club_id, limit=12):
    """Get gallery photos for a specific club"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT eg.*, e.title as event_title
                FROM event_gallery eg
                JOIN events e ON eg.event_id = e.id
                WHERE e.club_id = ?
                ORDER BY eg.uploaded_at DESC
                LIMIT ?
            """, (club_id, limit))
            gallery = [dict(row) for row in cursor.fetchall()]
            return gallery
    except Exception as e:
        print(f"Error in get_club_gallery: {e}")
        return []

def get_all_gallery_photos(limit=50):
    """Get all gallery photos from all clubs"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT eg.*, e.title as event_title, c.name as club_name
                FROM event_gallery eg
                JOIN events e ON eg.event_id = e.id
                JOIN clubs c ON e.club_id = c.id
                ORDER BY eg.uploaded_at DESC
                LIMIT ?
            """, (limit,))
            photos = [dict(row) for row in cursor.fetchall()]
            return photos
    except Exception as e:
        print(f"Error in get_all_gallery_photos: {e}")
        return []

# ═══════════════════════════════════════════════════════
# JOIN REQUEST QUERIES
# ═══════════════════════════════════════════════════════

def create_join_request(club_id, student_name, email, phone, year, department, reason):
    """Create a new join request"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO join_requests (club_id, student_name, email, phone, year, department, reason, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'pending')
            """, (club_id, student_name, email, phone, year, department, reason))
            return cursor.lastrowid
    except Exception as e:
        print(f"Error in create_join_request: {e}")
        return None

# ═══════════════════════════════════════════════════════
# SEARCH FUNCTIONS
# ═══════════════════════════════════════════════════════

def search_clubs(query):
    """Search clubs by name or description"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            search_pattern = f"%{query}%"
            cursor.execute("""
                SELECT c.*, COUNT(DISTINCT m.id) as member_count
                FROM clubs c
                LEFT JOIN members m ON c.id = m.club_id
                WHERE c.name LIKE ? OR c.description LIKE ? OR c.category LIKE ?
                GROUP BY c.id
                ORDER BY c.name
            """, (search_pattern, search_pattern, search_pattern))
            clubs = [dict(row) for row in cursor.fetchall()]
            return clubs
    except Exception as e:
        print(f"Error in search_clubs: {e}")
        return []

def search_events(query):
    """Search events by title or description"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            search_pattern = f"%{query}%"
            cursor.execute("""
                SELECT e.*, c.name as club_name, c.category
                FROM events e
                JOIN clubs c ON e.club_id = c.id
                WHERE (e.title LIKE ? OR e.description LIKE ?) 
                AND e.status = 'upcoming'
                ORDER BY e.event_date
            """, (search_pattern, search_pattern))
            events = [dict(row) for row in cursor.fetchall()]
            return events
    except Exception as e:
        print(f"Error in search_events: {e}")
        return []

# ═══════════════════════════════════════════════════════
# MAIN - FOR TESTING
# ═══════════════════════════════════════════════════════

if __name__ == '__main__':
    print("🔍 Initializing SQLite Database...")
    print("=" * 50)
    
    if init_database():
        print("\n📊 Fetching club stats...")
        stats = get_club_stats()
        print(f"   Total Clubs: {stats['total_clubs']}")
        print(f"   Total Members: {stats['total_members']}")
        print(f"   Upcoming Events: {stats['upcoming_events']}")
        print(f"\n✅ Database is ready!")
        print(f"📁 Database file: {DB_PATH}")
