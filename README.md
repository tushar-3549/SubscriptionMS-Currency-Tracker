## Subscription Management System with Currency Exchange Tracker

This task allows users to subscribe to plans, track their subscriptions, and view currency exchange rates. This system integrates REST APIs, Celery background tasks, external currency APIs, and a simple Bootstrap-based frontend UI.

### Features

- JWT-based user authentication
-  REST APIs for subscription operations
-  Currency Exchange API integration (real-time)
-  Celery background task to log hourly exchange rates
-  Admin panel to manage plans, subscriptions, and exchange logs
-  Bootstrap-powered frontend to list all subscriptions
-  SQLite used for local development

### Django Admin

Superusers can:

- Add / edit / delete Plans
- View all Subscriptions
- View Exchange Rate Logs

### Frontend UI

  - Path: `/subscriptions/`
  - Description: Public-facing page listing all users' subscriptions
  - No login required
  - Powered by Bootstrap
  - Columns Displayed: Username, Plan, Start Date, End Date, Status

###  Models

- **User** (Django built-in)
- **Plan**
  - `name`, `price (USD)`, `duration_days`
- **Subscription**
  - `user`, `plan`, `start_date`, `end_date`, `status` (`active`, `cancelled`, `expired`)
- **ExchangeRateLog**
  - `base_currency`, `target_currency`, `rate`, `fetched_at`

###  REST API Endpoints

| Method | Endpoint                     | Description                                                  |
|--------|------------------------------|--------------------------------------------------------------|
| POST   | `/api/token/`                | Obtain JWT access and refresh tokens                         |
| POST   | `/api/token/refresh/`        | Refresh access token using refresh token                     |
| POST   | `/api/subscribe/`            | Create a new subscription (JWT required)                     |
| GET    | `/api/subscriptions/`        | List logged-in user's subscriptions (JWT required)           |
| POST   | `/api/cancel/`               | Cancel a subscription (JWT required)                         |
| GET    | `/api/exchange-rate/`        | Fetch real-time exchange rate (public, no auth required)     |



### Installation Guide

1. Clone the Repo
```
git clone https://github.com/tushar-3549/SubscriptionMS-Currency-Tracker
cd SubscriptionMS-Currency-Tracker
```
2. Create Virtual Environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install Dependencies: `pip install -r requirements.txt`
4. Run Redis Server: `redis-server`
5. Run Celery Worker: `celery -A subscription_project worker -l info`
6. Run Django Server
```
python manage.py migrate
python manage.py createsuperuser 
python manage.py runserver
```
- Now visit: `http://localhost:8000/subscriptions/`

**Running Celery**

1. Check if Redis is Running: `redis-cli ping`
2. Start the Celery Worker: `celery -A subscription_project worker --loglevel=info`
3. Manually Trigger the Celery Task
   - Open the Django shell: `python manage.py shell`
   - Then run the following in the shell
     ```
     from subscriptions.tasks import fetch_usd_bdt
     fetch_usd_bdt.delay()
     ```
   The .delay() method sends the task to Celery to be executed asynchronously in the background.
   Now, at Admin panel:
   Then, Open the ExchangeRateLog model and verify that a new entry has been added with:
   ```
   base_currency: USD
   target_currency: BDT
   rate: (a number)
   fetched_at: (timestamp)
   ```

