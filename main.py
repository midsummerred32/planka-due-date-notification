
from plankapy import Planka, PasswordAuth
import requests
from datetime import datetime, timezone
import json
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
log_level = os.getenv('LOG_LEVEL', 'INFO')
logging.basicConfig(
    level=getattr(logging, log_level.upper()),
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def load_config():
    """Load configuration with environment variable substitution"""
    try:
        with open('config.json', 'r') as config_file:
            config_template = config_file.read()
        
        # Replace environment variables in config
        for key, value in os.environ.items():
            config_template = config_template.replace(f"${{{key}}}", value)
        
        config = json.loads(config_template)
        logger.info("Configuration loaded successfully")
        return config
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        raise

# Load configuration
config = load_config()

logger.info("Starting Planka task checker")

try:
    planka = Planka(config['planka']['url'],
                    PasswordAuth(config['planka']['username'], config['planka']['password']))
    
    logger.info(f"Connected to Planka as user: {planka.me.name}")
    logger.info(f"Found {len(planka.projects)} project(s)")

    # Home Assistant webhook URL
    webhook_url = f"{config['home_assistant']['url']}/api/webhook/{config['home_assistant']['webhook_id']}"
    logger.debug(f"Webhook URL configured: {webhook_url}")

    # Get today's date
    today = datetime.now(timezone.utc).date()
    logger.info(f"Checking for tasks due on: {today}")

    # List all cards with their due dates and check for today's tasks
    cards_due_today = []

    for project in planka.projects:
        logger.debug(f"Processing project: {project.name}")
        for board in project.boards:
            logger.debug(f"  Processing board: {board.name}")
            for list_item in board.lists:
                logger.debug(f"    Processing list: {list_item.name}")
                for card in list_item.cards:
                    if hasattr(card, 'dueDate') and card.dueDate:
                        # Parse the due date
                        due_date = datetime.fromisoformat(card.dueDate.replace('Z', '+00:00'))
                        due_date_only = due_date.date()

                        logger.debug(f"      Card: {card.name} - Due: {card.dueDate}")

                        # Check if due date is today
                        if due_date_only == today:
                            # Construct card URL
                            card_url = f"{config['planka']['url']}/cards/{card.id}"

                            # Format due date for webhook payload
                            formatted_due_date = due_date.strftime("%m/%d/%Y at %I:%M %p")

                            cards_due_today.append({
                                "taskname": card.name,
                                "due_date": formatted_due_date,
                                "card_url": card_url
                            })
                            logger.info(f"Found task due today: {card.name}")
                    else:
                        logger.debug(f"      Card: {card.name} - No due date")

    # Send webhook for cards due today
    if cards_due_today:
        logger.info(f"Found {len(cards_due_today)} card(s) due today. Sending webhooks...")

        for card_info in cards_due_today:
            payload = {
                "taskname": card_info["taskname"],
                "due_date": card_info["due_date"],
                "card_url": card_info["card_url"]
            }

            try:
                logger.debug(f"Sending webhook for task: {card_info['taskname']}")
                response = requests.post(webhook_url, json=payload, timeout=10)
                if response.status_code == 200:
                    logger.info(f"✅ Webhook sent successfully for: {card_info['taskname']}")
                else:
                    logger.error(f"❌ Webhook failed for {card_info['taskname']}: HTTP {response.status_code}")
            except requests.exceptions.RequestException as e:
                logger.error(f"❌ Error sending webhook for {card_info['taskname']}: {e}")
    else:
        logger.info("No cards due today")

    logger.info("Task checker completed successfully")

except Exception as e:
    logger.error(f"Fatal error in task checker: {e}")
    raise
