from django.urls import include, path
from rest_framework import routers

from api import views

"""
# GET: /api/v1/clients/
* Return all available clients

# GET: /api/v1/pallets_map/
* Return the pallet-key map

# GET: /api/v1/operators/ (only 'responsabile')
* Return all users with 'operator' status

# GET: /api/v1/ddt/
* Return the list of transport documents
* Available filters:
  * client
  * operator
  * from (date)
  * to (date)
* Pagination parameters:
  * page_size
  * page
  * limit
  * offset

# POST: /api/v1/ddt/
* Add new transport document
* Example (form data):
    serial: 12asd345
    client: 1
    date: 2020-08-17
    pallets: [
        {
            "type": 6,
            "received": 2,
            "returned": 0,
            "moved": 0,
        },
        ...
    ]
    photo: <FILE>

# GET: /api/v1/ddt/<PK>/
* Get single document info

# PATCH: /api/v1/ddt/<PK>/ (only 'responsabile')
* Modify transport documents

# POST: /api/v1/register/ (only 'responsabile')
* Create a new 'operator' account and send a mail with the OTP
* Example request:
    {
        "first_name": "Dawid",
        "last_name": "Weglarz",
        "email": "dawid.weglarz95@gmail.com",
    }

# POST: /api/v1/login/
* Receive the user OTP and returns the authentication token and info
* The OTP is set to "consumed" for this account
* Example request:
    {
        "OTP": "eb6603"
    }

# POST: /api/v1/logout/
* Remove the auth_token for the user
 
* Example response:
    {
        "pk": 4,
        "first_name": "Dawid",
        "last_name": "Weglarz",
        "email": "dawid.weglarz95@gmail.com",
        "user_kind": "OP",
        "auth_token": "7b5468071ab4d2b6e1d2ef341fcbfdc15ce4ac31"
    }


# POST /api/v1/otp-reset/
* POST: Receive the user mail and send a "reset OTP link" to that mail

# GET /ap1/v1/token/
* Check if supplied token is still valid. If it's valid return user info

# /download/excel ?
* Daily
* Monthly
"""

router = routers.DefaultRouter()
router.register(r'ddt', views.DDTViewSet)
router.register(r'client', views.ClientViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('pallets_map/', views.PalletMapView.as_view()),
    path('register/', views.RegistrationView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('token/', views.TokenCheckView.as_view()),
    path('otp-reset/', views.OTPResetView.as_view()),
]
