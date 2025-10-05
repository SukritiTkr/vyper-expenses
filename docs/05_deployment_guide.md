# 🚀 Deployment Guide

## Overview

This guide covers deploying Vyper smart contracts to various blockchain networks, from testnets to mainnets. We'll cover different deployment methods, verification processes, and best practices.

## Prerequisites

### 1. **Development Environment**
- [MetaMask](https://metamask.io/) wallet installed
- [Remix IDE](https://remix.ethereum.org) or local development setup
- Testnet tokens for deployment

### 2. **Required Tools**
- Web3 wallet (MetaMask recommended)
- Contract source code
- Contract ABI (Application Binary Interface)
- Deployment script (optional)

### 3. **Network Access**
- RPC endpoints for target networks
- Block explorer access
- Faucet access for testnet tokens

## Supported Networks

### Testnets

| Network | RPC URL | Faucet | Explorer | Chain ID |
|---------|---------|--------|----------|----------|
| **Celo Alfajores** | `https://alfajores-forno.celo-testnet.org` | [faucet.celo.org](https://faucet.celo.org/) | [explorer.celo.org](https://explorer.celo.org/alfajores) | 44787 |
| **Monad Testnet** | `https://testnet-rpc.monad.xyz` | [faucet.monad.xyz](https://faucet.monad.xyz) | [testnet-explorer.monad.xyz](https://testnet-explorer.monad.xyz) | 41434 |
| **Berachain Testnet** | `https://testnet-rpc.berachain.com` | [faucet.berachain.com](https://faucet.berachain.com) | [testnet-scan.berachain.com](https://testnet-scan.berachain.com) | 80085 |
| **Ethereum Sepolia** | `https://rpc.sepolia.org` | [sepoliafaucet.com](https://sepoliafaucet.com) | [sepolia.etherscan.io](https://sepolia.etherscan.io) | 11155111 |

### Mainnets

| Network | RPC URL | Explorer | Chain ID |
|---------|---------|----------|----------|
| **Ethereum** | `https://rpc.ankr.com/eth` | [etherscan.io](https://etherscan.io) | 1 |
| **Celo** | `https://rpc.ankr.com/celo` | [explorer.celo.org](https://explorer.celo.org) | 42220 |
| **Monad** | `https://rpc.monad.xyz` | [explorer.monad.xyz](https://explorer.monad.xyz) | 1 |
| **Berachain** | `https://rpc.berachain.com` | [scan.berachain.com](https://scan.berachain.com) | 1 |

## Deployment Methods

### Method 1: Remix IDE (Recommended for Beginners)

#### Step 1: Prepare Contract
1. Open [Remix IDE](https://remix.ethereum.org)
2. Create new workspace or open existing
3. Create new file: `ExpenseSplitter.vy`
4. Copy your Vyper contract code

#### Step 2: Compile Contract
1. Go to **Solidity Compiler** tab
2. Select **Vyper Compiler** from dropdown
3. Set compiler version to `0.4.1`
4. Set EVM version to `Cancun`
5. Click **Compile ExpenseSplitter.vy**

#### Step 3: Configure Network
1. Go to **Deploy & Run Transactions** tab
2. Select **Injected Provider - MetaMask**
3. Connect MetaMask to desired network
4. Ensure you have sufficient testnet tokens

#### Step 4: Deploy Contract
1. Click **Deploy** button
2. Confirm transaction in MetaMask
3. Wait for transaction confirmation
4. Copy contract address

#### Step 5: Verify Contract
1. Open block explorer for your network
2. Search for contract address
3. Click **Verify and Publish** (if available)
4. Upload source code and verify

### Method 2: Brownie (Python-based)

#### Installation
```bash
pip install eth-brownie
brownie init
```

#### Configuration
```python
# brownie-config.yaml
networks:
  celo-alfajores:
    host: https://alfajores-forno.celo-testnet.org
    chainid: 44787
    gas_price: 20 gwei
  monad-testnet:
    host: https://testnet-rpc.monad.xyz
    chainid: 41434
    gas_price: 20 gwei
```

#### Deployment Script
```python
# scripts/deploy.py
from brownie import ExpenseSplitter, accounts, network

def main():
    # Load account
    account = accounts.load("deployer")
    
    # Deploy contract
    contract = ExpenseSplitter.deploy({"from": account})
    
    print(f"Contract deployed at: {contract.address}")
    print(f"Transaction hash: {contract.tx.txid}")
    
    return contract
```

#### Deploy
```bash
brownie run scripts/deploy.py --network celo-alfajores
```

### Method 3: Hardhat (JavaScript-based)

#### Installation
```bash
npm init -y
npm install --save-dev hardhat
npx hardhat init
```

#### Configuration
```javascript
// hardhat.config.js
require("@nomiclabs/hardhat-ethers");

module.exports = {
  solidity: {
    version: "0.8.19",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  },
  networks: {
    celoAlfajores: {
      url: "https://alfajores-forno.celo-testnet.org",
      chainId: 44787,
      accounts: [process.env.PRIVATE_KEY]
    },
    monadTestnet: {
      url: "https://testnet-rpc.monad.xyz",
      chainId: 41434,
      accounts: [process.env.PRIVATE_KEY]
    }
  }
};
```

#### Deployment Script
```javascript
// scripts/deploy.js
async function main() {
  const [deployer] = await ethers.getSigners();
  
  console.log("Deploying contracts with account:", deployer.address);
  
  const ExpenseSplitter = await ethers.getContractFactory("ExpenseSplitter");
  const contract = await ExpenseSplitter.deploy();
  
  await contract.deployed();
  
  console.log("Contract deployed to:", contract.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
```

#### Deploy
```bash
npx hardhat run scripts/deploy.js --network celoAlfajores
```

## Contract Verification

### Why Verify Contracts?

- **Transparency**: Source code is publicly visible
- **Trust**: Users can verify contract functionality
- **Debugging**: Easier to debug issues
- **Integration**: Better tool support

### Verification Methods

#### Method 1: Block Explorer Verification

##### Ethereum Sepolia
1. Go to [sepolia.etherscan.io](https://sepolia.etherscan.io)
2. Search for your contract address
3. Click **Contract** tab
4. Click **Verify and Publish**
5. Select **Vyper (Single file)**
6. Upload source code
7. Set compiler version to `0.4.1`
8. Set EVM version to `Cancun`
9. Click **Verify and Publish**

##### Celo Alfajores
1. Go to [explorer.celo.org/alfajores](https://explorer.celo.org/alfajores)
2. Search for your contract address
3. Click **Contract** tab
4. Click **Verify and Publish**
5. Follow similar steps as Ethereum

#### Method 2: Programmatic Verification

##### Brownie
```python
# scripts/verify.py
from brownie import ExpenseSplitter, network

def main():
    contract = ExpenseSplitter[-1]  # Get latest deployment
    
    # Verify contract
    ExpenseSplitter.publish_source(contract)
```

##### Hardhat
```javascript
// scripts/verify.js
async function main() {
  const contractAddress = "0x..."; // Your contract address
  
  await hre.run("verify:verify", {
    address: contractAddress,
    constructorArguments: [],
  });
}
```

## Gas Optimization

### Understanding Gas Costs

#### Storage Operations
- **SSTORE (first time)**: 20,000 gas
- **SSTORE (update)**: 5,000 gas
- **SLOAD**: 800 gas

#### Memory Operations
- **MSTORE**: 3 gas per word
- **MLOAD**: 3 gas per word

#### Computational Operations
- **ADD/SUB**: 3 gas
- **MUL/DIV**: 5 gas
- **SHA3**: 30 gas + 6 gas per word

### Optimization Techniques

#### 1. **Pack Variables**
```vyper
# Pack multiple variables into single storage slot
struct PackedData:
    value1: uint128
    value2: uint128

packed_data: public(PackedData)
```

#### 2. **Use Events Instead of Storage**
```vyper
# Store data in events instead of storage
event DataStored:
    key: indexed(bytes32)
    value: uint256

@external
def store_data(key: bytes32, value: uint256):
    log DataStored(key=key, value=value)
```

#### 3. **Cache Storage Reads**
```vyper
# Cache frequently accessed storage
@external
def optimized_function():
    balance: uint256 = self.balances[msg.sender]  # Cache read
    if balance > 0:
        self.balances[msg.sender] = 0
        send(msg.sender, balance)
```

## Testing Before Deployment

### 1. **Local Testing**
```bash
# Test compilation
vyper contracts/ExpenseSplitter.vy

# Test with Brownie
brownie test

# Test with Hardhat
npx hardhat test
```

### 2. **Testnet Testing**
```bash
# Deploy to testnet
brownie run scripts/deploy.py --network celo-alfajores

# Test all functions
brownie run scripts/test_contract.py --network celo-alfajores
```

### 3. **Gas Estimation**
```python
# Estimate gas costs
contract = ExpenseSplitter.deploy({"from": account})
print(f"Deployment gas: {contract.tx.gas_used}")

# Estimate function calls
tx = contract.record_expense("Test", 1000000000000000000, {"from": account})
print(f"Function gas: {tx.gas_used}")
```

## Security Considerations

### 1. **Pre-Deployment Security**
- [ ] Code review completed
- [ ] Security audit performed
- [ ] Tests cover edge cases
- [ ] Access controls implemented
- [ ] Input validation added

### 2. **Deployment Security**
- [ ] Use secure deployment environment
- [ ] Verify contract source code
- [ ] Monitor deployment transaction
- [ ] Test on testnet first
- [ ] Use multisig for mainnet

### 3. **Post-Deployment Security**
- [ ] Monitor contract activity
- [ ] Set up alerts for suspicious activity
- [ ] Regular security reviews
- [ ] Update documentation
- [ ] Community feedback

## Monitoring and Maintenance

### 1. **Transaction Monitoring**
- Monitor all contract transactions
- Set up alerts for large transactions
- Track gas usage patterns
- Monitor for failed transactions

### 2. **Event Monitoring**
- Monitor contract events
- Set up event-based alerts
- Track important activities
- Analyze usage patterns

### 3. **Performance Monitoring**
- Monitor gas consumption
- Track transaction success rates
- Monitor network congestion
- Optimize based on usage

## Troubleshooting

### Common Issues

#### 1. **Compilation Errors**
```bash
# Check Vyper version
vyper --version

# Check syntax
vyper contracts/ExpenseSplitter.vy
```

#### 2. **Deployment Failures**
- Check gas limit
- Verify network connection
- Ensure sufficient balance
- Check contract size limits

#### 3. **Verification Failures**
- Verify compiler version
- Check EVM version
- Ensure source code matches
- Check constructor arguments

#### 4. **Function Call Failures**
- Check function parameters
- Verify contract state
- Check gas limits
- Monitor for reverts

### Debugging Tools

#### 1. **Remix Debugger**
- Step through transactions
- Inspect state variables
- Monitor gas usage
- Debug failed transactions

#### 2. **Block Explorers**
- View transaction details
- Check contract state
- Monitor events
- Debug failed transactions

#### 3. **Development Tools**
- Brownie console
- Hardhat console
- Web3.py
- ethers.js

## Best Practices

### 1. **Development**
- Write comprehensive tests
- Use version control
- Document code changes
- Follow coding standards

### 2. **Deployment**
- Test on testnets first
- Use secure deployment methods
- Verify contract source code
- Monitor deployment process

### 3. **Operations**
- Monitor contract activity
- Respond to issues quickly
- Maintain documentation
- Regular security reviews

### 4. **Community**
- Share knowledge
- Contribute to open source
- Help other developers
- Participate in discussions

## Resources

### Documentation
- [Vyper Documentation](https://vyper.readthedocs.io/)
- [Ethereum Documentation](https://ethereum.org/en/developers/docs/)
- [Brownie Documentation](https://eth-brownie.readthedocs.io/)
- [Hardhat Documentation](https://hardhat.org/docs)

### Tools
- [Remix IDE](https://remix.ethereum.org)
- [MetaMask](https://metamask.io/)
- [Etherscan](https://etherscan.io/)
- [Celo Explorer](https://explorer.celo.org/)

### Testnets
- [Celo Faucet](https://faucet.celo.org/)
- [Monad Faucet](https://faucet.monad.xyz)
- [Berachain Faucet](https://faucet.berachain.com)
- [Sepolia Faucet](https://sepoliafaucet.com)

---

**Next**: [Workshop Guide](WORKSHOP_GUIDE.md)
