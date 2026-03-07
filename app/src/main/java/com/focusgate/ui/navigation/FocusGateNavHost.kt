package com.focusgate.ui.navigation

import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.focusgate.data.repository.FocusSessionRepository
import com.focusgate.domain.model.SessionDraft
import com.focusgate.ui.dashboard.DashboardRoute
import com.focusgate.ui.focussession.FocusSessionRoute
import com.focusgate.ui.focussession.FocusSessionUiState
import com.focusgate.ui.review.ReviewRoute
import com.focusgate.ui.startsession.StartSessionRoute

@Composable
fun FocusGateNavHost(repository: FocusSessionRepository) {
    val navController = rememberNavController()

    var latestDraft by remember { mutableStateOf(SessionDraft()) }
    var latestResult by remember { mutableStateOf<FocusSessionUiState?>(null) }

    NavHost(
        navController = navController,
        startDestination = NavRoutes.START
    ) {
        composable(NavRoutes.START) {
            StartSessionRoute(
                onStartFocus = { draft ->
                    latestDraft = draft
                    navController.navigate(NavRoutes.FOCUS)
                }
            )
        }

        composable(NavRoutes.FOCUS) {
            FocusSessionRoute(
                draft = latestDraft,
                onSessionFinished = { state ->
                    latestResult = state
                    navController.navigate(NavRoutes.REVIEW)
                }
            )
        }

        composable(NavRoutes.REVIEW) {
            val result = latestResult
            if (result == null) {
                navController.popBackStack(NavRoutes.START, inclusive = false)
            } else {
                ReviewRoute(
                    repository = repository,
                    draft = result.draft,
                    startedAt = result.startTime,
                    endedAt = result.endTime,
                    completed = !result.endedEarly,
                    endedEarly = result.endedEarly,
                    distractions = result.distractions,
                    onOpenDashboard = {
                        navController.navigate(NavRoutes.DASHBOARD) {
                            popUpTo(NavRoutes.START)
                        }
                    }
                )
            }
        }

        composable(NavRoutes.DASHBOARD) {
            DashboardRoute(
                repository = repository,
                onNewSession = {
                    navController.navigate(NavRoutes.START) {
                        popUpTo(NavRoutes.DASHBOARD) { inclusive = true }
                    }
                }
            )
        }
    }
}
