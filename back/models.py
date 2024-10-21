from datetime import datetime
from sqlalchemy.orm import registry, Mapped, mapped_column
from sqlalchemy import func, text

table_registry=registry()

@table_registry.mapped_as_dataclass
class User:
  __tablename__='users'

  id: Mapped[int] = mapped_column(init=False, primary_key=True)
  username: Mapped[str] =mapped_column(unique=True)
  email: Mapped[str] = mapped_column(unique=True)
  password: Mapped[str]
  created_at: Mapped[datetime] = mapped_column(init=False,server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(init=False,server_default=func.now())
