# FocusGate (Android MVP)

FocusGate is a premium-styled productivity app that requires users to define their intention before entering a focus session.

## Architecture

The project uses a clean, layered structure:

- `data/local`: Room entity, DAO, and database.
- `data/repository`: `FocusSessionRepository` for persistence, scoring, and streak/dashboard aggregation.
- `domain/model`: domain models used by the UI.
- `ui`: Compose screens, reusable components, navigation, and theme.

### Stack

- Kotlin
- Jetpack Compose + Material 3
- Navigation Compose
- ViewModel + StateFlow
- Coroutines
- Room (local persistence)

## Project structure

```text
app/src/main/java/com/focusgate
├── data
│   ├── local
│   └── repository
├── domain
│   └── model
└── ui
    ├── components
    ├── dashboard
    ├── focussession
    ├── navigation
    ├── review
    ├── startsession
    └── theme
```

## Features

1. **Start Session ritual** with required validation:
   - session goal
   - session type
   - duration
   - why this matters
   - one main task
2. **Focus Session** with timer, pause/resume, distraction logging, finish, and end early.
3. **Session Review** showing outcome, distractions, focus score, streak, and reflection.
4. **Dashboard** with weekly sessions, completion %, average distractions, streak, recent score bars, and recent sessions.

## Business logic

- **Focus score**: starts from 100, subtracts 8 points per distraction, subtracts 25 if ended early, then clamps `0..100`.
- **Streak**: counts consecutive days (today or yesterday fallback) with at least one completed session.

## Run in Android Studio

1. Open this folder in Android Studio (Ladybug+ recommended).
2. Let Gradle sync using Android Gradle Plugin `8.5.2` and Kotlin `1.9.24`.
3. Run the `app` module on an emulator/device (minSdk 26).

## Dependencies

Main dependencies are defined in `app/build.gradle.kts`:

- Compose BOM `2024.06.00`
- Material3
- Navigation Compose `2.7.7`
- Lifecycle Compose/ViewModel `2.8.2`
- Room `2.6.1` with KSP
- Coroutines Android `1.8.1`

## Notes

- Portrait-oriented main activity.
- No backend, all data is local on-device via Room.
- UI emphasizes dark premium gradients and glass-like cards.
