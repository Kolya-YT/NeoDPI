package com.neodpi.app.services

import com.neodpi.app.data.AppStatus
import com.neodpi.app.data.Mode

var appStatus = AppStatus.Halted to Mode.VPN
    private set

fun setStatus(status: AppStatus, mode: Mode) {
    appStatus = status to mode
}
