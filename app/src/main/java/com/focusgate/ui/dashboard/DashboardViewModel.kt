package com.focusgate.ui.dashboard

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.focusgate.data.repository.FocusSessionRepository
import com.focusgate.domain.model.DashboardMetrics
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class DashboardViewModel(
    private val repository: FocusSessionRepository
) : ViewModel() {
    private val _uiState = MutableStateFlow(DashboardMetrics())
    val uiState: StateFlow<DashboardMetrics> = _uiState.asStateFlow()

    init {
        refresh()
    }

    fun refresh() {
        viewModelScope.launch {
            _uiState.value = repository.buildDashboardMetrics()
        }
    }
}
