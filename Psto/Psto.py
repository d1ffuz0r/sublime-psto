from sublimeplugin import WindowCommand
from sublime import statusMessage
from functools import partial
from os import path, curdir
import sys
sys.path.append(path.abspath(curdir)+'\\xmpppy-0.5.0rc1-py2.5.egg')
from xmpp import JID, Client, Message

settings = {"jid": "",
            "password": "",
            "pstobot": "psto@psto.net",
            "res": "Sublime Text Psto-Plugin"}

class PstoCommand(WindowCommand):
    def __init__(self):
        jid = JID(settings["jid"])
        conn = Client(jid.getDomain(), debug=[])
        if not conn.connect():
            statusMessage("PSTO: connection error")
        if not conn.auth(jid.getNode(), settings["password"], settings["res"]):
            statusMessage("PSTO: autentification error")
        self.conn = conn

    def run(self, window, args):
        view = window.activeView()
        window.showInputPanel("Message:", view.name(), partial(self.onDone), None, None)

    def onDone(self, text):
        if text:
            self.conn.send(Message(to=settings["pstobot"], body=text))
            statusMessage("PSTO: Message sended (%s)" % text)
        else:
            statusMessage("PSTO: Error. Not message")