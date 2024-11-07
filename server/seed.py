from datetime import datetime, timezone
from app import create_app, db  
from models import User, Asset, Category, Request, RequestHistory, UserRole, AssetStatus, RequestType, UrgencyLevel, RequestStatus

# Create sample categories
categories = [
    Category(category_name='Electronics', description='Electronic devices such as laptops, desktops, etc.'),
    Category(category_name='Furniture', description='Office furniture including desks, chairs, etc.'),
    Category(category_name='Stationery', description='Office stationery such as pens, paper, etc.')
]

# Create sample users
users = [
    User(username='john_doe', password='password123', role=UserRole.Admin, email='john@example.com'),
    User(username='jane_smith', password='password456', role=UserRole.Procurement_Manager, email='jane@example.com'),
    User(username='alice_walker', password='password789', role=UserRole.Employee, email='alice@example.com')
]

# Create sample assets
assets = [
    Asset(name='Dell Laptop', description='14-inch, 8GB RAM, Intel i5 processor laptop.', category_id=1, status=AssetStatus.Available, image_url='https://example.com/images/dell-laptop.jpg'),
    Asset(name='Office Chair', description='Ergonomic chair with lumbar support.', category_id=2, status=AssetStatus.Allocated, image_url='https://example.com/images/office-chair.jpg', allocated_to=1),  # Allocated to John Doe
    Asset(name='Projector', description='4K resolution projector for office presentations.', category_id=1, status=AssetStatus.Under_Repair, image_url='https://example.com/images/projector.jpg'),
    Asset(name='Samsung Monitor', description='27-inch curved monitor, 4K resolution.', category_id=1, status=AssetStatus.Available, image_url='https://example.com/images/samsung-monitor.jpg'),
    Asset(name='Desk Lamp', description='Adjustable LED desk lamp.', category_id=2, status=AssetStatus.Available, image_url='https://example.com/images/desk-lamp.jpg')
]

# Create sample requests
requests = [
    Request(user_id=2, asset_id=None, request_type=RequestType.New_Asset, reason='New laptop needed for work.', quantity=1, urgency=UrgencyLevel.High, status=RequestStatus.Pending),
    Request(user_id=3, asset_id=4, request_type=RequestType.Repair, reason='Monitor screen flickering.', quantity=1, urgency=UrgencyLevel.Medium, status=RequestStatus.Pending),
    Request(user_id=1, asset_id=2, request_type=RequestType.Repair, reason='Chair has a broken wheel.', quantity=1, urgency=UrgencyLevel.Low, status=RequestStatus.Approved)
]

# Create sample request histories
request_histories = [
    RequestHistory(request_id=1, status=RequestStatus.Pending, comments='Request created and awaiting approval.'),
    RequestHistory(request_id=2, status=RequestStatus.Pending, comments='Request created and awaiting repair.'),
    RequestHistory(request_id=3, status=RequestStatus.Approved, comments='Request approved for repair.')
]

# Insert data into the database
def seed_data():
    # Add categories to the database
    db.session.add_all(categories)
    
    # Add users to the database
    db.session.add_all(users)
    
    # Add assets to the database
    db.session.add_all(assets)
    
    # Add requests to the database
    db.session.add_all(requests)
    
    # Add request histories to the database
    db.session.add_all(request_histories)
    
    # Commit all changes to the database
    db.session.commit()

    print("Database seeded successfully.")

if __name__ == '__main__':
    # Create the Flask app context and run the seeding process
    app = create_app()  # Initialize the Flask app using your create_app function
    with app.app_context():  # Set the app context for database operations
        seed_data()