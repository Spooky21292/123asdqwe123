package com.focusgate.ui.focussession

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.focusgate.domain.model.SessionDraft
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class FocusSessionUiState(
    val draft: SessionDraft,
    val secondsRemaining: Long,
    val isPaused: Boolean = false,
    val distractions: Int = 0,
    val isFinished: Boolean = false,
    val endedEarly: Boolean = false,
    val startTime: Long = System.currentTimeMillis(),
    val endTime: Long = 0L
)

class FocusSessionViewModel(draft: SessionDraft) : ViewModel() {
    private var timerJob: Job? = null

    private val _uiState = MutableStateFlow(
        FocusSessionUiState(
            draft = draft,
            secondsRemaining = (draft.durationMinutes ?: 0) * 60L
        )
    )
    val uiState: StateFlow<FocusSessionUiState> = _uiState

    init {
        startTimer()
    }

    private fun startTimer() {
        timerJob?.cancel()
        timerJob = viewModelScope.launch {
            while (_uiState.value.secondsRemaining > 0 && !_uiState.value.isPaused) {
                delay(1000)
                _uiState.update { it.copy(secondsRemaining = it.secondsRemaining - 1) }
            }
            if (_uiState.value.secondsRemaining <= 0L && !_uiState.value.isFinished) {
                finishSession(endedEarly = false)
            }
        }
    }

    fun pauseSession() {
        timerJob?.cancel()
        _uiState.update { it.copy(isPaused = true) }
    }

    fun resumeSession() {
        _uiState.update { it.copy(isPaused = false) }
        startTimer()
    }

    fun markDistracted() {
        _uiState.update { it.copy(distractions = it.distractions + 1) }
    }

    fun finishSession(endedEarly: Boolean) {
        timerJob?.cancel()
        _uiState.update {
            it.copy(
                isFinished = true,
                endedEarly = endedEarly,
                isPaused = false,
                secondsRemaining = if (endedEarly) it.secondsRemaining else 0,
                endTime = System.currentTimeMillis()
            )
        }
    }

    override fun onCleared() {
        super.onCleared()
        timerJob?.cancel()
    }
}
