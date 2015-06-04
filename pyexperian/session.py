import requests
import ssl
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager


# Experian requires TLS over SSL
class ForceTLSV1Adapter(HTTPAdapter):
    """"Transport adapter" that allows us to use TLSv1"""

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

_session = None
def get_session():
    global _session
    if not _session:
        _session = requests.Session()
        _session.mount('https://', ForceTLSV1Adapter())

    return _session

