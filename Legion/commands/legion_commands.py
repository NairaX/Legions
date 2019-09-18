#!/usr/bin/env python3

# Legion - Shayan Eskandari, ConsenSys Diligence

import asyncio
import os
import socket
import typing
from termcolor import cprint
from nubia import command, argument
from legion_context import context
from web3 import Web3
import requests
from helper_functions import getChainName

w3 = Web3()
LEGION_VERSION = "0.0.1"

Protocols = ["http", "rpc", "ipc", "ws"]
host = None

@command(aliases=["sethost"])
@argument("host", description="Address of the RPC Node", aliases=["u"])
def sethost(host: str):
    """
    Setup the Web3 connection (RPC, IPC, HTTP) - This should be the first step 
    """
    if (host is None):
        cprint("Missing Argument 'host'?", "red")
        return 0

    ctx = context.get_context()
    cprint("Input: {}".format(host), "yellow")
    cprint("Verbose? {}".format(ctx.verbose), "yellow")

    w3 = Web3()
    if not any(ext in host for ext in Protocols):
        host = "https://" + host

    # if helper_functions.checkConnection(url = url, verbose=True)
    WEB3_PROVIDER_URI = host
    os.environ["WEB3_PROVIDER_URI"] = host

    if (w3.isConnected()):
        cprint("Web3 API Version: {}".format(w3.api), "green")
        cprint("connected to: {}".format(w3.provider._active_provider.endpoint_uri), "green")
        cprint("Version: {}".format(w3.clientVersion), "green")
    else:
        cprint("Web3 API Version: {}".format(w3.api), "red")
        cprint("Cannot connect to: {} ".format(host), "red")

    # optional, by default it's 0
    return 0


@command("getnodeinfo")
def getnodeinfo():
    """
    Prints information about the node (run setnode before this) 
    """
    if (w3.isConnected()):
        cprint("Web3 API Version: {}".format(w3.api), "white")
        cprint("connected to: {}".format(w3.provider._active_provider.endpoint_uri), "white")
        cprint("Version: {}".format(w3.clientVersion), "green")
        cprint("--" * 32)
        cprint("Last Block Number: {}".format(w3.eth.blockNumber), "green")
        cprint("Chain: {} (ChainID: {})".format(getChainName(w3.eth.chainId), w3.eth.chainId), "green")
        cprint("Protocol Version: {}".format(w3.eth.protocolVersion), "green")
        cprint("Is Listening: {}".format(w3.net.listening), "green")    
        cprint("Peer Count: {}".format(w3.net.peerCount), "green")  
        cprint("Is Syncing: {}".format(w3.eth.syncing), "green")
        cprint("Is Mining: {}".format(w3.eth.mining), "green")
        cprint("Hash Rate: {}".format(w3.eth.hashrate), "green")
        cprint("Gas Price: {}".format(w3.eth.gasPrice), "green")
        cprint("--" * 32)
        try:
            cprint("Coinbase Account: {}".format(w3.eth.coinbase), "green") 
        except Exception as e:
            cprint("Coinbase not available: {}".format(e), "red")   
            
        cprint("Accounts: {}".format(w3.eth.accounts), "green")    
    else:
        cprint("Web3 API Version: {}".format(w3.api), "red")
        cprint("Cannot connect to: {} ".format(host), "red")
        cprint("Did you run sethost?", "red")

    # optional, by default it's 0
    return 0

@command("version")
def version():
    """
    Print Versions (If connected to a node it will print the host version too)
    """
    cprint("Legion Version: {}".format(LEGION_VERSION), "white")
    cprint("Web3 API Version: {}".format(w3.api), "white")
    if (w3.isConnected()):
        cprint("connected to: {}".format(w3.provider._active_provider.endpoint_uri), "green")
        cprint("Version: {}".format(w3.clientVersion), "green")
    else:
        cprint("Not connected to any hosts.", "red")



# @command
# @argument("number", type=int)
# async def triple(number):
#     "Calculates the triple of the input value"
#     cprint("Input is {}".format(number))
#     cprint("Type of input is {}".format(type(number)))
#     cprint("{} * 3 = {}".format(number, number * 3))
#     await asyncio.sleep(2)


# @command
# @argument("style", description="Pick a style", choices=["test", "toast", "toad"])
# @argument("stuff", description="more colors", choices=["red", "green", "blue"])
# @argument("code", description="Color code", choices=[12, 13, 14])
# def pick(style: str, stuff: typing.List[str], code: int):
#     """
#     A style picking tool
#     """
#     cprint("Style is '{}' code is {}".format(style, code), "yellow")


# instead of replacing _ we rely on camelcase to - super-command


