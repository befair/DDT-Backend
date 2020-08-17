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
    operator: 1ebe405d-dc5a-4e80-ad4e-105e0feb6603
    client: 1
    date: 2020-08-17
    pallets: [
        {
            "type": 6,
            "received": 2,
            "returned": 0,
            "moved": 0,
            "human_type": "Cestoni"
        },
        ...
    ]
    photo: <FILE>

# GET: /api/v1/ddt/<PK>/
* Get single document info

# PATCH: /api/v1/ddt/<PK>/
* Modify transport documents (only 'responsabile')

# POST: /api/v1/login/
* Receive the user OTP and returns the ID and info
* The OTP is set to null for this account
* Example request:
    {
        "OTP": "eb6603"
    }
* Example response:
    {
        ...
    }

# POST /api/v1/otp-request/
* POST: Receive the user mail and send a "reset OTP link" to that mail

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
    path('login/', views.OTPLoginView.as_view())
]
