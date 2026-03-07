package com.focusgate

import android.app.Application
import com.focusgate.data.local.FocusGateDatabase
import com.focusgate.data.repository.FocusSessionRepository

class FocusGateApp : Application() {
    lateinit var repository: FocusSessionRepository
        private set

    override fun onCreate() {
        super.onCreate()
        val db = FocusGateDatabase.getInstance(this)
        repository = FocusSessionRepository(db.focusSessionDao())
    }
}
