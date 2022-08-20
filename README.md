# Models

- user
    - id
    - name
    - email
    - password
- app
    - id
    - name
    - owner (`user.id`)
- subscription
    - subscriber 
        - name
        - email
        - subscription (subscribed/unsubscribed)
        - services
    - app (`app.id`)
