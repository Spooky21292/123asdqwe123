package com.focusgate

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import com.focusgate.ui.navigation.FocusGateNavHost
import com.focusgate.ui.theme.FocusGateTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val app = application as FocusGateApp
        setContent {
            FocusGateTheme {
                FocusGateNavHost(repository = app.repository)
            }
        }
    }
}
