package com.example.outthedoor

import android.app.TimePickerDialog
import android.content.ContextWrapper
import android.content.Context
import android.os.Bundle
import android.speech.tts.TextToSpeech
import android.view.WindowManager
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.animation.animateColorAsState
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay
import org.json.JSONArray
import org.json.JSONObject
import java.util.Locale

private tailrec fun Context.findActivity(): ComponentActivity? = when (this) {
    is ComponentActivity -> this
    is ContextWrapper -> baseContext.findActivity()
    else -> null
}

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                App()
            }
        }
    }
}

@Composable
fun App() {
    val context = LocalContext.current
    var currentScreen by rememberSaveable { mutableStateOf(Screen.HOME) }
    var template by remember { mutableStateOf(loadTemplate(context)) }

    when (currentScreen) {
        Screen.HOME -> HomeScreen(
            template = template,
            onCreate = { currentScreen = Screen.EDITOR },
            onEdit = { currentScreen = Screen.EDITOR },
            onStart = {
                if (template != null && template!!.tasks.isNotEmpty()) {
                    currentScreen = Screen.FOCUS
                }
            }
        )

        Screen.EDITOR -> EditorScreen(
            initialTemplate = template,
            onSave = {
                template = it
                saveTemplate(context, it)
                currentScreen = Screen.HOME
            },
            onBack = { currentScreen = Screen.HOME },
            onDelete = {
                deleteTemplate(context)
                template = null
                currentScreen = Screen.HOME
            }
        )

        Screen.FOCUS -> {
            val activeTemplate = template
            if (activeTemplate == null || activeTemplate.tasks.isEmpty()) {
                currentScreen = Screen.HOME
            } else {
                FocusScreen(
                    template = activeTemplate,
                    onFinish = { currentScreen = Screen.HOME }
                )
            }
        }
    }
}

enum class Screen { HOME, EDITOR, FOCUS }

data class TaskBlock(
    val name: String,
    val minutes: Int
)

data class Template(
    val name: String,
    val deadlineHour: Int,
    val deadlineMinute: Int,
    val tasks: List<TaskBlock>
)

fun loadTemplate(context: Context): Template? {
    val prefs = context.getSharedPreferences("out_the_door_prefs", Context.MODE_PRIVATE)
    val json = prefs.getString("template_json", null) ?: return null
    return try {
        val root = JSONObject(json)
        val tasksArray = root.getJSONArray("tasks")
        val tasks = buildList {
            for (i in 0 until tasksArray.length()) {
                val taskJson = tasksArray.getJSONObject(i)
                add(
                    TaskBlock(
                        name = taskJson.getString("name"),
                        minutes = taskJson.getInt("minutes")
                    )
                )
            }
        }
        Template(
            name = root.getString("name"),
            deadlineHour = root.getInt("deadlineHour"),
            deadlineMinute = root.getInt("deadlineMinute"),
            tasks = tasks
        )
    } catch (_: Exception) {
        null
    }
}

fun saveTemplate(context: Context, template: Template) {
    val prefs = context.getSharedPreferences("out_the_door_prefs", Context.MODE_PRIVATE)
    val tasksArray = JSONArray()
    template.tasks.forEach {
        tasksArray.put(
            JSONObject()
                .put("name", it.name)
                .put("minutes", it.minutes)
        )
    }
    val root = JSONObject()
        .put("name", template.name)
        .put("deadlineHour", template.deadlineHour)
        .put("deadlineMinute", template.deadlineMinute)
        .put("tasks", tasksArray)
    prefs.edit().putString("template_json", root.toString()).apply()
}

fun deleteTemplate(context: Context) {
    val prefs = context.getSharedPreferences("out_the_door_prefs", Context.MODE_PRIVATE)
    prefs.edit().remove("template_json").apply()
}

fun totalMinutes(tasks: List<TaskBlock>): Int = tasks.sumOf { it.minutes }

fun calculateStartTime(deadlineHour: Int, deadlineMinute: Int, totalMinutes: Int): Pair<Int, Int> {
    val deadlineTotal = deadlineHour * 60 + deadlineMinute
    val startTotal = (deadlineTotal - totalMinutes + 24 * 60) % (24 * 60)
    return startTotal / 60 to startTotal % 60
}

fun formatTime(hour: Int, minute: Int): String = String.format(Locale.getDefault(), "%02d:%02d", hour, minute)

