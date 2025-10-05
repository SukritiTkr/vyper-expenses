#!/usr/bin/env python3
"""
VyperVerse Contract Interaction Script
Interact with deployed ExpenseSplitter contracts
"""

import os
import sys
import json
import time
from typing import Dict, Any, Optional
from web3 import Web3
from eth_account import Account

# Contract ABI
CONTRACT_ABI = [
    {
        "type": "event",
        "name": "ExpenseRecorded",
        "inputs": [
            {"name": "user", "type": "address", "indexed": True},
            {"name": "description", "type": "string"},
            {"name": "amount", "type": "uint256"},
            {"name": "timestamp", "type": "uint256"}
        ]
    },
    {
        "type": "event",
        "name": "ParticipantAdded",
        "inputs": [
            {"name": "participant", "type": "address", "indexed": True},
            {"name": "added_by", "type": "address", "indexed": True}
        ]
    },
    {
        "type": "event",
        "name": "PaymentReceived",
        "inputs": [
            {"name": "from_user", "type": "address", "indexed": True},
            {"name": "amount", "type": "uint256"}
        ]
    },
    {
        "type": "event",
        "name": "ExpenseSettled",
        "inputs": [
            {"name": "user", "type": "address", "indexed": True},
            {"name": "amount", "type": "uint256"}
        ]
    },
    {
        "type": "function",
        "name": "get_participant_count",
        "stateMutability": "view",
        "inputs": [],
        "outputs": [{"name": "", "type": "uint256"}]
    },
    {
        "type": "function",
        "name": "calculate_equal_split",
        "stateMutability": "view",
        "inputs": [],
        "outputs": [{"name": "", "type": "uint256"}]
    },
    {
        "type": "function",
        "name": "get_my_balance",
        "stateMutability": "view",
        "inputs": [],
        "outputs": [{"name": "", "type": "uint256"}]
    },
    {
        "type": "function",
        "name": "check_contract_balance",
        "stateMutability": "view",
        "inputs": [],
        "outputs": [{"name": "", "type": "uint256"}]
    },
    {
        "type": "function",
        "name": "get_participant_at",
        "stateMutability": "view",
        "inputs": [{"name": "index", "type": "uint256"}],
        "outputs": [{"name": "", "type": "address"}]
    },
    {
        "type": "function",
        "name": "is_participant",
        "stateMutability": "view",
        "inputs": [{"name": "check_address", "type": "address"}],
        "outputs": [{"name": "", "type": "bool"}]
    },
    {
        "type": "function",
        "name": "total_expenses",
        "stateMutability": "view",
        "inputs": [],
        "outputs": [{"name": "", "type": "uint256"}]
    },
    {
        "type": "function",
        "name": "expense_count",
        "stateMutability": "view",
        "inputs": [],
        "outputs": [{"name": "", "type": "uint256"}]
    },
    {
        "type": "function",
        "name": "owner",
        "stateMutability": "view",
        "inputs": [],
        "outputs": [{"name": "", "type": "address"}]
    },
    {
        "type": "function",
        "name": "record_expense",
        "stateMutability": "nonpayable",
        "inputs": [
            {"name": "description", "type": "string"},
            {"name": "amount", "type": "uint256"}
        ],
        "outputs": []
    },
    {
        "type": "function",
        "name": "add_participant",
        "stateMutability": "nonpayable",
        "inputs": [{"name": "new_participant", "type": "address"}],
        "outputs": []
    },
    {
        "type": "function",
        "name": "contribute",
        "stateMutability": "payable",
        "inputs": [],
        "outputs": []
    },
    {
        "type": "function",
        "name": "settle_expenses",
        "stateMutability": "nonpayable",
        "inputs": [],
        "outputs": []
    },
    {
        "type": "function",
        "name": "emergency_withdraw",
        "stateMutability": "nonpayable",
        "inputs": [],
        "outputs": []
    }
]

