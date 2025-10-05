# @version 0.4.3
#pragma evm-version cancun

# ==============================================================
# VyperVerse Workshop: Complete Expense Splitter Solution
# Designed by Prakhar Tripathi [https://x.com/he2plus]
# ==============================================================

# ---------------------- USER CUSTOMIZATION ----------------------
your_name: public(String[50])
your_goal: public(String[100])
# ----------------------------------------------------------------

# ============== STATE VARIABLES ==============
owner: public(address)
total_expenses: public(uint256)
expense_count: public(uint256)
balances: public(HashMap[address, uint256])
participants: public(DynArray[address, 100])

# ============== EVENTS ==============
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
@deploy
def __init__():
    # Set user customization
    self.your_name = "Prakhar - Blockchain Developer"
    self.your_goal = "Teaching the next generation of Web3 developers"
    
    assert len(self.your_name) > 0, "Please add your name!"
    assert len(self.your_goal) > 0, "Please add your learning goal!"
    
    self.owner = msg.sender
    self.total_expenses = 0
    self.expense_count = 0
    self.participants.append(msg.sender)
    
    log ParticipantAdded(participant=msg.sender, added_by=msg.sender)

# ============== CORE FUNCTIONS ==============

@external
def record_expense(description: String[100], amount: uint256):
    """Record a new expense"""
    assert amount > 0, "Amount must be greater than zero"
    
    self.total_expenses += amount
    self.expense_count += 1
    self.balances[msg.sender] += amount
    
    log ExpenseRecorded(
        user=msg.sender,
        description=description,
        amount=amount,
        timestamp=block.timestamp
    )

@external
def add_participant(new_participant: address):
    """Add a new participant to the group"""
    assert msg.sender == self.owner, "Only owner can add participants"
    assert new_participant != empty(address), "Invalid participant address"
    
    for participant: address in self.participants:
        assert participant != new_participant, "Already a participant"
    
    self.participants.append(new_participant)
    log ParticipantAdded(participant=new_participant, added_by=msg.sender)

@external
@payable
def contribute():
    """Contribute money to cover expenses"""
    assert msg.value > 0, "Must send some value"
    log PaymentReceived(from_user=msg.sender, amount=msg.value)

@external
def settle_expenses():
    """Settle your expenses"""
    amount_owed: uint256 = self.balances[msg.sender]
    
    assert amount_owed > 0, "No expenses to settle"
    assert self.balance >= amount_owed, "Insufficient contract balance"
    
    # Reset balance first (security pattern)
    self.balances[msg.sender] = 0
    
    # Then send funds
    send(msg.sender, amount_owed)
    
    log ExpenseSettled(user=msg.sender, amount=amount_owed)

# ============== VIEW FUNCTIONS ==============

@external
@view
def get_participant_count() -> uint256:
    """Get total number of participants"""
    return len(self.participants)

@external
@view
def calculate_equal_split() -> uint256:
    """Calculate equal split amount per person"""
    participant_count: uint256 = len(self.participants)
    
    if participant_count == 0:
        return 0
    
    return self.total_expenses // participant_count

@external
@view
def get_my_balance() -> uint256:
    """Get your current expense balance"""
    return self.balances[msg.sender]

@external
@view
def check_contract_balance() -> uint256:
    """Get total contract balance"""
    return self.balance

@external
@view
def get_participant_at(index: uint256) -> address:
    """Get participant at specific index"""
    assert index < len(self.participants), "Index out of bounds"
    return self.participants[index]

@external
@view
def is_participant(check_address: address) -> bool:
    """Check if address is a participant"""
    for participant: address in self.participants:
        if participant == check_address:
            return True
    return False

# ============== ADMIN FUNCTIONS ==============

@external
def emergency_withdraw():
    """Emergency function - only owner can withdraw all funds"""
    assert msg.sender == self.owner, "Only owner can withdraw"
    
    contract_balance: uint256 = self.balance
    send(self.owner, contract_balance)
