class AaveRepayMent:
    def repay_to_aave(self, price_open_close, borrow_pcg, buffer=0.01):
        staked_asset_percentage = 0.1
        price_repay_debt = price_open_close * (
            1 - (staked_asset_percentage * borrow_pcg * (1 + buffer))
        )
        return price_repay_debt

    def partial_repay_to_aave(
        self,
        price_open_close,
        lending_rate,
        collateral,
        asset_market_price,
        borrowing_rate,
        total_staked_asset,
    ):
        lending_fee = lending_rate * collateral * asset_market_price
        staked_asset_percentage = 0.1
        borrow_loan_percentage = 0.25
        current_debt_in_usd = (
            total_staked_asset * staked_asset_percentage * price_open_close
        )
        borrowing_fees = borrowing_rate * current_debt_in_usd
        if borrowing_fees > lending_fee:
            price_repay_partial_aave = price_open_close * (
                (borrowing_rate * borrow_loan_percentage)
                / (lending_rate * staked_asset_percentage)
            )
            position_size = (
                (lending_rate / borrowing_rate)
                * staked_asset_percentage
                * total_staked_asset
                * asset_market_price
            ) - current_debt_in_usd
            position_size = position_size / (asset_market_price - price_open_close)
            return {
                "repay_price": price_repay_partial_aave,
                "position_size": position_size,
            }


if __name__ == "__main__":
    a = AaveRepayMent()
    a = a.partial_repay_to_aave(
        price_open_close=996,
        lending_rate=0.0108,
        collateral=9,
        asset_market_price=770,
        borrowing_rate=0.0229,
        total_staked_asset=10,
    )
    # {'repay_price': 586.0468106995884, 'position_size': -14.989935030354667}
    # a  = a.repay_to_aave(price_open_close=996.4709841514826,borrow_pcg=0.25)
    print(a)
