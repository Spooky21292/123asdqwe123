package com.focusgate.data.repository

import com.focusgate.data.local.FocusSessionDao
import com.focusgate.data.local.toDomain
import com.focusgate.data.local.toEntity
import com.focusgate.domain.model.DashboardMetrics
import com.focusgate.domain.model.FocusSession
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import java.time.Instant
import java.time.LocalDate
import java.time.ZoneId

class FocusSessionRepository(
    private val dao: FocusSessionDao
) {

    fun observeSessions(): Flow<List<FocusSession>> = dao.observeAllSessions().map { entities ->
        entities.map { it.toDomain() }
    }

    suspend fun saveSession(session: FocusSession): Long = dao.insertSession(session.toEntity())

    suspend fun buildDashboardMetrics(): DashboardMetrics {
        val allSessions = dao.getAllSessions().map { it.toDomain() }
        val now = System.currentTimeMillis()
        val sevenDaysAgo = now - 7L * 24L * 60L * 60L * 1000L
        val weekly = dao.getSessionsFrom(sevenDaysAgo).map { it.toDomain() }

        val completionRate = if (allSessions.isNotEmpty()) {
            ((allSessions.count { it.completed }.toFloat() / allSessions.size) * 100).toInt()
        } else 0

        val avgDistractions = if (allSessions.isNotEmpty()) {
            allSessions.map { it.distractionCount }.average()
        } else 0.0

        return DashboardMetrics(
            weeklySessions = weekly.size,
            averageCompletionRate = completionRate,
            averageDistractions = avgDistractions,
            streak = calculateStreak(allSessions),
            recentScores = allSessions.take(7).map { it.focusScore }.reversed(),
            recentSessions = allSessions.take(5)
        )
    }

    suspend fun calculateCurrentStreak(): Int {
        val sessions = dao.getCompletedSessions().map { it.toDomain() }
        return calculateStreak(sessions)
    }

    private fun calculateStreak(sessions: List<FocusSession>): Int {
        if (sessions.isEmpty()) return 0
        val zone = ZoneId.systemDefault()
        val completedDays = sessions
            .filter { it.completed }
            .map {
                Instant.ofEpochMilli(it.endTime).atZone(zone).toLocalDate()
            }
            .distinct()
            .sortedDescending()

        if (completedDays.isEmpty()) return 0

        var streak = 0
        var cursor = LocalDate.now(zone)

        if (!completedDays.contains(cursor)) {
            cursor = cursor.minusDays(1)
            if (!completedDays.contains(cursor)) return 0
        }

        while (completedDays.contains(cursor)) {
            streak++
            cursor = cursor.minusDays(1)
        }

        return streak
    }

    fun calculateFocusScore(distractions: Int, endedEarly: Boolean): Int {
        val earlyPenalty = if (endedEarly) 25 else 0
        val score = 100 - distractions * 8 - earlyPenalty
        return score.coerceIn(0, 100)
    }
}
