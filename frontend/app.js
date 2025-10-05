// VyperVerse - Expense Splitter dApp JavaScript
// Web3 integration with ethers.js and MetaMask

// Global variables
let provider = null;
let signer = null;
let contract = null;
let userAddress = null;

// Contract ABI - This should match your deployed contract
const CONTRACT_ABI = [
    // Events
    "event ExpenseRecorded(address indexed user, string description, uint256 amount, uint256 timestamp)",
    "event ParticipantAdded(address indexed participant, address indexed added_by)",
    "event PaymentReceived(address indexed from_user, uint256 amount)",
    "event ExpenseSettled(address indexed user, uint256 amount)",
    
    // View functions
    "function get_participant_count() view returns (uint256)",
    "function calculate_equal_split() view returns (uint256)",
    "function get_my_balance() view returns (uint256)",
    "function check_contract_balance() view returns (uint256)",
    "function get_participant_at(uint256 index) view returns (address)",
    "function is_participant(address check_address) view returns (bool)",
    "function total_expenses() view returns (uint256)",
    "function expense_count() view returns (uint256)",
    "function participants(uint256) view returns (address)",
    "function balances(address) view returns (uint256)",
    "function owner() view returns (address)",
    
    // State-changing functions
    "function record_expense(string description, uint256 amount)",
    "function add_participant(address new_participant)",
    "function contribute() payable",
    "function settle_expenses()",
    "function emergency_withdraw()"
];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
});

// Initialize the application
async function initializeApp() {
    console.log('Initializing VyperVerse dApp...');
    
    // Check if MetaMask is installed
    if (typeof window.ethereum !== 'undefined') {
        console.log('MetaMask detected');
        provider = new ethers.providers.Web3Provider(window.ethereum);
        
        // Listen for account changes
        window.ethereum.on('accountsChanged', handleAccountsChanged);
        window.ethereum.on('chainChanged', handleChainChanged);
        
        // Check if already connected
        const accounts = await window.ethereum.request({ method: 'eth_accounts' });
        if (accounts.length > 0) {
            await connectWallet();
        }
    } else {
        showAlert('connectWallet', 'MetaMask is not installed. Please install MetaMask to use this dApp.', 'error');
        document.getElementById('connectWallet').textContent = 'Install MetaMask';
        document.getElementById('connectWallet').onclick = () => {
            window.open('https://metamask.io/', '_blank');
        };
    }
}

// Setup event listeners
function setupEventListeners() {
    // Wallet connection
    document.getElementById('connectWallet').addEventListener('click', connectWallet);
    
    // Contract interaction
    document.getElementById('loadContract').addEventListener('click', loadContract);
    document.getElementById('refreshData').addEventListener('click', refreshData);
    
    // Expense management
    document.getElementById('recordExpense').addEventListener('click', recordExpense);
    document.getElementById('addParticipant').addEventListener('click', addParticipant);
    document.getElementById('contribute').addEventListener('click', contribute);
    document.getElementById('settleExpenses').addEventListener('click', settleExpenses);
    
    // Enter key support for inputs
    document.getElementById('contractAddress').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') loadContract();
    });
    
    document.getElementById('expenseDesc').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') recordExpense();
    });
    
    document.getElementById('expenseAmount').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') recordExpense();
    });
    
    document.getElementById('participantAddress').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') addParticipant();
    });
    
    document.getElementById('contributeAmount').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') contribute();
    });
}

