package com.focusgate.data.local

import androidx.room.Entity
import androidx.room.PrimaryKey
import com.focusgate.domain.model.FocusSession
import com.focusgate.domain.model.SessionType

@Entity(tableName = "focus_sessions")
data class FocusSessionEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val goal: String,
    val sessionType: String,
    val durationMinutes: Int,
    val whyThisMatters: String,
    val mainTask: String,
    val startTime: Long,
    val endTime: Long,
    val completed: Boolean,
    val endedEarly: Boolean,
    val distractionCount: Int,
    val focusScore: Int,
    val reflection: String
)

fun FocusSessionEntity.toDomain(): FocusSession = FocusSession(
    id = id,
    goal = goal,
    sessionType = SessionType.valueOf(sessionType),
    durationMinutes = durationMinutes,
    whyThisMatters = whyThisMatters,
    mainTask = mainTask,
    startTime = startTime,
    endTime = endTime,
    completed = completed,
    endedEarly = endedEarly,
    distractionCount = distractionCount,
    focusScore = focusScore,
    reflection = reflection
)

fun FocusSession.toEntity(): FocusSessionEntity = FocusSessionEntity(
    id = id,
    goal = goal,
    sessionType = sessionType.name,
    durationMinutes = durationMinutes,
    whyThisMatters = whyThisMatters,
    mainTask = mainTask,
    startTime = startTime,
    endTime = endTime,
    completed = completed,
    endedEarly = endedEarly,
    distractionCount = distractionCount,
    focusScore = focusScore,
    reflection = reflection
)