@command
class Investigate:
    "Investigate further in the node (e.g. check if accounts are unlocked, etc)"

    def __init__(self) -> None:
        # self._shared = shared
        if not (w3.isConnected()):
            cprint("Web3 API Version: {}".format(w3.api), "red")
            cprint("Cannot connect to: {} ".format(host), "red")
            cprint("Did you run sethost?", "red")
            return None

    @property
    def shared(self) -> int:
        return self._shared

    """This is the super command help"""

    @command("accounts")
    def investigate_accounts(self):
        """
        Investigate accounts (e.g. check if accounts are unlocked, etc)
        """
        if (w3.isConnected()):
            try:
                coinbase = w3.eth.coinbase
            except Exception as e:
                cprint("Coinbase not available: {}".format(e), "red")   
            accounts = w3.eth.accounts
            if len(accounts) == 0:
                cprint("No accounts found", "red")
                if type(coinbase) is None: #TODO: check if we need this. If accounts = [] , then there shouldn't be coinbase (?)
                    cprint("Nothing to do here")
                    return 0
            
            for account in accounts:
                # cprint("Balance of {} is : {}".format(account, w3.eth.getBalance(account)), "white")
                # try:
                #     cprint("Trying to unlock {}: {}".format(account, w3.parity.personal.unlockAccount(account, "")), "white")
                # except Exception as e:
                #     cprint("Failed to unlock: {}".format(e))
                pass
            #web3.geth.personal.unlockAccount(self, account, passphrase, duration=None)
       #cprint("Web3 API Version: {}".format(w3.geth.personal.listAccounts()), "white")
            # cprint("importRawKey: {}".format(w3.parity.personal.importRawKey("0x98f55b035870ed23884334cafe62739128043414097e1c6a3a4872131dc393a9", "")), "white")
            cprint("Number of Accounts: {}".format(len(w3.eth.accounts)), "green")    
            #cprint("newAccount: {}".format(w3.parity.personal.newAccount("Legion2019")), "white") #WORKS!!

            #w3.geth.personal.newAccount(self, "Legion2019")

            cprint("Web3 API Version: {}".format(w3.api), "white")
            cprint("connected to: {}".format(w3.provider._active_provider.endpoint_uri), "white")
            cprint("Version: {}".format(w3.clientVersion), "green")
            cprint("--" * 32)


    @command("admin")
    def investigate_admin(self):
        """
        Investigate accounts (e.g. functionalities nder the admin_ namespace)
        """
        print(w3.clientVersion)
        # More interfaces here: https://web3py.readthedocs.io/en/stable/web3.geth.html
        # if "geth" in (w3.clientVersion.lower()): #TODO: make this figure out if the node is Geth or Parity and send the appropriate commands
        try:
            cprint("datadir: {}".format(w3.geth.admin.datadir()), "white")
        except Exception as e:
            cprint("datadir: {}".format(e), "red")
        try:
            cprint("nodeInfo: {}".format(w3.geth.admin.nodeInfo()), "white")
        except Exception as e:
            cprint("nodeInfo {}".format(e), "red")        
        try:
            cprint("peers: {}".format(w3.geth.admin.peers()), "white")
        except Exception as e:
            cprint("peers {}".format(e), "red")
        try:
            cprint("txpool.status: {}".format(w3.geth.txpool.status()), "white")
        except Exception as e:
            cprint("txpool.status {}".format(e), "red")       
        try:
            cprint("shh.version: {}".format(w3.geth.shh.version()), "white")
        except Exception as e:
            cprint("shh.version: {}".format(e), "red")       
        try:
            cprint("Wshh.info: {}".format(w3.geth.shh.info()), "white")
        except Exception as e:
            cprint("shh.info: {}".format(e), "red")
        # elif "parity" in (w3.clientVersion.lower()):
        #     try:
        #         cprint("datadir: {}".format(w3.parity_versionInfo()), "white")
        #     except Exception as e:
        #         cprint("datadir: {}".format(e), "red")
        #     try:
        #         cprint("nodeInfo: {}".format(w3.parity_lockedHardwareAccountsInfo()), "white")
        #     except Exception as e:
        #         cprint("nodeInfo {}".format(e), "red")        
        #     try:
        #         cprint("peers: {}".format(w3.parity_localTransactions()), "white")
        #     except Exception as e:
        #         cprint("peers {}".format(e), "red")
        #     try:
        #         cprint("txpool.status: {}".format(w3.make_request("parity_listVaults", [])), "white")
        #     except Exception as e:
        #         cprint("txpool.status {}".format(e), "red")       
        #     try:
        #         cprint("shh.version: {}".format(w3.parity.shh.__dict__), "white")
        #     except Exception as e:
        #         cprint("shh.version: {}".format(e), "red")       
        #     try:
        #         cprint("Wshh.info: {}".format(w3.parity.shh.info()), "white")
        #     except Exception as e:
        #         cprint("shh.info: {}".format(e), "red")
