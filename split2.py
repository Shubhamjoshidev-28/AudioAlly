import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import shutil
from pathlib import Path
import random

class DatasetSplitterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YOLO Dataset Splitter")
        self.root.geometry("700x650")
        
        self.create_widgets()
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Dataset Train/Val/Test Splitter", 
                                font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Source Folders Frame
        source_frame = ttk.LabelFrame(main_frame, text="Source Folders", padding="10")
        source_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Images Folder
        ttk.Label(source_frame, text="Images Folder:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.images_path_var = tk.StringVar()
        ttk.Entry(source_frame, textvariable=self.images_path_var, width=50).grid(row=0, column=1, pady=5, padx=5)
        ttk.Button(source_frame, text="Browse", command=self.browse_images).grid(row=0, column=2, padx=5)
        
        # Labels Folder
        ttk.Label(source_frame, text="Labels Folder:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.labels_path_var = tk.StringVar()
        ttk.Entry(source_frame, textvariable=self.labels_path_var, width=50).grid(row=1, column=1, pady=5, padx=5)
        ttk.Button(source_frame, text="Browse", command=self.browse_labels).grid(row=1, column=2, padx=5)
        
        # Output Folder
        ttk.Label(source_frame, text="Output Folder:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.output_path_var = tk.StringVar()
        ttk.Entry(source_frame, textvariable=self.output_path_var, width=50).grid(row=2, column=1, pady=5, padx=5)
        ttk.Button(source_frame, text="Browse", command=self.browse_output).grid(row=2, column=2, padx=5)
        
        # Split Ratio Frame
        ratio_frame = ttk.LabelFrame(main_frame, text="Split Ratios", padding="10")
        ratio_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(ratio_frame, text="Enter ratios in decimal (0.0-1.0) or percentage (1-100)", 
                  font=('Arial', 9, 'italic')).grid(row=0, column=0, columnspan=4, pady=5)
        
        # Train Ratio
        ttk.Label(ratio_frame, text="Train:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.train_ratio_var = tk.StringVar(value="0.7")
        ttk.Entry(ratio_frame, textvariable=self.train_ratio_var, width=10).grid(row=1, column=1, pady=5)
        
        # Validation Ratio
        ttk.Label(ratio_frame, text="Validation:").grid(row=1, column=2, sticky=tk.W, pady=5, padx=5)
        self.val_ratio_var = tk.StringVar(value="0.2")
        ttk.Entry(ratio_frame, textvariable=self.val_ratio_var, width=10).grid(row=1, column=3, pady=5)
        
        # Test Ratio
        ttk.Label(ratio_frame, text="Test:").grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.test_ratio_var = tk.StringVar(value="0.1")
        ttk.Entry(ratio_frame, textvariable=self.test_ratio_var, width=10).grid(row=2, column=1, pady=5)
        
        # Optional: Skip test split
        self.skip_test_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(ratio_frame, text="Skip Test Split (Only Train/Val)", 
                       variable=self.skip_test_var, 
                       command=self.toggle_test).grid(row=2, column=2, columnspan=2, sticky=tk.W, padx=5)
        
        # Options Frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Random Seed
        ttk.Label(options_frame, text="Random Seed:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.seed_var = tk.StringVar(value="42")
        ttk.Entry(options_frame, textvariable=self.seed_var, width=10).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Copy or Move
        ttk.Label(options_frame, text="Action:").grid(row=0, column=2, sticky=tk.W, pady=5, padx=(20,0))
        self.action_var = tk.StringVar(value="copy")
        ttk.Radiobutton(options_frame, text="Copy", variable=self.action_var, 
                       value="copy").grid(row=0, column=3, sticky=tk.W)
        ttk.Radiobutton(options_frame, text="Move", variable=self.action_var, 
                       value="move").grid(row=0, column=4, sticky=tk.W)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        self.split_btn = ttk.Button(btn_frame, text="Split Dataset", 
                                    command=self.split_dataset, width=20)
        self.split_btn.grid(row=0, column=0, padx=5)
        
        ttk.Button(btn_frame, text="Clear Log", command=self.clear_log, width=15).grid(row=0, column=1, padx=5)
        
        # Log Output
        ttk.Label(main_frame, text="Log:").grid(row=5, column=0, sticky=tk.W, pady=(10,5))
        self.log_text = scrolledtext.ScrolledText(main_frame, width=80, height=15, wrap=tk.WORD)
        self.log_text.grid(row=6, column=0, columnspan=3, pady=5)
        
    def browse_images(self):
        folder = filedialog.askdirectory(title="Select Images Folder")
        if folder:
            self.images_path_var.set(folder)
            
    def browse_labels(self):
        folder = filedialog.askdirectory(title="Select Labels Folder")
        if folder:
            self.labels_path_var.set(folder)
            
    def browse_output(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_path_var.set(folder)
            
    def toggle_test(self):
        if self.skip_test_var.get():
            self.test_ratio_var.set("0")
            
    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
        
    def parse_ratio(self, value_str):
        """Convert percentage or decimal to decimal"""
        try:
            value = float(value_str)
            if value > 1:  # Assume percentage
                return value / 100.0
            return value
        except ValueError:
            raise ValueError(f"Invalid ratio: {value_str}")
            
    def validate_inputs(self):
        # Check folders exist
        if not self.images_path_var.get():
            messagebox.showerror("Error", "Please select images folder")
            return False
        if not os.path.exists(self.images_path_var.get()):
            messagebox.showerror("Error", "Images folder does not exist")
            return False
            
        if not self.labels_path_var.get():
            messagebox.showerror("Error", "Please select labels folder")
            return False
        if not os.path.exists(self.labels_path_var.get()):
            messagebox.showerror("Error", "Labels folder does not exist")
            return False
            
        if not self.output_path_var.get():
            messagebox.showerror("Error", "Please select output folder")
            return False
            
        # Validate ratios
        try:
            train_ratio = self.parse_ratio(self.train_ratio_var.get())
            val_ratio = self.parse_ratio(self.val_ratio_var.get())
            test_ratio = self.parse_ratio(self.test_ratio_var.get())
            
            total = train_ratio + val_ratio + test_ratio
            if abs(total - 1.0) > 0.01:
                messagebox.showerror("Error", 
                    f"Ratios must sum to 1.0 (or 100%). Current sum: {total:.2f}")
                return False
                
            if train_ratio <= 0 or val_ratio <= 0:
                messagebox.showerror("Error", "Train and Validation ratios must be greater than 0")
                return False
                
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return False
            
        return True
        
    def split_dataset(self):
        if not self.validate_inputs():
            return
            
        try:
            self.split_btn.config(state=tk.DISABLED)
            self.log("=" * 60)
            self.log("🚀 Starting Dataset Split")
            self.log("=" * 60)
            
            # Parse ratios
            train_ratio = self.parse_ratio(self.train_ratio_var.get())
            val_ratio = self.parse_ratio(self.val_ratio_var.get())
            test_ratio = self.parse_ratio(self.test_ratio_var.get())
            
            self.log(f"\n📊 Split Ratios:")
            self.log(f"  Train: {train_ratio*100:.1f}%")
            self.log(f"  Validation: {val_ratio*100:.1f}%")
            if test_ratio > 0:
                self.log(f"  Test: {test_ratio*100:.1f}%")
            
            # Get paths
            images_dir = Path(self.images_path_var.get())
            labels_dir = Path(self.labels_path_var.get())
            output_dir = Path(self.output_path_var.get())
            
            # Get all image files
            image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff']
            image_files = []
            for ext in image_extensions:
                image_files.extend(list(images_dir.glob(f'*{ext}')))
                image_files.extend(list(images_dir.glob(f'*{ext.upper()}')))
            
            if not image_files:
                messagebox.showerror("Error", "No image files found in images folder")
                return
                
            self.log(f"\n📁 Found {len(image_files)} images")
            
            # Match with labels
            matched_pairs = []
            unmatched_images = []
            
            for img_path in image_files:
                label_path = labels_dir / (img_path.stem + '.txt')
                if label_path.exists():
                    matched_pairs.append((img_path, label_path))
                else:
                    unmatched_images.append(img_path.name)
            
            self.log(f"✅ Matched pairs: {len(matched_pairs)}")
            if unmatched_images:
                self.log(f"⚠️  Unmatched images: {len(unmatched_images)}")
                self.log(f"   First few: {', '.join(unmatched_images[:5])}")
            
            if not matched_pairs:
                messagebox.showerror("Error", "No matching image-label pairs found")
                return
            
            # Shuffle with seed
            random.seed(int(self.seed_var.get()))
            random.shuffle(matched_pairs)
            
            # Calculate split indices
            total = len(matched_pairs)
            train_end = int(total * train_ratio)
            val_end = train_end + int(total * val_ratio)
            
            train_pairs = matched_pairs[:train_end]
            val_pairs = matched_pairs[train_end:val_end]
            test_pairs = matched_pairs[val_end:] if test_ratio > 0 else []
            
            self.log(f"\n📦 Split Distribution:")
            self.log(f"  Train: {len(train_pairs)} samples")
            self.log(f"  Validation: {len(val_pairs)} samples")
            if test_pairs:
                self.log(f"  Test: {len(test_pairs)} samples")
            
            # Create output directories
            splits = {
                'train': train_pairs,
                'val': val_pairs
            }
            if test_pairs:
                splits['test'] = test_pairs
            
            action_func = shutil.copy2 if self.action_var.get() == "copy" else shutil.move
            action_name = "Copying" if self.action_var.get() == "copy" else "Moving"
            
            self.log(f"\n🔄 {action_name} files...")
            
            for split_name, pairs in splits.items():
                # Create directories
                img_out_dir = output_dir / split_name / 'images'
                lbl_out_dir = output_dir / split_name / 'labels'
                img_out_dir.mkdir(parents=True, exist_ok=True)
                lbl_out_dir.mkdir(parents=True, exist_ok=True)
                
                # Copy/Move files
                for img_path, lbl_path in pairs:
                    action_func(str(img_path), str(img_out_dir / img_path.name))
                    action_func(str(lbl_path), str(lbl_out_dir / lbl_path.name))
                
                self.log(f"  ✓ {split_name}: {len(pairs)} files")
            
            self.log("\n" + "=" * 60)
            self.log("✅ Dataset split completed successfully!")
            self.log(f"📁 Output directory: {output_dir}")
            self.log("=" * 60)
            
            # Show directory structure
            self.log("\n📂 Created directory structure:")
            self.log(f"{output_dir.name}/")
            for split_name in splits.keys():
                self.log(f"├── {split_name}/")
                self.log(f"│   ├── images/")
                self.log(f"│   └── labels/")
            
            messagebox.showinfo("Success", "Dataset split completed successfully!")
            
        except Exception as e:
            self.log(f"\n❌ Error: {str(e)}")
            messagebox.showerror("Error", str(e))
            
        finally:
            self.split_btn.config(state=tk.NORMAL)

def main():
    root = tk.Tk()
    app = DatasetSplitterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()