from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean, Table, MetaData, PrimaryKeyConstraint, schema
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import urllib.parse

Base = declarative_base()


class Complex(Base):
	__tablename__ = 'complex'

	complex_id = Column(Integer, primary_key=True)
	name = Column(String(100), nullable=False)
	objects = relationship('Objects', cascade="all,delete", backref='complex')


class Step(Base):
	__tablename__ = 'step'

	step_id = Column(Integer, primary_key=True)
	name = Column(String(50), nullable=False)
	objects = relationship('Objects', cascade="all,delete", backref='step')


class Specification(Base):
	__tablename__ = 'specification'

	specification_id = Column(Integer, primary_key=True)
	description = Column(String(300))
	signature = Column(Boolean)
	objects = relationship('Objects', cascade="all,delete", uselist=False)


class Objects(Base):
	__tablename__ = 'objects'

	object_id = Column(Integer, primary_key=True)
	complex_id = Column(Integer, ForeignKey("complex.complex_id"), nullable=False)
	step_id = Column(Integer, ForeignKey("step.step_id"), nullable=False)
	specification_id = Column(Integer, ForeignKey("specification.specification_id"))
	name_object = Column(String(100))
	date_start = Column(Date)
	date_expiration = Column(Date)
	cypher = Column(String(50))
	phase = Column(String(20))
	comments = relationship('Comment', cascade="all,delete", backref='objects')
	permits = relationship('Permit', cascade="all,delete", backref='objects')
	employees = relationship('Employee', secondary='object_employee', cascade="all,delete")
	trips = relationship('Trip', secondary='trip_object', cascade="all,delete")


object_employee = Table(
	'object_employee', Base.metadata,
	Column('object_id', Integer, ForeignKey('objects.object_id')),
	Column('employee_id', Integer, ForeignKey('employee.employee_id')),
	PrimaryKeyConstraint('object_id', 'employee_id', name='object_employee_pk')
)

trip_object = Table(
	'trip_object', Base.metadata,
	Column('trip_id', Integer, ForeignKey('trip.trip_id')),
	Column('object_id', Integer, ForeignKey('objects.object_id')),
	PrimaryKeyConstraint('trip_id', 'object_id', name='trip_object_pk')
)

trip_employee = Table(
	'trip_employee', Base.metadata,
	Column('trip_id', Integer, ForeignKey('trip.trip_id')),
	Column('employee_id', Integer, ForeignKey('employee.employee_id')),
	PrimaryKeyConstraint('trip_id', 'employee_id', name='trip_employee_pk')
)


class Comment(Base):
	__tablename__ = 'comment'

	comment_id = Column(Integer, primary_key=True)
	object_id = Column(Integer, ForeignKey('objects.object_id'))
	date_comment = Column(Date, nullable=False)
	description = Column(String(500))


class Employee(Base):
	__tablename__ = 'employee'

	employee_id = Column(Integer, primary_key=True)
	name = Column(String(50))
	permits = relationship('Permit', cascade='all,delete', backref='supervisor')
	objects = relationship('Objects', secondary='object_employee', cascade="all,delete")
	trips = relationship('Trip', secondary='trip_employee', cascade='all,delete')


class Trip(Base):
	__tablename__ = 'trip'

	trip_id = Column(Integer, primary_key=True)
	date_issue = Column(Date, nullable=False)
	date_expiration = Column(Date, nullable=False)
	description = Column(String(500))
	objects = relationship('Objects', secondary='trip_object', cascade='all,delete')
	employees = relationship('Employee', secondary='trip_employee', cascade='all,delete')


class PermitTypes(Base):
	__tablename__ = 'permit_type'

	type_id = Column(Integer, primary_key=True)
	permits = relationship('Permit', cascade="all,delete", backref='types')


class Permit(Base):
	__tablename__ = 'permit'
	permit_id = Column(Integer, primary_key=True)
	permit_num = Column(String(50))
	object_id = Column(Integer, ForeignKey("objects.object_id"))
	supervisor_id = Column(Integer, ForeignKey("employee.employee_id"))
	date_issue = Column(Date, nullable=False)
	date_expiration = Column(Date, nullable=False)
	type_id = Column(Integer, ForeignKey("permit_type.type_id"))


if __name__ == '__main__':
	password = urllib.parse.quote_plus("")
	db = f"mysql+mysqlconnector://rs1180w5_gal:{password}@rs1180w5.beget.tech:3306/rs1180w5_gal"
	engine = create_engine(db, echo=True)
	# Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)
