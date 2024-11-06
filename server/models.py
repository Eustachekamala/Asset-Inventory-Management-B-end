from datetime import datetime
from enum import Enum
from app import db

# Enums for user roles and statuses
class UserRole(Enum):
    Admin = "Admin"
    Procurement_Manager = "Procurement_Manager"
    Employee = "Employee"

class AssetStatus(Enum):
    Available = "Available"
    Allocated = "Allocated"
    Under_Repair = "Under_Repair"

class RequestType(Enum):
    New_Asset = "New_Asset"
    Repair = "Repair"

class UrgencyLevel(Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"

class RequestStatus(Enum):
    Pending = "Pending"
    Approved = "Approved"
    Rejected = "Rejected"

# User model
class User(db.Model):
    __tablename__ = 'User'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.timezone.utc)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.timezone.utc, onupdate=datetime.timezone.utc)

    # Relationships
    requests = db.relationship('Request', backref='user', lazy=True)
    assets_allocated = db.relationship('Asset', backref='allocated_user', lazy=True)

# Asset model
class Asset(db.Model):
    __tablename__ = 'Asset'
    
    asset_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('Category.category_id'), nullable=False)
    status = db.Column(db.Enum(AssetStatus), nullable=False)
    image_url = db.Column(db.Text)
    allocated_to = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.timezone.utc)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.timezone.utc, onupdate=datetime.timezone.utc)

    # Relationships
    category = db.relationship('Category', backref='assets', lazy=True)
    requests = db.relationship('Request', backref='asset', lazy=True)

# Category model
class Category(db.Model):
    __tablename__ = 'Category'
    
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.timezone.utc)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.timezone.utc, onupdate=datetime.timezone.utc)

# Request model
class Request(db.Model):
    __tablename__ = 'Request'
    
    request_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey('Asset.asset_id'), nullable=True)
    request_type = db.Column(db.Enum(RequestType), nullable=False)
    reason = db.Column(db.Text)
    quantity = db.Column(db.Integer, nullable=False)
    urgency = db.Column(db.Enum(UrgencyLevel), nullable=False)
    status = db.Column(db.Enum(RequestStatus), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.timezone.utc)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.timezone.utc, onupdate=datetime.timezone.utc)

    # Relationships
    history = db.relationship('RequestHistory', backref='request', lazy=True)

# RequestHistory model
class RequestHistory(db.Model):
    __tablename__ = 'RequestHistory'
    
    history_id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('Request.request_id'), nullable=False)
    status = db.Column(db.Enum(RequestStatus), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.timezone.utc)
    comments = db.Column(db.Text, nullable=True)