import logging
import sys
import json
import argparse

import matplotlib.pyplot as plt

from BCI import BCI

logger = logging.getLogger('matplotlib')
logger.setLevel(logging.WARN)
logger.addHandler(logging.StreamHandler(sys.stdout))

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

LOG = logging.getLogger(__name__)


def parse_args() -> dict:
    parser = argparse.ArgumentParser(description='Bitpanda Crypto Index Simulator')

    parser.add_argument('--index', help = 'Size of the index', default = 5, type = int)

    return vars(parser.parse_args())


if __name__ == "__main__":
    LOG.info("BCI Comparison")

    args = parse_args()

    indices = [args['index']]
    rebalancings = [0, 10, 60, 180]
    primary_volume_filters = [300000, 600000, 1000000, 1500000]
    secondary_volume_filters = [600000, 1000000, 1500000, 2000000]
    max_allocations = [0.2, 0.3, 0.35, 0.45, 0.5]
    running_avg_volume_periods = [20, 30, 45]
    primary_candidates = [3, 5, 8, 15]
    offsets = [0, 3, 6, 9, 12, 15, 20, 30]
    start_dt = "2017-07-01"
    end_dt = "2018-07-01"

    """
    indices = [4, 5]
    rebalancings = [0, 10]
    primary_volume_filters = [300000, 600000]
    secondary_volume_filters = [600000, 1000000]
    max_allocations = [0.3]
    running_avg_volume_periods = [10]
    primary_candidates = [3]
    offsets = [0]
    start_dt = "2017-07-01"
    end_dt = "2018-07-01"
    """

    with open("input_data.json", 'r') as file:
        input_data = json.loads(file.read())

    results = []
    for index in indices:
        for rebalancing in rebalancings:
            for primary_volume_filter in primary_volume_filters:
                for secondary_volume_filter in secondary_volume_filters:
                    if primary_volume_filter >= secondary_volume_filter:
                        continue

                    for max_allocation in max_allocations:
                        for running_avg_volume_period in running_avg_volume_periods:
                            for primary_candidate in primary_candidates:
                                if primary_candidate > index:
                                    continue

                                for offset in offsets:
                                    LOG.info(f"Index: {index}, "
                                             f"rebalancing: {rebalancing}, "
                                             f"primary_volume_filter: {primary_volume_filter}, "
                                             f"secondary_volume_filter: {secondary_volume_filter}, "
                                             f"max_allocation: {max_allocation}, "
                                             f"running_avg_volume_period: {running_avg_volume_period}, "
                                             f"primary_candidate: {primary_candidate}, "
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
                                            index_candidate_size = index * 2,
                                            primary_candidate_size = min(primary_candidate, index),
                                            secondary_candidate_size = min(primary_candidate, index) + 5,
                                            initial_funds = 1000,
                                            offset = offset,
                                            start_dt = start_dt,
                                            end_dt = end_dt
                                        )

                                        bci.set_input_data(input_data)

                                        [dates, baseline_values, index_values, fees] = bci.run()
                                        results.append([
                                            index,
                                            rebalancing,
                                            primary_volume_filter,
                                            secondary_volume_filter,
                                            max_allocation,
                                            running_avg_volume_period,
                                            primary_candidate,
                                            offset,
                                            dates, index_values, fees, baseline_values])
                                    except Exception as e:
                                        LOG.info(e)

    LOG.info(f"Best performing index configurations:")
    for data in sorted(results, key = lambda x: x[9][-1], reverse = True):
        LOG.info(f"{data[:8]}:{data[9][-1]:.2f}:{data[11][-1]:.2f}:{data[10]:.2f}")

    LOG.info(f"Best performing baseline configurations:")
    for data in sorted(results, key = lambda x: x[11][-1], reverse = True):
        LOG.info(f"{data[:8]}:{data[9][-1]:.2f}:{data[11][-1]:.2f}:{data[10]:.2f}")

    with open(f"results_{args['index']}_{start_dt}_{end_dt}.json", 'w') as file:
        file.write(json.dumps(results))

    with open(f"results_{args['index']}_{start_dt}_{end_dt}.csv", 'w') as file:
        for data in results:
            file.write(f"{';'.join(map(str, data[:8]))};{data[9][-1]};{data[11][-1]};{data[10]}\n")

    dates = None
    for data in results[-10:]:
        dates = data[8]
        plt.plot(data[8], data[9], label = str(data[:8]), linewidth = 0.7)

    plt.xlabel('Date')
    plt.xticks(list(filter(lambda x: x.split('-')[2] == '01' and int(x.split('-')[1]) % 3 == 0, dates)), rotation = 45, fontsize = 6)

    plt.ylabel('Value (USD)')

    plt.title(f'BCI {start_dt} - {end_dt}')

    plt.grid(linestyle = '--', linewidth = 0.5)

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)

    plt.savefig(f"index_comparison_{args['index']}_{start_dt}_{end_dt}.svg", format = "svg")

    #plt.show()