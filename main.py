import sys
import time
import logging
from platform import OAMPlatform

logger = logging.getLogger("OAM-Platform")

def main():
    logger.info("Starting 5G OA&M Automation and IP Protocol Simulation Platform")
    try:
        platform = OAMPlatform()
        platform.start()
        logger.info("Platform started successfully")
        logger.info("Press Ctrl+C to stop the platform")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping platform due to user interrupt")
        platform.stop()
        logger.info("Platform stopped successfully")
    except Exception as e:
        logger.error(f"Error running platform: {str(e)}")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main()) 