package com.focusgate.ui.focussession

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.focusgate.domain.model.SessionDraft

class FocusSessionViewModelFactory(
    private val draft: SessionDraft
) : ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return FocusSessionViewModel(draft) as T
    }
}
