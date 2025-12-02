from monitoring_app import MonitoringApp
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)

if __name__ == "__main__":
    logger.info("Starting MonitoringApp demo.")
    app = MonitoringApp()
    app.mainloop()
    logger.info("MonitoringApp demo closed.")
