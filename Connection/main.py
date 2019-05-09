import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print("Error")

def on_close(ws):
    print("Close")

def on_open(ws):
    print("Connected.")

    def run(*args, ws):
        for i in range(3):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)

    thread.start_new_thread(run, (ws))


def main():
    ws = websocket.WebSocketApp("ws://192.168.43.36:5000/connect/robot",
                             on_message=on_message,
                             on_error=on_error,
                             on_close=on_close)
    ws.on_open = on_open

    while True:
        ws.run_forever()
        time.sleep(1)

if __name__ == "__main__":
    main()