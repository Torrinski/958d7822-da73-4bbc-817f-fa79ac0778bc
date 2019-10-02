import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"Creating a Cashflow class, with attributes and methods:"
class Cashflow(object):

    def __init__(self, amount, t):
        self.amount = amount
        self.t = t

    def present_value (self, interest_rate):
        return self.amount / (1+interest_rate)**self.t

"Implementing the plot method on the invenstment porject class and plotting on main class"
class InvestmentProject(object):
    RISK_FREE_RATE = 0.08

    def __init__(self, cashflows, hurdle_rate=RISK_FREE_RATE):
        cashflows_positions = {str(flow.t): flow for flow in cashflows}
        self.cashflow_max_position = max((flow.t for flow in cashflows))
        self.cashflows = []
        for t in range(self.cashflow_max_position + 1):
            self.cashflows.append(cashflows_positions.get(str(t), Cashflow(t=t, amount=0)))
        self.hurdle_rate = hurdle_rate if hurdle_rate else InvestmentProject.RISK_FREE_RATE

    @staticmethod
    def from_csv(filepath, hurdle_rate=RISK_FREE_RATE):
        cashflows = [Cashflow(**row) for row in pd.read_csv(filepath).T.to_dict().values()]
        return InvestmentProject(cashflows=cashflows, hurdle_rate=hurdle_rate)

    @property
    def internal_return_rate(self):
        return np.irr([flow.amount for flow in self.cashflows])

    def plot(self, show=False,**kwargs):

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)


        self.figure=self.ax.plot([flow.t for flow in self.cashflows],[flow.amount for flow in self.cashflows])
        if show:
            plt.show()
        if kwargs.get('name'):
            plt.title('cashflows')
            plt.ylabel('amount')
            plt.xlabel('t')
            self.fig.savefig(kwargs.get('name'))

"Implementing Net present value method"
    def net_present_value(self, interest_rate=None):
        return sum([flow.present_value(interest_rate=interest_rate) for flow in self.cashflows]) if not interest_rate==None else sum([flow.present_value(interest_rate=self.hurdle_rate) for flow in self.cashflows])


"Defining the equivalent annuity"
    def equivalent_annuity(self, interest_rate=None):
        """ Equivalent Annuity
        Transform a set of cashflows into a constant payment.
        :param interest_rate: represents the interest-rate used with the annuity calculations.
        :return: a number (currency) representing the equivalent annuity.
        """
        return self.net_present_value(interest_rate=interest_rate)
        # TODO: implement equivalent_annuity methdo
        #raise NotImplementedError

    def describe(self):
        return {
            "irr": self.internal_return_rate,
            "hurdle-rate": self.hurdle_rate,
            "net-present-value": self.net_present_value(interest_rate=None),
            "equivalent-annuity": self.equivalent_annuity(interest_rate=None)
        }
cashflows=[Cashflow(100,1),Cashflow(100,2),Cashflow(100,3)]
investmentP=InvestmentProject(cashflows)
#investmentP.plot(name='test.png')
print(investmentP.net_present_value())
#plt.show()
