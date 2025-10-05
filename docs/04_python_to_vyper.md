# 🐍➡️🐍 Python to Vyper Migration Guide

## Introduction

Vyper is designed to be familiar to Python developers, but there are important differences when transitioning from traditional Python to blockchain development with Vyper. This guide provides side-by-side comparisons and migration patterns.

## Key Differences Overview

| Aspect | Python | Vyper |
|--------|--------|-------|
| **Execution Environment** | Local/Server | Blockchain (EVM) |
| **Data Persistence** | Files/Database | Blockchain Storage |
| **Cost Model** | Free | Gas-based |
| **Immutability** | Mutable | Immutable after deployment |
| **Type System** | Dynamic | Static |
| **Error Handling** | Exceptions | Assertions |
| **External Calls** | HTTP/APIs | Smart Contract Calls |

## Basic Syntax Comparison

### 1. **Variable Declarations**

#### Python
```python
# Dynamic typing
name = "Alice"
age = 25
balance = 100.50
is_active = True

# Lists and dictionaries
users = ["Alice", "Bob", "Charlie"]
balances = {"Alice": 100, "Bob": 200}
```

#### Vyper
```vyper
# Static typing required
name: String[50] = "Alice"
age: uint256 = 25
balance: uint256 = 100500000000000000000  # 100.5 ETH in wei
is_active: bool = True

# Arrays and mappings
users: DynArray[String[50], 100]
balances: HashMap[String[50], uint256]
```

### 2. **Function Definitions**

#### Python
```python
def calculate_total(amounts):
    """Calculate total of amounts list"""
    total = 0
    for amount in amounts:
        total += amount
    return total

def transfer_balance(from_user, to_user, amount):
    """Transfer balance between users"""
    if balances[from_user] >= amount:
        balances[from_user] -= amount
        balances[to_user] += amount
        return True
    return False
```

#### Vyper
```vyper
@external
@view
def calculate_total(amounts: DynArray[uint256, 100]) -> uint256:
    """Calculate total of amounts list"""
    total: uint256 = 0
    for amount in amounts:
        total += amount
    return total

@external
def transfer_balance(from_user: address, to_user: address, amount: uint256) -> bool:
    """Transfer balance between users"""
    assert self.balances[from_user] >= amount, "Insufficient balance"
    
    self.balances[from_user] -= amount
    self.balances[to_user] += amount
    
    log Transfer(from_user=from_user, to_user=to_user, amount=amount)
    return True
```

### 3. **Class vs Contract Structure**

#### Python Class
```python
class ExpenseSplitter:
    def __init__(self, owner):
        self.owner = owner
        self.total_expenses = 0
        self.participants = []
        self.balances = {}
    
    def add_participant(self, participant):
        if participant not in self.participants:
            self.participants.append(participant)
            self.balances[participant] = 0
            return True
        return False
    
    def record_expense(self, description, amount, payer):
        if payer in self.participants:
            self.total_expenses += amount
            self.balances[payer] += amount
            return True
        return False
    
    def get_balance(self, user):
        return self.balances.get(user, 0)
```

#### Vyper Contract
```vyper
# @version 0.4.1
#pragma evm-version cancun

# State variables (like class attributes)
owner: public(address)
total_expenses: public(uint256)
participants: public(DynArray[address, 100])
balances: public(HashMap[address, uint256])

# Events (like logging)
event ParticipantAdded:
    participant: indexed(address)
    added_by: indexed(address)

event ExpenseRecorded:
    payer: indexed(address)
    description: String[100]
    amount: uint256

# Constructor (like __init__)
@deploy
def __init__():
    self.owner = msg.sender
    self.total_expenses = 0
    self.participants.append(msg.sender)
    self.balances[msg.sender] = 0

# Functions (like class methods)
@external
def add_participant(participant: address):
    assert participant not in self.participants, "Already a participant"
    self.participants.append(participant)
    self.balances[participant] = 0
    log ParticipantAdded(participant=participant, added_by=msg.sender)

@external
def record_expense(description: String[100], amount: uint256):
    assert msg.sender in self.participants, "Not a participant"
    self.total_expenses += amount
    self.balances[msg.sender] += amount
    log ExpenseRecorded(payer=msg.sender, description=description, amount=amount)

@external
@view
def get_balance(user: address) -> uint256:
    return self.balances[user]
```

## Data Structure Migrations

### 1. **Lists to Arrays**

#### Python
```python
# Dynamic lists
users = []
users.append("Alice")
users.append("Bob")
users.remove("Alice")

# List comprehension
even_numbers = [x for x in range(10) if x % 2 == 0]
```

