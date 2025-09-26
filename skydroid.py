import socket
import threading
import time

class SkyCamera:
    def __init__(self, camera_ip="192.168.144.108", camera_port=5000, local_port=60000):
        self.camera_ip = camera_ip
        self.camera_port = camera_port
        self.local_port = local_port

        self.last_distance = None

        self.skysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.skysocket.bind(("0.0.0.0", self.local_port))

    def send_lrf_command(self, command=b"#TPUD2rSLR0055"):
        """
        send this command for requesting range
        """
        self.skysocket.sendto(command, (self.camera_ip, self.camera_port))

    def listen_lrf_data(self):
        """
        Listener
        """
        while True:
            try:
                data, _ = self.skysocket.recvfrom(1024)
                text = data.decode(errors='ignore')

                if "#TPDU" in text and "SLR" in text:
                    hex_value = text.split("SLR")[1][:4]
                    distance_cm = int(hex_value, 16) * 10
                    distance_m = distance_cm / 100
                    self.last_distance = distance_m  # Store the latest value
            except Exception as e:
                print("[Error] Problem receiving data:", e)

    def set_gimbal(self, position="down"):
        """
        Adjust gimbal position
        """
        if position == "down":
            message = b"#TPUG2wPTZ026C"
        elif position == "center":
            message = b"#TPUG2wPTZ056F"
        else:
            print("[Error] Unknown gimbal position:", position)
            return
        self.skysocket.sendto(message, (self.camera_ip, self.camera_port))
        time.sleep(0.2)
        print(f"[Gimbal] Position set to: {position}")
        #TPUG2wPTZ026C      down gimbal
        #TPUG2wPTZ056F      center gimbal
        #TPUG6wGAY0000 1012  -> . <-   ?

        #TPUG2wPTZ0E7F pitch +
        #TPUG2wPTZ0F80 pitch -
        #TPUG2wPTZ106B yaw  +
        #TPUG2wPTZ116C yaw  -
        #TPUG2wPTZ126D roll +
        #TPUG2wPTZ136E roll -

    def start_lrf_listener(self, send_interval=0.5):
        """
        call this function for the LRF Listener
        """
        t_send = threading.Thread(target=self._send_loop, args=(send_interval,), daemon=True)
        t_recv = threading.Thread(target=self.listen_lrf_data, daemon=True)
        t_send.start()
        t_recv.start()

    def _send_loop(self, interval):
        while True:
            self.send_lrf_command()
            time.sleep(interval)

    def get_last_distance(self):
        """
        call for the distace logging
        """
        return self.last_distance

if __name__ == "__main__":
    cam = SkyCamera()
    cam.set_gimbal("down")
    cam.start_lrf_listener()
    try:
        while True:
            dist = cam.get_last_distance()
            if dist is not None:
                print(f"[Distance] {dist:.2f} m")
            else:
                print("[Distance] No data yet...")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nProgram terminated.")
