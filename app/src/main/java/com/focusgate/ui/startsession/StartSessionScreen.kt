package com.focusgate.ui.startsession

import androidx.compose.animation.AnimatedContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.input.KeyboardCapitalization
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.focusgate.domain.model.SessionDraft
import com.focusgate.domain.model.SessionType
import com.focusgate.ui.components.GlassCard
import com.focusgate.ui.components.HeaderSection
import com.focusgate.ui.components.SelectablePill
import com.focusgate.ui.theme.BlueAccent
import com.focusgate.ui.theme.CyanAccent
import com.focusgate.ui.theme.DeepNavy
import com.focusgate.ui.theme.Night
import com.focusgate.ui.theme.SoftText

@Composable
fun StartSessionRoute(
    onStartFocus: (SessionDraft) -> Unit,
    vm: StartSessionViewModel = viewModel()
) {
    val state by vm.uiState.collectAsState()
    StartSessionScreen(
        state = state,
        onGoalChange = vm::onGoalChange,
        onSessionTypeSelected = vm::onSessionTypeSelected,
        onDurationSelected = vm::onDurationSelected,
        onWhyChange = vm::onWhyChange,
        onMainTaskChange = vm::onMainTaskChange,
        onStartFocus = onStartFocus
    )
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun StartSessionScreen(
    state: SessionDraft,
    onGoalChange: (String) -> Unit,
    onSessionTypeSelected: (SessionType) -> Unit,
    onDurationSelected: (Int) -> Unit,
    onWhyChange: (String) -> Unit,
    onMainTaskChange: (String) -> Unit,
    onStartFocus: (SessionDraft) -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Brush.verticalGradient(listOf(DeepNavy, Night)))
            .verticalScroll(rememberScrollState())
            .padding(horizontal = 20.dp, vertical = 24.dp),
        verticalArrangement = Arrangement.spacedBy(18.dp)
    ) {
        HeaderSection(
            title = "FocusGate",
            subtitle = "Define intention before you begin."
        )

        GlassCard {
            Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
                OutlinedTextField(
                    value = state.goal,
                    onValueChange = onGoalChange,
                    label = { Text("Session Goal") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true,
                    keyboardOptions = KeyboardOptions(capitalization = KeyboardCapitalization.Sentences)
                )

                Text("Session Type", style = MaterialTheme.typography.titleMedium, color = Color.White)
                FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    SessionType.entries.forEach { type ->
                        SelectablePill(
                            text = type.displayName,
                            selected = state.sessionType == type,
                            onClick = { onSessionTypeSelected(type) }
                        )
                    }
                }

                Text("Duration", style = MaterialTheme.typography.titleMedium, color = Color.White)
                FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    listOf(25, 45, 60, 90).forEach { minutes ->
                        SelectablePill(
                            text = "$minutes min",
                            selected = state.durationMinutes == minutes,
                            onClick = { onDurationSelected(minutes) }
                        )
                    }
                }

                OutlinedTextField(
                    value = state.whyThisMatters,
                    onValueChange = onWhyChange,
                    label = { Text("Why this matters") },
                    modifier = Modifier.fillMaxWidth(),
                    minLines = 3,
                    keyboardOptions = KeyboardOptions(capitalization = KeyboardCapitalization.Sentences)
                )

                OutlinedTextField(
                    value = state.mainTask,
                    onValueChange = onMainTaskChange,
                    label = { Text("One Main Task") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true,
                    keyboardOptions = KeyboardOptions(capitalization = KeyboardCapitalization.Sentences)
                )
            }
        }

        AnimatedContent(targetState = state.isValid, label = "start_button") { canStart ->
            Button(
                onClick = { onStartFocus(state) },
                enabled = canStart,
                modifier = Modifier.fillMaxWidth(),
                contentPadding = PaddingValues(vertical = 16.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = if (canStart) BlueAccent else SoftText.copy(alpha = 0.2f),
                    contentColor = if (canStart) Color.White else SoftText
                )
            ) {
                Text("Start Focus", style = MaterialTheme.typography.titleMedium)
            }
        }

        Text(
            text = "Your session starts only after intention is clear.",
            color = CyanAccent.copy(alpha = 0.8f),
            style = MaterialTheme.typography.bodyMedium,
            modifier = Modifier.padding(top = 4.dp)
        )
    }
}

@Preview(showBackground = true)
@Composable
private fun StartSessionPreview() {
    com.focusgate.ui.theme.FocusGateTheme {
        StartSessionScreen(
            state = SessionDraft(),
            onGoalChange = {},
            onSessionTypeSelected = {},
            onDurationSelected = {},
            onWhyChange = {},
            onMainTaskChange = {},
            onStartFocus = {}
        )
    }
}
