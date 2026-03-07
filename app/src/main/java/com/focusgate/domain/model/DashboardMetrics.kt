package com.focusgate.domain.model

data class DashboardMetrics(
    val weeklySessions: Int = 0,
    val averageCompletionRate: Int = 0,
    val averageDistractions: Double = 0.0,
    val streak: Int = 0,
    val recentScores: List<Int> = emptyList(),
    val recentSessions: List<FocusSession> = emptyList()
)
