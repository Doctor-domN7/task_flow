from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class TaskDB(Base):
    __tablename__ = "tasks" 
    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    completed: Mapped[bool] = mapped_column(default=False) 

class CategoryDB(Base):
    __tablename__ = "categories" 
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()