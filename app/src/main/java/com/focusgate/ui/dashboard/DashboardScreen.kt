package com.focusgate.ui.dashboard

import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.focusgate.data.repository.FocusSessionRepository
import com.focusgate.domain.model.DashboardMetrics
import com.focusgate.ui.components.GlassCard
import com.focusgate.ui.components.HeaderSection
import com.focusgate.ui.components.StatItem
import com.focusgate.ui.theme.BlueAccent
import com.focusgate.ui.theme.CyanAccent
import com.focusgate.ui.theme.DeepNavy
import com.focusgate.ui.theme.Night
import com.focusgate.ui.theme.SoftText
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@Composable
fun DashboardRoute(repository: FocusSessionRepository, onNewSession: () -> Unit) {
    val vm: DashboardViewModel = viewModel(factory = DashboardViewModelFactory(repository))
    val state by vm.uiState.collectAsStateWithLifecycle()

    DashboardScreen(state = state, onNewSession = onNewSession)
}

@Composable
private fun DashboardScreen(state: DashboardMetrics, onNewSession: () -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Brush.verticalGradient(listOf(Night, DeepNavy)))
            .verticalScroll(rememberScrollState())
            .padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        HeaderSection("Focus Intelligence", "Your weekly momentum, quantified.")

        Button(
            onClick = onNewSession,
            colors = ButtonDefaults.buttonColors(containerColor = BlueAccent),
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("New Session")
        }

        GlassCard {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                StatItem("Weekly Sessions", state.weeklySessions.toString())
                StatItem("Completion", "${state.averageCompletionRate}%")
            }
        }

        GlassCard {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                StatItem("Avg Distractions", String.format("%.1f", state.averageDistractions))
                StatItem("Streak", "${state.streak}d")
            }
        }

        GlassCard {
            Text("Recent Focus Scores", style = MaterialTheme.typography.titleMedium, color = Color.White)
            ScoreBarChart(scores = state.recentScores)
        }

        if (state.recentSessions.isNotEmpty()) {
            GlassCard {
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Recent Sessions", style = MaterialTheme.typography.titleMedium, color = Color.White)
                    val formatter = SimpleDateFormat("EEE, MMM d", Locale.getDefault())
                    state.recentSessions.forEach { session ->
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                            Text(session.goal, color = Color.White, modifier = Modifier.weight(1f))
                            Text(
                                "${session.focusScore} • ${formatter.format(Date(session.startTime))}",
                                color = SoftText,
                                style = MaterialTheme.typography.bodySmall
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun ScoreBarChart(scores: List<Int>) {
    val safeScores = if (scores.isEmpty()) listOf(0, 0, 0, 0, 0) else scores
    val animatedValues = safeScores.mapIndexed { idx, score ->
        animateFloatAsState(targetValue = (score / 100f).coerceIn(0f, 1f), label = "bar-$idx").value
    }

    Canvas(
        modifier = Modifier
            .fillMaxWidth()
            .height(160.dp)
            .padding(top = 12.dp)
    ) {
        val count = animatedValues.size
        val spacing = 18.dp.toPx()
        val barWidth = (size.width - (count + 1) * spacing) / count
        animatedValues.forEachIndexed { index, value ->
            val left = spacing + index * (barWidth + spacing)
            val top = size.height * (1f - value)
            drawRoundRect(
                brush = Brush.verticalGradient(listOf(CyanAccent, BlueAccent)),
                topLeft = androidx.compose.ui.geometry.Offset(left, top),
                size = androidx.compose.ui.geometry.Size(barWidth, size.height - top),
                cornerRadius = CornerRadius(12f, 12f)
            )
        }
    }
}
