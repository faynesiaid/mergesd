from flask import Flask, render_template
from flask_socketio import SocketIO
import pytchat
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    chat = pytchat.create(video_id="b85stPjfY1Y")

    @socketio.on('connect')
    def handle_connect():
        print('🔌 Browser terhubung')

    def polling_chat():
        print("▶️ Mulai polling YouTube Live Chat...")
        while chat.is_alive():
            for c in chat.get().sync_items():
                # Ambil isi chat-nya (bukan nama author)
                message = c.message.strip()

                # Hanya ambil jika:
                # - Hanya 1 kata
                # - Maksimal 8 huruf
                if len(message.split()) == 1 and len(message) <= 8:
                    print(f"✅ Menerima kata: {message}")
                    socketio.emit('new_name', message)
                    time.sleep(10)  # ⏱️ jeda 10 detik setelah kirim
                else:
                    print(f"❌ Diabaikan: {message}")

    t = threading.Thread(target=polling_chat)
    t.daemon = True
    t.start()

    socketio.run(app, host='0.0.0.0', port=5000)
