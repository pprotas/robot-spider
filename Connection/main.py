import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print("retry")
    main()

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)
        # ws.close()
    #     print("thread terminating...")
    thread.start_new_thread(run, ())

def main():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://192.168.43.36:5000/connect/robot",
                             on_message=on_message,
                             on_error=on_error,
                             on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
    input()

if __name__ == "__main__":
    main()