import logging
import tkinter as tk
from tkinter import ttk


"""
Simple industrial monitoring dashboard demo using Python Tkinter.

The layout includes:
- device/sensor list on the left
- current status panel on the top right
- chart placeholder area in the middle
- event log and control buttons at the bottom
"""

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)


class MonitoringApp(tk.Tk):
    """Sample industrial monitoring dashboard built with Tkinter."""

    def __init__(self) -> None:
        super().__init__()

        self.title("Industrial Monitoring Dashboard (Sample)")
        self.geometry("1000x600")

        self._create_header()
        self._create_main_area()

    # ===== UI construction methods ========================================

    def _create_header(self) -> None:
        """Create the top header bar with title and connection status."""
        header = ttk.Frame(self, padding=10)
        header.pack(side=tk.TOP, fill=tk.X)

        self.title_label = ttk.Label(
            header,
            text="Industrial Monitoring Dashboard",
            font=("Segoe UI", 16, "bold"),
        )
        self.title_label.pack(side=tk.LEFT)

        self.status_label = ttk.Label(
            header,
            text="Status: Disconnected",
            foreground="red",
            font=("Segoe UI", 10, "bold"),
        )
        self.status_label.pack(side=tk.RIGHT)

    def _create_main_area(self) -> None:
        """Create the main split layout: left device list, right details."""
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self._create_left_panel(main_frame)
        self._create_right_panel(main_frame)

    def _create_left_panel(self, parent: ttk.Frame) -> None:
        """Create the left-hand device/sensor list."""
        left_panel = ttk.Frame(parent, padding=10)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(left_panel, text="Devices / Sensors").pack(anchor=tk.W)

        self.device_list = tk.Listbox(left_panel, height=20)
        self.device_list.pack(fill=tk.Y, expand=True)

        # sample device names
        for name in (
            "Line A - Motor 1",
            "Line A - Pump 2",
            "Line B - Sensor 3",
            "Line C - Valve 4",
        ):
            self.device_list.insert(tk.END, name)

        self.device_list.bind("<<ListboxSelect>>", self.on_select_device)

    def _create_right_panel(self, parent: ttk.Frame) -> None:
        """Create the right-hand status, chart placeholder and log."""
        right_panel = ttk.Frame(parent, padding=10)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._create_status_frame(right_panel)
        self._create_chart_frame(right_panel)
        self._create_bottom_frame(right_panel)

    def _create_status_frame(self, parent: ttk.Frame) -> None:
        """Create the current device status panel."""
        status_frame = ttk.LabelFrame(parent, text="Current Status", padding=10)
        status_frame.pack(fill=tk.X)

        self.selected_device_label = ttk.Label(
            status_frame,
            text="Selected: (none)",
            font=("Segoe UI", 11, "bold"),
        )
        self.selected_device_label.grid(row=0, column=0, columnspan=2, sticky="w")

        ttk.Label(status_frame, text="Temperature:").grid(
            row=1,
            column=0,
            sticky="e",
        )
        self.temp_value = ttk.Label(status_frame, text="- °C")
        self.temp_value.grid(row=1, column=1, sticky="w")

        ttk.Label(status_frame, text="Pressure:").grid(
            row=2,
            column=0,
            sticky="e",
        )
        self.pressure_value = ttk.Label(status_frame, text="- bar")
        self.pressure_value.grid(row=2, column=1, sticky="w")

        ttk.Label(status_frame, text="Status:").grid(
            row=3,
            column=0,
            sticky="e",
        )
        self.device_status = ttk.Label(status_frame, text="Unknown")
        self.device_status.grid(row=3, column=1, sticky="w")

    def _create_chart_frame(self, parent: ttk.Frame) -> None:
        """Create a placeholder area for charts/trends."""
        chart_frame = ttk.LabelFrame(
            parent,
            text="Trend / Chart (placeholder)",
            padding=10,
        )
        chart_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.chart_placeholder = ttk.Label(
            chart_frame,
            text=(
                "(Chart area - can be implemented with matplotlib)\n"
                "This is just a sample GUI layout."
            ),
            anchor="center",
            justify="center",
        )
        self.chart_placeholder.pack(fill=tk.BOTH, expand=True)

    def _create_bottom_frame(self, parent: ttk.Frame) -> None:
        """Create the event log and control buttons at the bottom."""
        bottom_frame = ttk.Frame(parent)
        bottom_frame.pack(fill=tk.X)

        # log area
        log_frame = ttk.LabelFrame(bottom_frame, text="Event Log", padding=5)
        log_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=(5, 0))

        self.log_text = tk.Text(log_frame, height=6, state="disabled")
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        log_scroll = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.configure(yscrollcommand=log_scroll.set)

        # control buttons
        btn_frame = ttk.Frame(bottom_frame, padding=5)
        btn_frame.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Button(
            btn_frame,
            text="Connect",
            command=self.fake_connect,
        ).pack(fill=tk.X)
        ttk.Button(
            btn_frame,
            text="Start Monitoring",
            command=self.fake_start,
        ).pack(fill=tk.X, pady=2)
        ttk.Button(
            btn_frame,
            text="Stop",
            command=self.fake_stop,
        ).pack(fill=tk.X)

    # ===== Event handlers ==================================================

    def on_select_device(self, event: tk.Event | None) -> None:
        """Handle selection change in the device list."""
        selection = self.device_list.curselection()
        if not selection:
            return

        name = self.device_list.get(selection[0])
        self.selected_device_label.config(text=f"Selected: {name}")

        # Sample values for demo purposes
        self.temp_value.config(text="72.5 °C")
        self.pressure_value.config(text="3.2 bar")
        self.device_status.config(text="Normal")

        message = f"Selected device: {name}"
        self.append_log(message)
        logger.info(message)

    def fake_connect(self) -> None:
        """Simulate connecting to devices."""
        self.status_label.config(text="Status: Connected", foreground="green")
        message = "Connected to devices."
        self.append_log(message)
        logger.info(message)

    def fake_start(self) -> None:
        """Simulate starting monitoring."""
        message = "Monitoring started."
        self.append_log(message)
        logger.info(message)

    def fake_stop(self) -> None:
        """Simulate stopping monitoring."""
        message = "Monitoring stopped."
        self.append_log(message)
        logger.info(message)

    def append_log(self, message: str) -> None:
        """Append a message to the on-screen event log."""
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state="disabled")


if __name__ == "__main__":
    app = MonitoringApp()
    logger.info("Starting MonitoringApp demo.")
    app.mainloop()
    logger.info("MonitoringApp demo closed.")
