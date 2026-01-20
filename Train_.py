import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import threading
import os
from pathlib import Path
import yaml

class YOLOTrainerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YOLO Model Trainer")
        self.root.geometry("800x700")
        
        self.training_thread = None
        self.is_training = False
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Model Selection
        ttk.Label(main_frame, text="Model:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.model_var = tk.StringVar(value="yolov8n.pt")
        model_combo = ttk.Combobox(main_frame, textvariable=self.model_var, width=30)
        model_combo['values'] = ('yolov8n.pt', 'yolov8s.pt', 'yolov8m.pt', 'yolov8l.pt', 'yolov8x.pt',
                                   'yolov9c.pt', 'yolov9e.pt', 'yolov10n.pt', 'yolov10s.pt', 'yolov10m.pt')
        model_combo.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Data YAML Path
        ttk.Label(main_frame, text="Data YAML:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.data_path_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.data_path_var, width=40).grid(row=1, column=1, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_data_yaml).grid(row=1, column=2, padx=5)
        
        # Resume Checkpoint
        ttk.Label(main_frame, text="Resume From:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.resume_path_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.resume_path_var, width=40).grid(row=2, column=1, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_resume).grid(row=2, column=2, padx=5)
        
        # Training Parameters Frame
        params_frame = ttk.LabelFrame(main_frame, text="Training Parameters", padding="10")
        params_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Epochs
        ttk.Label(params_frame, text="Epochs:").grid(row=0, column=0, sticky=tk.W, pady=3)
        self.epochs_var = tk.StringVar(value="100")
        ttk.Entry(params_frame, textvariable=self.epochs_var, width=10).grid(row=0, column=1, sticky=tk.W, pady=3)
        
        # Image Size
        ttk.Label(params_frame, text="Image Size:").grid(row=0, column=2, sticky=tk.W, padx=(20,0), pady=3)
        self.imgsz_var = tk.StringVar(value="640")
        ttk.Entry(params_frame, textvariable=self.imgsz_var, width=10).grid(row=0, column=3, sticky=tk.W, pady=3)
        
        # Batch Size
        ttk.Label(params_frame, text="Batch Size:").grid(row=1, column=0, sticky=tk.W, pady=3)
        self.batch_var = tk.StringVar(value="16")
        ttk.Entry(params_frame, textvariable=self.batch_var, width=10).grid(row=1, column=1, sticky=tk.W, pady=3)
        
        # Learning Rate
        ttk.Label(params_frame, text="Learning Rate:").grid(row=1, column=2, sticky=tk.W, padx=(20,0), pady=3)
        self.lr_var = tk.StringVar(value="0.01")
        ttk.Entry(params_frame, textvariable=self.lr_var, width=10).grid(row=1, column=3, sticky=tk.W, pady=3)
        
        # Workers
        ttk.Label(params_frame, text="Workers:").grid(row=2, column=0, sticky=tk.W, pady=3)
        self.workers_var = tk.StringVar(value="8")
        ttk.Entry(params_frame, textvariable=self.workers_var, width=10).grid(row=2, column=1, sticky=tk.W, pady=3)
        
        # Device
        ttk.Label(params_frame, text="Device:").grid(row=2, column=2, sticky=tk.W, padx=(20,0), pady=3)
        self.device_var = tk.StringVar(value="0")
        ttk.Entry(params_frame, textvariable=self.device_var, width=10).grid(row=2, column=3, sticky=tk.W, pady=3)
        
        # Project Name
        ttk.Label(params_frame, text="Project:").grid(row=3, column=0, sticky=tk.W, pady=3)
        self.project_var = tk.StringVar(value="runs/train")
        ttk.Entry(params_frame, textvariable=self.project_var, width=20).grid(row=3, column=1, columnspan=3, sticky=tk.W, pady=3)
        
        # Buttons Frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        self.start_btn = ttk.Button(btn_frame, text="Start Training", command=self.start_training, width=15)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.stop_btn = ttk.Button(btn_frame, text="Stop Training", command=self.stop_training, state=tk.DISABLED, width=15)
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        ttk.Button(btn_frame, text="Clear Log", command=self.clear_log, width=15).grid(row=0, column=2, padx=5)
        
        # Log Output
        ttk.Label(main_frame, text="Training Log:").grid(row=5, column=0, sticky=tk.W, pady=(10,5))
        self.log_text = scrolledtext.ScrolledText(main_frame, width=90, height=20, wrap=tk.WORD)
        self.log_text.grid(row=6, column=0, columnspan=3, pady=5)
        
        # Status Bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5,0))
        
    def browse_data_yaml(self):
        filename = filedialog.askopenfilename(
            title="Select Data YAML",
            filetypes=(("YAML files", "*.yaml *.yml"), ("All files", "*.*"))
        )
        if filename:
            self.data_path_var.set(filename)
            
    def browse_resume(self):
        filename = filedialog.askopenfilename(
            title="Select Checkpoint",
            filetypes=(("PyTorch files", "*.pt"), ("All files", "*.*"))
        )
        if filename:
            self.resume_path_var.set(filename)
            
    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
        
    def validate_inputs(self):
        if not self.data_path_var.get():
            messagebox.showerror("Error", "Please select a data YAML file")
            return False
        
        if not os.path.exists(self.data_path_var.get()):
            messagebox.showerror("Error", "Data YAML file does not exist")
            return False
            
        if self.resume_path_var.get() and not os.path.exists(self.resume_path_var.get()):
            messagebox.showerror("Error", "Resume checkpoint file does not exist")
            return False
            
        return True
        
    def start_training(self):
        if not self.validate_inputs():
            return
            
        self.is_training = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_var.set("Training...")
        
        self.training_thread = threading.Thread(target=self.train_model, daemon=True)
        self.training_thread.start()
        
    def stop_training(self):
        self.is_training = False
        self.status_var.set("Stopping training...")
        self.log("⚠️ Training stop requested...")
        
    def train_model(self):
        try:
            from ultralytics import YOLO
            
            self.log("=" * 60)
            self.log("🚀 Starting YOLO Training")
            self.log("=" * 60)
            
            # Determine if resuming
            resume_path = self.resume_path_var.get()
            if resume_path:
                self.log(f"📂 Loading checkpoint: {resume_path}")
                model = YOLO(resume_path)
                resume_flag = True
            else:
                self.log(f"📂 Loading model: {self.model_var.get()}")
                model = YOLO(self.model_var.get())
                resume_flag = False
            
            # Training parameters
            train_args = {
                'data': self.data_path_var.get(),
                'epochs': int(self.epochs_var.get()),
                'imgsz': int(self.imgsz_var.get()),
                'batch': int(self.batch_var.get()),
                'lr0': float(self.lr_var.get()),
                'workers': int(self.workers_var.get()),
                'device': self.device_var.get(),
                'project': self.project_var.get(),
                'resume': resume_flag
            }
            
            self.log("\n📋 Training Configuration:")
            for key, value in train_args.items():
                self.log(f"  {key}: {value}")
            
            self.log("\n🔥 Training started...\n")
            
            # Train the model
            results = model.train(**train_args)
            
            if self.is_training:
                self.log("\n" + "=" * 60)
                self.log("✅ Training completed successfully!")
                self.log(f"📁 Results saved to: {results.save_dir}")
                self.log("=" * 60)
                self.status_var.set("Training completed!")
            else:
                self.log("\n⚠️ Training stopped by user")
                self.status_var.set("Training stopped")
                
        except Exception as e:
            self.log(f"\n❌ Error: {str(e)}")
            self.status_var.set("Error occurred")
            messagebox.showerror("Training Error", str(e))
            
        finally:
            self.is_training = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = YOLOTrainerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()