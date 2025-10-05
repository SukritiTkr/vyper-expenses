# 💡 Vyper Development Hints

## General Vyper Tips

### 1. **Type System**
```vyper
# Always specify types explicitly
amount: uint256 = 100
name: String[50] = "Alice"
is_active: bool = True
user_address: address = 0x1234...
```

### 2. **Function Decorators**
```vyper
@external          # Can be called from outside
@view             # Read-only, no gas cost
@payable          # Can receive Ether
@deploy           # Constructor function
```

### 3. **Common Patterns**

#### Access Control
```vyper
@external
def admin_function():
    assert msg.sender == self.owner, "Only owner can call this"
    # Function logic here
```

#### Input Validation
```vyper
@external
def safe_function(amount: uint256):
    assert amount > 0, "Amount must be positive"
    assert amount <= MAX_AMOUNT, "Amount too large"
    # Function logic here
```

#### Check-Effects-Interactions Pattern
```vyper
@external
def secure_transfer(recipient: address, amount: uint256):
    # 1. CHECK: Validate inputs
    assert amount > 0, "Invalid amount"
    assert self.balances[msg.sender] >= amount, "Insufficient balance"
    
    # 2. EFFECTS: Update state first
    self.balances[msg.sender] -= amount
    self.balances[recipient] += amount
    
    # 3. INTERACTIONS: External calls last
    log Transfer(sender=msg.sender, recipient=recipient, amount=amount)
```

## ExpenseSplitter Specific Hints

### 1. **HashMap Usage**
```vyper
# Declare
balances: public(HashMap[address, uint256])

# Read
user_balance: uint256 = self.balances[user_address]

# Write
self.balances[user_address] = new_balance

# Update
self.balances[user_address] += amount
```

### 2. **DynArray Operations**
```vyper
# Declare with max size
participants: public(DynArray[address, 100])

# Add element
self.participants.append(new_address)

# Get length
count: uint256 = len(self.participants)

# Access element
first_participant: address = self.participants[0]

# Loop through
for participant: address in self.participants:
    # Do something with participant
    pass
```

### 3. **Event Logging**
```vyper
# Declare event
event ExpenseRecorded:
    user: indexed(address)
    description: String[100]
    amount: uint256
    timestamp: uint256

# Emit event
log ExpenseRecorded(
    user=msg.sender,
    description=description,
    amount=amount,
    timestamp=block.timestamp
)
```

### 4. **Payable Functions**
```vyper
@external
@payable
def contribute():
    # msg.value contains the Ether sent
    assert msg.value > 0, "Must send some value"
    # Ether is automatically added to contract balance
    log PaymentReceived(from_user=msg.sender, amount=msg.value)
```

### 5. **Sending Ether**
```vyper
@external
def withdraw(amount: uint256):
    assert self.balance >= amount, "Insufficient contract balance"
    # Send Ether to caller
    send(msg.sender, amount)
```

## Common Mistakes to Avoid

### 1. **Integer Overflow/Underflow**
```vyper
# BAD: No overflow protection
total = total + amount

# GOOD: Vyper 0.4.1 has built-in overflow protection
total += amount  # Safe in Vyper 0.4.1+
```

### 2. **Reentrancy Attacks**
```vyper
# BAD: External call before state update
send(recipient, amount)
self.balances[msg.sender] -= amount

# GOOD: Update state first
self.balances[msg.sender] -= amount
send(recipient, amount)
```

### 3. **Missing Input Validation**
```vyper
# BAD: No validation
def transfer(recipient: address, amount: uint256):
    self.balances[msg.sender] -= amount

# GOOD: Validate inputs
def transfer(recipient: address, amount: uint256):
    assert amount > 0, "Amount must be positive"
    assert recipient != empty(address), "Invalid recipient"
    assert self.balances[msg.sender] >= amount, "Insufficient balance"
    self.balances[msg.sender] -= amount
```

### 4. **Gas Optimization**
```vyper
# BAD: Multiple storage reads
if self.balances[user1] > self.balances[user2]:
    return self.balances[user1]

# GOOD: Cache storage reads
balance1: uint256 = self.balances[user1]
balance2: uint256 = self.balances[user2]
if balance1 > balance2:
    return balance1
```

## Debugging Tips

### 1. **Use Events for Debugging**
```vyper
event Debug:
    message: String[100]
    value: uint256

# Emit debug events
log Debug(message="Function called", value=amount)
```

### 2. **Check Contract Balance**
```vyper
@external
@view
def get_balance() -> uint256:
    return self.balance
```

### 3. **Validate State Changes**
```vyper
@external
@view
def get_state() -> (uint256, uint256, uint256):
    return (self.total_expenses, self.expense_count, len(self.participants))
```

## Testing Checklist

Before deploying, verify:
- [ ] All functions have proper access control
- [ ] Input validation is comprehensive
- [ ] State updates follow check-effects-interactions pattern
- [ ] Events are emitted for important actions
- [ ] Edge cases are handled (zero values, empty arrays)
- [ ] Gas optimization is considered
- [ ] Contract balance is properly managed

## Resources

- [Vyper Documentation](https://vyper.readthedocs.io/)
- [Vyper Examples](https://github.com/vyperlang/vyper/tree/master/examples)
- [Ethereum Smart Contract Best Practices](https://consensys.github.io/smart-contract-best-practices/)
- [Remix IDE](https://remix.ethereum.org)