class ContractInteractor:
    def __init__(self, rpc_url: str, private_key: str, contract_address: str):
        """Initialize the contract interactor"""
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        
        if not self.w3.is_connected():
            raise ConnectionError(f"Failed to connect to {rpc_url}")
        
        self.account = Account.from_key(private_key)
        self.w3.eth.default_account = self.account.address
        
        # Create contract instance
        self.contract = self.w3.eth.contract(
            address=contract_address,
            abi=CONTRACT_ABI
        )
        
        print(f"Connected to contract at: {contract_address}")
        print(f"Account: {self.account.address}")
        print(f"Balance: {self.w3.eth.get_balance(self.account.address) / 10**18:.4f} ETH")
    
    def send_transaction(self, function_call, value: int = 0) -> str:
        """Send a transaction to the contract"""
        try:
            # Build transaction
            transaction = function_call.build_transaction({
                'from': self.account.address,
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price,
                'value': value,
                'nonce': self.w3.eth.get_transaction_count(self.account.address)
            })
            
            # Sign and send transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.account.key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            print(f"Transaction sent: {tx_hash.hex()}")
            print("Waiting for confirmation...")
            
            # Wait for transaction receipt
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            if receipt.status == 1:
                print(f"✅ Transaction successful!")
                print(f"Gas Used: {receipt.gasUsed}")
                return tx_hash.hex()
            else:
                raise Exception("Transaction failed")
                
        except Exception as e:
            raise Exception(f"Transaction failed: {e}")
    
    def call_view_function(self, function_name: str, *args) -> Any:
        """Call a view function on the contract"""
        try:
            function = getattr(self.contract.functions, function_name)
            result = function(*args).call()
            return result
        except Exception as e:
            raise Exception(f"Function call failed: {e}")
    
    def get_contract_info(self) -> Dict[str, Any]:
        """Get basic contract information"""
        try:
            info = {
                "owner": self.call_view_function("owner"),
                "total_expenses": self.call_view_function("total_expenses"),
                "expense_count": self.call_view_function("expense_count"),
                "participant_count": self.call_view_function("get_participant_count"),
                "contract_balance": self.call_view_function("check_contract_balance"),
                "my_balance": self.call_view_function("get_my_balance"),
                "equal_split": self.call_view_function("calculate_equal_split")
            }
            return info
        except Exception as e:
            raise Exception(f"Failed to get contract info: {e}")
    
    def record_expense(self, description: str, amount_eth: float) -> str:
        """Record a new expense"""
        try:
            amount_wei = int(amount_eth * 10**18)
            function_call = self.contract.functions.record_expense(description, amount_wei)
            return self.send_transaction(function_call)
        except Exception as e:
            raise Exception(f"Failed to record expense: {e}")
    
    def add_participant(self, participant_address: str) -> str:
        """Add a new participant"""
        try:
            function_call = self.contract.functions.add_participant(participant_address)
            return self.send_transaction(function_call)
        except Exception as e:
            raise Exception(f"Failed to add participant: {e}")
    
    def contribute(self, amount_eth: float) -> str:
        """Contribute funds to the contract"""
        try:
            amount_wei = int(amount_eth * 10**18)
            function_call = self.contract.functions.contribute()
            return self.send_transaction(function_call, value=amount_wei)
        except Exception as e:
            raise Exception(f"Failed to contribute: {e}")
    
    def settle_expenses(self) -> str:
        """Settle expenses for the caller"""
        try:
            function_call = self.contract.functions.settle_expenses()
            return self.send_transaction(function_call)
        except Exception as e:
            raise Exception(f"Failed to settle expenses: {e}")
    
    def emergency_withdraw(self) -> str:
        """Emergency withdraw (owner only)"""
        try:
            function_call = self.contract.functions.emergency_withdraw()
            return self.send_transaction(function_call)
        except Exception as e:
            raise Exception(f"Failed to emergency withdraw: {e}")
    
    def get_participants(self) -> list:
        """Get list of all participants"""
        try:
            participant_count = self.call_view_function("get_participant_count")
            participants = []
            
            for i in range(participant_count):
                participant_address = self.call_view_function("get_participant_at", i)
                balance = self.call_view_function("get_my_balance")
                participants.append({
                    "address": participant_address,
                    "balance": balance / 10**18
                })
            
            return participants
        except Exception as e:
            raise Exception(f"Failed to get participants: {e}")
    
    def print_contract_info(self):
        """Print formatted contract information"""
        try:
            info = self.get_contract_info()
            
            print("\n" + "="*50)
            print("CONTRACT INFORMATION")
            print("="*50)
            print(f"Owner: {info['owner']}")
            print(f"Total Expenses: {info['total_expenses'] / 10**18:.4f} ETH")
            print(f"Expense Count: {info['expense_count']}")
            print(f"Participants: {info['participant_count']}")
            print(f"Contract Balance: {info['contract_balance'] / 10**18:.4f} ETH")
            print(f"My Balance: {info['my_balance'] / 10**18:.4f} ETH")
            print(f"Equal Split: {info['equal_split'] / 10**18:.4f} ETH")
            print("="*50)
            
        except Exception as e:
            print(f"Failed to print contract info: {e}")

def main():
    """Main interaction function"""
    if len(sys.argv) < 4:
        print("Usage: python interact.py <rpc_url> <private_key> <contract_address> [command]")
        print("Commands: info, record <description> <amount>, add <address>, contribute <amount>, settle, withdraw")
        sys.exit(1)
    
    rpc_url = sys.argv[1]
    private_key = sys.argv[2]
    contract_address = sys.argv[3]
    command = sys.argv[4] if len(sys.argv) > 4 else "info"
    
    try:
        # Initialize interactor
        interactor = ContractInteractor(rpc_url, private_key, contract_address)
        
        # Execute command
        if command == "info":
            interactor.print_contract_info()
            
        elif command == "record":
            if len(sys.argv) < 7:
                print("Usage: python interact.py <rpc_url> <private_key> <contract_address> record <description> <amount>")
                sys.exit(1)
            description = sys.argv[5]
            amount = float(sys.argv[6])
            tx_hash = interactor.record_expense(description, amount)
            print(f"Expense recorded! Transaction: {tx_hash}")
            
        elif command == "add":
            if len(sys.argv) < 6:
                print("Usage: python interact.py <rpc_url> <private_key> <contract_address> add <address>")
                sys.exit(1)
            participant_address = sys.argv[5]
            tx_hash = interactor.add_participant(participant_address)
            print(f"Participant added! Transaction: {tx_hash}")
            
        elif command == "contribute":
            if len(sys.argv) < 6:
                print("Usage: python interact.py <rpc_url> <private_key> <contract_address> contribute <amount>")
                sys.exit(1)
            amount = float(sys.argv[5])
            tx_hash = interactor.contribute(amount)
            print(f"Contribution sent! Transaction: {tx_hash}")
            
        elif command == "settle":
            tx_hash = interactor.settle_expenses()
            print(f"Expenses settled! Transaction: {tx_hash}")
            
        elif command == "withdraw":
            tx_hash = interactor.emergency_withdraw()
            print(f"Emergency withdrawal! Transaction: {tx_hash}")
            
        else:
            print(f"Unknown command: {command}")
            print("Available commands: info, record, add, contribute, settle, withdraw")
            sys.exit(1)
        
        # Print updated info
        if command != "info":
            print("\nUpdated contract information:")
            interactor.print_contract_info()
        
    except Exception as e:
        print(f"❌ Interaction failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
