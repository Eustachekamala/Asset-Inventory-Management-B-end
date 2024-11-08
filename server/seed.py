from datetime import datetime, timezone
from app import db  
from models import User, Asset, Category, Request, RequestHistory, UserRole, AssetStatus, RequestType, UrgencyLevel, RequestStatus

# Create sample categories
categories = [
    Category(category_name='Electronics', description='Electronic devices such as laptops, desktops, etc.'),
    Category(category_name='Furniture', description='Office furniture including desks, chairs, etc.'),
    Category(category_name='Stationery', description='Office stationery such as pens, paper, etc.')
]

# Create sample users with timezone-aware timestamps for created_at field
users = [
    User(
        username='john_doe', 
        password='password123', 
        role=UserRole.Admin, 
        email='john@example.com', 
        created_at=datetime.now(timezone.utc)
    ),
    User(
        username='jane_smith', 
        password='password456', 
        role=UserRole.Procurement_Manager, 
        email='jane@example.com', 
        created_at=datetime.now(timezone.utc)
    ),
    User(
        username='alice_walker', 
        password='password789', 
        role=UserRole.Employee, 
        email='alice@example.com', 
        created_at=datetime.now(timezone.utc) 
    )
]

# Create sample assets
assets = [
    Asset(
        name='Dell Laptop', 
        description='14-inch, 8GB RAM, Intel i5 processor laptop.', 
        status=AssetStatus.Available, 
        image_url='https://example.com/images/dell-laptop.jpg',
        created_at=datetime.now(timezone.utc)
    ),
    Asset(
        name='Office Chair', 
        description='Ergonomic chair with lumbar support.', 
        status=AssetStatus.Allocated, 
        image_url='https://example.com/images/office-chair.jpg', 
        allocated_to=1,  # Allocated to John Doe
        created_at=datetime.now(timezone.utc) 
    ),
    Asset(
        name='Projector', 
        description='4K resolution projector for office presentations.', 
        status=AssetStatus.Under_Repair, 
        image_url='https://example.com/images/projector.jpg',
        created_at=datetime.now(timezone.utc) 
    ),
    Asset(
        name='Samsung Monitor', 
        description='27-inch curved monitor, 4K resolution.', 
        status=AssetStatus.Available, 
        image_url='https://example.com/images/samsung-monitor.jpg',
        created_at=datetime.now(timezone.utc)
    ),
    Asset(
        name='Desk Lamp', 
        description='Adjustable LED desk lamp.', 
        status=AssetStatus.Available, 
        image_url='https://example.com/images/desk-lamp.jpg',
        created_at=datetime.now(timezone.utc) 
    )
]

# Create sample requests with timezone-aware timestamps
requests = [
    Request(
        user_id=2, 
        asset_id=None, 
        request_type=RequestType.New_Asset, 
        reason='New laptop needed for work.', 
        quantity=1, 
        urgency=UrgencyLevel.High, 
        status=RequestStatus.Pending,
        created_at=datetime.now(timezone.utc)
    ),
    Request(
        user_id=3, 
        asset_id=4, 
        request_type=RequestType.Repair, 
        reason='Monitor screen flickering.', 
        quantity=1, 
        urgency=UrgencyLevel.Medium, 
        status=RequestStatus.Pending,
        created_at=datetime.now(timezone.utc)
    ),
    Request(
        user_id=1, 
        asset_id=2, 
        request_type=RequestType.Repair, 
        reason='Chair has a broken wheel.', 
        quantity=1, 
        urgency=UrgencyLevel.Low, 
        status=RequestStatus.Approved,
        created_at=datetime.now(timezone.utc)
    )
]

# Create sample request histories with timezone-aware timestamps
request_histories = [
    RequestHistory(
        request_id=1, 
        status=RequestStatus.Pending, 
        comments='Request created and awaiting approval.',
        created_at=datetime.now(timezone.utc)
    ),
    RequestHistory(
        request_id=2, 
        status=RequestStatus.Pending, 
        comments='Request created and awaiting repair.',
        created_at=datetime.now(timezone.utc) 
    ),
    RequestHistory(
        request_id=3, 
        status=RequestStatus.Approved, 
        comments='Request approved for repair.',
        created_at=datetime.now(timezone.utc)
    )
]

# Insert data into the database
def seed_data():
    # Add categories to the database
    db.session.add_all(categories)
    db.session.commit() 

    # Fetch category ids after they are inserted into the database
    electronics_category = Category.query.filter_by(category_name='Electronics').first()
    furniture_category = Category.query.filter_by(category_name='Furniture').first()
    stationery_category = Category.query.filter_by(category_name='Stationery').first()

    # Create and add assets
    assets[0].category_id = electronics_category.category_id  
    assets[1].category_id = furniture_category.category_id    
    assets[2].category_id = electronics_category.category_id  
    assets[3].category_id = electronics_category.category_id  
    assets[4].category_id = furniture_category.category_id 

    db.session.add_all(assets)
    db.session.add_all(users)
    db.session.add_all(requests)
    db.session.add_all(request_histories)
    db.session.commit()

    print("Database seeded successfully.")
