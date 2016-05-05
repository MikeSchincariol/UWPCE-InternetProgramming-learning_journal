from datetime import datetime

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Unicode,
    UnicodeText,
    DateTime,
    create_engine
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)

class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), nullable=False, unique=True)
    body = Column(UnicodeText)
    created = Column(DateTime, default=datetime.now)
    edited = Column(DateTime, default=datetime.now)

    @classmethod
    def all(cls, session):
        """
        Returns all entries from the database, ordered by most recent
        entry first.
        :param session: An SQLAlchemy session instance already configured with
                        the correct engine.
        :return: A list.:
        """
        # May need to import desc from sqlalchemy for this to work
        results = session.query(cls).order_by(cls.created.desc()).all()

        # For now, print out a table of the results. Later, this may be
        # removed in favor of just returning the result list.
        print("{0:<5} {1:32} {2:12}".format("--", "-----", "--------"))
        print("{0:<5} {1:32} {2:12}".format("ID", "TITLE", "DATETIME"))
        print("{0:<5} {1:32} {2:12}".format("--", "-----", "--------"))
        for row in results:
            print("{0:<5} {1:32} {2:12}".format(row.id, row.title, row.created.isoformat()))
        return results


    @classmethod
    def by_id(cls, entry_id, session):
        """
        Returns a single entry given by the ID number provided.
        :param entry_id: The integer value of the primary key, 'id', to search for.
        :param session: An SQLAlchemy session instance already configured with
                        the correct engine.
        :return: An instance of the Entry class.
        """
        results = session.query(cls).filter(cls.id == entry_id).one_or_none()
        print("{0:<5} {1:32} {2:12}".format("--", "-----", "--------"))
        print("{0:<5} {1:32} {2:12}".format("ID", "TITLE", "DATETIME"))
        print("{0:<5} {1:32} {2:12}".format("--", "-----", "--------"))
        print("{0:<5} {1:32} {2:12}".format(results.id, results.title, results.created.isoformat()))
        return results


if __name__ == "__main__":
    engine = create_engine('sqlite:///learning_journal.sqlite')
    DBSession.configure(bind=engine)
    session = DBSession()

    # Make some example calls to the class methods.
    Entry.all(session)
    print()
    Entry.by_id(1, session)
