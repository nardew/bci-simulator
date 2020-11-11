import logging

from BCI import BCI

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

LOG = logging.getLogger(__name__)

if __name__ == "__main__":
    LOG.info("Bitpanda Crypto Index Simulator")

    bci = BCI(5, 0, 600000, 1000000, 0.35, 0.02, 30, 10, 3, 7, 1000, "input_data.json", start_dt = '2020-10-01')
    #bci = BCI(10, 0, 600000, 1000000, 0.3, 0.002, 30, 20, 7, 13, 1000, "input_data.json", start_dt = '2016-07-01')
    bci.run()