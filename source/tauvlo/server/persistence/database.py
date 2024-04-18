from sqlalchemy import create_engine, create_mock_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship as orm_relationship


class ORM:
    """
    A primary ORM class
    """

    """
    A callable session factory object to be used for each DB operation.
    To create a new session use:

    from tauvlo.server.persistence.database import ORM
    with ORM.Session() as session:
        ...
        session.commit()
    """
    Session = sessionmaker(autocommit=False, autoflush=False)

    """
    A declarative base for all ORM model objects.
    """
    Model = declarative_base()

    """
    Relational pattern definition factory.
    """
    Relationship = orm_relationship

    """
    SQLAlchemy DB engine
    """
    engine = None

    @staticmethod
    def create_mock_engine(processor: callable) -> any:
        return create_mock_engine("postgresql://", processor)

    @staticmethod
    def configure_db_connection(connection_string: str,
                                json_serializer: any = None,
                                log_sql: bool = False) -> None:
        """
        Configuration method for the DB connection - needs to be run only once prior to performing any DB operations
        :param connection_string: DB connection string, such as "postgresql://USER:PASSWORD@HOST/tauvlo"
        :param json_serializer: custom json serializer for the ORM engine
        :param log_sql: enables or disables SQL logging (SQLAlchemy engine echo parameter)
        :return: None
        """

        additional_args = {
            "echo": log_sql
        }

        if json_serializer is not None:
            additional_args["json_serializer"] = json_serializer

        ORM.engine = create_engine(connection_string, **additional_args)

        ORM.Session.configure(bind=ORM.engine)
