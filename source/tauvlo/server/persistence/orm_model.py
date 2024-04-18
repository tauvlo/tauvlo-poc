import enum

import sqlalchemy as db

from tauvlo.server.persistence.database import ORM


class User(ORM.Model):
    """
    Table representing a user
    """
    __tablename__ = "user"

    user_id = db.Column(db.String, primary_key=True)
    details = db.Column(db.JSON)


class Property(ORM.Model):
    """
    Table representing a property
    """
    __tablename__ = "property"

    property_id = db.Column(db.String, primary_key=True)
    poster_id = db.Column(db.String, db.ForeignKey("user.user_id"))
    details = db.Column(db.JSON)


class Ownership(ORM.Model):
    """
    Table representing an ownership of a fraction of a property
    """
    __tablename__ = "ownership"

    user_id = db.Column(db.String, db.ForeignKey("user.user_id"), primary_key=True)
    property_id = db.Column(db.String, db.ForeignKey("property.property_id"), primary_key=True)
    tokens_owned = db.Column(db.BigInteger, nullable=False, default=0)


class TransactionRecordType(str, enum.Enum):
    OWNERSHIP = "OWNERSHIP"
    POSTING = "POSTING"
    BUY_TOKENS = "BUY_TOKENS"
    SELL_TOKENS = "SELL_TOKENS"


class TransactionRecord(ORM.Model):
    """
    Table representing any transaction in Tauvlo
    """
    __tablename__ = "transaction_record"

    transaction_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String, db.ForeignKey("user.user_id"), nullable=False)
    transaction_type = db.Column(db.Enum(TransactionRecordType, values_callable=lambda obj: [e.value for e in obj]),
                                 nullable=False)
    property_id = db.Column(db.String, db.ForeignKey("property.property_id"), nullable=True)
    details = db.Column(db.JSON)


class UniqueVisit(ORM.Model):
    """
    Table representing unique visits
    """
    __tablename__ = "unique_visit"

    ip_address = db.Column(db.String, primary_key=True)
    page_name = db.Column(db.String, primary_key=True)
    view_counter = db.Column(db.BigInteger, nullable=False, default=1)
    first_visit = db.Column(db.DateTime, nullable=False)
    last_visit = db.Column(db.DateTime, nullable=False)
