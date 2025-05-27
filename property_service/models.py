from sqlalchemy import Column, Integer, String, Enum
from database import Base
import enum

class PropertyStatus(str, enum.Enum):
    draft = "Draft"
    submitted = "Submitted"
    verified = "Verified"
    listed = "Listed"
    deal = "Deal"
    closed = "Closed"

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    type = Column(String)  # residential / commercial
    status = Column(Enum(PropertyStatus), default=PropertyStatus.draft)
