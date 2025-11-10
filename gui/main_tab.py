"""Main bot control tab with enhanced design"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, scrolledtext
import threading

from workflows.batch_manager import run_all_batches

class MainTab:
    """Handles the Main Bot tab functionality with modern design"""
    
    def __init__(self, parent, pause_event):
        """Initialize the main tab"""
        self.frame = ttk.Frame(parent, padding=15)
        self.pause_event = pause_event
        self.entries = {}
        self.btn_start = None
        self.btn_pause = None
        self.log_area = None
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create all widgets with modern styling"""
        # Header with icon and title
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=X, pady=(0, 20))
        
        ttk.Label(
            header_frame,
            text="🎮 Chaos Zero Nightmare",
            font=("Segoe UI", 24, "bold"),
            bootstyle="primary"
        ).pack()
        
        ttk.Label(
            header_frame,
            text="Automated Account Management System",
            font=("Segoe UI", 10),
            bootstyle="secondary"
        ).pack()
        
        # Configuration Card
        config_card = ttk.Labelframe(
            self.frame,
            text="⚙ Bot Configuration",
            padding=20,
            bootstyle="primary"
        )
        config_card.pack(fill=X, pady=(0, 15))
        
        self._create_input_fields(config_card)
        
        # Control Buttons
        self._create_control_buttons()
        
        # Log Card
        log_card = ttk.Labelframe(
            self.frame,
            text="📋 Activity Log",
            padding=10,
            bootstyle="info"
        )
        log_card.pack(fill=BOTH, expand=YES, pady=(15, 0))
        
        # Log Area with modern styling
        self.log_area = scrolledtext.ScrolledText(
            log_card,
            width=80,
            height=15,
            font=("Consolas", 9),
            bg="#1a1a1a",
            fg="#00ff00",
            insertbackground="#00ff00",
            relief="flat",
            wrap='word'
        )
        self.log_area.pack(fill=BOTH, expand=YES)
        self.log_area.configure(state='disabled')
    
    def _create_input_fields(self, parent):
        """Create modern input fields"""
        fields = [
            ("Instance Name", "Chaos_Base", "😁"),
            ("Total Accounts", "10", "📊"),
            ("Batch Size", "2", "📦")
        ]
        
        for i, (label_text, default, icon) in enumerate(fields):
            # Create row frame
            row_frame = ttk.Frame(parent)
            row_frame.pack(fill=X, pady=8)
            
            # Label with icon
            label_frame = ttk.Frame(row_frame)
            label_frame.pack(side=LEFT, fill=X, expand=YES)
            
            ttk.Label(
                label_frame,
                text=f"{icon} {label_text}:",
                font=("Segoe UI", 10),
                width=20,
                anchor=W
            ).pack(side=LEFT)
            
            # Entry with modern styling
            entry = ttk.Entry(
                row_frame,
                font=("Segoe UI", 10),
                bootstyle="info",
                width=30
            )
            entry.insert(0, default)
            entry.pack(side=RIGHT, padx=(10, 0))
            
            self.entries[label_text] = entry
    
    def _create_control_buttons(self):
        """Create modern control buttons"""
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=X, pady=15)
        
        # Start Button
        self.btn_start = ttk.Button(
            button_frame,
            text="▶ Start Bot",
            command=self.start_bot,
            bootstyle="success",
            width=20
        )
        self.btn_start.pack(side=LEFT, padx=5, expand=YES)
        
        # Pause/Resume Button
        self.btn_pause = ttk.Button(
            button_frame,
            text="⏸ Pause Bot",
            command=self.toggle_pause,
            bootstyle="warning",
            width=20
        )
        self.btn_pause.pack(side=LEFT, padx=5, expand=YES)
        
        # Stop Button
        self.btn_stop = ttk.Button(
            button_frame,
            text="⏹ Stop Bot",
            command=self.stop_bot,
            bootstyle="danger",
            width=20,
            state=DISABLED
        )
        self.btn_stop.pack(side=LEFT, padx=5, expand=YES)
    
    def get_config(self):
        """Get bot configuration"""
        return {
            'instance_name': self.entries["Instance Name"].get(),
            'total_accounts': int(self.entries["Total Accounts"].get()),
            'batch_size': int(self.entries["Batch Size"].get()),
        }
    
    def validate_config(self):
        """Validate configuration"""
        try:
            config = self.get_config()
            if config['total_accounts'] < 1 or config['batch_size'] < 1:
                raise ValueError("Values must be positive integers.")
            if config['batch_size'] > config['total_accounts']:
                raise ValueError("Batch size cannot exceed total accounts.")
            return True, config
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return False, None
    
    def start_bot(self):
        """Start the bot"""
        valid, config = self.validate_config()
        if not valid:
            return
        
        self.btn_start.config(state=DISABLED)
        self.btn_stop.config(state=NORMAL)
        self.log("🚀 Starting bot...")
        
        threading.Thread(
            target=self._run_bot,
            args=(config,),
            daemon=True
        ).start()
    
    def _run_bot(self, config):
        """Run the bot"""
        try:
            run_all_batches(
                config['instance_name'],
                config['total_accounts'],
                config['batch_size'],
                self.log,
                self.pause_event
            )
            self.log("✅ Bot completed successfully!")
        except Exception as e:
            self.log(f"❌ Error: {e}")
        finally:
            self.btn_start.config(state=NORMAL)
            self.btn_stop.config(state=DISABLED)
    
    def toggle_pause(self):
        """Toggle pause state"""
        if self.pause_event.is_set():
            self.pause_event.clear()
            self.btn_pause.config(text="▶ Resume Bot", bootstyle="success")
            self.log("⏸ Bot paused")
        else:
            self.pause_event.set()
            self.btn_pause.config(text="⏸ Pause Bot", bootstyle="warning")
            self.log("▶ Bot resumed")
    
    def stop_bot(self):
        """Stop the bot"""
        # Implement stop logic here
        self.log("⏹ Bot stopped")
        self.btn_start.config(state=NORMAL)
        self.btn_stop.config(state=DISABLED)
    
    def log(self, message):
        """Write to log"""
        self.log_area.configure(state='normal')
        self.log_area.insert('end', f"{message}\n")
        self.log_area.see('end')
        self.log_area.configure(state='disabled')
    
    def get_frame(self):
        """Return the frame"""
        return self.frame