package com.focusgate.data.local

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase

@Database(entities = [FocusSessionEntity::class], version = 1, exportSchema = false)
abstract class FocusGateDatabase : RoomDatabase() {
    abstract fun focusSessionDao(): FocusSessionDao

    companion object {
        @Volatile
        private var INSTANCE: FocusGateDatabase? = null

        fun getInstance(context: Context): FocusGateDatabase {
            return INSTANCE ?: synchronized(this) {
                INSTANCE ?: Room.databaseBuilder(
                    context.applicationContext,
                    FocusGateDatabase::class.java,
                    "focus_gate.db"
                ).build().also { INSTANCE = it }
            }
        }
    }
}
