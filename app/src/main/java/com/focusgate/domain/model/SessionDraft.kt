package com.focusgate.domain.model

data class SessionDraft(
    val goal: String = "",
    val sessionType: SessionType? = null,
    val durationMinutes: Int? = null,
    val whyThisMatters: String = "",
    val mainTask: String = ""
) {
    val isValid: Boolean
        get() = goal.isNotBlank() && sessionType != null && durationMinutes != null && mainTask.isNotBlank()
}
