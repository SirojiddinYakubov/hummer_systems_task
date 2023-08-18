![banner](https://i.postimg.cc/brrfqW8k/banner.jpg "banner")

<div align="center">
  <h1>API for Hummer Systems Task. </h1>
</div>

## Run project
We use the <a href="https://infobip.com/">InfoBip SMS service</a> to confirm the phone number and send the invite code via SMS. We need to get the API key and base url by going to this url: https://portal.infobip.com/homepage/

<img src="static/images/infobip.png">

### Clone the project from github
```bash
git clone https://github.com/SirojiddinYakubov/hummer_systems_task.git
```

### Create env file
```bash
cp deploy/.env.example deploy/.env.prod
```
We need to write api key and base url in deploy/.env.prod file

### Start docker containers
```bash
make docker-up
```

## Docs
Control data through django admin: https://onless.uz/admin/
> Test username: +998919791999
> 
> Test password: qwerty12345

You can check all APIs with swagger: https://onless.uz/swagger/ or with postman <a href="/static/postman_collection.json" download>collection</a>

## Base url for API
```
https://onless.uz
```
---
## Register
```
POST /api/v1/auth/register/
```
> Body:
> ```
> phone_number - User phone number
> ```

> Response:
> ```
> {"message": "We send confirmation code and invite code to this phone. Please verify your account and login with invite code!"}
> ```
---
## Verify phone number
```
POST /api/v1/auth/verify-code/
```
> Body:
> ```
> phone_number - User phone number
> code - confirmation code received via sms
> ```

> Response:
> ```
> {"message": "Your account has been verified!"}
> ```
---
## Login via a one-time invite_code
```
POST /api/v1/auth/login/
```

> Body:
> ```
> phone_number - User phone number
> invite_code - invite code received via sms
> ```

> Response:
> ```
> {
>   "token_type": "bearer", 
>   "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5MzIxOTE4NSwiaWF0IjoxNjkyMzU1MTg1LCJqdGkiOiI3MGI5ZmVhMTQwNWE0OWE0YTg1OTYzNzZmYzhjM2M3ZCIsInVzZXJfaWQiOjF9.zjpnMOXerbAanBeKMvjGVG_KG_HSQyU2UR6XbndLvuQ",
>   "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkyMzU4Nzg1LCJpYXQiOjE2OTIzNTUxODUsImp0aSI6IjgyZGQ2NmUwNjE0YjRkMjE5NjU2ODU4ODZhYmNhNTg2IiwidXNlcl9pZCI6MX0.vCb6luLjO31RaaETuwxGWMKzJkKyNyd18wmGel9Eht4"
> }
---
## Set new password
```
POST /api/v1/users/set-password/
```
> Headers:
> ```
> Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkyMzU4Nzg1LCJpYXQiOjE2OTIzNTUxODUsImp0aSI6IjgyZGQ2NmUwNjE0YjRkMjE5NjU2ODU4ODZhYmNhNTg2IiwidXNlcl9pZCI6MX0.vCb6luLjO31RaaETuwxGWMKzJkKyNyd18wmGel9Eht4
> ```

> Body:
> ```
> password - new password for account
> ```

> Response:
> ```
> {"message": "Password successfully changed!"}
> ```
---
## Login with password
```
POST /api/v1/auth/login/
```

> Body:
> ```
> phone_number - User phone number
> password - User password
> ```

> Response:
> ```
> {
>   "token_type": "bearer", 
>   "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5MzIxOTE4NSwiaWF0IjoxNjkyMzU1MTg1LCJqdGkiOiI3MGI5ZmVhMTQwNWE0OWE0YTg1OTYzNzZmYzhjM2M3ZCIsInVzZXJfaWQiOjF9.zjpnMOXerbAanBeKMvjGVG_KG_HSQyU2UR6XbndLvuQ",
>   "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkyMzU4Nzg1LCJpYXQiOjE2OTIzNTUxODUsImp0aSI6IjgyZGQ2NmUwNjE0YjRkMjE5NjU2ODU4ODZhYmNhNTg2IiwidXNlcl9pZCI6MX0.vCb6luLjO31RaaETuwxGWMKzJkKyNyd18wmGel9Eht4"
> }
---
## Get user info
```
GET /api/v1/users/me/
```
> Headers:
> ```
> Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkyMzU4Nzg1LCJpYXQiOjE2OTIzNTUxODUsImp0aSI6IjgyZGQ2NmUwNjE0YjRkMjE5NjU2ODU4ODZhYmNhNTg2IiwidXNlcl9pZCI6MX0.vCb6luLjO31RaaETuwxGWMKzJkKyNyd18wmGel9Eht4
> ```

> Response:
> ```
> {
>    "id": 1,
>    "phone_number": "+998919791999",
>    "invite_code": {
>        "code": ":;@#{-"
>    }
> }
> ```
---
## Get user list
```
GET /api/v1/users/list/
```
> Params
> ```
> search - any text for search
>```

> Headers:
> ```
> Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkyMzU4Nzg1LCJpYXQiOjE2OTIzNTUxODUsImp0aSI6IjgyZGQ2NmUwNjE0YjRkMjE5NjU2ODU4ODZhYmNhNTg2IiwidXNlcl9pZCI6MX0.vCb6luLjO31RaaETuwxGWMKzJkKyNyd18wmGel9Eht4
> ```

> Response:
> ```
> {
>    "count": 1,
>    "next": null,
>    "previous": null,
>    "results": [
>        {
>            "id": 1,
>            "phone_number": "+998919791999",
>            "invite_code": {
>                "code": ":;@#{-"
>            }
>        }
>    ]
> }
> ```
---
## Request code for phone number verification
```
POST /api/v1/auth/get-code/
```

> Body:
> ```
> phone_number - User phone number
> ```

> Response:
> ```
> {"message": "We have sent you a code via SMS to verify your account."}
> ```
---
## Verify access token
```
POST /api/v1/auth/get-code/
```

> Body:
> ```
> refresh - Refresh token received at login
> ```

> Response:
> ```
> "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkyMzYzODQyLCJpYXQiOjE2OTIyNTA5NzYsImp0aSI6IjJkNTI5ZTMzMGE0ODQzOGZhNWYxMTkxNWNjMjRhN2Y3IiwidXNlcl9pZCI6MX0.OXcxzEXUE4dXv8o83phyzyXBNIYqudUdbJFMPcs0poU"
> ```
## Author

[Sirojiddin Yakubov](https://t.me/Sirojiddin_Yakubov)