# 🏋️ Vyper Development Exercises

## Exercise 1: Basic State Management

### Task
Complete the `record_expense` function in the template.

### Requirements
1. Validate that `amount` is greater than 0
2. Add `amount` to `total_expenses`
3. Increment `expense_count` by 1
4. Add `amount` to the caller's balance in `balances` mapping
5. Emit the `ExpenseRecorded` event

### Hints
- Use `assert` for validation
- `msg.sender` is the caller's address
- `block.timestamp` gives current time
- Event parameters must match the event declaration

### Expected Behavior
```vyper
# Input: record_expense("Coffee", 5000000000000000000)  # 5 ETH in wei
# Should: Update totals, increment counter, update balance, emit event
```

## Exercise 2: Access Control

### Task
Complete the `add_participant` function.

### Requirements
1. Only the contract owner can add participants
2. Validate the new participant address is not zero
3. Check that the participant isn't already in the list
4. Add the participant to the `participants` array
5. Emit the `ParticipantAdded` event

### Hints
- Use `self.owner` for owner check
- `empty(address)` represents zero address
- Loop through `self.participants` to check duplicates
- Use `append()` to add to dynamic array

### Expected Behavior
```vyper
# Input: add_participant(0x1234...)
# Should: Add to participants array, emit event
# Error: If caller is not owner or address is invalid
```

## Exercise 3: Payment Handling

### Task
Complete the `contribute` function.

### Requirements
1. Validate that some Ether was sent (`msg.value > 0`)
2. Emit the `PaymentReceived` event

### Hints
- `@payable` decorator allows receiving Ether
- `msg.value` contains the amount sent
- Ether is automatically added to contract balance

### Expected Behavior
```vyper
# Input: contribute() with 1 ETH
# Should: Accept payment, emit event
# Error: If no Ether sent
```

## Exercise 4: Fund Settlement

### Task
Complete the `settle_expenses` function.

### Requirements
1. Get the amount owed by the caller
2. Validate they have expenses to settle
3. Check contract has enough balance
4. Reset the caller's balance to 0 (security)
5. Send the owed amount to the caller
6. Emit the `ExpenseSettled` event

### Hints
- Use `self.balances[msg.sender]` for amount owed
- Use `self.balance` for contract balance
- Use `send()` to transfer Ether
- Reset balance BEFORE sending (security pattern)

### Expected Behavior
```vyper
# Input: settle_expenses()
# Should: Transfer owed amount, reset balance, emit event
# Error: If no expenses or insufficient contract balance
```

## Exercise 5: View Functions

### Task
Complete the view functions.

### Requirements
1. `get_participant_count()`: Return length of participants array
2. `calculate_equal_split()`: Return total_expenses / participant_count
3. `get_my_balance()`: Return caller's balance
4. `check_contract_balance()`: Return contract's Ether balance

### Hints
- `@view` functions are read-only
- Handle division by zero in `calculate_equal_split`
- Use `len()` for array length
- Use `self.balance` for contract balance

### Expected Behavior
```vyper
# get_participant_count() -> 3
# calculate_equal_split() -> 1000000000000000000  # 1 ETH per person
# get_my_balance() -> 5000000000000000000  # 5 ETH
# check_contract_balance() -> 10000000000000000000  # 10 ETH
```

## Exercise 6: Admin Functions

### Task
Complete the `emergency_withdraw` function.

### Requirements
1. Only owner can call this function
2. Get the contract's total balance
3. Send all funds to the owner

### Hints
- Use `self.owner` for access control
- Use `self.balance` for contract balance
- Use `send()` to transfer Ether

### Expected Behavior
```vyper
# Input: emergency_withdraw() by owner
# Should: Transfer all contract funds to owner
# Error: If caller is not owner
```

## Advanced Exercises

### Exercise 7: Gas Optimization
Optimize the `record_expense` function to minimize gas usage.

**Tips:**
- Cache frequently accessed storage variables
- Minimize storage writes
- Use efficient data types

### Exercise 8: Error Handling
Add comprehensive error handling to all functions.

**Tips:**
- Validate all inputs
- Check for edge cases
- Provide clear error messages

### Exercise 9: Event Optimization
Optimize event emissions for gas efficiency.

**Tips:**
- Use `indexed` for frequently queried parameters
- Minimize event parameters
- Group related events

## Testing Your Solutions

### 1. **Compilation Test**
```bash
# In Remix IDE
1. Paste your code
2. Select Vyper compiler
3. Set version to 0.4.1
4. Click Compile
5. Check for errors
```

### 2. **Deployment Test**
```bash
# In Remix IDE
1. Go to Deploy & Run tab
2. Select Injected Provider
3. Connect MetaMask
4. Deploy contract
5. Check deployment success
```

### 3. **Function Test**
```bash
# Test each function
1. Call record_expense with valid inputs
2. Check state changes
3. Verify events emitted
4. Test error conditions
```

### 4. **Integration Test**
```bash
# Test complete workflow
1. Deploy contract
2. Add participants
3. Record expenses
4. Contribute funds
5. Settle expenses
6. Verify final state
```

## Common Issues & Solutions

### Issue 1: Compilation Errors
**Problem**: Syntax errors in Vyper code
**Solution**: Check version compatibility, verify syntax

### Issue 2: Deployment Fails
**Problem**: Contract deployment fails
**Solution**: Check gas limit, verify network connection

### Issue 3: Function Calls Fail
**Problem**: Function calls revert
**Solution**: Check input validation, verify state

### Issue 4: Events Not Emitted
**Problem**: Events not appearing in logs
**Solution**: Verify event parameters, check transaction success

## Success Criteria

Your solution is complete when:
- [ ] All functions compile without errors
- [ ] Contract deploys successfully
- [ ] All functions work as expected
- [ ] Events are emitted correctly
- [ ] Error conditions are handled
- [ ] Gas usage is reasonable
- [ ] Code follows best practices

## Next Steps

After completing exercises:
1. **Test on Testnet**: Deploy to a testnet
2. **Build Frontend**: Create Web3 interface
3. **Add Features**: Implement additional functionality
4. **Optimize**: Improve gas efficiency
5. **Document**: Add comprehensive comments

## Resources

- [Vyper Documentation](https://vyper.readthedocs.io/)
- [Remix IDE](https://remix.ethereum.org)
- [Ethereum Testnets](https://ethereum.org/en/developers/docs/networks/)
- [MetaMask](https://metamask.io/)

Happy coding! 🚀
