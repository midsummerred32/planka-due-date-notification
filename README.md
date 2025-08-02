# Planka Task Checker for Home Assistant

A Python script that monitors your Planka kanban boards for tasks due today and sends notifications to Home Assistant via webhooks.

## Features

- 🔍 Monitors all Planka projects and boards for tasks with due dates
- 📅 Identifies tasks due within the next 3 days
- 🏠 Sends webhook notifications to Home Assistant with task details
- 📊 Comprehensive logging with configurable levels
- ⚙️ Environment-based configuration for security
- 🐳 Docker support for containerized deployment
- ⏰ Designed for scheduled execution (every 2 hours recommended)

## Setup

### 1. Environment Configuration

Copy the example environment file and configure your settings:

```bash
cp .env.example .env
```

Edit `.env` with your actual values:

```env
# Planka Configuration
PLANKA_URL=https://your-planka-instance.com
PLANKA_USERNAME=your_username
PLANKA_PASSWORD=your_password

# Home Assistant Configuration
HOME_ASSISTANT_URL=https://your-home-assistant.com
WEBHOOK_ID=your_webhook_id

# Logging Configuration (optional)
LOG_LEVEL=INFO

# Done List Configuration (optional)
# Comma-separated list of list names to exclude from notifications
# Case-insensitive matching
DONE_LISTS=Done,Completed,Finished
```

### 2. Install Dependencies

This project uses UV for dependency management:

```bash
uv sync
```

### 3. Home Assistant Webhook Setup

1. In Home Assistant, go to **Settings** → **Automations & Scenes**
2. Create a new automation
3. Add a **Webhook** trigger
4. Copy the webhook ID from the automation and add it to your `.env` file

Example Home Assistant automation trigger:
```yaml
trigger:
  - platform: webhook
    webhook_id: your_webhook_id
```

The webhook will receive this payload:
```json
{
  "taskname": "Task Name",
  "due_date": "08/02/2025 at 03:30 PM",
  "card_url": "https://your-planka-instance.com/cards/card-id",
  "days_until_due": 1,
  "due_status": "tomorrow"
}
```

#### Quick Setup with Blueprint

This repository includes a Home Assistant blueprint (`home_assistant_automation.yaml`) for easy setup:

**Method 1: Import Blueprint**
1. Copy the contents of `home_assistant_automation.yaml`
2. In Home Assistant, go to **Settings** → **Blueprints**
3. Click **Import Blueprint** and paste the YAML content
4. Create a new automation using the blueprint
5. Fill in your webhook ID and notification target

**Method 2: Direct Automation Import**
1. Go to **Settings** → **Automations & Scenes**
2. Click **⋮** menu → **Import automation**
3. Paste the blueprint YAML content
4. Configure the required inputs

## Usage

### Manual Execution

Run the script once to check for tasks due today:

```bash
python3 main.py
```

### Scheduled Execution (Recommended)

#### Option 1: Replit Scheduled Deployments (Easiest)

1. Click **Deploy** in the Replit interface
2. Select **Scheduled** deployment
3. Set schedule to "Every 2 hours" or use cron: `0 */2 * * *`
4. Set run command to: `python3 main.py`
5. Deploy

#### Option 2: Docker with Cron

Build and run with Docker Compose:

```bash
docker-compose up -d
```

This will run the script every 2 hours using the included scheduler container.

## Configuration Files

### `.env`
Contains sensitive environment variables (never commit this file)

### `.env.example`
Template showing required environment variables

### `config.json`
Configuration template that uses environment variable substitution

### `Dockerfile` & `docker-compose.yml`
Docker configuration for containerized deployment

## Logging

The script provides detailed logging with the following levels:
- `DEBUG`: Detailed information for troubleshooting
- `INFO`: General information about script execution (default)
- `WARNING`: Warning messages
- `ERROR`: Error messages

Set the `LOG_LEVEL` environment variable to control verbosity.

## Webhook Payload

Each task due within the next 3 days will trigger a webhook with:
- `taskname`: Name of the task/card
- `due_date`: Formatted due date (MM/DD/YYYY at HH:MM AM/PM)
- `card_url`: Direct link to the card in Planka
- `days_until_due`: Number of days until the task is due (0 for today, 1 for tomorrow, etc.)
- `due_status`: Human-readable due status ("today", "tomorrow", or "in X days")

## Security Notes

- Never commit your `.env` file to version control
- Use strong, unique webhook IDs in Home Assistant
- Consider using HTTPS for all URLs
- Regularly rotate passwords and webhook IDs

## Troubleshooting

### Common Issues

1. **Authentication Failed**: Check your Planka credentials in `.env`
2. **Webhook Not Received**: Verify Home Assistant URL and webhook ID
3. **No Tasks Found**: Ensure tasks have due dates set within the next 3 days in Planka
4. **Date/Time Issues**: Script uses UTC timezone for date comparisons

### Debug Mode

Set `LOG_LEVEL=DEBUG` in your `.env` file for verbose logging:

```env
LOG_LEVEL=DEBUG
```

This will show detailed information about each project, board, list, and card being processed.

## Development

This project is designed to run on Replit and uses:
- Python 3.11+
- plankapy for Planka API integration
- requests for HTTP webhooks
- python-dotenv for environment management

## License

This project is open source and available under the MIT License.