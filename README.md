# bookshoop-test
web book store for test

```diff
- DO NOT PAY WITH YOUR REAL CARD
! ONLY USE 4242 4242 4242 4242 ITS A TESTING CARD FOR STRIPE PAYMENTS
```

### Start project at local machine

- Clone repo:
```
https://github.com/vanyatheman/bookshoop-test.git
```

- In project repository create .env file, as a template use .env.example:
```
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

SECRET_KEY='django-key'

BOOKS_PER_PAGE=2

STRIPE_PUBLISHABLE_KEY='public key'
STRIPE_SECRET_KEY='secret key'
```

 - Start docker compose:
```
docker compose up -d
```

 - Create superuser:
```
docker compose exec backend python manage.py createsuperuser
```

 - Create a few book objects at admin zone:
[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)


### Sent E-mails

When a user resets password the mail with password reset link is not sent to the user e-mail, instead it goes to the /app/sent_emails directory in the backend container.


### Payment system

- Payment system was implemented via Stripe in test developer mode

Payment for the cart of books:
![](https://i.imgur.com/CS8ggJN.jpg)

Payment check in stripe site:
![](https://i.imgur.com/5z1Skjf.png)
