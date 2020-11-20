import logging
import sys
import argparse

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
    parser.add_argument('--rebalancing', help = 'Rebalancing period in days. If set to 0, rebalancing takes place on the first day of month', default = 0, type = int)
    parser.add_argument('--fee', help = 'Transaction fees', default = 0.02, type = float)
    parser.add_argument('--max-allocation', help = 'Maximum percentage allocation of a coin in the index', default = 0.35, type = float)
    parser.add_argument('--volume-period', help = 'Running average volume period in days', default = 30, type = int)
    parser.add_argument('--primary-volume-filter', help = 'USD amount for the 1st volume filtering', default = 600000, type = float)
    parser.add_argument('--secondary-volume-filter', help = 'USD amount for the 2nd volume filtering', default = 1000000, type = float)
    parser.add_argument('--candidates', help = 'Number of candidates for the index', default = 10, type = int)
    parser.add_argument('--primary-candidates', help = 'Primary candidates size', default = 3, type = int)
    parser.add_argument('--secondary-candidates', help = 'Secondary candidates size', default = 7, type = int)
    parser.add_argument('--funds', help = 'Initial funds', default = 1000, type = float)
    parser.add_argument('--offset', help = 'Offset to consider top performing currencies', default = 0, type = int)
    parser.add_argument('--bypass-validation', help = 'Bypass validation of input parameters', action = 'store_true', default = False)
    parser.add_argument('--input-file', help = 'JSON file with the input data', default = "./input_data.json")
    parser.add_argument('--start-date', help = 'Start date in YYYY-MM-DD format. None for all dates', default = None)
    parser.add_argument('--end-date', help = 'End date in YYYY-MM-DD format. None for all dates', default = None)
    parser.add_argument('--show-graph', help = 'Display graph', action = 'store_true', default = False)
    parser.add_argument('--save-graph', help = 'Save graph into a file', action = 'store_true', default = False)

    return vars(parser.parse_args())


if __name__ == "__main__":
    LOG.info("Bitpanda Crypto Index Simulator")

    args = parse_args()

    bci = BCI(
        index_size = args['index'],
        rebalancing_period = args['rebalancing'],
        primary_usd_filtering = args['primary_volume_filter'],
        secondary_usd_filtering = args['secondary_volume_filter'],
        max_asset_allocation = args['max_allocation'],
        fee = args['fee'],
        running_avg_volume_period = args['volume_period'],
        index_candidate_size = args['candidates'],
        primary_candidate_size = args['primary_candidates'],
        secondary_candidate_size = args['secondary_candidates'],
        initial_funds = args['funds'],
        offset = args['offset'],
        bypass_validation = args['bypass_validation'],
        input_file_name = args['input_file'],
        start_dt = args['start_date'],
        end_dt = args['end_date'],
        show_graph = args['show_graph'],
        save_graph = args['save_graph']
    )

    bci.run()