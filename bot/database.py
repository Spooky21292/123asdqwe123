from __future__ import annotations

import aiosqlite
from typing import Any


class Database:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    async def init(self) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS videos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    url TEXT NOT NULL,
                    title TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    is_watched INTEGER DEFAULT 0,
                    is_favorite INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    watched_at TIMESTAMP NULL
                )
                """
            )
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS playlists (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, name)
                )
                """
            )
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS playlist_videos (
                    playlist_id INTEGER NOT NULL,
                    video_id INTEGER NOT NULL,
                    PRIMARY KEY (playlist_id, video_id),
                    FOREIGN KEY (playlist_id) REFERENCES playlists(id) ON DELETE CASCADE,
                    FOREIGN KEY (video_id) REFERENCES videos(id) ON DELETE CASCADE
                )
                """
            )
            await db.commit()

    async def add_video(self, user_id: int, url: str, title: str, platform: str) -> int:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "INSERT INTO videos (user_id, url, title, platform) VALUES (?, ?, ?, ?)",
                (user_id, url, title, platform),
            )
            await db.commit()
            return cursor.lastrowid

    async def get_video(self, user_id: int, video_id: int) -> dict[str, Any] | None:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT * FROM videos WHERE user_id = ? AND id = ?", (user_id, video_id)
            )
            row = await cursor.fetchone()
            return dict(row) if row else None

    async def list_unwatched(self, user_id: int) -> list[dict[str, Any]]:
        return await self._list_videos_by_clause(user_id, "is_watched = 0")

    async def list_watched(self, user_id: int) -> list[dict[str, Any]]:
        return await self._list_videos_by_clause(user_id, "is_watched = 1")

    async def list_favorites(self, user_id: int) -> list[dict[str, Any]]:
        return await self._list_videos_by_clause(user_id, "is_favorite = 1")

    async def _list_videos_by_clause(self, user_id: int, clause: str) -> list[dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            query = f"SELECT * FROM videos WHERE user_id = ? AND {clause} ORDER BY created_at DESC"
            cursor = await db.execute(query, (user_id,))
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def set_watched(self, user_id: int, video_id: int, watched: bool = True) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                UPDATE videos
                SET is_watched = ?, watched_at = CASE WHEN ? = 1 THEN CURRENT_TIMESTAMP ELSE NULL END
                WHERE user_id = ? AND id = ?
                """,
                (int(watched), int(watched), user_id, video_id),
            )
            await db.commit()

    async def toggle_favorite(self, user_id: int, video_id: int) -> int:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT is_favorite FROM videos WHERE user_id = ? AND id = ?", (user_id, video_id)
            )
            row = await cursor.fetchone()
            if not row:
                return 0
            new_value = 0 if row["is_favorite"] else 1
            await db.execute(
                "UPDATE videos SET is_favorite = ? WHERE user_id = ? AND id = ?",
                (new_value, user_id, video_id),
            )
            await db.commit()
            return new_value

    async def create_playlist(self, user_id: int, name: str) -> int | None:
        async with aiosqlite.connect(self.db_path) as db:
            try:
                cursor = await db.execute(
                    "INSERT INTO playlists (user_id, name) VALUES (?, ?)", (user_id, name)
                )
                await db.commit()
                return cursor.lastrowid
            except aiosqlite.IntegrityError:
                return None

    async def list_playlists(self, user_id: int) -> list[dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT * FROM playlists WHERE user_id = ? ORDER BY name COLLATE NOCASE", (user_id,)
            )
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def add_video_to_playlist(self, user_id: int, playlist_id: int, video_id: int) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT id FROM playlists WHERE id = ? AND user_id = ?", (playlist_id, user_id)
            )
            playlist_row = await cursor.fetchone()
            if not playlist_row:
                return False

            cursor = await db.execute(
                "SELECT id FROM videos WHERE id = ? AND user_id = ?", (video_id, user_id)
            )
            video_row = await cursor.fetchone()
            if not video_row:
                return False

            await db.execute(
                "INSERT OR IGNORE INTO playlist_videos (playlist_id, video_id) VALUES (?, ?)",
                (playlist_id, video_id),
            )
            await db.commit()
            return True

    async def get_playlist_videos(self, user_id: int, playlist_id: int) -> list[dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """
                SELECT v.*
                FROM videos v
                JOIN playlist_videos pv ON pv.video_id = v.id
                JOIN playlists p ON p.id = pv.playlist_id
                WHERE p.user_id = ? AND p.id = ?
                ORDER BY v.created_at DESC
                """,
                (user_id, playlist_id),
            )
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def get_stats(self, user_id: int) -> dict[str, int]:
        async with aiosqlite.connect(self.db_path) as db:
            queries = {
                "total": "SELECT COUNT(*) FROM videos WHERE user_id = ?",
                "watched": "SELECT COUNT(*) FROM videos WHERE user_id = ? AND is_watched = 1",
                "unwatched": "SELECT COUNT(*) FROM videos WHERE user_id = ? AND is_watched = 0",
                "favorites": "SELECT COUNT(*) FROM videos WHERE user_id = ? AND is_favorite = 1",
                "playlists": "SELECT COUNT(*) FROM playlists WHERE user_id = ?",
            }
            result: dict[str, int] = {}
            for key, query in queries.items():
                cursor = await db.execute(query, (user_id,))
                row = await cursor.fetchone()
                result[key] = row[0] if row else 0
            return result
