import logging
import sys
import json

import matplotlib.pyplot as plt

from BCI import BCI

logger = logging.getLogger('matplotlib')
logger.setLevel(logging.WARN)
logger.addHandler(logging.StreamHandler(sys.stdout))

logger = logging.getLogger('BCI')
logger.setLevel(logging.WARN)
logger.addHandler(logging.StreamHandler(sys.stdout))

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

LOG = logging.getLogger(__name__)

GRAPH = True
EXPORT_CSV_RESULTS = False
EXPORT_FULL_RESULTS = False


if __name__ == "__main__":
    LOG.info("BCI Comparison")

    """
    index size
    rebalancing
    primary volume filter
    secondary volume filter
    max. allocation
    running volume average
    candidate list size
    primary candidate size
    secondary candidate size
    offset
    label
    """
    parameters = [
        #(5, 0, 600000, 1000000, 0.35, 30, 10, 3, 7, 0, "BCI5"),
        #(5, 0, 0, 0, 0.35, 30, 10, 0, 0, 0, "TOP5"),
        #(5, 10000, 0, 0, 0.35, 30, 10, 0, 0, 0, "HODL5"),
        (10, 0, 600000, 1000000, 0.3, 30, 20, 7, 13, 0, "BCI10"),
        (10, 0, 0, 0, 0.3, 30, 20, 0, 0, 0, "TOP10"),
        (10, 10000, 0, 0, 0.3, 30, 20, 0, 0, 0, "HODL10"),
    ]
    start_dt = "2020-01-01"
    end_dt = "2020-11-01"

    with open("input_data.json", 'r') as file:
        input_data = json.loads(file.read())

    data = None
    dates = None
    data_by_coin = None

    results = []
    for (index,
         rebalancing,
         primary_volume_filter,
         secondary_volume_filter,
         max_allocation,
         running_avg_volume_period,
         candidates,
         primary_candidate,
         secondary_candidate,
         offset,
         label) in parameters:
        LOG.debug(f"Index: {index}, "
                 f"rebalancing: {rebalancing}, "
                 f"primary_volume_filter: {primary_volume_filter}, "
                 f"secondary_volume_filter: {secondary_volume_filter}, "
                 f"max_allocation: {max_allocation}, "
                 f"running_avg_volume_period: {running_avg_volume_period}, "
                 f"candidates: {candidates}"
                 f"primary_candidate: {primary_candidate}, "
                 f"secondary_candidate: {secondary_candidate}, "
                 f"offset: {offset}")

        try:
            bci = BCI(
                index_size = index,
                rebalancing_period = rebalancing,
                primary_usd_filtering = primary_volume_filter,
                secondary_usd_filtering = secondary_volume_filter,
                max_asset_allocation = max_allocation,
                fee = 0.02,
                running_avg_volume_period = running_avg_volume_period,
                index_candidate_size = candidates,
                primary_candidate_size = primary_candidate,
                secondary_candidate_size = secondary_candidate,
                initial_funds = 1000,
                offset = offset,
                start_dt = start_dt,
                end_dt = end_dt
            )

            # use previously calculated data to save initialization time
            if data_by_coin is None:
                bci.set_input_data(input_data)
            else:
                bci.data = data
                bci.dates = dates
                bci.data_by_coin = data_by_coin

            [dates, baseline_values, index_values, fees] = bci.run()
            results.append([dates, index_values, fees, baseline_values, label])

            if data_by_coin is None:
                data = bci.data
                dates = bci.dates
                data_by_coin = bci.data_by_coin
        except Exception as e:
            LOG.debug(e)

    LOG.info(f"Best performing index configurations:")
    for data in sorted(results, key = lambda x: x[1][-1], reverse = True):
        LOG.info(f"{data[4]}:{data[1][-1]:.2f}:{data[3][-1]:.2f}:{data[2]:.2f}")

    LOG.info(f"Best performing baseline configurations:")
    for data in sorted(results, key = lambda x: x[3][-1], reverse = True):
        LOG.info(f"{data[4]}:{data[1][-1]:.2f}:{data[3][-1]:.2f}:{data[2]:.2f}")

    if EXPORT_FULL_RESULTS is True:
        with open(f"results_{start_dt}_{end_dt}.json", 'w') as file:
            file.write(json.dumps(results))

    if EXPORT_CSV_RESULTS is True:
        with open(f"results_{start_dt}_{end_dt}.csv", 'w') as file:
            for data in results:
                file.write(f"{';'.join(map(str, data[4]))};{data[1][-1]};{data[3][-1]};{data[2]}\n")

    if GRAPH is True:
        dates = None
        for data in results[-10:]:
            dates = data[0]
            plt.plot(data[0], data[1], label = str(data[4]), linewidth = 0.8)

        plt.xlabel('Date')
        plt.xticks(list(filter(lambda x: x.split('-')[2] == '01' and int(x.split('-')[1]) % 3 == 0, dates)), rotation = 45, fontsize = 6)

        plt.ylabel('Value (USD)')

        plt.title(f'{start_dt} - {end_dt}')

        plt.grid(linestyle = '--', linewidth = 0.5)

        plt.legend(fancybox=True, shadow=True, ncol=5)

        plt.savefig(f"index_comparison_10_{start_dt}_{end_dt}.png", format = "png")
        #plt.show()