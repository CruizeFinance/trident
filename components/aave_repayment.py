
class AaveRepayMent():

    def repay_to_aave(self,p_open_close,debt,size,pcg=0.01):
        # Prepay debt = Popen close + debt ∗pcg/size
        p_repay_debt = p_open_close + ((debt*pcg)/size)
        return p_repay_debt

    def partial_repay_to_aave(self,lending_rate,collateral,P,borrowing_rate,debt):

        lending_fee = lending_rate* collateral * P
        borrowing_fees = borrowing_rate*debt
        if borrowing_fees > lending_fee:
            PopencloserB = 0
            Prepay_partial_aave = PopencloserB*((borrowing_rate*0.25)/(lending_rate*0.9))