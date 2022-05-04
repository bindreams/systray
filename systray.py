from multiprocessing import Process, Pipe
from threading import Thread
from enum import Enum


class Icon:
    class Command(Enum):
        SET_VISIBLE = 1
        SET_TOOLTIP = 2
        SET_IMAGE = 3
        NOTIFY = 5

    def __init__(self):
        ours, theirs = Pipe()

        self._pipe = ours
        self._process = Process(target=self._spawn, args=(theirs,), daemon=True)
        self._process.start()

        self._visible = False
        self._tooltip = ""
        self._image = None

    @classmethod
    def _spawn(cls, pipe):
        from PySide6.QtGui import QIcon
        from PySide6.QtWidgets import QSystemTrayIcon, QApplication

        app = QApplication()
        icon = QSystemTrayIcon()

        def poll():
            try:
                while True:
                    msg = pipe.recv()

                    if msg[0] == cls.Command.SET_VISIBLE:
                        icon.setVisible(msg[1])
                    elif msg[0] == cls.Command.SET_TOOLTIP:
                        icon.setToolTip(msg[1])
                    elif msg[0] == cls.Command.SET_IMAGE:
                        icon.setIcon(QIcon(msg[1]))
                    elif msg[0] == cls.Command.NOTIFY:
                        icon.showMessage(msg[1], msg[2])
            except EOFError:
                app.exit()

        poll_thread = Thread(target=poll)
        poll_thread.start()
        app.exec()

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        value = bool(value)

        self._pipe.send((self.Command.SET_VISIBLE, value))
        self._visible = value

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

    @property
    def tooltip(self):
        return self._tooltip

    @tooltip.setter
    def tooltip(self, value):
        value = str(value)

        self._pipe.send((self.Command.SET_TOOLTIP, value))
        self._tooltip = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        value = str(value)

        self._pipe.send((self.Command.SET_IMAGE, value))
        self._image = value

    def notify(self, title, message):
        title = str(title)
        message = str(message)

        self._pipe.send((self.Command.NOTIFY, title, message))
