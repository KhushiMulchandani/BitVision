from decimal import Decimal, ROUND_DOWN

from django.db import transaction

from .models import OHLCV, Portfolio, Trade

CENT = Decimal("0.01")
SATOSHI = Decimal("0.00000001")


class TradeError(Exception):
    def __init__(self, message, details=None, status=400):
        super().__init__(message)
        self.message, self.details, self.status = message, details, status


def execute_trade(user, side, amount_usd):
    """Paper-trade BTC at the latest daily close. Returns (portfolio, trade)."""
    latest = OHLCV.objects.order_by("-date").first()
    if latest is None or latest.close <= 0:
        raise TradeError("Market data currently unavailable.", status=503)
    price = latest.close

    usd = Decimal(amount_usd).quantize(CENT, rounding=ROUND_DOWN)
    btc = (usd / price).quantize(SATOSHI, rounding=ROUND_DOWN)
    if usd <= 0 or btc <= 0:
        raise TradeError("Amount is too small to trade.")

    Portfolio.objects.get_or_create(user=user)
    with transaction.atomic():
        portfolio = Portfolio.objects.select_for_update().get(user=user)
        if side == "buy":
            if portfolio.cash_balance < usd:
                raise TradeError("Insufficient funds.", {"cash_balance": str(portfolio.cash_balance),
                                                         "requested_usd": str(usd)})
            portfolio.cash_balance -= usd
            portfolio.btc_holdings += btc
        else:
            if portfolio.btc_holdings < btc:
                raise TradeError("Insufficient BTC holdings.", {"btc_holdings": str(portfolio.btc_holdings),
                                                                "requested_btc": str(btc)})
            usd = (btc * price).quantize(CENT, rounding=ROUND_DOWN)   # credit exactly what the BTC is worth
            portfolio.cash_balance += usd
            portfolio.btc_holdings -= btc
        portfolio.save()
        trade = Trade.objects.create(user=user, side=side, usd_amount=usd, btc_amount=btc, price=price)
    return portfolio, trade