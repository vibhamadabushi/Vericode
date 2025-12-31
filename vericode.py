import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox, simpledialog
import qrcode
from PIL import Image, ImageTk
import cv2
from cryptography.fernet import Fernet
from fpdf import FPDF
import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledFrame
import pandas as pd
import os
import csv

class QRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart QR Generator & Scanner")
        self.root.geometry("900x800")

        self.style = tb.Style("cosmo")

        self.notebook = tb.Notebook(root, bootstyle="primary")
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)

        self.is_dark_mode = False
        self.dark_bg_color = "#1c1c1c"
        self.light_bg_color = "#f9f9f9"

        self.gen_tab = tk.Frame(self.notebook, bg=self.light_bg_color)
        self.scan_tab = tk.Frame(self.notebook, bg=self.light_bg_color)
        self.notebook.add(self.gen_tab, text="➕ Generate QR")
        self.notebook.add(self.scan_tab, text="📷 Scan QR")

        self.fg_color = "black"
        self.bg_color = "white"
        self.qr_img = None
        self.logo_path = None

        self.build_generate_tab()
        self.build_scan_tab()
        
        self.toggle_btn = tb.Button(root, text="🌙 Dark Mode", command=self.toggle_dark_mode)
        self.toggle_btn.pack(pady=10)

    def toggle_dark_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            self.style.theme_use("darkly")
            bg_color = self.dark_bg_color
            self.toggle_btn.config(text="☀️ Light Mode")
        else:
            self.style.theme_use("cosmo")
            bg_color = self.light_bg_color
            self.toggle_btn.config(text="🌙 Dark Mode")

        self.gen_tab.config(bg=bg_color)
        self.scan_tab.config(bg=bg_color)

        for widget in self.gen_tab.winfo_children():
            if isinstance(widget, ScrolledFrame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg=bg_color)
            if isinstance(widget, tk.Label):
                widget.config(bg=bg_color)
        
        for widget in self.scan_tab.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg=bg_color)

    def build_generate_tab(self):
        scrolled_frame = ScrolledFrame(self.gen_tab)
        scrolled_frame.pack(fill="both", expand=True)

        tk.Label(scrolled_frame, text="Generate QR Code", font=("Arial", 20, "bold"), bg=self.light_bg_color).pack(pady=15)

        self.data_entry = tb.Entry(scrolled_frame, width=60)
        self.data_entry.pack(pady=10)

        btn_frame = tk.Frame(scrolled_frame, bg=self.light_bg_color)
        btn_frame.pack(pady=5)
        tb.Button(btn_frame, text="🎨 Foreground", command=self.choose_fg).pack(side="left", padx=5)
        tb.Button(btn_frame, text="🎨 Background", command=self.choose_bg).pack(side="left", padx=5)

        self.pass_var = tk.BooleanVar()
        tb.Checkbutton(scrolled_frame, text="Password Protect", variable=self.pass_var, bootstyle="info").pack(pady=5)
        self.pass_entry = tb.Entry(scrolled_frame, width=30, show="*")
        self.pass_entry.pack(pady=5)
        
        file_frame = tk.Frame(scrolled_frame, bg=self.light_bg_color)
        file_frame.pack(pady=5)
        tb.Button(file_frame, text="📂 Upload File", bootstyle="secondary", command=self.upload_file).pack(side="left", padx=5)
        tb.Button(file_frame, text="🖼️ Upload Logo", bootstyle="info", command=self.upload_logo).pack(side="left", padx=5)
        
        generate_btn_frame = tk.Frame(scrolled_frame, bg=self.light_bg_color)
        generate_btn_frame.pack(pady=15)
        
        tb.Button(generate_btn_frame, text="Generate QR", bootstyle="success", command=self.generate_qr).pack(side="left", padx=5)
        tb.Button(generate_btn_frame, text="Generate from File", bootstyle="primary", command=self.generate_batch_qr).pack(side="left", padx=5)
        
        self.qr_label = tk.Label(scrolled_frame, bg=self.light_bg_color)
        self.qr_label.pack(pady=10)

        save_frame = tk.Frame(scrolled_frame, bg=self.light_bg_color)
        save_frame.pack(pady=5)
        
        tb.Button(save_frame, text="Save as PNG", command=lambda: self.save_qr("png")).pack(side="left", padx=5)
        tb.Button(save_frame, text="Save as JPG", command=lambda: self.save_qr("jpg")).pack(side="left", padx=5)
        tb.Button(save_frame, text="Save as PDF", command=lambda: self.save_qr("pdf")).pack(side="left", padx=5)

    def _generate_and_save_qr(self, data, file_path):
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=self.fg_color, back_color=self.bg_color).convert("RGB")
        
        if self.logo_path:
            try:
                logo = Image.open(self.logo_path)
                qr_width, qr_height = img.size
                logo_size = int(qr_width * 0.2)
                logo.thumbnail((logo_size, logo_size), Image.LANCZOS)
                box = Image.new('RGB', (logo_size + 20, logo_size + 20), 'white')
                box.paste(logo, (10, 10))
                pos = ((qr_width - box.size[0]) // 2, (qr_height - box.size[1]) // 2)
                img.paste(box, pos)
            except Exception as e:
                messagebox.showerror("Error", f"Could not embed logo: {e}")
                self.logo_path = None
        
        img.save(file_path)

    def generate_batch_qr(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel Files", "*.xlsx *.xls"), ("CSV Files", "*.csv")]
        )
        if not file_path:
            return

        column_letter = simpledialog.askstring("Roll No Column", "Enter the letter of the column with Roll Numbers (e.g., 'A', 'B'):")
        if not column_letter or len(column_letter) != 1 or not column_letter.isalpha():
            messagebox.showerror("Invalid Input", "Please enter a single letter (e.g., A, B).")
            return
        
        column_index = ord(column_letter.upper()) - ord('A')
            
        save_dir = filedialog.askdirectory(title="Select a folder to save QR codes")
        if not save_dir:
            return

        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
            
            if column_index >= len(df.columns):
                messagebox.showerror("Error", f"Column '{column_letter.upper()}' does not exist in the file.")
                return

            qr_count = 0
            for index, row in df.iterrows():
                roll_no = row.iloc[column_index]
                if pd.isna(roll_no):
                    continue

                # Prepare the data string with all row details
                # Format: "Column1:Value1 | Column2:Value2 | ..."
                qr_data_parts = [f"{col}: {row[col]}" for col in df.columns]
                qr_data_string = " | ".join(qr_data_parts)
                
                # Use the roll number for the filename
                file_name = f"{roll_no}.png"
                output_path = os.path.join(save_dir, file_name)
                
                self._generate_and_save_qr(qr_data_string, output_path)
                qr_count += 1
            
            messagebox.showinfo("Success", f"Successfully generated {qr_count} QR codes in '{save_dir}'")
        
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def build_scan_tab(self):
        frame = self.scan_tab
        tk.Label(frame, text="Scan QR Code", font=("Arial", 20, "bold"), bg=self.light_bg_color).pack(pady=15)

        tb.Button(frame, text="Upload QR Image", bootstyle="primary", command=self.scan_upload).pack(pady=10)

        self.scan_result = tk.Text(frame, height=10, width=70, wrap="word")
        self.scan_result.pack(pady=10)

    def choose_fg(self):
        color = colorchooser.askcolor()[1]
        if color: self.fg_color = color

    def choose_bg(self):
        color = colorchooser.askcolor()[1]
        if color: self.bg_color = color

    def generate_qr(self):
        data = self.data_entry.get()
        if not data:
            messagebox.showerror("Error", "Please enter some data")
            return

        if self.pass_var.get():
            password = self.pass_entry.get()
            if not password:
                messagebox.showerror("Error", "Password required")
                return
            key = Fernet.generate_key()
            cipher = Fernet(key)
            encrypted = cipher.encrypt(data.encode())
            data = encrypted.decode() + "|" + key.decode()
        
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=self.fg_color, back_color=self.bg_color).convert("RGB")
        
        if self.logo_path:
            try:
                logo = Image.open(self.logo_path)
                
                qr_width, qr_height = img.size
                logo_size = int(qr_width * 0.2)
                
                logo.thumbnail((logo_size, logo_size), Image.LANCZOS)
                
                box = Image.new('RGB', (logo_size + 20, logo_size + 20), 'white')
                box.paste(logo, (10, 10))
                
                pos = ((qr_width - box.size[0]) // 2, (qr_height - box.size[1]) // 2)
                
                img.paste(box, pos)
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not embed logo: {e}")
                self.logo_path = None
        
        self.qr_img = img
        tk_img = ImageTk.PhotoImage(img)
        self.qr_label.config(image=tk_img)
        self.qr_label.image = tk_img

    def save_qr(self, fmt):
        if not self.qr_img:
            messagebox.showerror("Error", "No QR generated")
            return
        path = filedialog.asksaveasfilename(defaultextension=f".{fmt}")
        if path:
            if fmt in ["png", "jpg"]:
                self.qr_img.save(path, fmt.upper())
            else:
                pdf = FPDF()
                pdf.add_page()
                temp = path.replace(".pdf", ".png")
                self.qr_img.save(temp, "PNG")
                pdf.image(temp, x=50, y=50, w=100)
                pdf.output(path)
            messagebox.showinfo("Saved", f"QR saved as {path}")

    def scan_upload(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg")])
        if file_path:
            img = cv2.imread(file_path)
            detector = cv2.QRCodeDetector()
            data, _, _ = detector.detectAndDecode(img)
            if data:
                if "|" in data:
                    encrypted, key = data.rsplit("|", 1)
                    password = simpledialog.askstring("Password", "Enter password:", show="*")
                    if password:
                        try:
                            cipher = Fernet(key.encode())
                            decrypted = cipher.decrypt(encrypted.encode()).decode()
                            self.scan_result.delete("1.0", tk.END)
                            self.scan_result.insert(tk.END, decrypted)
                        except:
                            messagebox.showerror("Error", "Invalid password")
                else:
                    self.scan_result.delete("1.0", tk.END)
                    self.scan_result.insert(tk.END, data)
            else:
                messagebox.showerror("Error", "No QR found")
    
    def upload_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.data_entry.delete(0, tk.END)
                self.data_entry.insert(0, content.strip())
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {e}")

    def upload_logo(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg")]
        )
        if file_path:
            self.logo_path = file_path
            messagebox.showinfo("Success", "Logo image uploaded successfully!")
        else:
            self.logo_path = None

if __name__ == "__main__":
    root = tb.Window(themename="cosmo")
    app = QRApp(root)
    root.mainloop()