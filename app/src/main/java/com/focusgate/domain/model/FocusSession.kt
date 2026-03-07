package com.focusgate.domain.model

data class FocusSession(
    val id: Long = 0,
    val goal: String,
    val sessionType: SessionType,
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
