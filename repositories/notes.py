from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Note


class NoteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user_id: int, content: str) -> Note:
        note = Note(user_id=user_id, content=content)
        self.session.add(note)
        await self.session.commit()
        await self.session.refresh(note)
        return note

    async def get_recent(self, user_id: int, limit: int = 10) -> list[Note]:
        result = await self.session.scalars(
            select(Note).where(Note.user_id == user_id).order_by(Note.created_at.desc()).limit(limit)
        )
        return list(result)

    async def get_by_id(self, note_id: int, user_id: int) -> Note | None:
        return await self.session.scalar(select(Note).where(and_(Note.id == note_id, Note.user_id == user_id)))

    async def delete(self, note: Note) -> None:
        await self.session.delete(note)
        await self.session.commit()
