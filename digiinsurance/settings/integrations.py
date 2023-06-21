from ._helper import getenv
import os

""" GOOGLE_APPLICATION_CREDENTIALS = 'C:/Users/cuyug/Desktop/DigiInsurance-backend/kyc/google_api.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_APPLICATION_CREDENTIALS """

# GOOGLE CLOUD VISION
#GOOGLE_APPLICATION_CREDENTIALS = '/Users/lorenzovalentino/Projects/digiinsurance/digiinsurance/kyc/google_api.json'
# GOOGLE_APPLICATION_CREDENTIALS = 'D:/UC/4th_year/Practicum/System/QuestronixBackend/DigiInsurance-backend/kyc/google_api.json'
GOOGLE_APPLICATION_CREDENTIALS = getenv(
     'GOOGLE_APPLICATION_CREDENTIALS', 'C:/Users/cuyug/Desktop/DigiInsurance-backend/kyc/google_api.json')

# Magpie keys
MAGPIE_SECRET_KEY = getenv(
    'MAGPIE_SECRET_KEY', 'sk_test_ZIZCo7F2DKcSpsTfQgItIQ')
MAGPIE_PUBLIC_KEY = getenv(
    'MAGPIE_PUBLIC_KEY', 'pk_test_Q3HQ3QWOc8GcEYFnWqsnmQ')

# DragonPay
# set to True when in test env
DRAGONPAY_TEST_MODE = getenv('DRAGONPAY_TEST_MODE', True)
DRAGONPAY_ID = getenv('DRAGONPAY_ID', 'EASTWEST')
DRAGONPAY_PASSWORD = getenv('DRAGONPAY_PASSWORD', '7E5L4nyA3R4fLsq')
DRAGONPAY_API_KEY = getenv(
    'DRAGONPAY_API_KEY', '1af1a48aa21d4acb23177c7ba317826eb1c6fa2d')

DRAGONPAY_ENCRYPT_PARAMS = True    # Enable encryption of request parameters
DRAGONPAY_TXN_LENGTH = 20          # Length of transaction Ids
DRAGONPAY_SAVE_DATA = True
