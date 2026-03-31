import threading

def start_tray(app, on_show, on_quit):
    try:
        import pystray
        from PIL import Image, ImageDraw

        def make_icon():
            img = Image.new("RGB", (64, 64), color="#5976DF")
            d = ImageDraw.Draw(img)
            d.ellipse([8, 8, 56, 56], fill="white")
            return img

        def show(icon, item):
            icon.stop()
            app.after(0, on_show)

        def quit_app(icon, item):
            icon.stop()
            app.after(0, on_quit)

        icon = pystray.Icon(
            "NeoDPI",
            make_icon(),
            "NeoDPI",
            menu=pystray.Menu(
                pystray.MenuItem("Открыть", show, default=True),
                pystray.MenuItem("Выход", quit_app),
            )
        )
        threading.Thread(target=icon.run, daemon=True).start()
        return icon
    except ImportError:
        return None
