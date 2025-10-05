# 🔗 Smart Contracts Guide

## What are Smart Contracts?

Smart contracts are self-executing programs that run on blockchain networks. They automatically execute when predetermined conditions are met, without requiring intermediaries or manual intervention.

### Key Features

- **Autonomous**: Execute automatically when conditions are met
- **Transparent**: Code is visible to all network participants
- **Immutable**: Cannot be changed once deployed
- **Trustless**: No need for third-party intermediaries
- **Programmable**: Can implement complex business logic

## How Smart Contracts Work

### 1. **Code Writing**
- Developers write smart contract code in languages like Solidity, Vyper, or Rust
- Code defines the contract's behavior and state

### 2. **Compilation**
- High-level code is compiled to bytecode
- Bytecode is what the EVM actually executes

### 3. **Deployment**
- Contract is deployed to the blockchain network
- Deployment creates a unique contract address
- Contract becomes part of the blockchain's state

### 4. **Interaction**
- Users interact with contracts by sending transactions
- Transactions trigger contract functions
- Contract state changes are recorded on the blockchain

### 5. **Execution**
- EVM executes the contract code
- Gas is consumed for computational work
- Results are recorded on the blockchain

## Smart Contract Architecture

### State Variables
- **Storage**: Persistent data stored on the blockchain
- **Memory**: Temporary data during function execution
- **Stack**: Local variables and function parameters

### Functions
- **External**: Can be called from outside the contract
- **Public**: Can be called internally or externally
- **Internal**: Can only be called from within the contract
- **Private**: Can only be called from the same contract

### Events
- **Logging**: Record important contract activities
- **Indexed Parameters**: Enable efficient filtering
- **Gas Efficient**: Cheaper than storing data in state

## Smart Contract Lifecycle

### Development Phase
1. **Requirements Analysis**: Define contract functionality
2. **Design**: Plan contract architecture and data structures
3. **Coding**: Write contract code in chosen language
4. **Testing**: Test contract functionality and edge cases
5. **Security Review**: Audit for vulnerabilities

### Deployment Phase
1. **Compilation**: Convert code to bytecode
2. **Network Selection**: Choose mainnet or testnet
3. **Gas Estimation**: Calculate deployment costs
4. **Deployment**: Send transaction to create contract
5. **Verification**: Verify contract source code

### Operation Phase
1. **User Interaction**: Users call contract functions
2. **State Changes**: Contract state updates
3. **Event Emission**: Important events are logged
4. **Gas Consumption**: Computational costs are paid
5. **Persistence**: Changes are permanent

## Smart Contract Languages

### Solidity
- **Most Popular**: Widely used in Ethereum ecosystem
- **JavaScript-like**: Familiar syntax for web developers
- **Mature**: Well-established with extensive tooling
- **Complex**: Can be complex for beginners

### Vyper
- **Python-like**: Familiar syntax for Python developers
- **Security-focused**: Designed to prevent common vulnerabilities
- **Readable**: Emphasizes code readability
- **Limited**: Fewer features than Solidity

### Rust (for other chains)
- **Performance**: High-performance language
- **Memory Safety**: Prevents common memory errors
- **Growing**: Increasing adoption in blockchain
- **Complex**: Steeper learning curve

## Smart Contract Patterns

### Access Control
```vyper
# Only owner can call this function
@external
def admin_function():
    assert msg.sender == self.owner, "Only owner can call this"
    # Function logic here
```

### State Machine
```vyper
# Contract with different states
enum State:
    PENDING
    ACTIVE
    COMPLETED

state: public(State)

@external
def activate():
    assert self.state == State.PENDING, "Must be pending"
    self.state = State.ACTIVE
```

### Pull Payment
```vyper
# Users withdraw their own funds
@external
def withdraw():
    amount: uint256 = self.balances[msg.sender]
    assert amount > 0, "No funds to withdraw"
    self.balances[msg.sender] = 0
    send(msg.sender, amount)
```

### Circuit Breaker
```vyper
# Emergency stop mechanism
paused: public(bool)

@external
def emergency_stop():
    assert msg.sender == self.owner, "Only owner"
    self.paused = True

@external
def resume():
    assert msg.sender == self.owner, "Only owner"
    self.paused = False
```

## Smart Contract Security

### Common Vulnerabilities

#### 1. **Reentrancy**
- **Problem**: External calls before state updates
- **Solution**: Update state before external calls
- **Example**: Check-Effects-Interactions pattern

#### 2. **Integer Overflow/Underflow**
- **Problem**: Arithmetic operations exceed type limits
- **Solution**: Use safe math libraries or Vyper's built-in protection
- **Example**: Vyper 0.4.1+ has automatic overflow protection

#### 3. **Access Control**
- **Problem**: Unauthorized access to sensitive functions
- **Solution**: Implement proper access control mechanisms
- **Example**: Owner-only functions, role-based access

#### 4. **Front-running**
- **Problem**: Transactions can be seen before execution
- **Solution**: Use commit-reveal schemes or private mempools
- **Example**: Vickrey auctions, sealed bids

