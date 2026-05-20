import tkinter as tk
from tkinter import ttk
import json
import time
import random

class EncomSluiceGateGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ENCOM-SHORTE-CORE // Binary Sluice-Gate Filter")
        self.root.geometry("750x550")
        self.root.configure(bg="#111111")
        
        # State Control Variables
        self.is_running = False
        self.last_valid_length = None
        self.total_processed = 0
        self.accepted_count = 0
        self.rejected_count = 0
        self.energy_saved = 0.0
        self.energy_per_reject = 0.00000002 # kWh estimation per dropped disk write
        
        # Configure Styling
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Courier", 11, "bold"), background="#222222", foreground="#00FF00")
        
        self.create_widgets()
        self.update_loop()

    def create_widgets(self):
        # --- TITLE BANNER ---
        title = tk.Label(self.root, text="ENCOM-SHORTE SYSTEM V1.0 (PUBLIC DOMAIN)", 
                         font=("Courier", 16, "bold"), bg="#111111", fg="#00FF00")
        title.pack(pady=10)
        
        # --- INTERACTIVE CONTROL BUTTONS ---
        btn_frame = tk.Frame(self.root, bg="#111111")
        btn_frame.pack(pady=10)
        
        self.btn_start = tk.Button(btn_frame, text="START", width=10, bg="#003300", fg="#00FF00", font=("Courier", 12, "bold"), command=self.action_start)
        self.btn_start.grid(row=0, column=0, padx=5)
        
        self.btn_test = tk.Button(btn_frame, text="TEST", width=10, bg="#333300", fg="#FFFF00", font=("Courier", 12, "bold"), command=self.action_test)
        self.btn_test.grid(row=0, column=1, padx=5)
        
        self.btn_resume = tk.Button(btn_frame, text="RESUME", width=10, bg="#000033", fg="#00FFFF", font=("Courier", 12, "bold"), command=self.action_resume)
        self.btn_resume.grid(row=0, column=2, padx=5)
        
        self.btn_end = tk.Button(btn_frame, text="END", width=10, bg="#330000", fg="#FF0000", font=("Courier", 12, "bold"), command=self.action_end)
        self.btn_end.grid(row=0, column=3, padx=5)

        # --- DATA METRICS DASHBOARD ---
        metrics_frame = tk.LabelFrame(self.root, text=" SYSTEM RESOURCE METRICS ", font=("Courier", 10, "bold"), bg="#111111", fg="#00FF00", padx=10, pady=10)
        metrics_frame.pack(pady=15, fill="x", padx=20)
        
        self.lbl_total = tk.Label(metrics_frame, text="Total Ingested Packets: 0", font=("Courier", 11), bg="#111111", fg="#FFFFFF", anchor="w")
        self.lbl_total.pack(fill="x")
        
        self.lbl_accepted = tk.Label(metrics_frame, text="Accepted (New Species Pattern): 0", font=("Courier", 11), bg="#111111", fg="#00FF00", anchor="w")
        self.lbl_accepted.pack(fill="x")
        
        self.lbl_rejected = tk.Label(metrics_frame, text="Truncated/Rejected (Breed Metadata Bloat): 0", font=("Courier", 11), bg="#111111", fg="#FF3333", anchor="w")
        self.lbl_rejected.pack(fill="x")
        
        self.lbl_rate = tk.Label(metrics_frame, text="Sluice Rejection Rate: 0.00%", font=("Courier", 11), bg="#111111", fg="#FFFF00", anchor="w")
        self.lbl_rate.pack(fill="x")
        
        self.lbl_energy = tk.Label(metrics_frame, text="Estimated Energy Saved: 0.00000000 kWh", font=("Courier", 11), bg="#111111", fg="#00FFFF", anchor="w")
        self.lbl_energy.pack(fill="x")

        # --- LIVE TERMINAL OUTPUT MATRIX ---
        term_frame = tk.LabelFrame(self.root, text=" LIVE STREAM ROUTING LOG ", font=("Courier", 10, "bold"), bg="#111111", fg="#00FF00")
        term_frame.pack(pady=10, fill="both", expand=True, padx=20)
        
        self.txt_terminal = tk.Text(term_frame, bg="#000000", fg="#00FF00", font=("Courier", 10), insertbackground="#00FF00")
        self.txt_terminal.pack(fill="both", expand=True, padx=5, pady=5)
        self.txt_terminal.insert("1.0", "SYSTEM STANDBY. PRESS 'START' TO INITIALIZE SLUICE GATE...\n")

    # --- ACTION LOGIC FOR CORE BUTTONS ---
    def action_start(self):
        self.is_running = True
        self.log_to_terminal(">>> EMERGENCY GATE INITIALIZED: Streaming Active.")
        
    def action_test(self):
        self.log_to_terminal(">>> TESTING GATE PATTERNS: Pausing automation to run diagnostics.")
        self.is_running = False
        # Manually force sample packages for testing behavior
        self.process_binary_packet("BINARY_PACKET_LENGTH_64_SPECIES_DOG")
        self.process_binary_packet("BINARY_PACKET_LENGTH_64_SPECIES_DOG") # Duplicate
        self.process_binary_packet("BINARY_PACKET_LENGTH_128_BREED_METADATA_BLOAT") # Rejected length

    def action_resume(self):
        self.is_running = True
        self.log_to_terminal(">>> RESUMING AUTOMATION STREAMS...")

    def action_end(self):
        self.is_running = False
        self.log_to_terminal(">>> GATE SUSPENDED: Absolute Network Lock.")

    # --- CORE FILTER PROCESSOR (SPECIES LENGTH FILTER) ---
    def process_binary_packet(self, packet_string):
        self.total_processed += 1
        current_length = len(packet_string)
        timestamp = time.strftime('%H:%M:%S')

        # Logic: If binary length matches breed metadata changes but species is structurally flat
        if self.last_valid_length is not None and current_length == self.last_valid_length:
            # Rejects breed metadata duplicates
            self.rejected_count += 1
            self.energy_saved += self.energy_per_reject
            self.log_to_terminal(f"[{timestamp}] REJECT: Binary structure redundant. Truncated {current_length} bits.")
        else:
            # Accepts clean baseline structural boundaries
            self.last_valid_length = current_length
            self.accepted_count += 1
            self.log_to_terminal(f"[{timestamp}] ACCEPT: Valid baseline structural profile passed to mainframe.")
            
        self.refresh_dashboard()

    def update_loop(self):
        if self.is_running:
            # Generate random simulated binary data profiles (switching between stable states and breed bloat)
            patterns = [
                "BINARY_PACKET_LENGTH_64_SPECIES_DOG",
                "BINARY_PACKET_LENGTH_64_SPECIES_DOG", # Replicates flat sequential readings
                "BINARY_PACKET_LENGTH_96_BREED_POODLE_METADATA_IGNORE",
            ]
            selected_packet = random.choice(patterns)
            self.process_binary_packet(selected_packet)
            
        # Run every 1500ms (1.5 seconds)
        self.root.after(1500, self.update_loop)

    def refresh_dashboard(self):
        rate = (self.rejected_count / self.total_processed * 100) if self.total_processed > 0 else 0.0
        self.lbl_total.config(text=f"Total Ingested Packets: {self.total_processed}")
        self.lbl_accepted.config(text=f"Accepted (New Species Pattern): {self.accepted_count}")
        self.lbl_rejected.config(text=f"Truncated/Rejected (Breed Metadata Bloat): {self.rejected_count}")
        self.lbl_rate.config(text=f"Sluice Rejection Rate: {rate:.2f}%")
        self.lbl_energy.config(text=f"Estimated Energy Saved: {self.energy_saved:.8f} kWh")

    def log_to_terminal(self, message):
        self.txt_terminal.insert(tk.END, message + "\n")
        self.txt_terminal.see(tk.END)

if __name__ == "__main__":
    window = tk.Tk()
    app = EncomSluiceGateGUI(window)
    window.mainloop()
