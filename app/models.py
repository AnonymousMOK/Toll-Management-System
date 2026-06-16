from sqlalchemy import Column, String, Integer, DateTime, Numeric, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base

# --- EXCISE SCHEMA ---
class Owner(Base):
    __tablename__ = "owners"
    __table_args__ = {"schema": "excise"}

    owner_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String)
    national_id = Column(String, unique=True)
    phone_number = Column(String)

class Vehicle(Base):
    __tablename__ = "vehicles"
    __table_args__ = {"schema": "excise"}

    plate_number = Column(String, primary_key=True, index=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("excise.owners.owner_id"))
    make = Column(String)
    model = Column(String)
    registered_class = Column(String)
    status = Column(String, default="Active")

# --- TOLL SCHEMA ---
class Plaza(Base):
    __tablename__ = "plazas"
    __table_args__ = {"schema": "toll"}

    plaza_id = Column(Integer, primary_key=True)
    plaza_name = Column(String)
    location_gps = Column(String)

class Lane(Base):
    __tablename__ = "lanes"
    __table_args__ = {"schema": "toll"}

    lane_id = Column(Integer, primary_key=True)
    plaza_id = Column(Integer, ForeignKey("toll.plazas.plaza_id"))
    lane_type = Column(String)
    direction = Column(String)

class Passage(Base):
    __tablename__ = "passages"
    __table_args__ = {"schema": "toll"}

    passage_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lane_id = Column(Integer, ForeignKey("toll.lanes.lane_id"))
    captured_plate = Column(String)
    entry_timestamp = Column(DateTime)
    exit_timestamp = Column(DateTime, nullable=True)
    payment_method_used = Column(String)

class QRToken(Base):
    __tablename__ = "qr_tokens"
    __table_args__ = {"schema": "toll"}

    qr_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    passage_id = Column(UUID(as_uuid=True), ForeignKey("toll.passages.passage_id"))
    secure_token = Column(String, unique=True, default=lambda: str(uuid.uuid4()))
    generated_at = Column(DateTime)
    expires_at = Column(DateTime)
    status = Column(String, default='Active')

class AdminAlert(Base):
    __tablename__ = "admin_alerts"
    __table_args__ = {"schema": "toll"}

    alert_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    passage_id = Column(UUID(as_uuid=True), ForeignKey("toll.passages.passage_id"))
    alert_type = Column(String)
    details = Column(String)
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime)

# --- PAYMENT SCHEMA ---
class ETag(Base):
    __tablename__ = "e_tags"
    __table_args__ = {"schema": "payment"}

    e_tag_id = Column(String, primary_key=True)
    registered_plate = Column(String, unique=True)
    balance = Column(Numeric(10, 2))
    status = Column(String, default='Active')

class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = {"schema": "payment"}

    transaction_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    passage_id = Column(UUID(as_uuid=True), ForeignKey("toll.passages.passage_id"))
    amount_charged = Column(Numeric(10, 2))
    payment_gateway = Column(String)
    gateway_reference = Column(String)
    status = Column(String, default='Pending')
    created_at = Column(DateTime)