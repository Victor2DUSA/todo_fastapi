from sqlmodel import Field, Session, SQLModel, create_engine, select

class TodoBase(SQLModel):
    title: str = Field(index=True)
    completed: bool = Field(default=False)


class Todo(TodoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class TodoGet(TodoBase):
    id: int 


class TodoCreate(TodoBase):
    id: int | None = None

class TodoUpdate(TodoBase):
    tilte: str | None = None
    complete: bool | None = None
