import requests
import threading
import time
import random
import string

# Fungsi untuk membuat payload acak
def generate_payload(size):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))

# Fungsi untuk mengirim permintaan POST
def send_post_request(url, timeout, payload_size):
    try:
        payload = generate_payload(payload_size)
        response = requests.post(url, data={"data": payload}, timeout=timeout)
        print(f"Response: {response.status_code}, Time: {response.elapsed.total_seconds()}s")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

# Fungsi untuk menjalankan stress test
def stress_test(url, timeout, threads, duration, payload_size, num_sockets):
    socket_counter = 0
    def worker():
        nonlocal socket_counter
        end_time = time.time() + duration
        while time.time() < end_time:
            send_post_request(url, timeout, payload_size)
            socket_counter += 1
            if socket_counter % num_sockets == 0:
                print(f"Sedang mengirim {socket_counter} socket ke {url}...")

    thread_list = []
    for _ in range(threads):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()

# Input dari pengguna
url = input("Masukkan URL target (contoh: https://example.com): ")
timeout = float(input("Masukkan timeout untuk setiap permintaan (detik): "))
threads = int(input("Masukkan jumlah threads: "))
duration = int(input("Berapa lama pengujian berlangsung (detik): "))
payload_size = int(input("Masukkan ukuran payload (dalam byte): "))
num_sockets = int(input("Masukkan jumlah socket yang ingin digunakan: "))

print("\nMulai pengujian...\n")
stress_test(url, timeout, threads, duration, payload_size, num_sockets)
print("\nPengujian selesai.")
