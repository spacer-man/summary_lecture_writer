from typing import Any, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel
from sqlmodel import delete
from sqlmodel import select
from sqlmodel import update

from .abc import Repository


class SQLModelRepository[T: SQLModel, T_id](Repository[T, T_id]):
    def __init__(self, model: type[T], session: AsyncSession) -> None:
        self.session = session
        self.model = model

    async def commit(self) -> None:
        await self.session.commit()

    async def add(self, obj: T) -> T_id:
        self.session.add(obj)
        await self.session.flush()
        return getattr(obj, "id")

    async def get_one(self, **properties) -> T | None:
        stmt = select(self.model)
        if properties:
            stmt = stmt.filter_by(**properties)
        obj = await self.session.scalar(stmt)
        return obj

    async def get_many(
            self,
            filters: list[Any] | None = None,
            order_by: Any | None = None,
            limit: int | None = None,
            **properties,
            ) -> Sequence[T]:
        stmt = select(self.model)
        if limit is not None:
            stmt = stmt.limit(limit)
        if properties:
            stmt = stmt.filter_by(**properties)
        if filters:
            stmt = stmt.where(*filters)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        responses = await self.session.scalars(stmt)
        return responses.all()

    async def update(self, obj: T) -> None:
        obj_data = obj.model_dump()
        obj_data.pop("id")
        stmt = (
            update(self.model)
            .values(**obj_data)
            .filter_by(id=getattr(obj, "id"))
        )
        await self.session.execute(stmt)

    async def remove(
            self,
            filters: list[Any] | None = None,
            order_by: Any | None = None,
            limit: int | None = None,
            **properties,
            ) -> Sequence[T]:
        objs = []
        if len(properties) > 0:
            objs = await self.get_many(
                    **properties,
                    filters=filters,
                    order_by=order_by,
                    limit=limit)
            if len(objs) > 0:
                del_stmt = (
                    delete(self.model)
                    .filter_by(**properties)
                )
                await self.session.execute(del_stmt)
        return objs
