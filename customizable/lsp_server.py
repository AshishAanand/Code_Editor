import subprocess
import json
from PyQt5.QtCore import QThread, pyqtSignal

class LSPClient(QThread):
    response_received = pyqtSignal(dict)

    def __init__(self, language_server_path, root_path):
        super().__init__()
        self.language_server_path = language_server_path
        self.root_path = root_path
        self.process = None

    def run(self):
        # Start the LSP server process
        self.process = subprocess.Popen(
            self.language_server_path,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Send the initialization message to the LSP server
        initialize_message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "capabilities": {},
                "rootUri": f"file://{self.root_path}"
            },
        }
        self.send_message(initialize_message)

        # Continuously listen to server responses
        while True:
            output = self.process.stdout.readline()
            if output.strip():
                try:
                    response = json.loads(output)
                    self.response_received.emit(response)
                except json.JSONDecodeError:
                    pass

    def send_message(self, message):
        """Send a JSON-RPC message to the LSP server."""
        if self.process and self.process.stdin:
            self.process.stdin.write(json.dumps(message) + "\n")
            self.process.stdin.flush()

    def stop(self):
        """Terminate the LSP process."""
        if self.process:
            self.process.terminate()
