# 🐍 Vyper Guide

## What is Vyper?

Vyper is a contract-oriented, pythonic programming language that targets the Ethereum Virtual Machine (EVM). It was designed to be more secure, readable, and auditable than Solidity.

### Key Features

- **Python-like Syntax**: Familiar to Python developers
- **Security-focused**: Designed to prevent common vulnerabilities
- **Readable**: Emphasizes code clarity and simplicity
- **Gas Efficient**: Optimized for gas consumption
- **Type Safe**: Strong typing system prevents errors

## Why Choose Vyper?

### Advantages

#### 1. **Security**
- Prevents common vulnerabilities by design
- No function overloading (reduces complexity)
- No inheritance (simplifies code analysis)
- Explicit type conversions

#### 2. **Readability**
- Python-like syntax is easy to read
- Clear and explicit code structure
- Minimal language features
- Self-documenting code

#### 3. **Simplicity**
- Fewer language features to learn
- No complex inheritance hierarchies
- Straightforward control flow
- Predictable behavior

#### 4. **Gas Efficiency**
- Optimized bytecode generation
- Efficient storage patterns
- Minimal overhead
- Predictable gas costs

### Disadvantages

#### 1. **Limited Features**
- No inheritance
- No function overloading
- Limited library ecosystem
- Fewer development tools

#### 2. **Smaller Community**
- Fewer developers
- Limited resources
- Smaller ecosystem
- Less community support

#### 3. **Learning Curve**
- Different from Solidity
- Limited examples
- Fewer tutorials
- Smaller documentation

## Vyper vs Solidity

| Feature | Vyper | Solidity |
|---------|-------|----------|
| **Syntax** | Python-like | JavaScript-like |
| **Inheritance** | No | Yes |
| **Function Overloading** | No | Yes |
| **Type System** | Explicit | Implicit |
| **Security** | Built-in | Manual |
| **Readability** | High | Medium |
| **Ecosystem** | Small | Large |
| **Learning Curve** | Medium | Medium |

## Getting Started with Vyper

### Installation

#### 1. **Using pip**
```bash
pip install vyper
```

#### 2. **Using Docker**
```bash
docker run -v $(pwd):/code vyperlang/vyper:latest
```

