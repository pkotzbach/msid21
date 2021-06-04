CURRENCY1 = "USD"
CURRENCY2 = "BTC"
DEBUG = True
SLEEP_TIME = 5
USDT_SYMBOL = "USDT"

BITTREX_ALL_TRADES_URL = "https://api.bittrex.com/v3/markets"
BITTREX_ALL_TRADES_BASE_NAME = "baseCurrencySymbol"
BITTREX_ALL_TRADES_QUOTE_NAME = "quoteCurrencySymbol"

BITBAY_BIDS_NAME = "bids"
BITBAY_BASE_URL = "https://bitbay.net/API/Public/{}{}/orderbook.json"

M_NAME = ["bitbay", "bittrex"]
M_URL = ["https://bitbay.net/API/Public/{}{}/orderbook.json", "https://api.bittrex.com/api/v1.1/public/getorderbook?market={}-{}&type=both"]
M_TAKER = [0.0043, 0.0035]
M_TRANSFER_FEE = [0.005, 0.005]
M_BIDS_NAME = ["bids", "buy"]
M_ASKS_NAME = ["asks", "sell"]
M_DATA_PATH = [[], ["result"]]
M_PRICE_NAME = [0, "Rate"]
M_VOLUME_NAME = [1, "Quantity"]

COMMON_PAIRS = [('AAVE', 'BTC'), ('AAVE', 'EUR'), ('AAVE', 'USDT'), ('BAT', 'BTC'), ('BAT', 'USD'), ('BSV', 'BTC'), ('BSV', 'ETH'), ('BSV', 'EUR'), ('BSV', 'USD'), ('BSV', 'USDT'), ('BTC', 'EUR'), ('BTC', 'USD'), ('BTC', 'USDT'), ('COMP', 'BTC'), ('COMP', 'USDT'), ('DAI', 'BTC'), ('DAI', 'USDT'), ('DOT', 'BTC'), ('DOT', 'EUR'), ('DOT', 'USDT'), ('EOS', 'BTC'), ('EOS', 'USDT'), ('ETH', 'BTC'), ('ETH', 'EUR'), ('ETH', 'USD'), ('ETH', 'USDT'), ('GAME', 'BTC'), ('GRT', 'BTC'), ('GRT', 'EUR'), ('GRT', 'USDT'), ('LINK', 'BTC'), ('LINK', 'ETH'), ('LINK', 'USDT'), ('LSK', 'BTC'), ('LSK', 'USDT'), ('LTC', 'BTC'), ('LTC', 'ETH'), ('LTC', 'USD'), ('LTC', 'USDT'), ('LUNA', 'BTC'), ('LUNA', 'USDT'), ('MANA', 'BTC'), ('MKR', 'BTC'), ('OMG', 'BTC'), ('OMG', 'ETH'), ('OMG', 'USD'), ('PAY', 'BTC'), ('SRN', 'BTC'), ('TRX', 'BTC'), ('TRX', 'ETH'), ('TRX', 'EUR'), ('TRX', 'USD'), ('TRX', 'USDT'), ('UNI', 'BTC'), ('UNI', 'EUR'), ('UNI', 'USDT'), ('USDC', 'USD'), ('XLM', 'BTC'), ('XLM', 'ETH'), ('XLM', 'EUR'), ('XLM', 'USD'), ('XLM', 'USDT'), ('XRP', 'BTC'), ('XRP', 'ETH'), ('XRP', 'EUR'), ('XRP', 'USD'), ('XRP', 'USDT'), ('XTZ', 'BTC'), ('XTZ', 'USDT'), ('ZRX', 'BTC'), ('ZRX', 'USD')]
# COMMON_CURRENCY_WE_PAY = {pair[1] for pair in COMMON_PAIRS}