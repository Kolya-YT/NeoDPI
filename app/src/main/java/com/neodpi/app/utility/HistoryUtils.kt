package com.neodpi.app.utility

import android.content.Context
import android.content.SharedPreferences
import com.neodpi.app.data.Command
import com.google.gson.Gson
import androidx.core.content.edit

class HistoryUtils(context: Context) {

    private val context = context.applicationContext
    private val sharedPreferences: SharedPreferences = context.getPreferences()
    private val historyKey = "byedpi_command_history"
    private val maxHistorySize = 40

    fun addCommand(command: String) {
        if (command.isBlank()) return

        val history = getHistory().toMutableList()
        val unpinned = history.filter { !it.pinned }
        val search = history.find { it.text == command }

        if (search == null) {
            history.add(0, Command(command))
            if (history.size > maxHistorySize) {
                if (unpinned.isNotEmpty()) {
                    history.remove(unpinned.last())
                }
            }
        }

        saveHistory(history)
    }

    fun pinCommand(command: String) {
        val history = getHistory().toMutableList()
        history.find { it.text == command }?.pinned = true
        saveHistory(history)
    }

    fun unpinCommand(command: String) {
        val history = getHistory().toMutableList()
        history.find { it.text == command }?.pinned = false
        saveHistory(history)
    }

    fun deleteCommand(command: String) {
        val history = getHistory().toMutableList()
        history.removeAll { it.text == command }
        saveHistory(history)
    }

    fun renameCommand(command: String, newName: String) {
        val history = getHistory().toMutableList()
        history.find { it.text == command }?.name = newName
        saveHistory(history)
    }

    fun editCommand(command: String, newText: String) {
        val history = getHistory().toMutableList()
        history.find { it.text == command }?.text = newText
        saveHistory(history)
    }

    fun getHistory(): List<Command> {
        val historyJson = sharedPreferences.getString(historyKey, null)
        return if (historyJson != null) {
            Gson().fromJson(historyJson, Array<Command>::class.java).toList()
        } else {
            val defaults = getDefaultCommands()
            saveHistory(defaults)
            defaults
        }
    }

    private fun getDefaultCommands(): List<Command> = listOf(
        Command(
            text = "-K t,h -s1 -d1 -a1 -At,r,s -f-1 -r1+s -a1",
            pinned = true,
            name = "Telegram"
        ),
        Command(
            text = "-f1+nme -t6 -s1:6+sm -a1 -As -s5:12+sm -a1 -As -d3 -q7 -r6 -Mh -a1",
            pinned = true,
            name = "YouTube"
        ),
        Command(
            text = "-Qr -f-204 -K t,h -s1:5+sm -a1 -As -d1 -s3+s -s5+s -q7 -a1 -As -o2 -f-43 -a1",
            pinned = true,
            name = "Discord"
        ),
        Command(
            text = "-f-200 -Qr -s3:5+sm -a1 -As -d1 -s4+sm -s8+sh -f-300 -d6+sh -a1 -At,r,s -o2 -f-30 -As -r5 -Mh -r6+sh -f-250 -s2:7+s -s3:6+sm -a1",
            pinned = true,
            name = "Универсальная"
        ),
    )

    fun saveHistory(history: List<Command>) {
        val historyJson = Gson().toJson(history)
        sharedPreferences.edit { putString(historyKey, historyJson) }
        ShortcutUtils.update(context)
    }

    fun clearAllHistory() {
        saveHistory(emptyList())
    }

    fun clearUnpinnedHistory() {
        val history = getHistory().filter { it.pinned }
        saveHistory(history)
    }
}
