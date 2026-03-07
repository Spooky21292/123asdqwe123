package com.focusgate.ui.review

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.focusgate.data.repository.FocusSessionRepository
import com.focusgate.domain.model.FocusSession
import com.focusgate.domain.model.SessionDraft
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class ReviewUiState(
    val draft: SessionDraft,
    val completed: Boolean,
    val endedEarly: Boolean,
    val distractions: Int,
    val focusScore: Int,
    val streak: Int,
    val reflection: String = "",
    val isSaving: Boolean = false,
    val saved: Boolean = false
)

class ReviewViewModel(
    private val repository: FocusSessionRepository,
    draft: SessionDraft,
    private val startedAt: Long,
    private val endedAt: Long,
    completed: Boolean,
    endedEarly: Boolean,
    distractions: Int
) : ViewModel() {
    private val _uiState = MutableStateFlow(
        ReviewUiState(
            draft = draft,
            completed = completed,
            endedEarly = endedEarly,
            distractions = distractions,
            focusScore = repository.calculateFocusScore(distractions, endedEarly),
            streak = 0
        )
    )
    val uiState: StateFlow<ReviewUiState> = _uiState.asStateFlow()

    init {
        viewModelScope.launch {
            _uiState.update { it.copy(streak = repository.calculateCurrentStreak()) }
        }
    }

    fun onReflectionChange(value: String) {
        _uiState.update { it.copy(reflection = value) }
    }

    fun saveSession() {
        if (_uiState.value.isSaving || _uiState.value.saved) return
        viewModelScope.launch {
            _uiState.update { it.copy(isSaving = true) }
            val state = _uiState.value
            val session = FocusSession(
                goal = state.draft.goal,
                sessionType = state.draft.sessionType!!,
                durationMinutes = state.draft.durationMinutes!!,
                whyThisMatters = state.draft.whyThisMatters,
                mainTask = state.draft.mainTask,
                startTime = startedAt,
                endTime = endedAt,
                completed = state.completed,
                endedEarly = state.endedEarly,
                distractionCount = state.distractions,
                focusScore = state.focusScore,
                reflection = state.reflection
            )
            repository.saveSession(session)
            _uiState.update { it.copy(isSaving = false, saved = true) }
        }
    }
}
