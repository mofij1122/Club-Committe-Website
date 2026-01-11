from flask import Flask, render_template, request, redirect, url_for, flash
import database as db
import os

APP_NAME = "SGM Clubs & Committees"

app = Flask(__name__)
app.secret_key = os.environ.get("CLUB_SECRET_KEY", "club-dev-secret-key-change-in-production")

# ═══════════════════════════════════════════════════════
# ROUTES
# ═══════════════════════════════════════════════════════

@app.route('/')
def index():
    """Home page with club overview"""
    try:
        clubs = db.get_all_clubs()
        stats = db.get_club_stats()
        return render_template('index.html', app_name=APP_NAME, clubs=clubs, stats=stats)
    except Exception as e:
        flash(f'Error loading data: {str(e)}', 'danger')
        print(f"Error in index: {e}")
        return render_template('index.html', app_name=APP_NAME, clubs=[], stats={'total_clubs': 0, 'total_members': 0, 'upcoming_events': 0})

@app.route('/clubs')
def clubs_list():
    """List all clubs with filtering"""
    try:
        category_filter = request.args.get('category', '')
        categories = db.get_all_categories()
        
        if category_filter:
            clubs = db.get_clubs_by_category(category_filter)
        else:
            clubs = db.get_all_clubs()
        
        return render_template('clubs.html', app_name=APP_NAME, clubs=clubs, 
                             categories=categories, selected_category=category_filter)
    except Exception as e:
        flash(f'Error loading clubs: {str(e)}', 'danger')
        print(f"Error in clubs_list: {e}")
        return render_template('clubs.html', app_name=APP_NAME, clubs=[], categories=[], selected_category='')

@app.route('/club/<int:club_id>')
def club_detail(club_id):
    """Individual club detail page"""
    try:
        club = db.get_club_by_id(club_id)
        
        if not club:
            flash('Club not found', 'warning')
            return redirect(url_for('clubs_list'))
        
        members = db.get_club_members(club_id)
        events = db.get_club_events(club_id, limit=5)
        gallery = db.get_club_gallery(club_id, limit=12)
        
        return render_template('club_detail.html', app_name=APP_NAME, club=club, 
                             members=members, events=events, gallery=gallery)
    except Exception as e:
        flash(f'Error loading club details: {str(e)}', 'danger')
        print(f"Error in club_detail: {e}")
        import traceback
        traceback.print_exc()
        return redirect(url_for('clubs_list'))

@app.route('/events')
def events_list():
    """List all upcoming events"""
    try:
        events = db.get_all_upcoming_events()
        return render_template('events.html', app_name=APP_NAME, events=events)
    except Exception as e:
        flash(f'Error loading events: {str(e)}', 'danger')
        print(f"Error in events_list: {e}")
        return render_template('events.html', app_name=APP_NAME, events=[])

@app.route('/join/<int:club_id>', methods=['GET', 'POST'])
def join_club(club_id):
    """Join club form"""
    try:
        club = db.get_club_by_id(club_id)
        
        if not club:
            flash('Club not found', 'warning')
            return redirect(url_for('clubs_list'))
        
        if request.method == 'POST':
            # Get form data
            student_name = request.form.get('student_name', '').strip()
            email = request.form.get('email', '').strip()
            phone = request.form.get('phone', '').strip()
            year = request.form.get('year', '').strip()
            department = request.form.get('department', '').strip()
            reason = request.form.get('reason', '').strip()
            
            # Validate required fields
            if not student_name:
                flash('Please enter your name', 'warning')
                return render_template('join.html', app_name=APP_NAME, club=club)
            
            if not email:
                flash('Please enter your email', 'warning')
                return render_template('join.html', app_name=APP_NAME, club=club)
            
            if not year:
                flash('Please select your year', 'warning')
                return render_template('join.html', app_name=APP_NAME, club=club)
            
            if not department:
                flash('Please enter your department', 'warning')
                return render_template('join.html', app_name=APP_NAME, club=club)
            
            # Create join request
            try:
                request_id = db.create_join_request(club_id, student_name, email, phone, year, department, reason)
                
                if request_id:
                    flash(f'✅ Your request to join {club["name"]} has been submitted successfully!', 'success')
                    return redirect(url_for('join_success', club_id=club_id))
                else:
                    flash('Failed to submit join request. Please try again.', 'danger')
                    return render_template('join.html', app_name=APP_NAME, club=club)
                    
            except Exception as e:
                flash(f'Database error: {str(e)}', 'danger')
                print(f"Error creating join request: {e}")
                import traceback
                traceback.print_exc()
                return render_template('join.html', app_name=APP_NAME, club=club)
        
        # GET request - show form
        return render_template('join.html', app_name=APP_NAME, club=club)
        
    except Exception as e:
        flash(f'Error processing request: {str(e)}', 'danger')
        print(f"Error in join_club: {e}")
        import traceback
        traceback.print_exc()
        return redirect(url_for('clubs_list'))

@app.route('/join-success/<int:club_id>')
def join_success(club_id):
    """Join request success page"""
    try:
        club = db.get_club_by_id(club_id)
        if not club:
            flash('Club not found', 'warning')
            return redirect(url_for('clubs_list'))
        
        return render_template('join_success.html', app_name=APP_NAME, club=club)
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('clubs_list'))

@app.route('/gallery')
def gallery():
    """Photo gallery from all clubs"""
    try:
        photos = db.get_all_gallery_photos(limit=50)
        return render_template('gallery.html', app_name=APP_NAME, photos=photos)
    except Exception as e:
        flash(f'Error loading gallery: {str(e)}', 'danger')
        print(f"Error in gallery: {e}")
        return render_template('gallery.html', app_name=APP_NAME, photos=[])

@app.route('/search')
def search():
    """Search clubs and events"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return redirect(url_for('index'))
    
    try:
        clubs = db.search_clubs(query)
        events = db.search_events(query)
        return render_template('search_results.html', app_name=APP_NAME, 
                             query=query, clubs=clubs, events=events)
    except Exception as e:
        flash(f'Error performing search: {str(e)}', 'danger')
        print(f"Error in search: {e}")
        return redirect(url_for('index'))

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', app_name=APP_NAME), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html', app_name=APP_NAME), 500

if __name__ == '__main__':
    print("🚀 Starting College Clubs Website...")
    print("=" * 50)
    
    # Initialize database
    try:
        db.init_database()
        print("✅ Database ready!")
    except Exception as e:
        print(f"❌ Database error: {e}")
    
    print("\n🌐 Server running at: http://127.0.0.1:5000")
    print("=" * 50)
    
    app.run(debug=True, port=5000)
