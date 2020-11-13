from typing import Dict
import json
import logging

import matplotlib.pyplot as plt

LOG = logging.getLogger(__name__)


class BCI(object):
    def __init__(self,
                 index_size: int,
                 rebalancing_period: int,
                 primary_usd_filtering: float,
                 secondary_usd_filtering: float,
                 max_asset_allocation: float,
                 fee: float,
                 running_avg_volume_period: int,
                 index_candidate_size: int,
                 primary_candidate_size: int,
                 secondary_candidate_size: int,
                 initial_funds: float,
                 input_file_name: str,
                 start_dt: str = None,
                 end_dt: str = None,
                 graph: bool = False):
        self.index_size = index_size
        self.rebalancing_period = rebalancing_period
        self.primary_usd_filtering = primary_usd_filtering
        self.secondary_usd_filtering = secondary_usd_filtering
        self.max_asset_allocation = max_asset_allocation
        self.fee = fee
        self.running_avg_volume_period = running_avg_volume_period
        self.index_candidate_size = index_candidate_size
        self.primary_candidate_size = primary_candidate_size
        self.secondary_candidate_size = secondary_candidate_size
        self.initial_funds = initial_funds
        self.graph = graph

        self.portfolio: Dict = {}
        self.orig_portfolio: Dict = {}
        self.overall_fee: float = 0

        with open(input_file_name, 'r') as file:
            self.data = json.loads(file.read())

        self.dates = sorted(self.data.keys())

        self.data_by_coin = {}
        self.calc_data_by_coin()

        self.calc_running_avg_volume()

        self.prune_dates(start_dt, end_dt)

        LOG.debug(f"\nConfiguration:\n"
                  f"\tindex size: {index_size}\n"
                  f"\trebalancing period: {rebalancing_period}\n"
                  f"\tprimary USD filtering: {primary_usd_filtering}\n"
                  f"\tsecondary USD filtering: {secondary_usd_filtering}\n"
                  f"\tmaximal asset allocation: {max_asset_allocation}\n"
                  f"\tfee: {fee}\n"
                  f"\trunning average volume period: {running_avg_volume_period}\n"
                  f"\tindex candidate size: {index_candidate_size}\n"
                  f"\tprimary candidate size: {primary_candidate_size}\n"
                  f"\tsecondary candidate size: {secondary_candidate_size}\n"
                  f"\tinitial funds: {initial_funds}\n"
                  f"\tstart date: {start_dt}\n"
                  f"\tend date: {end_dt}\n"
                  f"\tinput filename: {input_file_name}")

    # remove dates outside the selected window
    def prune_dates(self, start_dt: str = None, end_dt: str = None):
        for date in list(self.data.keys()):
            if (start_dt is not None and date < start_dt) or (end_dt is not None and date > end_dt):
                self.data.pop(date)

        self.data_by_coin = {coin: list(filter(lambda x: (start_dt is None or x[0] >= start_dt) and (end_dt is None or x[0] <= end_dt), data))
                             for coin, data in self.data_by_coin.items()}

        self.dates = list(filter(lambda x: (start_dt is None or x >= start_dt) and (end_dt is None or x <= end_dt), self.dates))

    # transform input from {'date': {'coin1': {data1}, 'coin2': {...}}, ...} to {'coin1': [[date,data1],...], ...}
    def calc_data_by_coin(self):
        coins = set()
        for _, v in self.data.items():
            coins.update(v.keys())

        for coin in coins:
            self.data_by_coin[coin] = []
            for date in self.dates:
                if coin in self.data[date]:
                    self.data_by_coin[coin].append([date, self.data[date][coin]])
                else:
                    self.data_by_coin[coin].append([date, {}])

    # enrich input with average volume over past X days
    def calc_running_avg_volume(self):
        for coin, data in self.data_by_coin.items():
            volumes = [x[1]['volume'] if 'volume' in x[1] else 0 for x in data]
            [sum(volumes[i - (self.running_avg_volume_period - 1):i + 1]) if i > (self.running_avg_volume_period - 1) else sum(volumes[:i + 1]) for i in range(len(volumes))]

            for d, v in zip(data, volumes):
                d[1]['volume_avg'] = v / self.running_avg_volume_period

                if coin not in self.data[d[0]]:
                    self.data[d[0]][coin] = {'cap': 0, 'price': 0, 'volume': 0}
                self.data[d[0]][coin]['volume_avg'] = v / self.running_avg_volume_period

    def run(self):
        LOG.info(f"\nSimulation period: {self.dates[0]} - {self.dates[-1]}")

        self.init_portfolio(self.initial_funds)

        value_baseline = []
        value_index = []
        graph_x_dates = []
        for (i, date) in zip(range(len(self.dates)), self.dates):
            # if rebalancing period is other than 0, then rebalance every (rebalancing period) days. Otherwise rebalance
            # on the first day of month. Do not rebalance on the very first day since the result would be equal to the initialized portfolio
            [year, month, day] = date.split('-')
            if i != 0 and ((self.rebalancing_period > 0 and i % self.rebalancing_period == 0) or (self.rebalancing_period == 0 and day == '01')):
                LOG.info(f"\nRebalancing {date}")
                if day == '01' and int(month) % 3 == 0:
                    graph_x_dates.append(date)

                candidate_coins = []

                # filter out existing portfolio coins with average daily volume less than self.primary_usd_filtering over the current month
                LOG.debug(f"\tPrimary filtering:")
                for coin in [key for key, _ in self.portfolio.items()]:
                    LOG.debug(f"\t\t{coin}: value $: {self.data[date][coin]['volume_avg'] * self.data[date][coin]['price']:,} (average volume: {self.data[date][coin]['volume_avg']}, price: {self.data[date][coin]['price']})")
                    if self.data[date][coin]['volume_avg'] * self.data[date][coin]['price'] > self.primary_usd_filtering:
                        candidate_coins.append(coin)

                LOG.debug(f"\t\tPreserved coins: {candidate_coins}")

                # filter out all other coins with average daily volume less than self.secondary_usd_filtering over the current month
                LOG.debug(f"\tSecondary filtering:")
                ranking = sorted(self.data[date].items(), key = lambda x: x[1]['cap'], reverse = True)
                for rank in ranking[:self.index_candidate_size]:
                    if rank[0] not in candidate_coins:
                        LOG.debug(f"\t\t{rank[0]}: value $: {rank[1]['volume_avg'] * rank[1]['price']:,} (average volume: {rank[1]['volume_avg']}, price: {rank[1]['price']})")
                        if rank[1]['volume_avg'] * rank[1]['price'] > self.secondary_usd_filtering:
                            candidate_coins.append(rank[0])

                    if len(candidate_coins) >= self.index_candidate_size:
                        break

                LOG.debug(f"\tCandidate list: {candidate_coins}")

                # if filtering leads to having not enough coins, then add even the ones not meeting volume criteria
                if len(candidate_coins) < self.index_candidate_size:
                    candidate_coins += [rank[0] for rank in ranking[:self.index_candidate_size]]
                    candidate_coins = list(set(candidate_coins))
                    LOG.info(f"\tNot enough candidates, adding additional ones despite not meeting volume criteria: {candidate_coins}")

                # order all new candidates by their capitalization
                candidate_coins = sorted(candidate_coins, key = lambda x: self.data[date][x]['cap'], reverse = True)
                LOG.debug(f"\tSorted candidate list:")
                LOG.debug("\n".join(map(lambda x: f"\t\t{x}:\t{self.data[date][x]['cap']:,}", candidate_coins)))

                # add best X coins directly to the new portfolio
                final_coins = candidate_coins[:self.primary_candidate_size]

                # add next coins to the portfolio where coins in the current portfolio are prioritized even if having
                # worse capitalization
                for coin in candidate_coins[self.primary_candidate_size:self.secondary_candidate_size]:
                    if coin in self.portfolio.keys() and len(final_coins) < self.index_size:
                        final_coins.append(coin)

                # add remaning coins to reach the index size
                for coin in candidate_coins[:self.index_candidate_size]:
                    if coin not in final_coins and len(final_coins) < self.index_size:
                        final_coins.append(coin)
                LOG.info(f"\tIndex composition: {final_coins}")

                # calculate normalized percentage composition according to the capitalization
                ranking = []
                for coin in final_coins:
                    ranking.append((coin, self.data[date][coin]))
                perc_allocation = self.calc_portfolio_percentage(ranking, self.max_asset_allocation)

                LOG.debug(f"\tCapped percentage allocation:")
                LOG.debug("\n".join(map(lambda x: f"\t\t{x}", perc_allocation)))

                # calculate USD value of the current portfolio and then distribute it into the new portfolio
                # based on the calculated percentage
                portfolio_sum = sum([qty * self.data[date][coin]['price'] for coin, qty in self.portfolio.items()])
                new_portfolio = {coin[0]: portfolio_sum * coin[1] / self.data[date][coin[0]]['price'] for coin in perc_allocation}

                LOG.info(f"\tNew portfolio allocation: {new_portfolio}")
                new_portfolio_usd = {coin: qty * self.data[date][coin]['price'] for coin, qty in new_portfolio.items()}
                LOG.info(f"\tNew portfolio USD allocation: {new_portfolio_usd}")
                LOG.info(f"\tPortfolio value: {portfolio_sum:,}")

                # for each coin in the old and new portfolio calculate the amount to be bought/sold
                diff = {}
                for coin, qty in new_portfolio.items():
                    if coin in self.portfolio:
                        diff[coin] = qty - self.portfolio[coin]
                    else:
                        diff[coin] = qty - 0
                for coin, qty in self.portfolio.items():
                    if coin not in new_portfolio:
                        diff[coin] = 0 - self.portfolio[coin]

                LOG.info(f"\tPortfolio updates: {diff}")

                diff_usd = {coin: self.data[date][coin]['price'] * qty for coin, qty in diff.items()}
                LOG.info(f"\tPortfolio USD updates: {diff_usd}")

                # calculate fee for the bought/sold coins
                diff_usd = {coin: abs(qty * self.data[date][coin]['price']) * self.fee for coin, qty in diff.items()}
                fee = sum([usd for _, usd in diff_usd.items()])
                self.overall_fee += fee
                LOG.info(f"\tFee: {fee} USD")

                self.portfolio = new_portfolio

                # display value of the original portfolio with current prices
                orig_portfolio_value = sum([qty * self.data[date][coin]['price'] for coin, qty in self.orig_portfolio.items()])
                LOG.info(f"\tBaseline portfolio value: {orig_portfolio_value:,}")

            value_baseline.append(sum([qty * self.data[date][coin]['price'] for coin, qty in self.orig_portfolio.items()]))
            value_index.append(sum([qty * self.data[date][coin]['price'] for coin, qty in self.portfolio.items()]))

        LOG.info(f"\nBaseline portfolio value: {value_baseline[-1]:,}")
        LOG.info(f"Index portfolio value: {value_index[-1]:,}")
        LOG.info(f"Fees: {self.overall_fee:,}")

        if self.graph is True:
            self.plot_graph(value_baseline, value_index, graph_x_dates)

    def init_portfolio(self, funds: float):
        LOG.debug(f"\nInitializing portfolio for ${funds}...")

        # sort all currencies by their market capitalization and pick first N ones based on the index size
        ranking = sorted(self.data[self.dates[0]].items(), key = lambda x: x[1]['cap'], reverse = True)
        ranking = ranking[:self.index_size]

        LOG.debug(f"\tTop {self.index_size} assets:")
        LOG.debug("\n".join(map(lambda x: f"\t\t{x}", ranking)))

        # calculate percentage distribution according to the capitalization
        perc_cap = self.calc_portfolio_percentage(ranking, self.max_asset_allocation)

        LOG.debug(f"\tCapped percentage allocation:")
        LOG.debug("\n".join(map(lambda x: f"\t\t{x}", perc_cap)))

        # split funds among top coins according to the percentage distribution
        self.portfolio = {coin[0]: funds * coin[1] / self.data[self.dates[0]][coin[0]]['price'] for coin in perc_cap}
        LOG.info(f"Portfolio allocation: {self.portfolio}")

        new_portfolio_usd = {coin: qty * self.data[self.dates[0]][coin]['price'] for coin, qty in self.portfolio.items()}
        LOG.info(f"Portfolio USD allocation: {new_portfolio_usd}")

        # store initial portfolio for sake of performance comparison later on
        self.orig_portfolio = dict(self.portfolio)

    def calc_portfolio_percentage(self, ranking, max_allocation):
        # normalize percentage allocation according to the capitalization
        sum_cap = sum(coin[1]['cap'] for coin in ranking)
        perc_cap = [[coin[0], coin[1]['cap'] / sum_cap] for coin in ranking]

        LOG.debug(f"\tPercentage allocation according to capitalization:")
        LOG.debug("\n".join(map(lambda x: f"\t\t{x}", perc_cap)))

        # cap percentage allocation at the selected maximum level
        for i in range(len(perc_cap)):
            if perc_cap[i][1] > max_allocation:
                surplus = perc_cap[i][1] - max_allocation
                perc_cap[i][1] = max_allocation

                s = sum(coin[1] for coin in perc_cap[i + 1:])
                perc_cap[i + 1:] = map(lambda x: [x[0], x[1] + surplus / (s / x[1])], perc_cap[i + 1:])
            else:
                break

        return perc_cap

    def plot_graph(self, value_baseline, value_index, graph_x_dates):
        plt.plot(self.dates, value_baseline, label = 'baseline', linewidth = 0.7)
        plt.plot(self.dates, value_index, label = f'BCI{self.index_size}', linewidth = 0.7)

        plt.xlabel('Date')
        plt.xticks(graph_x_dates, rotation = 45, fontsize = 6)

        plt.ylabel('Value (USD)')

        plt.title(f'BCI{self.index_size} {self.dates[0]} - {self.dates[-1]}')

        plt.grid(linestyle = '--', linewidth = 0.5)

        plt.legend()
        plt.savefig(f"index{self.index_size}_{self.dates[0]}_{self.dates[-1]}.svg", format = "svg")
        plt.show()