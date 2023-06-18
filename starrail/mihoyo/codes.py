from enum import Enum

# version dependent: 2.50.1
salt_k2 = 'A4lPYtN0KGRVwE5M5Fm0DqQiC5VVMVM3	'
salt_lk2 = 'kkFiNdhyHqZ1VnDRHnU1podIvO4eiHcs'

# version irrelevant
salt_4x = 'xV8v4Qu54lUKrEYFZkJhB8cuOh9Asafs'
salt_6x = 't0qEgfub6cvueAPgR5m9aQWWVciEer7v'
salt_prod = 'JwYDpKvLj6MrMqqYU6jTKF17KNO2PXoS'


class SaltType(Enum):

    SALT_K2 = salt_k2
    SALT_LK2 = salt_lk2
    SALT_4X = salt_4x
    SALT_6X = salt_6x
    SALT_PROD = salt_prod
