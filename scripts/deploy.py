#!/usr/bin/env python3
"""
VyperVerse Deployment Script
Deploy ExpenseSplitter contract to various networks
"""

import os
import sys
import json
import time
from typing import Dict, Any, Optional
from web3 import Web3
from eth_account import Account
from vyper import compile_code

# Network configurations
NETWORKS = {
    "celo-alfajores": {
        "rpc_url": "https://alfajores-forno.celo-testnet.org",
        "chain_id": 44787,
        "explorer": "https://explorer.celo.org/alfajores",
        "gas_price": "20 gwei"
    },
    "monad-testnet": {
        "rpc_url": "https://testnet-rpc.monad.xyz",
        "chain_id": 41434,
        "explorer": "https://testnet-explorer.monad.xyz",
        "gas_price": "20 gwei"
    },
    "berachain-testnet": {
        "rpc_url": "https://testnet-rpc.berachain.com",
        "chain_id": 80085,
        "explorer": "https://testnet-scan.berachain.com",
        "gas_price": "20 gwei"
    },
    "ethereum-sepolia": {
        "rpc_url": "https://rpc.sepolia.org",
        "chain_id": 11155111,
        "explorer": "https://sepolia.etherscan.io",
        "gas_price": "20 gwei"
    }
}

class ContractDeployer:
    def __init__(self, network: str, private_key: str):
        """Initialize the contract deployer"""
        if network not in NETWORKS:
            raise ValueError(f"Unsupported network: {network}")
        
        self.network_config = NETWORKS[network]
        self.w3 = Web3(Web3.HTTPProvider(self.network_config["rpc_url"]))
        
        if not self.w3.is_connected():
            raise ConnectionError(f"Failed to connect to {network}")
        
        self.account = Account.from_key(private_key)
        self.w3.eth.default_account = self.account.address
        
        print(f"Connected to {network}")
        print(f"Account: {self.account.address}")
        print(f"Balance: {self.w3.eth.get_balance(self.account.address) / 10**18:.4f} ETH")
    
    def load_contract_source(self, contract_path: str) -> str:
        """Load Vyper contract source code"""
        try:
            with open(contract_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Contract file not found: {contract_path}")
    
    def compile_contract(self, source_code: str) -> Dict[str, Any]:
        """Compile Vyper contract"""
        try:
            print("Compiling contract...")
            compiled = compile_code(source_code, ["abi", "bytecode"])
            print("✅ Contract compiled successfully")
            return compiled
        except Exception as e:
            raise Exception(f"Compilation failed: {e}")
    
    def estimate_gas(self, bytecode: str, constructor_args: list = None) -> int:
        """Estimate gas for contract deployment"""
        try:
            if constructor_args:
                # Encode constructor arguments if needed
                # This is a simplified version - in practice, you'd need proper ABI encoding
                pass
            
            gas_estimate = self.w3.eth.estimate_gas({
                'data': bytecode,
                'from': self.account.address
            })
            
            # Add 20% buffer
            return int(gas_estimate * 1.2)
        except Exception as e:
            print(f"Gas estimation failed: {e}")
            return 2000000  # Default gas limit
    
    def deploy_contract(self, bytecode: str, abi: list, constructor_args: list = None) -> str:
        """Deploy contract to blockchain"""
        try:
            print("Deploying contract...")
            
            # Estimate gas
            gas_limit = self.estimate_gas(bytecode, constructor_args)
            
            # Get current gas price
            gas_price = self.w3.eth.gas_price
            
            # Build transaction
            transaction = {
                'from': self.account.address,
                'data': bytecode,
                'gas': gas_limit,
                'gasPrice': gas_price,
                'nonce': self.w3.eth.get_transaction_count(self.account.address)
            }
            
            # Sign and send transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.account.key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            print(f"Transaction sent: {tx_hash.hex()}")
            print("Waiting for confirmation...")
            
            # Wait for transaction receipt
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            if receipt.status == 1:
                contract_address = receipt.contractAddress
                print(f"✅ Contract deployed successfully!")
                print(f"Contract Address: {contract_address}")
                print(f"Transaction Hash: {tx_hash.hex()}")
                print(f"Gas Used: {receipt.gasUsed}")
                print(f"Block Number: {receipt.blockNumber}")
                
                return contract_address
            else:
                raise Exception("Transaction failed")
                
        except Exception as e:
            raise Exception(f"Deployment failed: {e}")
    
    def verify_contract(self, contract_address: str, source_code: str, abi: list) -> bool:
        """Verify contract on block explorer"""
        try:
            print("Contract verification...")
            print("Note: Automatic verification is not implemented in this script.")
            print("Please verify manually on the block explorer:")
            print(f"{self.network_config['explorer']}/address/{contract_address}")
            print("\nVerification details:")
            print(f"- Compiler: Vyper 0.4.1")
            print(f"- EVM Version: Cancun")
            print(f"- Source Code: {source_code[:100]}...")
            return True
        except Exception as e:
            print(f"Verification failed: {e}")
            return False
    
    def save_deployment_info(self, contract_address: str, tx_hash: str, abi: list, network: str):
        """Save deployment information to file"""
        deployment_info = {
            "network": network,
            "contract_address": contract_address,
            "transaction_hash": tx_hash,
            "abi": abi,
            "deployed_at": time.time(),
            "deployer": self.account.address
        }
        
        filename = f"deployment_{network}_{int(time.time())}.json"
        with open(filename, 'w') as f:
            json.dump(deployment_info, f, indent=2)
        
        print(f"Deployment info saved to: {filename}")

def main():
    """Main deployment function"""
    if len(sys.argv) < 3:
        print("Usage: python deploy.py <network> <private_key> [contract_path]")
        print("Networks: celo-alfajores, monad-testnet, berachain-testnet, ethereum-sepolia")
        sys.exit(1)
    
    network = sys.argv[1]
    private_key = sys.argv[2]
    contract_path = sys.argv[3] if len(sys.argv) > 3 else "contracts/solutions/ExpenseSplitter_Complete.vy"
    
    try:
        # Initialize deployer
        deployer = ContractDeployer(network, private_key)
        
        # Load and compile contract
        source_code = deployer.load_contract_source(contract_path)
        compiled = deployer.compile_contract(source_code)
        
        # Deploy contract
        contract_address = deployer.deploy_contract(
            compiled["bytecode"],
            compiled["abi"]
        )
        
        # Verify contract
        deployer.verify_contract(contract_address, source_code, compiled["abi"])
        
        # Save deployment info
        deployer.save_deployment_info(
            contract_address,
            "tx_hash_placeholder",  # Would be actual tx hash in real implementation
            compiled["abi"],
            network
        )
        
        print("\n🎉 Deployment completed successfully!")
        print(f"Contract Address: {contract_address}")
        print(f"Network: {network}")
        print(f"Explorer: {NETWORKS[network]['explorer']}/address/{contract_address}")
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
