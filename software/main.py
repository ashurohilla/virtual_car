import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow
import mqtt_client
import threading
import piet_client
import video_stream
import gyro
import websocketchanels


if __name__ == "__main__":
    # # Start MQTT client in a separate thread
    # mqtt_thread = threading.Thread(target=mqtt_client.start_mqtt_client)
    # mqtt_thread.daemon = True
    # mqtt_thread.start()
    
    # # Start speech recognition in a separate thread
    # speech_thread = threading.Thread(target=piet_client.sendmessgaetocar)
    # speech_thread.daemon = True
    # speech_thread.start()

    # gyro_thread = threading.Thread(target=gyro.start_gyro_client)
    # gyro_thread.daemon = True
    # gyro_thread.start()
        # Start the WebSocket client in a separate thread
    websocket_thread = threading.Thread(target=websocketchanels.start_websocket_client)
    websocket_thread.daemon = True
    websocket_thread.start()

    # GUI
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

