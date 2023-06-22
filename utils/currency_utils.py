import requests


# {
# "id": 69,
# "Code": "840",
# "Ccy": "USD",
# "CcyNm_RU": "Доллар США",
# "CcyNm_UZ": "AQSH dollari",
# "CcyNm_UZC": "АҚШ доллари",
# "CcyNm_EN": "US Dollar",
# "Nominal": "1",
# "Rate": "10998.06",
# "Diff": "40.7",
# "Date": "14.03.2022"
# },
# {
# "id": 21,
# "Code": "978",
# "Ccy": "EUR",
# "CcyNm_RU": "Евро",
# "CcyNm_UZ": "EVRO",
# "CcyNm_UZC": "EВРО",
# "CcyNm_EN": "Euro",
# "Nominal": "1",
# "Rate": "12062.67",
# "Diff": "-34.26",
# "Date": "14.03.2022"
# },
# {
# "id": 57,
# "Code": "643",
# "Ccy": "RUB",
# "CcyNm_RU": "Российский рубль",
# "CcyNm_UZ": "Rossiya rubli",
# "CcyNm_UZC": "Россия рубли",
# "CcyNm_EN": "Russian Ruble",
# "Nominal": "1",
# "Rate": "94.79",
# "Diff": "2.77",
# "Date": "14.03.2022"
# },

def get_currencies() -> dict:
	currencies = {}

	currency_data = requests.get('https://cbu.uz/ru/arkhiv-kursov-valyut/json/')

	for data in currency_data.json():
		if data["id"] == 69 and not currencies.get("USD"):
			currencies["USD"] = data["Rate"]
			currencies["date"] = data["Date"]
		elif data["id"] == 15 and not currencies.get("CNY"):
			currencies["CNY"] = data["Rate"]
		elif data["id"] == 57 and not currencies.get("RUB"):
			currencies["RUB"] = data["Rate"]

	return currencies
