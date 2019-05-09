import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    print(message)

def retry(ws, error):
    ws.close();
    main()

def on_open(ws):
    print("Connected.")

    def run(*args, ws):
        for i in range(3):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)
        ws.


    thread.start_new_thread(run, (ws))


def main():
    ws = websocket.WebSocketApp("ws://192.168.43.36:5000/connect/robot",
                             on_message=on_message,
                             on_error=retry,
                             on_close=retry)
    ws.on_open = on_open
    input("Press a key")

if __name__ == "__main__":
    main()