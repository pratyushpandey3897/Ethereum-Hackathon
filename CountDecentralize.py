# importing module
# https://mainnet.infura.io/v3/63b844a0c1c747e48c711b4f7d6cb859

import os
from ethereumetl.service.eth_service import EthService
from pandas import *
import matplotlib.pyplot as plt
import numpy as np
from ethereumetl.web3_utils import build_web3
from web3 import HTTPProvider, Web3
from dateutil.parser import parse
from ethereumetl.cli.export_blocks_and_transactions import export_blocks_and_transactions


date = '2022-10-26' # change date here

def get_new_eth_service():
    provider_url = os.environ.get('PROVIDER_URL', 'https://mainnet.infura.io/v3/63b844a0c1c747e48c711b4f7d6cb859')
    web3 = build_web3(HTTPProvider(provider_url))
    return EthService(web3)


eth_service = get_new_eth_service()

blocks = eth_service.get_block_range_for_date(parse(date))
print ("Start Block :" ,blocks[0] )
print ("End Block :" ,blocks[1] )

provider_uri = 'https://mainnet.infura.io/v3/63b844a0c1c747e48c711b4f7d6cb859'

block_dir = "blocks_" + date+".csv"
start_block = str(blocks[0])
end_block = str(blocks[1])

os.system("ethereumetl export_blocks_and_transactions --start-block "+start_block+ " --end-block "+ end_block+ " --blocks-output "+ block_dir+ " --provider-uri https://mainnet.infura.io/v3/63b844a0c1c747e48c711b4f7d6cb859")


#define function to calculate Gini coefficient
def gini(x):
    total = 0
    for i, xi in enumerate(x[:-1], 1):
        total += np.sum(np.abs(xi - x[i:]))
    return total / (len(x)**2 * np.mean(x))
 
data = read_csv(block_dir)

miner = data['miner'].tolist()
freq = {}
a =set()
for m in miner:
    a.add(m)
    if m in freq:
        freq[m] += 1
    else:
        freq[m] = 1

valuesList = list(freq.values())
print("Gini Coefficient: " , gini(np.array(valuesList)))

print("total validators :", len(miner))
print("unique validators :", len(a))

# Data to plot
labels = []
sizes = []

for x, y in freq.items():
    if y<20:
        labels.append("")
    else:
        labels.append(y)
    sizes.append(y)

# Plot
plt.pie(sizes, labels=labels)

plt.axis('equal')
plt.show()
