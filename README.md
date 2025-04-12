## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ResourceMonitorKoro
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Configure the application:
   - Update the `config.py` file with your alert settings and notification preferences.

4. Run the application:
   ```
   python run.py
   ```

5. Access the dashboard:
   - Open your web browser and go to `http://127.0.0.1:5000`.

## Features

- Real-time monitoring of system resources.
- Dashboard displaying resource metrics and top 5 resource-hungry processes.
- Alerts sent via Slack or WhatsApp when resource usage exceeds 90%.
- Automatic management of predefined processes when resource usage is critically high.