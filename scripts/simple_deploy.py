#!/usr/bin/env python3
"""
Simple Vyper Contract Deployment Script
Works without external dependencies - uses subprocess to call vyper directly
"""

import subprocess
import sys
import os
import json

def compile_contract(contract_path):
    """Compile Vyper contract and return bytecode and ABI"""
    try:
        # Compile to bytecode
        result = subprocess.run(['vyper', '-f', 'bytecode', contract_path], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Bytecode compilation failed: {result.stderr}")
            return None, None
        
        bytecode = result.stdout.strip()
        
        # Compile to ABI
        result_abi = subprocess.run(['vyper', '-f', 'abi', contract_path], 
                                  capture_output=True, text=True)
        if result_abi.returncode != 0:
            print(f"❌ ABI compilation failed: {result_abi.stderr}")
            return None, None
        
        abi = json.loads(result_abi.stdout)
        
        return bytecode, abi
        
    except Exception as e:
        print(f"❌ Compilation error: {e}")
        return None, None

def save_deployment_artifacts(contract_name, bytecode, abi):
    """Save deployment artifacts to files"""
    try:
        # Save bytecode
        with open(f'{contract_name}_bytecode.txt', 'w') as f:
            f.write(bytecode)
        
        # Save ABI
        with open(f'{contract_name}_abi.json', 'w') as f:
            json.dump(abi, f, indent=2)
        
        print(f"✅ Artifacts saved:")
        print(f"   📄 {contract_name}_bytecode.txt")
        print(f"   📄 {contract_name}_abi.json")
        
        return True
        
    except Exception as e:
        print(f"❌ Error saving artifacts: {e}")
        return False

def generate_remix_deployment_code(contract_name, bytecode, abi):
    """Generate JavaScript code for Remix deployment"""
    js_code = f"""
// Deployment code for {contract_name}
// Copy this code to Remix IDE console

const bytecode = "{bytecode}";
const abi = {json.dumps(abi, indent=2)};

// Deploy contract
async function deployContract() {{
    const contractFactory = new ethers.ContractFactory(abi, bytecode, signer);
    const contract = await contractFactory.deploy();
    await contract.deployed();
    
    console.log("Contract deployed at:", contract.address);
    console.log("Transaction hash:", contract.deployTransaction.hash);
    
    return contract;
}}

// Call this function in Remix console
deployContract();
"""
    
    with open(f'{contract_name}_remix_deploy.js', 'w') as f:
        f.write(js_code)
    
    print(f"   📄 {contract_name}_remix_deploy.js")

def generate_web3_deployment_script(contract_name, bytecode, abi):
    """Generate Python Web3 deployment script"""
    py_code = f'''#!/usr/bin/env python3
"""
Web3.py deployment script for {contract_name}
Install dependencies: pip install web3
"""

from web3 import Web3
import json

# Network configuration
RPC_URL = "https://alfajores-forno.celo-testnet.org"  # Change to your network
PRIVATE_KEY = "YOUR_PRIVATE_KEY_HERE"  # Replace with your private key

def deploy_contract():
    # Connect to network
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    
    if not w3.is_connected():
        print("❌ Failed to connect to network")
        return None
    
    # Setup account
    account = w3.eth.account.from_key(PRIVATE_KEY)
    w3.eth.default_account = account.address
    
    print(f"Deploying from: {{account.address}}")
    print(f"Balance: {{w3.eth.get_balance(account.address) / 10**18:.4f}} ETH")
    
    # Contract details
    bytecode = "{bytecode}"
    abi = {json.dumps(abi, indent=4)}
    
    # Deploy contract
    contract = w3.eth.contract(bytecode=bytecode, abi=abi)
    
    # Build transaction
    transaction = contract.constructor().build_transaction({{
        'from': account.address,
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.get_transaction_count(account.address)
    }})
    
    # Sign and send transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    
    print(f"Transaction sent: {{tx_hash.hex()}}")
    print("Waiting for confirmation...")
    
    # Wait for receipt
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    if receipt.status == 1:
        contract_address = receipt.contractAddress
        print(f"✅ Contract deployed successfully!")
        print(f"Contract Address: {{contract_address}}")
        print(f"Gas Used: {{receipt.gasUsed}}")
        return contract_address
    else:
        print("❌ Deployment failed")
        return None

if __name__ == "__main__":
    deploy_contract()
'''
    
    with open(f'{contract_name}_web3_deploy.py', 'w') as f:
        f.write(py_code)
    
    print(f"   📄 {contract_name}_web3_deploy.py")

def main():
    """Main deployment function"""
    if len(sys.argv) < 2:
        print("Usage: python simple_deploy.py <contract_path>")
        print("Example: python simple_deploy.py contracts/solutions/ExpenseSplitter_Complete.vy")
        sys.exit(1)
    
    contract_path = sys.argv[1]
    
    if not os.path.exists(contract_path):
        print(f"❌ Contract file not found: {contract_path}")
        sys.exit(1)
    
    contract_name = os.path.splitext(os.path.basename(contract_path))[0]
    
    print(f"🔨 Compiling {contract_name}...")
    
    # Compile contract
    bytecode, abi = compile_contract(contract_path)
    
    if not bytecode or not abi:
        print("❌ Compilation failed")
        sys.exit(1)
    
    print(f"✅ Compilation successful!")
    print(f"   Bytecode length: {len(bytecode)} characters")
    print(f"   ABI functions: {len([item for item in abi if item.get('type') == 'function'])}")
    print(f"   ABI events: {len([item for item in abi if item.get('type') == 'event'])}")
    
    # Save artifacts
    if save_deployment_artifacts(contract_name, bytecode, abi):
        print(f"\n🚀 Generating deployment scripts...")
        
        # Generate deployment scripts
        generate_remix_deployment_code(contract_name, bytecode, abi)
        generate_web3_deployment_script(contract_name, bytecode, abi)
        
        print(f"\n🎉 Deployment preparation complete!")
        print(f"\n📋 Next steps:")
        print(f"1. For Remix: Copy {contract_name}_remix_deploy.js to Remix console")
        print(f"2. For Web3.py: Install web3 (pip install web3) and run {contract_name}_web3_deploy.py")
        print(f"3. For Brownie: Use the bytecode and ABI files with Brownie")
        print(f"4. For Hardhat: Import the ABI and bytecode into your Hardhat project")
        
    else:
        print("❌ Failed to save artifacts")
        sys.exit(1)

if __name__ == "__main__":
    main()
