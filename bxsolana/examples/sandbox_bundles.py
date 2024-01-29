from bxsolana_trader_proto import api as proto

from bxsolana.examples.order_utils import place_order_with_tip
from .. import provider


if __name__ == "__main__":
    openbook_tx_with = place_order_with_tip()
