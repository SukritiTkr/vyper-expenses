# @version 0.4.3
#pragma evm-version cancun

# ==============================================================
# VyperVerse Workshop: Expense Splitter Contract Template
# Designed by Prakhar Tripathi [https://x.com/he2plus]
# ==============================================================

# ============== EDUCATIONAL COMPARISON ==============
# Python Version (Traditional):
# -------------------------------------------
# class ExpenseSplitter:
#     def __init__(self):
#         self.owner = "Alice"
#         self.total_amount = 0
#         self.participants = []
#     
#     def add_expense(self, description, amount):
#         if amount > 0:
#             self.total_amount += amount
#             return True
#         return False
# -------------------------------------------
# Vyper Version (Blockchain):
# Same logic, but on blockchain = immutable, transparent, trustless!
# ====================================================

# ---------------------- YOUR CUSTOMIZATION START ----------------------
# >>> REQUIRED: Add your name and intro
your_name: public(String[50])
# Example: "Prakhar - Blockchain Developer from Delhi"

# >>> REQUIRED: What do you hope to learn from this workshop?
your_goal: public(String[100])
# Example: "Master Vyper to build DeFi applications and contribute to Web3"
# ----------------------- YOUR CUSTOMIZATION END -----------------------

# ============== CONTRACT STATE VARIABLES ==============
# Think of these as your database tables

# Storage: Who created this contract?
owner: public(address)

# Storage: What's the total amount of all expenses?
total_expenses: public(uint256)

# Storage: How many expenses have been recorded?
expense_count: public(uint256)

# Storage: Track each participant's balance
# HashMap = Python dictionary on blockchain!
balances: public(HashMap[address, uint256])

# Storage: List of all participants
participants: public(DynArray[address, 100])

# ============== EVENTS (Blockchain Logs) ==============
# Events are like console.log() but permanent on blockchain!

event ExpenseRecorded:
    user: indexed(address)
    description: String[100]
    amount: uint256
    timestamp: uint256

event ParticipantAdded:
    participant: indexed(address)
    added_by: indexed(address)

event PaymentReceived:
    from_user: indexed(address)
    amount: uint256

event ExpenseSettled:
    user: indexed(address)
    amount: uint256

# ============== CONSTRUCTOR ==============
# This runs ONCE when contract is deployed

@deploy
def __init__():
    """
    Initialize the contract.
    In Python: __init__(self)
    In Vyper: Same but deployed to blockchain!
    """
    # Set user customization (REQUIRED: Replace with your details)
    self.your_name = "YOUR_NAME_HERE"
    self.your_goal = "YOUR_LEARNING_GOAL_HERE"
    
    # Validation: Did you customize the contract?
    assert len(self.your_name) > 0, "Please add your name!"
    assert len(self.your_goal) > 0, "Please add your learning goal!"
    
    # Set the contract deployer as owner
    self.owner = msg.sender
    
    # Initialize counters
    self.total_expenses = 0
    self.expense_count = 0
    
    # Owner is first participant
    self.participants.append(msg.sender)
    
    # Log deployment
    log ParticipantAdded(participant=msg.sender, added_by=msg.sender)

# ============== MODULE 1: BASIC FUNCTIONS ==============
# Your first hands-on coding starts here!

@external
def record_expense(description: String[100], amount: uint256):
    """
    Record a new expense in the contract.
    
    📝 YOUR TASK: Complete this function!
    
    Python equivalent:
    def record_expense(self, description, amount):
        if amount > 0:
            self.total_expenses += amount
            self.expense_count += 1
    
    Vyper requirements:
    1. Check that amount is greater than 0
    2. Add amount to total_expenses
    3. Increment expense_count by 1
    4. Add amount to the caller's balance
    5. Log the ExpenseRecorded event
    
    Hints:
    - Use 'assert' to validate (like 'if' but reverts on fail)
    - msg.sender = the person calling this function
    - block.timestamp = current time
    """
    
    # STEP 1: Validate amount is positive
    # TODO: Write your assertion here
    assert amount > 0, "Amount must be greater than zero"
    
    # STEP 2: Update total expenses
    # TODO: Add amount to self.total_expenses
    self.total_expenses += amount
    
    # STEP 3: Increment expense counter
    # TODO: Increase self.expense_count by 1
    self.expense_count += 1
    
    # STEP 4: Update caller's balance
    # TODO: Add amount to self.balances[msg.sender]
    self.balances[msg.sender] += amount
    
    # STEP 5: Emit event for transparency
    # TODO: Log the ExpenseRecorded event with all parameters
    log ExpenseRecorded(
        user=msg.sender,
        description=description,
        amount=amount,
        timestamp=block.timestamp
    )

# ============== MODULE 2: PARTICIPANT MANAGEMENT ==============

@external
def add_participant(new_participant: address):
    """
    Add a new participant to the expense group.
    
    📝 YOUR TASK: Complete this function!
    
    Requirements:
    1. Only owner can add participants (access control)
    2. Participant address must be valid (not zero address)
    3. Check participant isn't already added
    4. Add to participants array
    5. Log the event
    
    Hints:
    - empty(address) = 0x0000...0000 (invalid address)
    - Use a loop to check if already exists
    """
    
    # STEP 1: Check only owner can call this
    # TODO: Assert msg.sender is the owner
    assert msg.sender == self.owner, "Only owner can add participants"
    
    # STEP 2: Validate address
    # TODO: Assert new_participant is not empty address
    assert new_participant != empty(address), "Invalid participant address"
    
    # STEP 3: Check not already participant
    # TODO: Loop through participants and assert not duplicate
    for participant: address in self.participants:
        assert participant != new_participant, "Already a participant"
    
    # STEP 4: Add to array
    # TODO: Append new_participant to self.participants
    self.participants.append(new_participant)
    
    # STEP 5: Log the event
    # TODO: Emit ParticipantAdded event
    log ParticipantAdded(participant=new_participant, added_by=msg.sender)

