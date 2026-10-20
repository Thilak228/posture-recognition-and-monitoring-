import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
import time
import os
import threading

# Import the main logic from your specified file
from enhanced_pose_estimation_with_email import EnhancedPoseEstimationEmailReporter

class PostureMonitorGUI:
    """
    A graphical user interface for the Enhanced AI Posture Monitor
    with periodic email reporting and a final report graph display.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced AI Posture Monitor")
        self.root.geometry("1200x700")
        self.root.option_add("*Font", "Helvetica 10")

        # --- Style Configuration ---
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TButton", padding=6, relief="flat", font=("Helvetica", 10))
        self.style.configure("TLabel", padding=5)
        self.style.configure("TLabelframe.Label", font=("Helvetica", 11, "bold"))

        # --- Application State ---
        self.monitor = EnhancedPoseEstimationEmailReporter(config_file='email_config.json')
        self.cap = cv2.VideoCapture(0)
        self.is_monitoring = False
        self.monitoring_thread = None

        # --- UI Setup ---
        self.create_widgets()
        self.update_video_feed()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        """
        Creates and arranges all the GUI widgets in the main window.
        """
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Left Panel: Video Feed ---
        video_frame = ttk.LabelFrame(main_frame, text="Camera Feed")
        video_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.video_label = ttk.Label(video_frame)
        self.video_label.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # --- Right Panel: Controls and Statistics ---
        controls_frame = ttk.Frame(main_frame, width=350)
        controls_frame.pack(side=tk.RIGHT, fill=tk.Y)
        controls_frame.pack_propagate(False)

        # --- Control Buttons ---
        status_panel = ttk.LabelFrame(controls_frame, text="Controls & Status")
        status_panel.pack(fill=tk.X, pady=(0, 10))

        self.start_button = ttk.Button(status_panel, text="Start Monitoring", command=self.start_monitoring)
        self.start_button.pack(fill=tk.X, padx=10, pady=5)

        self.stop_button = ttk.Button(status_panel, text="Stop Monitoring", command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_button.pack(fill=tk.X, padx=10, pady=5)

        # --- Status Labels ---
        self.status_label = ttk.Label(status_panel, text="Status: Idle", font=("Helvetica", 10, "bold"))
        self.status_label.pack(fill=tk.X, padx=10, pady=10)

        self.time_label = ttk.Label(status_panel, text="Elapsed Time: 00:00")
        self.time_label.pack(fill=tk.X, padx=10, pady=5)

        self.pose_label = ttk.Label(status_panel, text="Current Pose: N/A")
        self.pose_label.pack(fill=tk.X, padx=10, pady=5)

        # --- Statistics Display ---
        stats_panel = ttk.LabelFrame(controls_frame, text="Session Statistics")
        stats_panel.pack(fill=tk.BOTH, expand=True)

        self.stats_text = tk.Text(stats_panel, height=15, width=40, state=tk.DISABLED, wrap=tk.WORD, font=("Courier", 9))
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def start_monitoring(self):
        """
        Handles the logic for starting a monitoring session.
        """
        if self.is_monitoring:
            return

        self.is_monitoring = True
        self.monitor = EnhancedPoseEstimationEmailReporter(config_file='email_config.json') # Reset session
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Monitoring...", foreground="green")

        # Run monitoring in a separate thread to keep the GUI responsive
        self.monitoring_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        self.update_stats_display() # Start periodic stats updates

    def stop_monitoring(self):
        """
        Handles the logic for stopping a monitoring session and generating reports.
        """
        if not self.is_monitoring:
            return

        self.is_monitoring = False

        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Stopped. Generating final report...", foreground="orange")
        self.root.update_idletasks()

        # Finalize statistics and generate outputs
        stats = self.monitor.calculate_real_pose_statistics()
        self.update_stats_display(stats)

        # Generate final reports in a separate thread to avoid freezing the GUI
        threading.Thread(target=self.generate_final_reports, daemon=True).start()

    def monitoring_loop(self):
        """
        The main loop for processing frames during monitoring. Runs in a thread.
        """
        while self.is_monitoring:
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.01)
                continue

            # The core logic class handles all processing
            self.monitor.process_frame_with_enhanced_detection(frame)
            time.sleep(0.05) # Control processing rate

    def update_video_feed(self):
        """
        Continuously captures frames from the webcam and displays them.
        """
        ret, frame = self.cap.read()
        if not ret:
            self.root.after(20, self.update_video_feed)
            return

        frame = cv2.resize(frame, (800, 600))
        display_frame = frame.copy()

        if self.is_monitoring:
            # Update timers and labels
            elapsed_seconds = int(time.time() - self.monitor.session_start_time.timestamp())
            mins, secs = divmod(elapsed_seconds, 60)
            self.time_label.config(text=f"Elapsed Time: {mins:02d}:{secs:02d}")

            if self.monitor.last_pose:
                self.pose_label.config(text=f"Current Pose: {self.monitor.last_pose.upper()}")

            # Draw landmarks if available from the last processed frame
            try:
                results = self.monitor.pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                if results.pose_landmarks:
                    self.monitor.mp_drawing.draw_landmarks(
                        display_frame, results.pose_landmarks, self.monitor.mp_pose.POSE_CONNECTIONS)
            except Exception:
                pass # This can happen during thread transitions

        # Convert for Tkinter display
        cv2image = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        self.root.after(20, self.update_video_feed)

    def update_stats_display(self, stats=None):
        """
        Updates the statistics text box with the latest data.
        """
        if self.is_monitoring:
            stats = self.monitor.calculate_real_pose_statistics()

        if not stats:
            stats = self.monitor.get_default_statistics()

        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete('1.0', tk.END)

        report_str = (
            f"Duration: {stats['session_minutes']:.1f} min\n"
            f"Frames:   {stats['total_frames']}\n"
            f"Moves:    {stats['transitions']}\n"
            f"Avg Conf: {stats['avg_confidence']:.1f}%\n"
            f"--------------------------------\n"
            f"{'Pose':<12} {'Mins':<8} {'%':<8}\n"
            f"--------------------------------\n"
        )

        for pose in ['standing', 'walking', 'sitting', 'lying', 'fall', 'unknown']:
            p_mins = stats.get(f'{pose}_minutes', 0.0)
            p_perc = stats.get(f'{pose}_percentage', 0.0)
            emoji = {'standing': '🧍', 'walking': '🚶', 'sitting': '💺', 'lying': '🛏️', 'fall': '🚨', 'unknown': '❓'}
            pose_display = f"{emoji.get(pose, '')} {pose.capitalize()}"
            report_str += f"{pose_display:<12} {p_mins:<8.1f} {p_perc:<8.1f}\n"

        self.stats_text.insert(tk.END, report_str)
        self.stats_text.config(state=tk.DISABLED)

        # Schedule next update if still monitoring
        if self.is_monitoring:
            self.root.after(2000, self.update_stats_display)

    def generate_final_reports(self):
        """
        Generates final graphs and schedules the report window display.
        """
        # These I/O bound tasks run in the background
        generated_files = self.monitor.generate_comprehensive_graphs()

        # Schedule the GUI update on the main thread
        self.root.after(0, self.finalize_session_ui, generated_files)

    def finalize_session_ui(self, generated_files):
        """
        Updates the UI after report generation is complete. Runs on the main thread.
        """
        self.status_label.config(text="Status: Final report generated.", foreground="blue")
        
        if generated_files:
            messagebox.showinfo("Report Complete", "Final reports and graphs have been generated. Displaying graphs...")
            self.display_report_window(generated_files)
        else:
            messagebox.showinfo("Report Complete", "Final reports have been generated, but there were no graphs to display.")
        
        self.status_label.config(text="Status: Idle", foreground="black")

    def display_report_window(self, image_paths):
        """
        Creates a new Toplevel window to display the generated report images.
        """
        report_window = tk.Toplevel(self.root)
        report_window.title("Final Session Report")
        report_window.geometry("800x600")

        # Create a scrollable frame
        canvas = tk.Canvas(report_window)
        scrollbar = ttk.Scrollbar(report_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for img_path in image_paths:
            try:
                # Load and resize the image
                original_image = Image.open(img_path)
                original_image.thumbnail((750, 750), Image.Resampling.LANCZOS)
                photo_image = ImageTk.PhotoImage(original_image)

                # Create a label to hold the image
                img_label = ttk.Label(scrollable_frame, image=photo_image)
                img_label.image = photo_image # Keep a reference!
                img_label.pack(pady=10, padx=10)

            except Exception as e:
                print(f"Error loading image {img_path}: {e}")
                error_label = ttk.Label(scrollable_frame, text=f"Could not load image: {os.path.basename(img_path)}")
                error_label.pack(pady=5)

    def on_closing(self):
        """
        Handles the application window being closed.
        """
        if self.is_monitoring:
            if messagebox.askyesno("Quit", "Monitoring is active. Do you want to stop and quit?"):
                self.is_monitoring = False # Stop the thread
                if self.periodic_report_timer:
                    self.root.after_cancel(self.periodic_report_timer)
                time.sleep(0.1) # Allow thread to finish
                self.cap.release()
                self.root.destroy()
        else:
            self.cap.release()
            self.root.destroy()

def check_dependencies():
    """Checks for required files before launching the GUI."""
    required_files = [
        'enhanced_pose_estimation_with_email.py',
        'smtp_email_system.py',
        'enhanced_pose_graphs.py',
        'email_config.json'
    ]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        messagebox.showerror(
            "Missing Files",
            "The following required files are missing:\n\n" + "\n".join(missing_files) +
            "\n\nPlease ensure all files are in the correct directory."
        )
        return False
    return True


if __name__ == "__main__":
    if check_dependencies():
        root = tk.Tk()
        app = PostureMonitorGUI(root)
        root.mainloop()
