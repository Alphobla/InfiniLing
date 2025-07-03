from tkinter import Tk, Frame, Label, Button, filedialog, messagebox, ttk, Text, Scrollbar
import os
from whisper.transcriber import Transcriber

class WhisperInterface:
    def __init__(self, master, back_callback=None):
        self.master = master
        self.back_callback = back_callback
        self.master.title("🎤 InfiniLing - Whisper Mode")
        self.master.geometry("700x600")
        self.master.configure(bg='#f8f9fa')

        self.audio_file_path = None
        self.transcriber = None
        self.setup_ui()

    def setup_ui(self):
        # Main container
        main_frame = Frame(self.master, bg='#f8f9fa')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Header with back button
        header_frame = Frame(main_frame, bg='#f8f9fa')
        header_frame.pack(fill='x', pady=(0, 15))

        if self.back_callback:
            back_button = Button(header_frame, text="← Menu", 
                               command=self.back_callback,
                               font=("Segoe UI", 10, "bold"),
                               bg='#95a5a6', fg='white',
                               activebackground='#7f8c8d',
                               relief='flat', bd=0, pady=5, padx=15)
            back_button.pack(side='left')

        # Title
        title_label = Label(main_frame, text="🎤 Audio Transcription", 
                           font=("Segoe UI", 20, "bold"), 
                           bg='#f8f9fa', fg='#2c3e50')
        title_label.pack(pady=(0, 20))

        # File selection frame
        file_frame = Frame(main_frame, bg='#ffffff', relief='raised', bd=1)
        file_frame.pack(fill='x', pady=(0, 20), padx=10)
        file_frame.pack_propagate(False)
        file_frame.configure(height=120)

        Label(file_frame, text="Select Audio File", 
              font=("Segoe UI", 12, "bold"), 
              bg='#ffffff', fg='#2c3e50').pack(pady=(15, 5))

        self.file_label = Label(file_frame, text="No file selected", 
                               font=("Segoe UI", 10), 
                               bg='#ffffff', fg='#7f8c8d')
        self.file_label.pack(pady=5)

        select_button = Button(file_frame, text="Browse Audio Files", 
                              command=self.select_audio_file,
                              font=("Segoe UI", 11, "bold"),
                              bg='#3498db', fg='white',
                              activebackground='#2980b9',
                              relief='flat', bd=0, pady=8, padx=20)
        select_button.pack(pady=10)

        # Transcription controls
        control_frame = Frame(main_frame, bg='#f8f9fa')
        control_frame.pack(fill='x', pady=(0, 20))

        self.transcribe_button = Button(control_frame, text="🎯 Start Transcription", 
                                       command=self.transcribe_audio,
                                       font=("Segoe UI", 12, "bold"),
                                       bg='#27ae60', fg='white',
                                       activebackground='#219a52',
                                       relief='flat', bd=0, pady=12, padx=30,
                                       state='disabled')
        self.transcribe_button.pack(side='left', padx=(0, 10))

        self.save_button = Button(control_frame, text="💾 Save Transcription", 
                                 command=self.save_transcription,
                                 font=("Segoe UI", 12, "bold"),
                                 bg='#f39c12', fg='white',
                                 activebackground='#e67e22',
                                 relief='flat', bd=0, pady=12, padx=30,
                                 state='disabled')
        self.save_button.pack(side='left')

        # Status label
        self.status_label = Label(main_frame, text="Ready to transcribe", 
                                 font=("Segoe UI", 10), 
                                 bg='#f8f9fa', fg='#7f8c8d')
        self.status_label.pack(pady=(0, 10))

        # Transcription result area
        result_frame = Frame(main_frame, bg='#ffffff', relief='raised', bd=1)
        result_frame.pack(expand=True, fill='both', padx=10)

        Label(result_frame, text="Transcription Result", 
              font=("Segoe UI", 12, "bold"), 
              bg='#ffffff', fg='#2c3e50').pack(pady=(15, 5), anchor='w', padx=15)

        # Text area with scrollbar
        text_frame = Frame(result_frame, bg='#ffffff')
        text_frame.pack(expand=True, fill='both', padx=15, pady=(0, 15))

        self.transcription_text = Text(text_frame, 
                                      font=("Segoe UI", 11),
                                      wrap='word',
                                      bg='#ffffff',
                                      fg='#2c3e50',
                                      relief='flat',
                                      bd=5)
        scrollbar = Scrollbar(text_frame, orient='vertical', command=self.transcription_text.yview)
        self.transcription_text.configure(yscrollcommand=scrollbar.set)

        self.transcription_text.pack(side='left', expand=True, fill='both')
        scrollbar.pack(side='right', fill='y')

    def select_audio_file(self):
        """Select an audio file for transcription"""
        filetypes = [
            ("All Audio Files", "*.mp3;*.wav;*.m4a;*.flac;*.aac;*.ogg"),
            ("MP3 Files", "*.mp3"),
            ("WAV Files", "*.wav"),
            ("M4A Files", "*.m4a"),
            ("FLAC Files", "*.flac"),
            ("All Files", "*.*")
        ]
        
        self.audio_file_path = filedialog.askopenfilename(
            title="Select Audio File for Transcription",
            filetypes=filetypes
        )
        
        if self.audio_file_path:
            filename = os.path.basename(self.audio_file_path)
            self.file_label.config(text=f"Selected: {filename}", fg='#27ae60')
            self.transcribe_button.config(state='normal')
            self.status_label.config(text="File selected. Ready to transcribe.")

    def transcribe_audio(self):
        """Transcribe the selected audio file"""
        if not self.audio_file_path:
            messagebox.showwarning("Warning", "Please select an audio file first.")
            return

        try:
            self.status_label.config(text="Initializing transcriber...")
            self.master.update()
            
            if not self.transcriber:
                self.transcriber = Transcriber(model_size="base")
            
            self.status_label.config(text="Transcribing audio... This may take a while.")
            self.transcribe_button.config(state='disabled')
            self.master.update()
            
            # Perform transcription
            transcription = self.transcriber.transcribe(self.audio_file_path)
            
            # Display result
            self.transcription_text.delete(1.0, 'end')
            self.transcription_text.insert(1.0, transcription)
            
            self.save_button.config(state='normal')
            self.transcribe_button.config(state='normal')
            self.status_label.config(text="Transcription completed successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during transcription:\n{str(e)}")
            self.transcribe_button.config(state='normal')
            self.status_label.config(text="Transcription failed. Please try again.")

    def save_transcription(self):
        """Save the transcription to a file"""
        if not self.transcription_text.get(1.0, 'end').strip():
            messagebox.showwarning("Warning", "No transcription to save.")
            return

        try:
            # Suggest filename based on audio file
            if self.audio_file_path:
                suggested_name = os.path.splitext(os.path.basename(self.audio_file_path))[0] + "_transcription.txt"
            else:
                suggested_name = "transcription.txt"

            filepath = filedialog.asksaveasfilename(
                defaultextension=".txt",
                initialvalue=suggested_name,
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
                title="Save Transcription"
            )

            if filepath:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(self.transcription_text.get(1.0, 'end'))
                
                messagebox.showinfo("Success", f"Transcription saved to:\n{filepath}")
                self.status_label.config(text=f"Transcription saved to {os.path.basename(filepath)}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save transcription:\n{str(e)}")

def run_whisper_interface():
    root = Tk()
    app = WhisperInterface(root)
    root.mainloop()