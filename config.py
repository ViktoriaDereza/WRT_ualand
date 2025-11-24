
BASE_URL = "https://qa.ualand.space"
BASE_URL_ADMIN = "https://qa.ualand.space/land-admin"
USER_NAME_PARTICIPANT1 = "ukr@gmail.com"
PARTICIPANT1_PROFILE_ID = "142"
USER_NAME_PARTICIPANT2 = "ukr3@gmail.com"
USER_NAME_ORGANIZER = "ukr11@gmail.com"
PASSWORD = "Test12345!"
AUCTION_NAME = "AuctionName"
CSP_PAYLOAD = {
    "bankAccounts": [
        {
            "type": "GUARANTEE",
            "bankAccounts": [
                {
                    "bankName": "monooo",
                    "currency": "UAH",
                    "holderLegalName": "monooo",
                    "holderIdentifierScheme": "UA-IPN",
                    "holderIdentifier": "1212121211",
                    "identifiers": [
                        {
                            "scheme": "UA-IBAN",
                            "id": "UA424424424244242424424424444"
                        }
                    ]
                }
            ]
        }
    ],
    "attempts": 1,
    "description": "test",
    "name": AUCTION_NAME,
    "subtype": "FAST_MANUAL",
    "type": "COMMERCIAL_SELL_PRIORITY_ENGLISH",
    "userProfileId": 97,
    "startedAt": "2025-11-26T07:00:00.000Z",
    "lotNumber": "1",
    "accessDetails": None,
    "currency": "UAH",
    "initialAmount": 10000,
    "includePdv": True,
    "specificData": {
        "documentRequirements": None,
        "additionalInformation": None,
        "valueAddedTaxCharged": False,
        "guaranteeAmount": 2000,
        "registrationAmount": 15,
        "lots": [
            {
                "address": {
                    "city": "Київ",
                    "country": "Україна",
                    "region": "Київ",
                    "addressID": "3200000000",
                    "zipCode": "02000",
                    "street": "rtertt"
                },
                "additionalClassifications": None,
                "cav": "18000000-9",
                "description": "test",
                "measureUnit": "H87",
                "quantity": 1,
                "id": None,
                "registrationDetails": {
                    "id": None,
                    "date": None,
                    "status": "notRegistered"
                },
                "props": None
            }
        ],
        "stepAmount": 100,
        "minNumberOfQualifiedBids": 1,
        "sellingEntity": {
            "address": {
                "country": "Україна",
                "region": "Київ",
                "city": "Хрещатик",
                "street": "Test",
                "zipCode": "11111",
                "addressID": None,
                "type": "MAIN"
            },
            "contactPerson": {
                "name": "testttt",
                "email": "test@gmail.com",
                "phone": "09988899899",
                "url": None,
                "faxNumber": None,
                "id": 110
            },
            "name": "ТОВ \"Буб\"",
            "identifier": "32323232",
            "identifierScheme": "UA-EDR"
        },
        "tenants": [
            {
                "address": {
                    "country": "Україна",
                    "region": "Закарпатська область",
                    "street": "test",
                    "city": "test",
                    "zipCode": "12121"
                },
                "name": "api_1",
                "identifier": "32323232",
                "identifierScheme": "UA-EDR",
                "representativeInfo": "",
                "contractFrom": None,
                "contractTill": None
            }
        ]
    },
    "documents": []
}