#### 5. **Denial of Service**
- **Problem**: Contract can be made unusable
- **Solution**: Implement circuit breakers and gas limits
- **Example**: Emergency stop functions

### Security Best Practices

#### 1. **Input Validation**
```vyper
@external
def safe_function(amount: uint256):
    assert amount > 0, "Amount must be positive"
    assert amount <= MAX_AMOUNT, "Amount too large"
    # Function logic here
```

#### 2. **Access Control**
```vyper
@external
def admin_function():
    assert msg.sender == self.owner, "Only owner can call this"
    # Function logic here
```

#### 3. **State Updates**
```vyper
@external
def secure_transfer(recipient: address, amount: uint256):
    # Check conditions
    assert self.balances[msg.sender] >= amount, "Insufficient balance"
    
    # Update state first
    self.balances[msg.sender] -= amount
    self.balances[recipient] += amount
    
    # External interaction last
    log Transfer(sender=msg.sender, recipient=recipient, amount=amount)
```

#### 4. **Event Logging**
```vyper
event Transfer:
    sender: indexed(address)
    recipient: indexed(address)
    amount: uint256

@external
def transfer(recipient: address, amount: uint256):
    # Function logic
    log Transfer(sender=msg.sender, recipient=recipient, amount=amount)
```

## Gas Optimization

### Gas Costs by Operation

#### Storage Operations
- **SSTORE**: 20,000 gas (first time), 5,000 gas (update)
- **SLOAD**: 800 gas (read from storage)
- **SSTORE to zero**: 5,000 gas (refund)

#### Memory Operations
- **MSTORE**: 3 gas per word
- **MLOAD**: 3 gas per word
- **Memory expansion**: Additional gas for new memory

#### Computational Operations
- **ADD/SUB**: 3 gas
- **MUL/DIV**: 5 gas
- **SHA3**: 30 gas + 6 gas per word
- **CALL**: 700 gas + additional costs

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
        # Use cached value
        self.balances[msg.sender] = 0
        send(msg.sender, balance)
```

#### 4. **Use View Functions**
```vyper
# View functions don't cost gas for callers
@external
@view
def get_balance(user: address) -> uint256:
    return self.balances[user]
```

## Testing Smart Contracts

### Testing Strategies

#### 1. **Unit Testing**
- Test individual functions
- Mock external dependencies
- Test edge cases and error conditions

#### 2. **Integration Testing**
- Test contract interactions
- Test with real blockchain state
- Test gas consumption

#### 3. **Security Testing**
- Static analysis tools
- Dynamic analysis tools
- Manual code review

### Testing Tools

#### 1. **Remix IDE**
- Browser-based development environment
- Built-in compiler and debugger
- Easy deployment and testing

#### 2. **Hardhat**
- Development environment for Ethereum
- Testing framework and deployment tools
- Plugin ecosystem

#### 3. **Truffle**
- Development framework
- Testing suite and deployment tools
- Asset pipeline

## Deployment Strategies

### 1. **Testnet Deployment**
- Deploy to testnets first
- Test all functionality
- Verify contract behavior

### 2. **Mainnet Deployment**
- Deploy to mainnet
- Verify contract source code
- Monitor contract activity

### 3. **Upgradeable Contracts**
- Use proxy patterns
- Implement upgrade mechanisms
- Maintain backward compatibility

## Monitoring and Maintenance

### 1. **Event Monitoring**
- Monitor contract events
- Set up alerts for important activities
- Track contract usage

### 2. **Security Monitoring**
- Monitor for suspicious activity
- Track gas usage patterns
- Watch for potential attacks

### 3. **Performance Monitoring**
- Monitor transaction success rates
- Track gas consumption
- Optimize based on usage patterns

## Common Use Cases

### 1. **Token Contracts**
- ERC-20 tokens
- NFT contracts
- Utility tokens

### 2. **DeFi Protocols**
- Lending platforms
- Decentralized exchanges
- Yield farming

### 3. **Governance**
- Voting systems
- Proposal mechanisms
- Treasury management

### 4. **Supply Chain**
- Product tracking
- Authenticity verification
- Compliance monitoring

## Best Practices Summary

### Development
- Write clear, readable code
- Implement comprehensive testing
- Follow security best practices
- Use established patterns

### Deployment
- Test thoroughly on testnets
- Verify contract source code
- Monitor deployment process
- Document contract functionality

### Operation
- Monitor contract activity
- Respond to security issues
- Optimize based on usage
- Maintain documentation

## Resources

### Documentation
- [Vyper Documentation](https://vyper.readthedocs.io/)
- [Ethereum Smart Contract Best Practices](https://consensys.github.io/smart-contract-best-practices/)
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts/)

### Tools
- [Remix IDE](https://remix.ethereum.org)
- [Hardhat](https://hardhat.org/)
- [Truffle](https://trufflesuite.com/)

### Security
- [MythX](https://mythx.io/)
- [Slither](https://github.com/crytic/slither)
- [Echidna](https://github.com/crytic/echidna)

---

**Next**: [Vyper Guide](03_vyper_guide.md)
