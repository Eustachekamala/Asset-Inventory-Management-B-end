from datetime import datetime, timezone
from enum import Enum
from database import db

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
    __tablename__ = 'user'  
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

    # Relationships
    requests = db.relationship('Request', back_populates='user', cascade='all, delete-orphan', lazy=True)
    assets_allocated = db.relationship('Asset', backref='allocated_user', lazy=True)


# Asset model
class Asset(db.Model):
    __tablename__ = 'asset'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    status = db.Column(db.Enum(AssetStatus), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    allocated_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category_id': self.category_id,
            'status': self.status,
            'image_url': self.image_url,
            'allocated_to': self.allocated_to,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    # Relationships
    category = db.relationship('Category', backref='assets', lazy=True)
    requests = db.relationship('Request', back_populates='asset', cascade='all, delete-orphan', lazy=True)


# Category model
class Category(db.Model):
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'category_name': self.category_name,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


# Request model
class Request(db.Model):
    __tablename__ = 'request' 
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=True)
    request_type = db.Column(db.Enum(RequestType), nullable=False)
    reason = db.Column(db.Text)
    quantity = db.Column(db.Integer, nullable=False)
    urgency = db.Column(db.Enum(UrgencyLevel), nullable=False)
    status = db.Column(db.Enum(RequestStatus), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'asset_id': self.asset_id,
            'request_type': self.request_type.value,
            'reason': self.reason,
            'quantity': self.quantity,
            'urgency': self.urgency.value,
            'status': self.status.value,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        
    # Relationships
    user = db.relationship('User', back_populates='requests', lazy=True)
    asset = db.relationship('Asset', back_populates='requests', lazy=True)
    history = db.relationship('RequestHistory', back_populates='request', cascade='all, delete-orphan', lazy=True)


# RequestHistory model
class RequestHistory(db.Model):
    __tablename__ = 'request_history'
    
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), nullable=False)
    status = db.Column(db.Enum(RequestStatus), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    comments = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'request_id': self.request_id,
            'status': self.status,
            'updated_at': self.updated_at,
            'comments': self.comments,
            'created_at': self.created_at
        }
    
    # Relationships
    request = db.relationship('Request', back_populates='history', lazy=True)