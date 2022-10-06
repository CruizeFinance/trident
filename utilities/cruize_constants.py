# MAINNET CONSTANTS
import pytz

MAINNET_INFURA_URL = "https://mainnet.infura.io/v3/4e55b6d7c94d4c58a931971dc807d055"
STARK_CONTRACT_ADDRESS = "0x014F738EAd8Ec6C50BCD456a971F8B84Cd693BBe"
CRUIZE_CONTRACT_ADDRESS = ""
WALLET_ADDRESS = "0xE0E24a32A7e50Ea1c7881c54bfC1934e9b50B520"
USDC_ADDRESS = ""
LINK_ADDRESS = "0x01BE23585060835E02B77ef475b0Cc51aA1e0709"


# PRICE PARAMS
MAX_WAIT_SECONDS = 60
BLOCK_SAMPLE_SIZE = 20
PROBABILITY = 100
# NETWORKS
MAINNET_CHAIN_ID = 1
GOERLI_CHAIN_ID = 5


# CRYPTO NOTATION

"""This represents 10^8. Crypto currency values
 always have certain decimal notations appended to them 
and this variable is used to remove those decimals
 to get the real world value(price)"""

DECIMAL_NOTATION = 1e8
# CRUIZE CONTRACTS

# DYDX POSITION CONSTANT
BTC = "BTC"
ETH = "ETH"
POSITION_CLOSED = "CLOSED"
POSITION_OPEN = "OPEN"
TIME_IN_FORCE_IOC = "IOC"
SIGNATURE = "0x"
PRICE_ROUNDED_VALUE = 3

# TESTNET_ADDRESS
# TEST_LINK_ADDRESS = "0xD4a33860578De61DBAbDc8BFdb98FD742fA7028e"
TEST_OWNER_ADDRESS = "0xDf0137207dA77459e54C03658F43Ef159d06341a"
TEST_CRUIZE_CONTRACT_ADDRESS = "0xD363F02cBa41eDA05e335ADb6A66E9fe66604b36"
POSITION_LEVERAGE = 5
TEST_BTC_USD_ORACLE_ADDRESS = "0xA39434A63A52E749F02807ae27335515BA4b07F7"
TEST_ETH_USD_ORACLE_ADDRESS = "0xD4a33860578De61DBAbDc8BFdb98FD742fA7028e"

# COINGECKO CONSTANT
TIMEZONE = pytz.timezone("Asia/Kolkata")
COINGECKO_HOST = "https://api.coingecko.com/api/v3"
SECONDS_PER_HOUR = 3600
# CELERY CONFIG CONSTANT
# need to run on server before testnet

BROKER_URL = "redis://127.0.0.1:6379/0"
RESULT_BACKEND = "redis://127.0.0.1:6379/1"

# FIREBASE CONSTANT
CRUIZE_USER = "cruize_users"