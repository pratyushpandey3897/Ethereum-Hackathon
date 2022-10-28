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
import math
from datetime import datetime, date, timedelta




def get_new_eth_service():
    provider_url = os.environ.get('PROVIDER_URL', 'https://mainnet.infura.io/v3/63b844a0c1c747e48c711b4f7d6cb859')
    web3 = build_web3(HTTPProvider(provider_url))
    return EthService(web3)

#define function to calculate Gini coefficient
def gini(x):
    total = 0
    for i, xi in enumerate(x[:-1], 1):
        total += np.sum(np.abs(xi - x[i:]))
    return total / (len(x)**2 * np.mean(x))

def shanon_entropy(x):
    total_blocks = sum(x)
    entropy = 0
    for validations in x:
        validation_prob = validations / total_blocks
        if validation_prob > 0:
            entropy = entropy + -(validation_prob * math.log(validation_prob, 2))
        
    return entropy

def plot_validation_distribution_piechart(freq):

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


def initialize_blocks(date,block_dir):

    eth_service = get_new_eth_service()

    blocks = eth_service.get_block_range_for_date(parse(date))
    print ("Start Block :" ,blocks[0] )
    print ("End Block :" ,blocks[1] )
    get_block_data(blocks,block_dir)

def get_block_data(blocks,block_dir):
    provider_uri = 'https://mainnet.infura.io/v3/63b844a0c1c747e48c711b4f7d6cb859'

    
    start_block = str(blocks[0])
    end_block = str(blocks[1])

    os.system("ethereumetl export_blocks_and_transactions --start-block "+start_block+ " --end-block "+ end_block+ " --blocks-output "+ block_dir+ " --provider-uri https://mainnet.infura.io/v3/63b844a0c1c747e48c711b4f7d6cb859")


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)



start_date = date(2022, 9, 1)
end_date = date(2022, 9, 30)

gini_values = {}
shanon_values = {}

for date in daterange(start_date, end_date):
    date = date.strftime("%Y-%m-%d")
    block_dir = "blocks_data.csv"

    print(date)
    initialize_blocks(date, block_dir)

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

    date_time_obj = datetime.strptime(date, '%Y-%m-%d')

    valuesList = list(freq.values())
    gini_values[date_time_obj.date()] = gini(np.array(valuesList))
    shanon_values[date_time_obj.date()] = shanon_entropy(np.array(valuesList))
    print("Gini Coefficient: " , gini_values[date_time_obj.date()])
    print("Shanon Entropy: " , shanon_values[date_time_obj.date()])
    # print("total validators :", len(miner))
    # print("unique validators :", len(a))


lists = sorted(gini_values.items())
x1, y1 = zip(*lists) # unpack a list of pairs into two tuples


lists = sorted(shanon_values.items())
x2, y2 = zip(*lists) # unpack a list of pairs into two tuples


figure, axis = plt.subplots(2, 1)
axis[0].plot(x1, y1)
axis[0].set_title("Gini's Coefficient")

axis[1].plot(x2, y2)
axis[1].set_title("Shanon Entropy")

plt.show()
