package com.focusgate.ui.review

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.focusgate.data.repository.FocusSessionRepository
import com.focusgate.domain.model.SessionDraft
import com.focusgate.ui.components.FadeInCard
import com.focusgate.ui.components.HeaderSection
import com.focusgate.ui.components.TwoColumnStats
import com.focusgate.ui.theme.BlueAccent
import com.focusgate.ui.theme.DeepNavy
import com.focusgate.ui.theme.Night
import com.focusgate.ui.theme.SoftText

@Composable
fun ReviewRoute(
    repository: FocusSessionRepository,
    draft: SessionDraft,
    startedAt: Long,
    endedAt: Long,
    completed: Boolean,
    endedEarly: Boolean,
    distractions: Int,
    onOpenDashboard: () -> Unit
) {
    val vm: ReviewViewModel = viewModel(
        factory = ReviewViewModelFactory(
            repository = repository,
            draft = draft,
            startedAt = startedAt,
            endedAt = endedAt,
            completed = completed,
            endedEarly = endedEarly,
            distractions = distractions
        )
    )
    val state by vm.uiState.collectAsStateWithLifecycle()

    LaunchedEffect(state.saved) {
        if (state.saved) onOpenDashboard()
    }

    ReviewScreen(
        state = state,
        onReflectionChange = vm::onReflectionChange,
        onSave = vm::saveSession
    )
}

@Composable
private fun ReviewScreen(
    state: ReviewUiState,
    onReflectionChange: (String) -> Unit,
    onSave: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Brush.verticalGradient(listOf(DeepNavy, Night)))
            .verticalScroll(rememberScrollState())
            .padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        HeaderSection(title = "Session Review", subtitle = "Close the loop with intention.")

        FadeInCard {
            TwoColumnStats(
                firstLabel = "Outcome",
                firstValue = if (state.completed) "Completed" else "Ended Early",
                secondLabel = "Distractions",
                secondValue = state.distractions.toString()
            )
        }
        FadeInCard {
            TwoColumnStats(
                firstLabel = "Focus Score",
                firstValue = "${state.focusScore}",
                secondLabel = "Streak",
                secondValue = "${state.streak}d"
            )
        }

        OutlinedTextField(
            value = state.reflection,
            onValueChange = onReflectionChange,
            modifier = Modifier.fillMaxWidth(),
            minLines = 4,
            label = { Text("Reflection") },
            supportingText = {
                Text("What helped or challenged your focus?", color = SoftText)
            }
        )

        Button(
            onClick = onSave,
            enabled = !state.isSaving,
            modifier = Modifier.fillMaxWidth(),
            colors = ButtonDefaults.buttonColors(containerColor = BlueAccent)
        ) {
            Text(
                text = if (state.isSaving) "Saving..." else "Save & Open Dashboard",
                style = MaterialTheme.typography.titleMedium,
                color = Color.White
            )
        }
    }
}
