import tradePair
import time
import consts
import requests
from currency_converter import CurrencyConverter

# bids = za ile sprzedajemy, asks = za ile kupujemy
def printBidsAsks(tradePair1, tradePair2):
    print(f"BIDS {tradePair1.getName()} / BIDS {tradePair2.getName()}: ", tradePair1.getBestBidPrice()/tradePair2.getBestBidPrice() * 100, "%", sep='') # kupno (w sensie gielda za ile kupuje)
    print(f"ASKS {tradePair1.getName()} / ASKS {tradePair2.getName()}: ", tradePair1.getBestAskPrice()/tradePair2.getBestAskPrice() * 100, "%", sep='') # sprzedaz
    print(f"BIDS {tradePair1.getName()} / ASKS {tradePair2.getName()}: ", tradePair1.getBestBidPrice()/tradePair2.getBestAskPrice() * 100, "%", sep='')
    print(f"BIDS {tradePair2.getName()} / ASKS {tradePair1.getName()}: ", tradePair2.getBestBidPrice()/tradePair1.getBestAskPrice() * 100, "%", sep='')

def calcBidPrice(tradePairBid, volume, number):
    bidPrice = volume * tradePairBid.getBestBidPrice(number)
    bidPrice -= bidPrice * tradePairBid.getTaker()
    return bidPrice

def calcAskPrice(tradePairAsk, volume, number):
    askPrice = volume * tradePairAsk.getBestAskPrice(number)
    askPrice += askPrice * tradePairAsk.getTaker() + askPrice * tradePairAsk.getTransferFee()
    return askPrice

def getArbitage(tradePairBid, tradePairAsk):
    bidNum = 0
    askNum = 0
    earn = 0
    volumeBid = tradePairBid.getBestBidVolume()
    volumeAsk = tradePairAsk.getBestAskVolume()
    volume = min(volumeAsk, volumeBid)
    loss = calcBidPrice(tradePairBid, volume, bidNum) - calcAskPrice(tradePairAsk, volume, askNum)

    while calcBidPrice(tradePairBid, volume, bidNum) > calcAskPrice(tradePairAsk, volume, askNum):
        earn += calcBidPrice(tradePairBid, volume, bidNum) - calcAskPrice(tradePairAsk, volume, askNum)
        volumeBid -= volume
        volumeAsk -= volume 
        if volumeBid == 0:
            bidNum += 1
            volumeBid = tradePairBid.getBestBidVolume(bidNum)
        if volumeAsk == 0:
            askNum += 1
            volumeAsk = tradePairAsk.getBestAskVolume(bidNum)
        volume = min(volumeAsk, volumeBid)

    if earn > 0:
        return earn
    return loss

def printArbitage(tradePairBid, tradePairAsk):
    arbitage = getArbitage(tradePairBid, tradePairAsk)
    
    print(f"gielda sprzedajaca: {tradePairAsk.getName()}, gielda kupujaca: {tradePairBid.getName()} zysk: ", round(arbitage, 5), tradePairBid.getCurrencies()[1])


def getCommonTradesList(bittrexAllTradesUrl, bitbayBaseUrl):
    try:
        allTradesJson = requests.get(bittrexAllTradesUrl).json()
    except requests.exceptions.ConnectionError:
        if consts.DEBUG == True:
            print("Blad w uzyskaniu wspolnych walut")

    commonList = []

    for pair in allTradesJson:
        base = pair[consts.BITTREX_ALL_TRADES_BASE_NAME]
        quote = pair[consts.BITTREX_ALL_TRADES_QUOTE_NAME]
        try:
            json = requests.get(bitbayBaseUrl.format(base, quote)).json()
            if json[consts.BITBAY_BIDS_NAME] != None:
                commonList.append((base, quote))
                # print((base, quote))
        except:
            # print((base, quote), " - brak!")
            pass
    # print(commonList)
    return commonList

def getUSDApprox(currency):
    if currency == consts.USDT_SYMBOL:
        return 1
        
    approx = 0
    try:
        converter = CurrencyConverter()
        approx = converter.convert(1, currency, consts.CURRENCY1)
    except:
        tp = tradePair.TradePair(consts.M_NAME[0], (currency, consts.CURRENCY1), consts.M_URL[0].format(currency, consts.CURRENCY1), consts.M_TAKER[0], consts.M_TRANSFER_FEE[0], consts.M_BIDS_NAME[0], consts.M_ASKS_NAME[0], consts.M_DATA_PATH[0], consts.M_PRICE_NAME[0], consts.M_VOLUME_NAME[0])
        tp.updateOrderBook()
        approx = tp.getBestBidPrice()
    return approx

def createMarkets(pairs):
    markets = [[], []]
    for pair in pairs:
        markets[0].append(tradePair.TradePair(consts.M_NAME[0], pair, consts.M_URL[0].format(pair[0], pair[1]), consts.M_TAKER[0], consts.M_TRANSFER_FEE[0], consts.M_BIDS_NAME[0], consts.M_ASKS_NAME[0], consts.M_DATA_PATH[0], consts.M_PRICE_NAME[0], consts.M_VOLUME_NAME[0]))
        markets[1].append(tradePair.TradePair(consts.M_NAME[1], pair, consts.M_URL[1].format(pair[1], pair[0]), consts.M_TAKER[1], consts.M_TRANSFER_FEE[1], consts.M_BIDS_NAME[1], consts.M_ASKS_NAME[1], consts.M_DATA_PATH[1], consts.M_PRICE_NAME[1], consts.M_VOLUME_NAME[1]))

    return markets

def L42(pairs):
    markets = createMarkets(pairs)

    while True:
        for i in range(len(pairs)):
            markets[0][i].updateOrderBook()
            markets[1][i].updateOrderBook()
        
            if markets[0][i].isOrderBookFine() == False or markets[1][i].isOrderBookFine() == False:
                if consts.DEBUG == True:
                    print("BLAD, czekam")
                continue

            # printBidsAsks(market1[i], market2[i])
            print(markets[0][i].getCurrencies())
            printArbitage(markets[0][i], markets[1][i])
            printArbitage(markets[1][i], markets[0][i])

            print()

        time.sleep(consts.SLEEP_TIME)

def L43(pairs):
    markets = createMarkets(pairs)
    ranking = []
    for i in range(len(pairs)):
            markets[0][i].updateOrderBook()
            markets[1][i].updateOrderBook()
        
            if markets[0][i].isOrderBookFine() == False or markets[1][i].isOrderBookFine() == False:
                if consts.DEBUG == True:
                    print("BLAD, ignoruje pare")
                continue
            
            # print(getUSDApprox(markets[0][i].getCurrencies()[0]), getArbitage(markets[0][i], markets[1][i]))
            ranking.append((markets[0][0].getName(), markets[1][0].getName(), markets[0][i].getCurrencies(), getUSDApprox(markets[0][i].getCurrencies()[1]) * getArbitage(markets[0][i], markets[1][i])))
            ranking.append((markets[1][0].getName(), markets[0][0].getName(), markets[0][i].getCurrencies(), getUSDApprox(markets[0][i].getCurrencies()[1]) * getArbitage(markets[1][i], markets[0][i])))

    ranking.sort(reverse = True, key = lambda a : a[3])
    for pair in ranking:
        print(pair) 

if __name__ == '__main__':
    # print(getCommonTradesList(consts.BITTREX_ALL_TRADES_URL, consts.BITBAY_BASE_URL))
    # L42(consts.COMMON_PAIRS)
    L43(consts.COMMON_PAIRS)