# ============== MODULE 3: PAYMENT FUNCTIONS ==============

@external
@payable
def contribute():
    """
    Allow participants to contribute money to pay expenses.
    
    📝 YOUR TASK: Complete this function!
    
    The @payable decorator means this function can receive Ether/tokens!
    
    Requirements:
    1. Must send some value (msg.value > 0)
    2. Log the payment received
    
    Hints:
    - msg.value = amount of crypto sent with transaction
    - Vyper automatically handles receiving money
    """
    
    # STEP 1: Validate payment amount
    # TODO: Assert msg.value is greater than 0
    assert msg.value > 0, "Must send some value"
    
    # STEP 2: Log the contribution
    # TODO: Emit PaymentReceived event
    log PaymentReceived(from_user=msg.sender, amount=msg.value)

@external
def settle_expenses():
    """
    Settle expenses for the caller - pay what they owe.
    
    📝 YOUR TASK: Complete this function!
    
    Requirements:
    1. Check caller has expenses to settle
    2. Calculate amount owed
    3. Transfer funds
    4. Reset their balance
    5. Log settlement
    
    Hints:
    - send() = transfer Ether to address
    - Always reset balance AFTER transfer (security!)
    """
    
    # STEP 1: Get amount owed
    # TODO: Store self.balances[msg.sender] in a variable
    amount_owed: uint256 = self.balances[msg.sender]
    
    # STEP 2: Validate they owe something
    # TODO: Assert amount_owed > 0
    assert amount_owed > 0, "No expenses to settle"
    
    # STEP 3: Check contract has enough balance
    # TODO: Assert self.balance >= amount_owed
    assert self.balance >= amount_owed, "Insufficient contract balance"
    
    # STEP 4: Reset balance FIRST (security - prevents re-entrancy)
    # TODO: Set self.balances[msg.sender] = 0
    self.balances[msg.sender] = 0
    
    # STEP 5: Send the money
    # TODO: Use send() to transfer amount_owed to msg.sender
    send(msg.sender, amount_owed)
    
    # STEP 6: Log settlement
    # TODO: Emit ExpenseSettled event
    log ExpenseSettled(user=msg.sender, amount=amount_owed)

# ============== VIEW FUNCTIONS (Read-Only) ==============
# These don't cost gas and can't modify state!

@external
@view
def get_participant_count() -> uint256:
    """
    Get total number of participants.
    
    📝 YOUR TASK: Complete this function!
    
    Python equivalent:
    def get_participant_count(self):
        return len(self.participants)
    """
    # TODO: Return the length of participants array
    return len(self.participants)

@external
@view
def calculate_equal_split() -> uint256:
    """
    Calculate how much each person owes if split equally.
    
    📝 YOUR TASK: Complete this function!
    
    Formula: total_expenses / number_of_participants
    
    Hints:
    - Division in Vyper is integer division
    - Handle zero participants case
    """
    # STEP 1: Get participant count
    # TODO: Store participant count
    participant_count: uint256 = len(self.participants)
    
    # STEP 2: Handle edge case
    # TODO: If no participants, return 0
    if participant_count == 0:
        return 0
    
    # STEP 3: Calculate split
    # TODO: Return total_expenses divided by participant_count
    return self.total_expenses // participant_count

@external
@view
def get_my_balance() -> uint256:
    """
    Get the calling user's current balance (what they've spent).
    
    📝 YOUR TASK: Complete this function!
    """
    # TODO: Return balance of msg.sender
    return self.balances[msg.sender]

@external
@view
def check_contract_balance() -> uint256:
    """
    Get total contract balance (contributions received).
    
    📝 YOUR TASK: Complete this function!
    """
    # TODO: Return self.balance
    return self.balance

# ============== ADMIN FUNCTIONS ==============

@external
def emergency_withdraw():
    """
    Emergency function - only owner can withdraw all funds.
    
    📝 YOUR TASK: Complete this function!
    
    Use case: In case of issues or after all settlements
    """
    # STEP 1: Check authorization
    # TODO: Assert caller is owner
    assert msg.sender == self.owner, "Only owner can withdraw"
    
    # STEP 2: Get balance
    # TODO: Store self.balance
    contract_balance: uint256 = self.balance
    
    # STEP 3: Transfer everything
    # TODO: Send contract_balance to owner
    send(self.owner, contract_balance)

# ============== CONGRATULATIONS! ==============
# You've completed the Expense Splitter contract template!
#
# What you've learned:
# ✅ State variables and storage
# ✅ Events and logging
# ✅ Function decorators (@external, @payable, @view)
# ✅ Access control (only owner)
# ✅ Handling payments
# ✅ Data structures (HashMap, DynArray)
# ✅ Security patterns (check-effects-interactions)
#
# Next Steps:
# 1. Test your contract on Remix
# 2. Deploy to a testnet
# 3. Build the frontend
# 4. Add this to your portfolio!
#
# Keep building! 🚀
# ==================================================