#### Vyper
```vyper
# Fixed-size arrays
users: DynArray[address, 100]  # Max 100 users
users.append(0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6)
users.append(0x1234567890123456789012345678901234567890)

# No list comprehension, use loops
even_numbers: DynArray[uint256, 10]
for i in range(10):
    if i % 2 == 0:
        even_numbers.append(i)
```

### 2. **Dictionaries to Mappings**

#### Python
```python
# Dynamic dictionaries
balances = {}
balances["Alice"] = 100
balances["Bob"] = 200

# Dictionary operations
if "Alice" in balances:
    print(balances["Alice"])

# Dictionary comprehension
squared = {x: x**2 for x in range(5)}
```

#### Vyper
```vyper
# Static mappings
balances: HashMap[address, uint256]
balances[0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6] = 100
balances[0x1234567890123456789012345678901234567890] = 200

# Mapping operations
user_balance: uint256 = self.balances[user_address]  # Returns 0 if not set

# No mapping comprehension, use loops
squared: HashMap[uint256, uint256]
for i in range(5):
    squared[i] = i * i
```

### 3. **Objects to Structs**

#### Python
```python
class User:
    def __init__(self, name, balance, is_active):
        self.name = name
        self.balance = balance
        self.is_active = is_active

# Usage
user = User("Alice", 100, True)
users = {"alice": user}
```

#### Vyper
```vyper
struct User:
    name: String[50]
    balance: uint256
    is_active: bool

# Usage
users: HashMap[address, User]

@external
def create_user(name: String[50]):
    self.users[msg.sender] = User(
        name=name,
        balance=0,
        is_active=True
    )
```

## Control Flow Migrations

### 1. **Conditional Statements**

#### Python
```python
def process_payment(amount, user_balance):
    if amount <= 0:
        raise ValueError("Amount must be positive")
    elif amount > user_balance:
        raise ValueError("Insufficient balance")
    else:
        return user_balance - amount
```

#### Vyper
```vyper
@external
def process_payment(amount: uint256) -> uint256:
    assert amount > 0, "Amount must be positive"
    assert amount <= self.balances[msg.sender], "Insufficient balance"
    
    self.balances[msg.sender] -= amount
    return self.balances[msg.sender]
```

### 2. **Loops**

#### Python
```python
def calculate_totals(amounts):
    total = 0
    for amount in amounts:
        total += amount
    return total

def find_user(users, target):
    for i, user in enumerate(users):
        if user == target:
            return i
    return -1
```

#### Vyper
```vyper
@external
@view
def calculate_totals(amounts: DynArray[uint256, 100]) -> uint256:
    total: uint256 = 0
    for amount in amounts:
        total += amount
    return total

@external
@view
def find_user(target: address) -> uint256:
    for i in range(len(self.participants)):
        if self.participants[i] == target:
            return i
    # Return max uint256 to indicate not found
    return MAX_UINT256
```

### 3. **Error Handling**

#### Python
```python
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return None
```

#### Vyper
```vyper
@external
@view
def safe_divide(a: uint256, b: uint256) -> uint256:
    assert b > 0, "Division by zero"
    return a / b  # Integer division in Vyper
```

## Advanced Patterns

### 1. **Singleton Pattern**

#### Python
```python
class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.data = {}
            self.initialized = True
```

#### Vyper
```vyper
# Vyper contracts are naturally singletons
# Each deployment creates a unique instance
# No need for singleton pattern

# @version 0.4.1
#pragma evm-version cancun

data: HashMap[bytes32, uint256]

@external
def set_data(key: bytes32, value: uint256):
    self.data[key] = value

@external
@view
def get_data(key: bytes32) -> uint256:
    return self.data[key]
```

### 2. **Factory Pattern**

#### Python
```python
class ContractFactory:
    def __init__(self):
        self.contracts = []
    
    def create_contract(self, owner):
        contract = ExpenseSplitter(owner)
        self.contracts.append(contract)
        return contract
    
    def get_contract(self, index):
        return self.contracts[index]
```

#### Vyper
```vyper
# Factory contract
# @version 0.4.1
#pragma evm-version cancun

contracts: DynArray[address, 1000]

@external
def create_contract() -> address:
    # Deploy new contract
    new_contract: address = create_forwarder_to(ExpenseSplitter)
    self.contracts.append(new_contract)
    return new_contract

@external
@view
def get_contract(index: uint256) -> address:
    assert index < len(self.contracts), "Index out of bounds"
    return self.contracts[index]
```

### 3. **Observer Pattern**

#### Python
```python
class Subject:
    def __init__(self):
        self.observers = []
    
    def attach(self, observer):
        self.observers.append(observer)
    
    def notify(self, event):
        for observer in self.observers:
            observer.update(event)

class Observer:
    def update(self, event):
        print(f"Received event: {event}")
```

