import click
from pathlib import Path
from web3 import Web3, HTTPProvider

from .transfer import transfer as _transfer, encrypt as _encrypt
from .erc20 import erc20_balance, Erc20


@click.group()
def _cli():
    pass


@_cli.command(help="test the connection, using a given address")
@click.option(
    "--node-address",
    type=str,
    default="https://geth.golem.network:55555",
    # default="https://rpc.ankr.com/eth_holesky",
)
@click.argument(
    "wallet_address",
    default="0xb929ac45b74e182b287d9ce1142e5bda76d1a3d0"
)
def test(node_address: str, wallet_address: str):
    wallet_address = Web3.to_checksum_address(wallet_address)
    w3 = Web3(HTTPProvider(node_address))
    print(Web3.from_wei(w3.eth.get_balance(wallet_address), "ether"))
    #print(w3.eth.get_logs({"fromBlock": "0x10369d2", "toBlock": "0x10369d2","address": "0x7DD9c5Cba05E151C895FDe1CF355C9A1D5DA6429","topics": ["0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"]}))

@_cli.command(help="test connection, using the GLM transfer and a given address")
@click.option(
    "--node-address",
    type=str,
    default="https://rpc.ankr.com/eth_holesky",
)
@click.argument(
    "wallet_address",
    default="0xb929ac45b74e182b287d9ce1142e5bda76d1a3d0"
)
def glm_balance(node_address: str, wallet_address: str):
    GLM = {
        17000: "0x8888888815bf4DB87e57B609A50f938311EEd068"
    }

    w3 = Web3(Web3.HTTPProvider(node_address))
    wallet_address = Web3.to_checksum_address(wallet_address)
    balance = erc20_balance(w3, GLM.get(w3.eth.chain_id), wallet_address)
    print(balance)

@_cli.command(help="test GLM transfer")
@click.option(
    "--node-address",
    type=str,
    default="https://rpc.ankr.com/eth_holesky",
)
@click.option(
    "--keyfile",
    type=Path,
    default=Path("key.json")
)
@click.option(
    "--key-password",
    type=str,
    default="",
)
@click.argument(
    "to_address",
    type=str,
)
@click.argument(
    "value",
    type=str,
)
def glm_transfer(node_address: str, keyfile: Path, key_password: str, to_address: str, value: float):
    GLM = {
        17000: "0x8888888815bf4DB87e57B609A50f938311EEd068"
    }

    w3 = Web3(Web3.HTTPProvider(node_address))
    to_address = w3.to_checksum_address(to_address)
    erc20 = Erc20(w3, GLM.get(w3.eth.chain_id), )
    erc20.use_private_key(keyfile.open("r").read(), key_password)
    tx_hash = erc20.send_glm(to_address, int(w3.to_wei(value, "ether")))
    print(tx_hash)
    print(erc20.wait_for_receipt(tx_hash))

@_cli.command(help="test transfer")
@click.option(
    "--node-address",
    type=str,
    default="https://geth.golem.network:55555",
)
@click.option(
    "--keyfile",
    type=Path,
    default=Path("key.json")
)
@click.option(
    "--key-password",
    type=str,
    default="",
)
@click.argument(
    "to_address",
    type=str,
)
@click.argument(
    "value",
    type=float,
)
def transfer(node_address: str, keyfile: Path, key_password: str, to_address: str, value: float):
    _transfer(node_address, keyfile, key_password, to_address, value)

@_cli.command(help="encrypt the key")
@click.option(
    "--keyfile",
    type=Path,
    default=Path("key.json")
)
@click.option(
    "--key-password",
    type=str,
    default="",
)
def encrypt(keyfile: Path, key_password: str):
    _encrypt(keyfile, key_password)

if __name__ == "__main__":
    _cli()
