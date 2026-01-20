import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from ultralytics import YOLO
from PIL import Image, ImageTk
import threading

class AudioallyModelTester:
    def __init__(self, root):
        self.root = root
        self.root.title("Audioally – Live Model Testing Framework")
        self.root.geometry("1000x650")

        self.model = None
        self.cap = None
        self.running = False

        # -------- TOP CONTROLS --------
        top = tk.Frame(root)
        top.pack(pady=10)

        tk.Button(top, text="Select YOLO Model (.pt)", width=25,
                  command=self.load_model).grid(row=0, column=0, padx=5)

        tk.Button(top, text="Laptop Camera", width=20,
                  command=self.start_laptop_camera).grid(row=0, column=1, padx=5)

        tk.Button(top, text="Phone Camera", width=20,
                  command=self.start_phone_camera).grid(row=0, column=2, padx=5)

        tk.Button(top, text="Stop", width=20,
                  command=self.stop_camera).grid(row=0, column=3, padx=5)

        # -------- STATUS --------
        self.status = tk.Label(root, text="Status: Select a model",
                               fg="blue", font=("Arial", 11))
        self.status.pack(pady=5)

        # -------- VIDEO PANEL --------
        self.video_label = tk.Label(root)
        self.video_label.pack(expand=True)

    # ---------- MODEL ----------
    def load_model(self):
        path = filedialog.askopenfilename(
            title="Select YOLO Model",
            filetypes=[("YOLO model", "*.pt")]
        )
        if path:
            try:
                self.model = YOLO(path)
                self.status.config(
                    text=f"Model loaded: {path.split('/')[-1]}",
                    fg="green"
                )
            except Exception as e:
                messagebox.showerror("Model Error", str(e))

    # ---------- CAMERA ----------
    def start_laptop_camera(self):
        self.start_camera(0)

    def start_phone_camera(self):
        url = filedialog.askstring(
            "Phone Camera",
            "Enter IP camera URL (e.g. http://192.168.1.5:8080/video)"
        )
        if url:
            self.start_camera(url)

    def start_camera(self, source):
        if self.model is None:
            messagebox.showerror("Error", "Please select a model first")
            return

        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            messagebox.showerror("Camera Error", "Unable to open camera")
            return

        self.running = True
        self.status.config(text="Camera running...", fg="green")
        threading.Thread(target=self.detect_loop, daemon=True).start()

    def stop_camera(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.video_label.config(image="")
        self.status.config(text="Camera stopped", fg="red")

    # ---------- DETECTION LOOP ----------
    def detect_loop(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break

            results = self.model(frame, conf=0.4, verbose=False)

            for r in results:
                for box in r.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    label = f"{self.model.names[cls]} {conf:.2f}"

                    cv2.rectangle(frame, (x1, y1), (x2, y2),
                                  (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 8),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                (0, 255, 0), 2)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img = img.resize((900, 500))
            imgtk = ImageTk.PhotoImage(image=img)

            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

        self.stop_camera()


# ---------- MAIN ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = AudioallyModelTester(root)
    root.mainloop()