#### Vyper
```vyper
# Events serve as the observer pattern
# @version 0.4.1
#pragma evm-version cancun

event StateChanged:
    old_value: uint256
    new_value: uint256
    changed_by: indexed(address)

state: public(uint256)

@external
def update_state(new_value: uint256):
    old_value: uint256 = self.state
    self.state = new_value
    log StateChanged(old_value=old_value, new_value=new_value, changed_by=msg.sender)
```

## Common Migration Challenges

### 1. **Type System Differences**

#### Challenge: Dynamic vs Static Typing
```python
# Python - dynamic typing
def process_data(data):
    if isinstance(data, str):
        return data.upper()
    elif isinstance(data, int):
        return data * 2
    else:
        return None
```

#### Solution: Explicit Type Handling
```vyper
# Vyper - static typing
@external
def process_string_data(data: String[100]) -> String[100]:
    # String operations in Vyper
    return data  # Vyper doesn't have .upper() method

@external
def process_uint_data(data: uint256) -> uint256:
    return data * 2
```

### 2. **Error Handling Differences**

#### Challenge: Exceptions vs Assertions
```python
# Python - exceptions
def transfer(amount):
    try:
        if amount <= 0:
            raise ValueError("Invalid amount")
        # Transfer logic
        return True
    except ValueError as e:
        print(f"Error: {e}")
        return False
```

#### Solution: Assertions
```vyper
# Vyper - assertions
@external
def transfer(amount: uint256) -> bool:
    assert amount > 0, "Invalid amount"
    # Transfer logic
    return True  # If assertion fails, transaction reverts
```

### 3. **State Management**

#### Challenge: Mutable vs Immutable State
```python
# Python - mutable state
class Counter:
    def __init__(self):
        self.count = 0
    
    def increment(self):
        self.count += 1
        return self.count
```

#### Solution: Blockchain State
```vyper
# Vyper - immutable contract, mutable state
# @version 0.4.1
#pragma evm-version cancun

count: public(uint256)

@external
def increment() -> uint256:
    self.count += 1
    return self.count
```

## Best Practices for Migration

### 1. **Start Simple**
- Begin with basic data structures
- Migrate simple functions first
- Test each component thoroughly

### 2. **Understand Gas Costs**
- Storage operations are expensive
- Use events instead of storage when possible
- Optimize for gas efficiency

### 3. **Security First**
- Validate all inputs
- Use assertions for error handling
- Follow security best practices

### 4. **Test Thoroughly**
- Test on testnets first
- Use comprehensive test suites
- Test edge cases and error conditions

### 5. **Document Changes**
- Document migration decisions
- Explain Vyper-specific patterns
- Maintain migration notes

## Migration Checklist

### Pre-Migration
- [ ] Understand Vyper syntax and features
- [ ] Identify core functionality to migrate
- [ ] Plan data structure changes
- [ ] Design contract architecture

### During Migration
- [ ] Migrate data structures first
- [ ] Convert functions one by one
- [ ] Handle error cases properly
- [ ] Add necessary events
- [ ] Test each component

### Post-Migration
- [ ] Test on testnet
- [ ] Optimize for gas usage
- [ ] Security audit
- [ ] Documentation update
- [ ] Deployment to mainnet

## Tools and Resources

### Development Tools
- [Remix IDE](https://remix.ethereum.org) - Browser-based development
- [Brownie](https://eth-brownie.readthedocs.io/) - Python-based framework
- [Hardhat](https://hardhat.org/) - JavaScript-based framework

### Testing Tools
- [pytest](https://pytest.org/) - Python testing framework
- [Brownie testing](https://eth-brownie.readthedocs.io/en/stable/tests.html) - Vyper testing
- [Hardhat testing](https://hardhat.org/tutorial/testing-contracts.html) - JavaScript testing

### Documentation
- [Vyper Documentation](https://vyper.readthedocs.io/)
- [Ethereum Documentation](https://ethereum.org/en/developers/docs/)
- [Smart Contract Best Practices](https://consensys.github.io/smart-contract-best-practices/)

## Conclusion

Migrating from Python to Vyper requires understanding the fundamental differences between traditional programming and blockchain development. Key areas to focus on:

1. **Type System**: Embrace static typing
2. **State Management**: Understand blockchain storage
3. **Error Handling**: Use assertions instead of exceptions
4. **Gas Optimization**: Consider computational costs
5. **Security**: Implement proper access controls

With practice and understanding of these concepts, Python developers can successfully transition to Vyper and build secure, efficient smart contracts.

---

**Next**: [Deployment Guide](05_deployment_guide.md)