@Composable
fun HomeScreen(
    template: Template?,
    onCreate: () -> Unit,
    onEdit: () -> Unit,
    onStart: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text("OutTheDoor", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)

        if (template == null) {
            Text("Шаблон не создан")
            Button(onClick = onCreate) { Text("Создать") }
        } else {
            val sum = totalMinutes(template.tasks)
            val (startHour, startMinute) = calculateStartTime(template.deadlineHour, template.deadlineMinute, sum)

            Card(modifier = Modifier.fillMaxWidth()) {
                Column(
                    modifier = Modifier.padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Text(template.name, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.SemiBold)
                    Text("Выйти в ${formatTime(template.deadlineHour, template.deadlineMinute)}")
                    Text("Всего шагов: ${template.tasks.size}")
                    Text("Сумма: $sum мин")
                    Text("Старт в ${formatTime(startHour, startMinute)}")
                }
            }

            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Button(onClick = onEdit) { Text("Редактировать") }
                Button(onClick = onStart, enabled = template.tasks.isNotEmpty()) { Text("Старт") }
            }
        }
    }
}

@Composable
fun EditorScreen(
    initialTemplate: Template?,
    onSave: (Template) -> Unit,
    onBack: () -> Unit,
    onDelete: () -> Unit
) {
    val context = LocalContext.current
    var name by remember { mutableStateOf(initialTemplate?.name ?: "Мой шаблон") }
    var deadlineHour by remember { mutableIntStateOf(initialTemplate?.deadlineHour ?: 8) }
    var deadlineMinute by remember { mutableIntStateOf(initialTemplate?.deadlineMinute ?: 0) }
    val tasks = remember {
        mutableStateListOf<TaskBlock>().apply {
            addAll(initialTemplate?.tasks ?: emptyList())
        }
    }

    var showAddDialog by remember { mutableStateOf(false) }
    var newTaskName by remember { mutableStateOf("") }
    var newTaskMinutes by remember { mutableStateOf("5") }

    if (showAddDialog) {
        AlertDialog(
            onDismissRequest = { showAddDialog = false },
            title = { Text("Добавить шаг") },
            text = {
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedTextField(
                        value = newTaskName,
                        onValueChange = { newTaskName = it },
                        label = { Text("Название шага") },
                        singleLine = true
                    )
                    OutlinedTextField(
                        value = newTaskMinutes,
                        onValueChange = { newTaskMinutes = it.filter { ch -> ch.isDigit() } },
                        label = { Text("Минуты") },
                        singleLine = true
                    )
                }
            },
            confirmButton = {
                TextButton(
                    onClick = {
                        val mins = newTaskMinutes.toIntOrNull() ?: 0
                        if (newTaskName.isNotBlank() && mins > 0) {
                            tasks.add(TaskBlock(newTaskName.trim(), mins))
                            newTaskName = ""
                            newTaskMinutes = "5"
                            showAddDialog = false
                        }
                    }
                ) { Text("Добавить") }
            },
            dismissButton = { TextButton(onClick = { showAddDialog = false }) { Text("Отмена") } }
        )
    }

    val sum = totalMinutes(tasks)
    val (startHour, startMinute) = calculateStartTime(deadlineHour, deadlineMinute, sum)

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        OutlinedTextField(
            value = name,
            onValueChange = { name = it },
            label = { Text("Название шаблона") },
            modifier = Modifier.fillMaxWidth(),
            singleLine = true
        )

        Button(onClick = {
            TimePickerDialog(
                context,
                { _, hour, minute ->
                    deadlineHour = hour
                    deadlineMinute = minute
                },
                deadlineHour,
                deadlineMinute,
                true
            ).show()
        }) {
            Text("Время выхода: ${formatTime(deadlineHour, deadlineMinute)}")
        }

        LazyColumn(
            modifier = Modifier
                .weight(1f)
                .fillMaxWidth(),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            itemsIndexed(tasks) { index, item ->
                Card(modifier = Modifier.fillMaxWidth()) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(12.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column(modifier = Modifier.weight(1f)) {
                            Text(item.name, fontWeight = FontWeight.Medium)
                            Text("${item.minutes} мин")
                        }
                        Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                            TextButton(
                                onClick = {
                                    if (index > 0) {
                                        val temp = tasks[index - 1]
                                        tasks[index - 1] = tasks[index]
                                        tasks[index] = temp
                                    }
                                }
                            ) { Text("↑") }
                            TextButton(
                                onClick = {
                                    if (index < tasks.lastIndex) {
                                        val temp = tasks[index + 1]
                                        tasks[index + 1] = tasks[index]
                                        tasks[index] = temp
                                    }
                                }
                            ) { Text("↓") }
                            TextButton(onClick = { tasks.removeAt(index) }) { Text("❌") }
                        }
                    }
                }
            }
        }

        Button(onClick = { showAddDialog = true }) { Text("Добавить шаг") }

        Card(modifier = Modifier.fillMaxWidth()) {
            Column(modifier = Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text("Сумма шагов: $sum мин")
                Text("Время старта: ${formatTime(startHour, startMinute)}")
            }
        }

        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Button(
                onClick = {
                    val safeName = if (name.isBlank()) "Мой шаблон" else name.trim()
                    onSave(Template(safeName, deadlineHour, deadlineMinute, tasks.toList()))
                },
                enabled = tasks.isNotEmpty()
            ) { Text("Сохранить") }
            Button(onClick = onBack) { Text("Назад") }
            if (initialTemplate != null) {
                TextButton(onClick = onDelete) { Text("Удалить") }
            }
        }
    }
}

