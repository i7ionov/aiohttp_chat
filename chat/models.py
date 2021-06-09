from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, Table, select
from sqlalchemy.orm import relationship
from database import Base, BaseModel

users_chats = Table('users_chats', Base.metadata,
                    Column('chat_id', Integer, ForeignKey('chats.id')),
                    Column('user_id', Integer, ForeignKey('users.id'))
                    )


class User(BaseModel):
    __tablename__ = 'users'

    login = Column(VARCHAR(255), nullable=False, unique=True)
    password = Column(VARCHAR(255), nullable=False)
    messages = relationship("Message", back_populates="user")
    own_chats = relationship("Chat", back_populates="owner")
    chats = relationship(
        "Chat",
        secondary=users_chats,
        back_populates="users")


class Chat(BaseModel):
    __tablename__ = 'chats'

    name = Column(VARCHAR(255), nullable=False, unique=True)
    messages = relationship("Message", back_populates="chat")
    users = relationship(
        "User",
        secondary=users_chats,
        back_populates="chats")
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="own_chats")


class Message(BaseModel):
    __tablename__ = 'messages'
    chat_id = Column(Integer, ForeignKey('chats.id'))
    chat = relationship("Chat", back_populates="messages")
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="messages")
    text = Column(VARCHAR(255), nullable=False)