#### 3. **Using Remix IDE**
- Visit [remix.ethereum.org](https://remix.ethereum.org)
- Select Vyper compiler
- Start coding immediately

### Hello World Contract

```vyper
# @version 0.4.1
#pragma evm-version cancun

# Simple greeting contract
greeting: public(String[100])

@deploy
def __init__():
    self.greeting = "Hello, Vyper!"

@external
def set_greeting(new_greeting: String[100]):
    self.greeting = new_greeting

@external
@view
def get_greeting() -> String[100]:
    return self.greeting
```

## Vyper Syntax

### Basic Structure

```vyper
# @version 0.4.1
#pragma evm-version cancun

# State variables
owner: public(address)
balance: public(uint256)

# Events
event Transfer:
    from: indexed(address)
    to: indexed(address)
    amount: uint256

# Constructor
@deploy
def __init__():
    self.owner = msg.sender
    self.balance = 0

# Functions
@external
def deposit():
    self.balance += msg.value

@external
@view
def get_balance() -> uint256:
    return self.balance
```

### Data Types

#### 1. **Basic Types**
```vyper
# Integers
count: uint256 = 100
small_count: uint8 = 255
negative: int256 = -50

# Booleans
is_active: bool = True
is_complete: bool = False

# Addresses
user: address = 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6
zero_address: address = empty(address)

# Bytes
data: bytes32 = 0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
short_data: bytes4 = 0x12345678

# Strings
name: String[50] = "Vyper Contract"
description: String[200] = "A simple Vyper contract"
```

#### 2. **Complex Types**
```vyper
# Arrays
numbers: DynArray[uint256, 100]
fixed_array: uint256[10]

# Mappings
balances: HashMap[address, uint256]
permissions: HashMap[address, bool]

# Structs
struct User:
    name: String[50]
    balance: uint256
    is_active: bool

users: HashMap[address, User]
```

### Functions

#### 1. **Function Decorators**
```vyper
@external          # Can be called from outside
@view             # Read-only, no gas cost
@payable          # Can receive Ether
@deploy           # Constructor function
```

#### 2. **Function Types**
```vyper
# External function (can be called from outside)
@external
def external_function():
    pass

# Public function (can be called internally or externally)
@external
def public_function():
    pass

# Internal function (only within contract)
@internal
def internal_function():
    pass

# Private function (only within same contract)
@internal
def private_function():
    pass
```

#### 3. **View Functions**
```vyper
@external
@view
def get_balance() -> uint256:
    return self.balance

@external
@view
def get_user_info(user: address) -> (String[50], uint256, bool):
    return (self.users[user].name, self.users[user].balance, self.users[user].is_active)
```

#### 4. **Payable Functions**
```vyper
@external
@payable
def deposit():
    self.balance += msg.value
    log Deposit(user=msg.sender, amount=msg.value)

event Deposit:
    user: indexed(address)
    amount: uint256
```

### Control Flow

#### 1. **Conditional Statements**
```vyper
@external
def conditional_example(amount: uint256):
    if amount > 100:
        self.balance += amount
    elif amount > 50:
        self.balance += amount / 2
    else:
        self.balance += amount / 4
```

#### 2. **Loops**
```vyper
@external
def loop_example():
    # For loop
    for i in range(10):
        self.numbers.append(i)
    
    # While loop
    i: uint256 = 0
    while i < 10:
        self.numbers.append(i)
        i += 1
```

#### 3. **Assertions**
```vyper
@external
def assertion_example(amount: uint256):
    assert amount > 0, "Amount must be positive"
    assert self.balance >= amount, "Insufficient balance"
    assert msg.sender == self.owner, "Only owner can call this"
```

### Events

#### 1. **Event Declaration**
```vyper
event Transfer:
    from: indexed(address)
    to: indexed(address)
    amount: uint256

event UserRegistered:
    user: indexed(address)
    name: String[50]
    timestamp: uint256
```

#### 2. **Event Emission**
```vyper
@external
def transfer(to: address, amount: uint256):
    assert self.balances[msg.sender] >= amount, "Insufficient balance"
    
    self.balances[msg.sender] -= amount
    self.balances[to] += amount
    
    log Transfer(from=msg.sender, to=to, amount=amount)
```

### Error Handling

#### 1. **Assertions**
```vyper
@external
def safe_function(amount: uint256):
    assert amount > 0, "Amount must be positive"
    assert amount <= MAX_AMOUNT, "Amount too large"
    assert self.balance >= amount, "Insufficient balance"
    
    # Function logic here
```

#### 2. **Custom Errors**
```vyper
# Vyper 0.4.1+ supports custom errors
error InsufficientBalance()
error UnauthorizedAccess()

@external
def function_with_errors(amount: uint256):
    if self.balance < amount:
        raise InsufficientBalance()
    
    if msg.sender != self.owner:
        raise UnauthorizedAccess()
    
    # Function logic here
```

## Advanced Vyper Features

### 1. **Structs**
```vyper
struct User:
    name: String[50]
    balance: uint256
    is_active: bool
    created_at: uint256

users: HashMap[address, User]

@external
def create_user(name: String[50]):
    self.users[msg.sender] = User(
        name=name,
        balance=0,
        is_active=True,
        created_at=block.timestamp
    )
```

### 2. **Enums**
```vyper
enum Status:
    PENDING
    ACTIVE
    COMPLETED
    CANCELLED

status: public(Status)

@external
def update_status(new_status: Status):
    self.status = new_status
```

### 3. **Constants**
```vyper
# Constants are computed at compile time
MAX_USERS: constant(uint256) = 1000
MIN_DEPOSIT: constant(uint256) = 1000000000000000000  # 1 ETH in wei
OWNER_ROLE: constant(bytes32) = keccak256("OWNER_ROLE")
```

### 4. **Immutables**
```vyper
# Immutables are set once in constructor
owner: immutable(address)
max_supply: immutable(uint256)

@deploy
def __init__(_max_supply: uint256):
    owner = msg.sender
    max_supply = _max_supply
```

## Gas Optimization

### 1. **Storage Optimization**
```vyper
# Pack variables into single storage slot
struct PackedData:
    value1: uint128
    value2: uint128

packed_data: public(PackedData)
```

### 2. **Memory vs Storage**
```vyper
@external
def optimized_function():
    # Cache storage reads
    balance: uint256 = self.balances[msg.sender]
    
    if balance > 0:
        # Use cached value
        self.balances[msg.sender] = 0
        send(msg.sender, balance)
```

### 3. **Event Optimization**
```vyper
# Use indexed parameters for filtering
event Transfer:
    from: indexed(address)
    to: indexed(address)
    amount: uint256
```

## Security Best Practices

### 1. **Input Validation**
```vyper
@external
def safe_function(amount: uint256, recipient: address):
    assert amount > 0, "Amount must be positive"
    assert recipient != empty(address), "Invalid recipient"
    assert self.balances[msg.sender] >= amount, "Insufficient balance"
    
    # Function logic here
```

### 2. **Access Control**
```vyper
@external
def admin_function():
    assert msg.sender == self.owner, "Only owner can call this"
    # Function logic here
```

### 3. **Reentrancy Protection**
```vyper
@external
def secure_withdraw():
    amount: uint256 = self.balances[msg.sender]
    assert amount > 0, "No funds to withdraw"
    
    # Update state first
    self.balances[msg.sender] = 0
    
    # External call last
    send(msg.sender, amount)
```

### 4. **Integer Overflow Protection**
```vyper
# Vyper 0.4.1+ has automatic overflow protection
@external
def safe_arithmetic(a: uint256, b: uint256):
    # This is safe in Vyper 0.4.1+
    result: uint256 = a + b
    return result
```

## Testing Vyper Contracts

### 1. **Using Remix IDE**
- Write contract code
- Compile with Vyper compiler
- Deploy to testnet
- Test functions interactively

### 2. **Using Brownie**
```python
# test_contract.py
import brownie
from brownie import Contract

def test_contract():
    # Deploy contract
    contract = Contract.deploy({"from": accounts[0]})
    
    # Test functions
    assert contract.get_balance() == 0
    
    # Test with value
    contract.deposit({"from": accounts[0], "value": "1 ether"})
    assert contract.get_balance() == "1 ether"
```

### 3. **Using Hardhat**
```javascript
// test/Contract.test.js
const { expect } = require("chai");

describe("Contract", function () {
  it("Should return the right balance", async function () {
    const Contract = await ethers.getContractFactory("Contract");
    const contract = await Contract.deploy();
    
    expect(await contract.getBalance()).to.equal(0);
  });
});
```

## Deployment

### 1. **Using Remix IDE**
- Compile contract
- Deploy to testnet
- Verify source code
- Interact with contract

### 2. **Using Brownie**
```python
# deploy.py
from brownie import Contract, accounts

def main():
    account = accounts.load("deployer")
    contract = Contract.deploy({"from": account})
    print(f"Contract deployed at: {contract.address}")
```

### 3. **Using Hardhat**
```javascript
// scripts/deploy.js
async function main() {
  const Contract = await ethers.getContractFactory("Contract");
  const contract = await Contract.deploy();
  
  console.log("Contract deployed to:", contract.address);
}
```

## Common Patterns

### 1. **Ownable Contract**
```vyper
owner: public(address)

@deploy
def __init__():
    self.owner = msg.sender

@external
def transfer_ownership(new_owner: address):
    assert msg.sender == self.owner, "Only owner"
    assert new_owner != empty(address), "Invalid address"
    self.owner = new_owner
```

### 2. **Pausable Contract**
```vyper
paused: public(bool)

@external
def pause():
    assert msg.sender == self.owner, "Only owner"
    self.paused = True

@external
def unpause():
    assert msg.sender == self.owner, "Only owner"
    self.paused = False

@external
def protected_function():
    assert not self.paused, "Contract is paused"
    # Function logic here
```

### 3. **Pull Payment Pattern**
```vyper
balances: HashMap[address, uint256]

@external
@payable
def deposit():
    self.balances[msg.sender] += msg.value

@external
def withdraw():
    amount: uint256 = self.balances[msg.sender]
    assert amount > 0, "No funds to withdraw"
    
    self.balances[msg.sender] = 0
    send(msg.sender, amount)
```

## Resources

### Documentation
- [Vyper Documentation](https://vyper.readthedocs.io/)
- [Vyper by Example](https://vyper.readthedocs.io/en/stable/vyper-by-example.html)
- [Vyper Style Guide](https://vyper.readthedocs.io/en/stable/style-guide.html)

### Tools
- [Remix IDE](https://remix.ethereum.org)
- [Brownie](https://eth-brownie.readthedocs.io/)
- [Hardhat](https://hardhat.org/)

### Examples
- [Vyper Examples](https://github.com/vyperlang/vyper/tree/master/examples)
- [OpenZeppelin Vyper](https://github.com/OpenZeppelin/openzeppelin-contracts-vyper)

---

**Next**: [Python to Vyper Guide](04_python_to_vyper.md)