@Composable
fun FocusScreen(
    template: Template,
    onFinish: () -> Unit
) {
    val context = LocalContext.current
    DisposableEffect(Unit) {
        val activity = context.findActivity()
        activity?.window?.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        onDispose {
            activity?.window?.clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        }
    }

    val tts = rememberFocusTts()
    var currentIndex by remember { mutableIntStateOf(0) }
    var isPaused by remember { mutableStateOf(false) }
    var remainingSeconds by remember { mutableIntStateOf(template.tasks[0].minutes * 60) }

    val currentTask = template.tasks.getOrNull(currentIndex)

    LaunchedEffect(currentIndex) {
        val task = template.tasks.getOrNull(currentIndex)
        if (task == null) {
            tts?.speak("Готово. Время выходить", TextToSpeech.QUEUE_FLUSH, null, "done")
            delay(700)
            onFinish()
        } else {
            remainingSeconds = task.minutes * 60
            tts?.speak("Пора: ${task.name}", TextToSpeech.QUEUE_FLUSH, null, "step_$currentIndex")
        }
    }

    LaunchedEffect(currentIndex, isPaused, remainingSeconds) {
        if (!isPaused && currentTask != null && remainingSeconds > 0) {
            delay(1000)
            remainingSeconds -= 1
        } else if (!isPaused && currentTask != null && remainingSeconds == 0) {
            currentIndex += 1
        }
    }

    val progress = if (currentTask == null) 0f else remainingSeconds / (currentTask.minutes * 60f)
    val targetColor = when {
        progress > 0.6f -> Color(0xFF2E7D32)
        progress > 0.3f -> Color(0xFFF9A825)
        else -> Color(0xFFC62828)
    }
    val animatedColor by animateColorAsState(targetValue = targetColor, label = "timerColor")

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = currentTask?.name ?: "Завершение",
            style = MaterialTheme.typography.headlineSmall,
            textAlign = TextAlign.Center
        )
        Spacer(modifier = Modifier.height(24.dp))
        Text(
            text = String.format(Locale.getDefault(), "%02d:%02d", remainingSeconds / 60, remainingSeconds % 60),
            fontSize = 72.sp,
            fontWeight = FontWeight.ExtraBold,
            color = animatedColor
        )
        Spacer(modifier = Modifier.height(24.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Button(onClick = { isPaused = !isPaused }) {
                Text(if (isPaused) "Продолжить" else "Пауза")
            }
            Button(
                onClick = {
                    if (currentIndex < template.tasks.lastIndex) {
                        currentIndex += 1
                    } else {
                        tts?.speak("Готово. Время выходить", TextToSpeech.QUEUE_FLUSH, null, "done_manual")
                        onFinish()
                    }
                }
            ) {
                Text("Следующий шаг")
            }
        }
        Spacer(modifier = Modifier.height(8.dp))
        Button(onClick = onFinish) { Text("Завершить") }
    }
}

@Composable
fun rememberFocusTts(): TextToSpeech? {
    val context = LocalContext.current
    var tts by remember { mutableStateOf<TextToSpeech?>(null) }
    DisposableEffect(Unit) {
        val engine = TextToSpeech(context.applicationContext) { status ->
            if (status == TextToSpeech.SUCCESS) {
                val localeStatus = engine.setLanguage(Locale("ru", "RU"))
                if (localeStatus == TextToSpeech.LANG_MISSING_DATA || localeStatus == TextToSpeech.LANG_NOT_SUPPORTED) {
                    engine.setLanguage(Locale.getDefault())
                }
            }
        }
        tts = engine
        onDispose {
            tts?.stop()
            tts?.shutdown()
            tts = null
        }
    }
    return tts
}
