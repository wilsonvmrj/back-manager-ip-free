from datetime import datetime
from enum import Enum
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()

class TodoState(str, Enum):
    draft = 'draft'
    todo = 'todo'
    doing = 'doing'
    done = 'done'
    trash = 'trash'


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )


@table_registry.mapped_as_dataclass
class Todo:
    __tablename__= 'todos'
    
    id: Mapped[int] = mapped_column(init=False,primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    state: Mapped[TodoState]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()    
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    

@table_registry.mapped_as_dataclass
class Vlan:
    __tablename__= 'vlans'
    id: Mapped[int] = mapped_column(init=False,primary_key=True)
    vlan:Mapped[int]
    network: Mapped[str]
    netmask: Mapped[str]
    gateway: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()    
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

