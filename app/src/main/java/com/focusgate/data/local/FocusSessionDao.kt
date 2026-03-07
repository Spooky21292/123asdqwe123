package com.focusgate.data.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface FocusSessionDao {
    @Insert
    suspend fun insertSession(session: FocusSessionEntity): Long

    @Query("SELECT * FROM focus_sessions ORDER BY startTime DESC")
    fun observeAllSessions(): Flow<List<FocusSessionEntity>>

    @Query("SELECT * FROM focus_sessions ORDER BY startTime DESC")
    suspend fun getAllSessions(): List<FocusSessionEntity>

    @Query("SELECT * FROM focus_sessions WHERE startTime >= :fromTime ORDER BY startTime DESC")
    suspend fun getSessionsFrom(fromTime: Long): List<FocusSessionEntity>

    @Query("SELECT * FROM focus_sessions WHERE completed = 1 ORDER BY startTime DESC")
    suspend fun getCompletedSessions(): List<FocusSessionEntity>
}
