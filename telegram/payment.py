from rest_framework.response import Response
import requests



def create_invoice_func(active_user, fiat_amount, fiat_currency, crypto_currency, order_id):

    location = "https://api.nowpayments.io/v1/invoice"
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': '9PPNE60-72EMTB1-GV53R01-9VEHFKC'
    }
    data = {
        "price_amount": f"{fiat_amount}",
        "price_currency": f"{fiat_currency}",
        "order_id": f"{order_id}",
        "pay_currency":f"{crypto_currency}",
        "order_description": f"{active_user}",
        # "ipn_callback_url": "https://nowpayments.io",
        # "success_url": "https://nowpayments.io",
        # "cancel_url": "https://nowpayments.io"
    }

    try:
        response = requests.post(location, headers=headers, json=data)
        response.raise_for_status()

        # Debugging: Print raw response content
        print(response.content)
        response_data = response.json()
        return Response(response_data)
    except requests.exceptions.RequestException as err:
        print("The payment didn't go through")
        print(err)
        return Response({"error": str(err)}, status=500)
