package com.neodpi.app.utility

import android.app.Activity
import android.content.Intent
import android.net.Uri
import androidx.appcompat.app.AlertDialog
import com.neodpi.app.BuildConfig
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.net.URL

object UpdateUtils {

    private const val API_URL = "https://api.github.com/repos/Kolya-YT/NeoDPI/releases/latest"

    data class Release(val version: String, val url: String)

    suspend fun checkForUpdate(): Release? = withContext(Dispatchers.IO) {
        try {
            val json = URL(API_URL).readText()
            val obj = JSONObject(json)
            val tag = obj.getString("tag_name").trimStart('v')
            val htmlUrl = obj.getString("html_url")

            // Find APK asset for current ABI
            val assets = obj.getJSONArray("assets")
            var apkUrl = htmlUrl
            for (i in 0 until assets.length()) {
                val asset = assets.getJSONObject(i)
                val name = asset.getString("name")
                if (name.endsWith(".apk") && name.contains("universal")) {
                    apkUrl = asset.getString("browser_download_url")
                    break
                }
            }

            if (isNewer(tag, BuildConfig.VERSION_NAME)) Release(tag, apkUrl) else null
        } catch (e: Exception) {
            null
        }
    }

    private fun isNewer(latest: String, current: String): Boolean {
        fun parse(v: String) = v.split(".").map { it.toIntOrNull() ?: 0 }
        val l = parse(latest)
        val c = parse(current)
        for (i in 0 until maxOf(l.size, c.size)) {
            val lv = l.getOrElse(i) { 0 }
            val cv = c.getOrElse(i) { 0 }
            if (lv > cv) return true
            if (lv < cv) return false
        }
        return false
    }

    fun showUpdateDialog(activity: Activity, release: Release) {
        if (activity.isFinishing || activity.isDestroyed) return
        AlertDialog.Builder(activity)
            .setTitle("Доступно обновление ${release.version}")
            .setMessage("Текущая версия: ${BuildConfig.VERSION_NAME}\n\nХотите скачать новую версию?")
            .setPositiveButton("Скачать") { _, _ ->
                activity.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(release.url)))
            }
            .setNegativeButton("Позже", null)
            .show()
    }
}
