import websocket
import threading
import json
import main_frame

def get_command():
    command = input("type: ")
    message = input("message: ")

    return {
        "type": command,
        "message": message
    }


def on_message(ws, message):
    print((message))


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    print("Opened connection")

def on_msg_custom(ws,message):
    print(message)

def run_ws(ws):
    ws.run_forever()

def run_ws_from_other_program(room_id,self):
    
    ws = websocket.WebSocketApp(f"ws://localhost:8000/ws/api/{room_id}/",
                                on_open=on_open,
                                on_message=self.onMSG,
                                on_error=on_error,
                                on_close=on_close)

    # Start connection thread
    x = threading.Thread(target=run_ws, args=(ws,))
    x.start()
    return ws
if __name__ == "__main__":
    # websocket.enableTrace(True)  # Debugging
    room_id = input("room_id: ")
    ws = websocket.WebSocketApp(f"ws://localhost:8000/ws/api/{room_id}/",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    # Start connection thread
    x = threading.Thread(target=run_ws, args=(ws,))
    x.start()

    # Interact with websocket

    s = get_command()
    while s["type"] != "exit":
        ws.send(json.dumps(s))
        s = get_command()