// Connect to MetaMask wallet
async function connectWallet() {
    try {
        showLoading(true);
        
        // Request account access
        await window.ethereum.request({ method: 'eth_requestAccounts' });
        
        // Get signer
        signer = provider.getSigner();
        userAddress = await signer.getAddress();
        
        // Update UI
        const connectBtn = document.getElementById('connectWallet');
        const walletInfo = document.getElementById('walletInfo');
        
        if (connectBtn) connectBtn.style.display = 'none';
        if (walletInfo) walletInfo.style.display = 'flex';
        document.getElementById('walletAddress').textContent = 
            `${userAddress.slice(0, 6)}...${userAddress.slice(-4)}`;
        
        // Get and display balance
        const balance = await provider.getBalance(userAddress);
        const balanceInEth = ethers.utils.formatEther(balance);
        document.getElementById('walletBalance').textContent = `${parseFloat(balanceInEth).toFixed(4)} ETH`;
        
        showAlert('connectWallet', 'Wallet connected successfully!', 'success');
        
    } catch (error) {
        console.error('Error connecting wallet:', error);
        showAlert('connectWallet', `Failed to connect wallet: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

// Handle account changes
function handleAccountsChanged(accounts) {
    if (accounts.length === 0) {
        // User disconnected
        location.reload();
    } else {
        // User switched accounts
        connectWallet();
    }
}

// Handle chain changes
function handleChainChanged(chainId) {
    console.log('Chain changed to:', chainId);
    location.reload();
}

// Load contract
async function loadContract() {
    try {
        const contractAddress = document.getElementById('contractAddress').value.trim();
        
        if (!contractAddress) {
            showAlert('contractStatus', 'Please enter a contract address', 'error');
            return;
        }
        
        if (!ethers.utils.isAddress(contractAddress)) {
            showAlert('contractStatus', 'Invalid contract address format', 'error');
            return;
        }
        
        showLoading(true);
        
        // Create contract instance
        contract = new ethers.Contract(contractAddress, CONTRACT_ABI, signer);
        
        // Test contract connection
        try {
            const owner = await contract.owner();
            console.log('Contract loaded successfully, owner:', owner);
            
            // Show contract info section
            document.getElementById('contractInfo').style.display = 'block';
            document.getElementById('participantsSection').style.display = 'block';
            document.getElementById('transactionHistory').style.display = 'block';
            
            // Refresh data
            await refreshData();
            
            showAlert('contractStatus', 'Contract loaded successfully!', 'success');
            
        } catch (error) {
            console.error('Error testing contract:', error);
            showAlert('contractStatus', 'Failed to connect to contract. Please check the address.', 'error');
        }
        
    } catch (error) {
        console.error('Error loading contract:', error);
        showAlert('contractStatus', `Failed to load contract: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

// Refresh contract data
async function refreshData() {
    if (!contract) {
        showAlert('contractStatus', 'Please load a contract first', 'error');
        return;
    }
    
    try {
        showLoading(true);
        
        // Get contract data
        const [
            totalExpenses,
            expenseCount,
            participantCount,
            contractBalance,
            yourBalance,
            equalSplit
        ] = await Promise.all([
            contract.total_expenses(),
            contract.expense_count(),
            contract.get_participant_count(),
            contract.check_contract_balance(),
            contract.get_my_balance(),
            contract.calculate_equal_split()
        ]);
        
        // Update UI
        document.getElementById('totalExpenses').textContent = `${ethers.utils.formatEther(totalExpenses)} ETH`;
        document.getElementById('expenseCount').textContent = expenseCount.toString();
        document.getElementById('participantCount').textContent = participantCount.toString();
        document.getElementById('contractBalance').textContent = `${ethers.utils.formatEther(contractBalance)} ETH`;
        document.getElementById('yourBalance').textContent = `${ethers.utils.formatEther(yourBalance)} ETH`;
        document.getElementById('equalSplit').textContent = `${ethers.utils.formatEther(equalSplit)} ETH`;
        
        // Load participants
        await loadParticipants(participantCount);
        
    } catch (error) {
        console.error('Error refreshing data:', error);
        showAlert('contractStatus', `Failed to refresh data: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

// Load participants list
async function loadParticipants(count) {
    try {
        const participantsList = document.getElementById('participantsList');
        participantsList.innerHTML = '';
        
        for (let i = 0; i < count; i++) {
            const participantAddress = await contract.get_participant_at(i);
            const balance = await contract.balances(participantAddress);
            
            const participantItem = document.createElement('div');
            participantItem.className = 'participant-item';
            participantItem.innerHTML = `
                <span class="participant-address">${participantAddress}</span>
                <span class="participant-balance">${ethers.utils.formatEther(balance)} ETH</span>
            `;
            
            participantsList.appendChild(participantItem);
        }
        
    } catch (error) {
        console.error('Error loading participants:', error);
    }
}

// Record expense
async function recordExpense() {
    if (!contract) {
        showAlert('expenseAlert', 'Please load a contract first', 'error');
        return;
    }
    
    try {
        const description = document.getElementById('expenseDesc').value.trim();
        const amount = document.getElementById('expenseAmount').value.trim();
        
        if (!description || !amount) {
            showAlert('expenseAlert', 'Please fill all fields', 'error');
            return;
        }
        
        const amountWei = ethers.utils.parseEther(amount);
        
        showLoading(true);
        
        const tx = await contract.record_expense(description, amountWei);
        await tx.wait();
        
        // Clear form
        document.getElementById('expenseDesc').value = '';
        document.getElementById('expenseAmount').value = '';
        
        // Refresh data
        await refreshData();
        
        showAlert('expenseAlert', 'Expense recorded successfully!', 'success');
        
    } catch (error) {
        console.error('Error recording expense:', error);
        showAlert('expenseAlert', `Failed to record expense: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

// Add participant
async function addParticipant() {
    if (!contract) {
        showAlert('participantAlert', 'Please load a contract first', 'error');
        return;
    }
    
    try {
        const participantAddress = document.getElementById('participantAddress').value.trim();
        
        if (!participantAddress) {
            showAlert('participantAlert', 'Please enter participant address', 'error');
            return;
        }
        
        if (!ethers.utils.isAddress(participantAddress)) {
            showAlert('participantAlert', 'Invalid address format', 'error');
            return;
        }
        
        showLoading(true);
        
        const tx = await contract.add_participant(participantAddress);
        await tx.wait();
        
        // Clear form
        document.getElementById('participantAddress').value = '';
        
        // Refresh data
        await refreshData();
        
        showAlert('participantAlert', 'Participant added successfully!', 'success');
        
    } catch (error) {
        console.error('Error adding participant:', error);
        showAlert('participantAlert', `Failed to add participant: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

// Contribute funds
async function contribute() {
    if (!contract) {
        showAlert('contributeAlert', 'Please load a contract first', 'error');
        return;
    }
    
    try {
        const amount = document.getElementById('contributeAmount').value.trim();
        
        if (!amount) {
            showAlert('contributeAlert', 'Please enter contribution amount', 'error');
            return;
        }
        
        const amountWei = ethers.utils.parseEther(amount);
        
        showLoading(true);
        
        const tx = await contract.contribute({ value: amountWei });
        await tx.wait();
        
        // Clear form
        document.getElementById('contributeAmount').value = '';
        
        // Refresh data
        await refreshData();
        
        showAlert('contributeAlert', 'Contribution successful!', 'success');
        
    } catch (error) {
        console.error('Error contributing:', error);
        showAlert('contributeAlert', `Failed to contribute: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

// Settle expenses
async function settleExpenses() {
    if (!contract) {
        showAlert('settleAlert', 'Please load a contract first', 'error');
        return;
    }
    
    try {
        showLoading(true);
        
        const tx = await contract.settle_expenses();
        await tx.wait();
        
        // Refresh data
        await refreshData();
        
        showAlert('settleAlert', 'Expenses settled successfully!', 'success');
        
    } catch (error) {
        console.error('Error settling expenses:', error);
        showAlert('settleAlert', `Failed to settle expenses: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

// Show alert message
function showAlert(elementId, message, type) {
    const alertElement = document.getElementById(elementId);
    if (alertElement) {
        alertElement.textContent = message;
        alertElement.className = `alert ${type}`;
        alertElement.style.display = 'block';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            alertElement.style.display = 'none';
        }, 5000);
    }
}

// Show loading overlay
function showLoading(show) {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.style.display = show ? 'flex' : 'none';
    }
}

// Utility function to format addresses
function formatAddress(address) {
    if (!address) return '';
    return `${address.slice(0, 6)}...${address.slice(-4)}`;
}

// Utility function to format Ether values
function formatEther(value) {
    if (!value) return '0';
    return parseFloat(ethers.utils.formatEther(value)).toFixed(4);
}

// Error handling
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    showAlert('contractStatus', 'An unexpected error occurred', 'error');
});

// Unhandled promise rejection handling
window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
    showAlert('contractStatus', 'An unexpected error occurred', 'error');
});

console.log('VyperVerse dApp loaded successfully!');
