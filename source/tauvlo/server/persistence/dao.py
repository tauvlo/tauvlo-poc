from datetime import datetime
from typing import Optional, List

from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert

from tauvlo.server.persistence.database import ORM
from tauvlo.server.persistence.json_models.property import PropertyDetails
from tauvlo.server.persistence.json_models.transaction import TransactionDetails
from tauvlo.server.persistence.json_models.user import UserDetails
from tauvlo.server.persistence.orm_model import Property, User, Ownership, TransactionRecord, TransactionRecordType, \
    UniqueVisit


class UserDAO:
    def get_user_detail(self, user_id: str) -> Optional[User]:
        """
        Retrieves a user detail.
        @param user_id: ID of the user
        @return User detail
        """
        with ORM.Session() as session:
            return session.query(User).get(user_id)

    def create_user(self, user_id: str, details: UserDetails) -> None:
        """
        Creates a new user.
        @user_id: New user ID
        @details: User details
        """
        new_user = User(user_id=user_id, details=details)
        with ORM.Session() as session:
            session.merge(new_user)
            session.commit()


class PropertyDAO:
    def get_property_detail(self, property_id: str) -> Optional[Property]:
        """
        Retrieves a property detail.
        @param property_id: ID of the property
        @return Property detail
        """
        with ORM.Session() as session:
            return session.query(Property).get(property_id)

    def get_properties_list(self, offset: int, limit: int) -> List[Property]:
        """
        Retrieves a list of properties.
        @offset: Paging offset
        @limit: Paging limit
        @return List of properties
        """
        with ORM.Session() as session:
            return session.query(Property).offset(offset).limit(limit).all()

    def create_property(self, property_id: str, poster_id: str, details: PropertyDetails) -> None:
        """
        Creates a new property.
        @property_id: New property ID
        @poster_id: User ID of the poster of the property
        @details: Property details
        """
        new_property = Property(property_id=property_id, poster_id=poster_id, details=details)
        with ORM.Session() as session:
            session.merge(new_property)
            session.commit()

    def delete_property(self, property_id: str) -> bool:
        with ORM.Session() as session:
            statement = delete(Property).where(Property.property_id == property_id)
            result = session.execute(statement)
            session.commit()
            return True


class OwnershipDAO:
    def get_ownership_list(self, user_id: Optional[str] = None, property_id: Optional[str] = None) -> List[Ownership]:
        """
        Retrieves a list of ownership information filtered either by user ID, property ID or both. At least one
        argument must be provided
        @param user_id: Optional ID of the user
        @param property_id: Optional ID of the property
        @return List of filtered ownership details
        """

        if user_id is None and property_id is None:
            raise ValueError("Neither user_id nor property_id were provided for filtering.")

        with ORM.Session() as session:
            query = session.query(Ownership)
            if user_id is not None:
                query.where(Ownership.user_id == user_id)
            if property_id is not None:
                query.where(Ownership.property_id == property_id)
            return list(query.all())

    def set_ownership(self, user_id: str, property_id: str, tokens_owned: int) -> None:
        """
        Stores or updates fractional ownership.
        @user_id: Fraction owner user ID
        @property_id: Property of which the fraction is owned
        @details: Ownership fraction in tokens
        """
        ownership_record = Ownership(user_id=user_id, property_id=property_id, tokens_owned=tokens_owned)
        with ORM.Session() as session:
            session.merge(ownership_record)
            session.commit()


class TransactionRecordDAO:
    def record_transaction(self,
                           user_id: str,
                           transaction_type: TransactionRecordType,
                           property_id: Optional[str],
                           details: TransactionDetails) -> None:
        """
        Stores transaction details.
        @user_id: User performing the transaction
        @transaction_type: Type of the transaction
        @property_id: Property affected by the transaction, if any
        @details: Transaction details
        """
        transaction_record = TransactionRecord(user_id=user_id,
                                               transaction_type=transaction_type,
                                               property_id=property_id,
                                               details=details)
        with ORM.Session() as session:
            session.add(transaction_record)
            session.commit()


class UniqueVisitsDAO:

    def log_visit(self, ip_address: str, page_name: str) -> None:
        now = datetime.now()
        insert_stmt = insert(UniqueVisit) \
            .values(ip_address=ip_address,
                    page_name=page_name,
                    view_counter=1,
                    first_visit=now,
                    last_visit=now) \
            .on_conflict_do_update(
            index_elements=[UniqueVisit.ip_address, UniqueVisit.page_name],
            set_=dict(view_counter=UniqueVisit.view_counter + 1, last_visit=now)
        )

        with ORM.Session() as session:
            session.execute(insert_stmt)
            session.commit()
