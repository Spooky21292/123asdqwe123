package com.focusgate.ui.startsession

import androidx.lifecycle.ViewModel
import com.focusgate.domain.model.SessionDraft
import com.focusgate.domain.model.SessionType
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.update

class StartSessionViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(SessionDraft())
    val uiState: StateFlow<SessionDraft> = _uiState

    fun onGoalChange(value: String) = _uiState.update { it.copy(goal = value) }
    fun onSessionTypeSelected(value: SessionType) = _uiState.update { it.copy(sessionType = value) }
    fun onDurationSelected(value: Int) = _uiState.update { it.copy(durationMinutes = value) }
    fun onWhyChange(value: String) = _uiState.update { it.copy(whyThisMatters = value) }
    fun onMainTaskChange(value: String) = _uiState.update { it.copy(mainTask = value) }
}
