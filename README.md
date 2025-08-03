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

***Example***

<img width="1786" height="533" alt="Screenshot from 2025-08-03 10-52-45" src="https://github.com/user-attachments/assets/c0f66e62-29f0-40af-af80-f7023dd3f7c6" />
<img width="1786" height="533" alt="Screenshot from 2025-08-03 10-59-37" src="https://github.com/user-attachments/assets/332cd205-682a-4f8f-a1f8-4b19628cf2bc" />
<img width="1786" height="730" alt="Screenshot from 2025-08-03 11-05-59" src="https://github.com/user-attachments/assets/29ff53f4-eafa-4be8-bf8d-275fd580ee4f" />
<img width="1786" height="472" alt="Screenshot from 2025-08-03 11-07-49" src="https://github.com/user-attachments/assets/decb623f-8a55-4a8a-b616-73bad1f91345" />
<img width="1788" height="414" alt="Screenshot from 2025-08-03 11-09-30" src="https://github.com/user-attachments/assets/6a79321b-1949-486c-a477-c2073fb343be" />

<img width="1794" height="532" alt="Screenshot from 2025-08-03 11-21-54" src="https://github.com/user-attachments/assets/e47f4b9c-28c5-4184-8e84-94c594498c37" />

<img width="1193" height="581" alt="Screenshot from 2025-08-03 11-26-56" src="https://github.com/user-attachments/assets/28481079-aca2-46ce-aa60-7ddc29abdc34" />
<img width="1193" height="581" alt="Screenshot from 2025-08-03 11-27-48" src="https://github.com/user-attachments/assets/96a516fd-f29e-4e76-a818-b9c1fd60157f" />
<img width="1273" height="652" alt="Screenshot from 2025-08-03 11-28-21" src="https://github.com/user-attachments/assets/a3b8f52e-5d04-4a5b-b415-1929cccf2004" />
<img width="1273" height="652" alt="Screenshot from 2025-08-03 11-28-54" src="https://github.com/user-attachments/assets/c0320279-5272-4d88-a8f3-ebb372d6c2d6" />


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

