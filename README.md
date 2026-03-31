<div align="center">
  <h1>NeoDPI</h1>
  <p>
    <a href="https://github.com/Kolya-YT/NeoDPI/releases/latest"><img src="https://img.shields.io/github/v/release/Kolya-YT/NeoDPI" alt="Latest Release" /></a>
    <a href="https://github.com/Kolya-YT/NeoDPI/releases"><img src="https://img.shields.io/github/downloads/Kolya-YT/NeoDPI/total" alt="Downloads" /></a>
    <a href="https://github.com/Kolya-YT/NeoDPI/blob/master/LICENSE"><img src="https://img.shields.io/github/license/Kolya-YT/NeoDPI" alt="License" /></a>
  </p>
  <p>
    <a href="https://t.me/NeoTunl">Telegram</a> •
    <a href="http://neotun.ru/">Сайт</a>
  </p>
</div>

Инструмент для обхода блокировок DPI. Доступен для **Android** и **Windows**.

Не является VPN. Не шифрует трафик и не скрывает IP-адрес. Использует десинхронизацию пакетов для обхода блокировок.

---

### Платформы

| Платформа | Статус |
|-----------|--------|
| Android | ✅ APK |
| Windows | ✅ EXE (GUI) |

---

### Возможности
- Обход блокировок DPI без VPN
- Автоподбор стратегий десинхронизации
- Встроенная стратегия для Telegram
- Режимы: VPN (Android) / Proxy (Android + Windows)
- Раздельное туннелирование приложений (Android)
- Системный прокси для всего ПК (Windows)
- Автозапуск при старте устройства/системы
- Импорт/экспорт настроек (Android)
- История стратегий командной строки

---

### Android

#### Установка
Скачай APK из [Releases](https://github.com/Kolya-YT/NeoDPI/releases/latest) и установи на устройство.

#### Использование с AdGuard
1. Запусти NeoDPI в режиме прокси
2. Добавь NeoDPI в исключения AdGuard → "Управление приложениями"
3. В настройках AdGuard укажи прокси:
```
Тип: SOCKS5
Хост: 127.0.0.1
Порт: 1080
```

---

### Windows

#### Требования
- Windows 10/11
- Python 3.10+ (для запуска из исходников)

#### Запуск из исходников
```bash
pip install customtkinter pystray pillow
python windows/main.py
```

#### Использование
1. Нажми **Старт** — прокси запустится и системный прокси включится автоматически
2. Весь трафик браузеров и приложений пойдёт через NeoDPI
3. Нажми **Стоп** для отключения

---

### Сборка Android

```bash
git clone --recurse-submodules https://github.com/Kolya-YT/NeoDPI.git
cd NeoDPI
./gradlew assembleRelease
```

APK будет в `app/build/outputs/apk/release/`

> Для сборки на Windows нужен WSL или MSYS2 для компиляции нативных библиотек.

---

### Зависимости
- [ByeDPI](https://github.com/hufrea/byedpi)
- [hev-socks5-tunnel](https://github.com/heiher/hev-socks5-tunnel)
