import random
import time

from bxsolana_trader_proto import api as proto

from bxsolana import provider
from bxsolana.transaction import signing

crank_timeout = 60
