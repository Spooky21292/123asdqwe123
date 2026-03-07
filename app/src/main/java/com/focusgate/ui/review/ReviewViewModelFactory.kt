package com.focusgate.ui.review

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.focusgate.data.repository.FocusSessionRepository
import com.focusgate.domain.model.SessionDraft

class ReviewViewModelFactory(
    private val repository: FocusSessionRepository,
    private val draft: SessionDraft,
    private val startedAt: Long,
    private val endedAt: Long,
    private val completed: Boolean,
    private val endedEarly: Boolean,
    private val distractions: Int
) : ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return ReviewViewModel(
            repository = repository,
            draft = draft,
            startedAt = startedAt,
            endedAt = endedAt,
            completed = completed,
            endedEarly = endedEarly,
            distractions = distractions
        ) as T
    }
}
