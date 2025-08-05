import json
import websocket

def on_message(ws, message):
    print("Received message from server:", message)

def on_error(ws, error):
    print("WebSocket error:", error)

def on_close(ws):
    print("WebSocket connection closed")

def on_open(ws):
    print("WebSocket connection opened")
    send_command("turn_on")

def send_command(command):
    message = json.dumps({"command": command})
    ws.send(message)
    print("Sent command to server:", command)

if __name__ == "__main__":
    ws = websocket.WebSocket()
    ws.connect("ws://localhost:8000/ws/raspberry-pi/")

    ws.on_message = on_message
    ws.on_error = on_error
    ws.on_close = on_close
    ws.on_open = on_open

    while True:
        try:
            ws.run_forever()
        except KeyboardInterrupt:
            ws.close()
            break