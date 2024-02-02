import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
# import timedelta
from datetime import timedelta

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    # Main section
    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=False, nullable=True)
    password = Column(String, unique=False, index=False, nullable=False)

    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)

    # Flags
    active = Column(Boolean, nullable=False, default=True)
    admin = Column(Boolean, default=False, doc="An admin can log into the Piccolo admin GUI.")
    superuser = Column(Boolean, default=False, doc="If True, this user can manage other users's passwords in the Piccolo admin GUI.")

    # Dates
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    birthdate = Column(DateTime, nullable=True)

    # Relations
    roles = relationship("M2MUserRole", back_populates="user")
    groups = relationship("M2MUserGroup", back_populates="user")


class M2MUserRole(Base):
    __tablename__ = 'm2m_user_role'

    user_id = Column(String, ForeignKey('users.id'), primary_key=True)
    role_id = Column(String, ForeignKey('roles.id'), primary_key=True)

    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")

class M2MUserGroup(Base):
    __tablename__ = 'm2m_user_group'

    user_id = Column(String, ForeignKey('users.id'), primary_key=True)
    group_id = Column(String, ForeignKey('groups.id'), primary_key=True)

    user = relationship("User", back_populates="groups")
    group = relationship("Group", back_populates="users")

class Role(Base):
    __tablename__ = 'roles'

    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    name = Column(String, unique=True, index=True, nullable=False)
    active = Column(Boolean, nullable=False, default=True)

    users = relationship("M2MUserRole", back_populates="role")
    policies = relationship("Policy", back_populates="role")

class Group(Base):
    __tablename__ = 'groups'

    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    name = Column(String, unique=True, index=True, nullable=False)
    active = Column(Boolean, nullable=False, default=True)

    users = relationship("M2MUserGroup", back_populates="group")

class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    name = Column(String, unique=True, index=False, nullable=False)
    object = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, unique=False, index=False, nullable=True)

    policies = relationship("Policy", back_populates="permission")

class Policy(Base):
    __tablename__ = 'policies'

    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    permission_id = Column(String, ForeignKey('permissions.id'), nullable=False)
    role_id = Column(String, ForeignKey('roles.id'), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    name = Column(String, unique=False, index=False, nullable=False)
    description = Column(String, unique=False, index=False, nullable=True)

    permission = relationship("Permission", back_populates="policies")
    role = relationship("Role", back_populates="policies")
class Sessions(Base):
    __tablename__ = 'sessions'

    token = Column(String(100), nullable=False, primary_key=True)
    user_id = Column(String, nullable=False)
    expiry_date = Column(DateTime, nullable=False, default=datetime.utcnow() + timedelta(hours=1))
    max_expiry_date = Column(DateTime, nullable=False, default=datetime.utcnow() + timedelta(days=7))
