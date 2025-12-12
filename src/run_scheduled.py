"""
Day 5: Local scheduler for weather pipeline
Runs pipeline every 15 minutes automatically
"""

import schedule
import time
from datetime import datetime
from weather_pipeline_scheduled import WeatherPipeline
from logger_config import setup_logger

def run_pipeline():
    """Execute pipeline - called by scheduler"""
    logger = setup_logger('scheduler')
    logger.info(f"Scheduled execution triggered at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    pipeline = WeatherPipeline()
    success = pipeline.run()
    
    if success:
        logger.info("Scheduled execution completed successfully")
    else:
        logger.error("Scheduled execution failed")
    
    return success

def main():
    """Main scheduler loop"""
    logger = setup_logger('scheduler')
    
    print("="*70)
    print("WEATHER PIPELINE SCHEDULER")
    print("="*70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Schedule: Every 15 minutes")
    print("Press Ctrl+C to stop")
    print("="*70)
    
    logger.info("Scheduler started")
    logger.info("Schedule: Every 15 minutes")
    
    # Run immediately on startup
    logger.info("Running initial execution")
    run_pipeline()
    
    # Schedule every 15 minutes
    schedule.every(15).minutes.do(run_pipeline)
    
    # Keep running
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
        print("\n" + "="*70)
        print("Scheduler stopped")
        print("="*70)

if __name__ == "__main__":
    main()

