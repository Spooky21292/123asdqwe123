package com.focusgate.ui.focussession

import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.focusgate.domain.model.SessionDraft
import com.focusgate.ui.components.GlassCard
import com.focusgate.ui.theme.BlueAccent
import com.focusgate.ui.theme.CyanAccent
import com.focusgate.ui.theme.DeepNavy
import com.focusgate.ui.theme.Night
import com.focusgate.ui.theme.SoftText

@Composable
fun FocusSessionRoute(
    draft: SessionDraft,
    onSessionFinished: (FocusSessionUiState) -> Unit
) {
    val vm: FocusSessionViewModel = viewModel(factory = FocusSessionViewModelFactory(draft))
    val state by vm.uiState.collectAsStateWithLifecycle()

    if (state.isFinished) {
        onSessionFinished(state)
    }

    FocusSessionScreen(
        state = state,
        onPause = vm::pauseSession,
        onResume = vm::resumeSession,
        onDistracted = vm::markDistracted,
        onFinish = { vm.finishSession(endedEarly = false) },
        onEndEarly = { vm.finishSession(endedEarly = true) }
    )
}

@Composable
private fun FocusSessionScreen(
    state: FocusSessionUiState,
    onPause: () -> Unit,
    onResume: () -> Unit,
    onDistracted: () -> Unit,
    onFinish: () -> Unit,
    onEndEarly: () -> Unit
) {
    var showConfirmEnd by remember { mutableStateOf(false) }
    val emphasis by animateFloatAsState(targetValue = if (state.isPaused) 0.7f else 1f, label = "timer_alpha")

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Brush.verticalGradient(listOf(Night, DeepNavy)))
            .padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        GlassCard(modifier = Modifier.fillMaxWidth()) {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text(text = state.draft.goal, style = MaterialTheme.typography.titleLarge, color = Color.White)
                Text(
                    text = "${state.draft.sessionType?.displayName} • ${state.draft.mainTask}",
                    style = MaterialTheme.typography.bodyMedium,
                    color = SoftText
                )
                Text(
                    text = "stay with intent",
                    style = MaterialTheme.typography.labelLarge,
                    color = CyanAccent
                )
            }
        }

        GlassCard(modifier = Modifier.fillMaxWidth()) {
            Column(
                modifier = Modifier.fillMaxWidth(),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                AnimatedContent(targetState = formatTime(state.secondsRemaining), label = "timer") { value ->
                    Text(
                        text = value,
                        style = MaterialTheme.typography.headlineLarge,
                        color = Color.White,
                        modifier = Modifier.alpha(emphasis)
                    )
                }
                Text("Distractions: ${state.distractions}", color = SoftText)
            }
        }

        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            if (state.isPaused) {
                Button(
                    onClick = onResume,
                    modifier = Modifier.weight(1f),
                    colors = ButtonDefaults.buttonColors(containerColor = BlueAccent)
                ) {
                    Text("Resume")
                }
            } else {
                OutlinedButton(onClick = onPause, modifier = Modifier.weight(1f)) {
                    Text("Pause")
                }
            }
            Button(
                onClick = onDistracted,
                modifier = Modifier.weight(1f),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF224063))
            ) {
                Text("I got distracted")
            }
        }

        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            Button(
                onClick = onFinish,
                modifier = Modifier.weight(1f),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF1C7C54))
            ) {
                Text("Finish Session")
            }
            OutlinedButton(
                onClick = { showConfirmEnd = true },
                modifier = Modifier.weight(1f)
            ) {
                Text("End Early")
            }
        }
    }

    if (showConfirmEnd) {
        AlertDialog(
            onDismissRequest = { showConfirmEnd = false },
            title = { Text("End session early?") },
            text = { Text("You can still reflect and save your progress.") },
            confirmButton = {
                TextButton(
                    onClick = {
                        showConfirmEnd = false
                        onEndEarly()
                    }
                ) {
                    Text("End Early")
                }
            },
            dismissButton = {
                TextButton(onClick = { showConfirmEnd = false }) {
                    Text("Continue")
                }
            }
        )
    }
}

private fun formatTime(totalSeconds: Long): String {
    val safe = totalSeconds.coerceAtLeast(0)
    val mins = safe / 60
    val secs = safe % 60
    return "%02d:%02d".format(mins, secs)
}
