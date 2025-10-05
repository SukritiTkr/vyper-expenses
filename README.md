# 🐍 VyperVerse: Complete Web3 Development Workshop

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Vyper](https://img.shields.io/badge/Vyper-0.4.3-blue.svg)](https://vyper.readthedocs.io/)
[![EVM](https://img.shields.io/badge/EVM-Cancun-green.svg)](https://ethereum.org/en/developers/docs/evm/)
[![Workshop](https://img.shields.io/badge/Workshop-Ready-orange.svg)](https://github.com/he2plus/vyper-devs)

> **Learn Vyper smart contract development from Python to production deployment**

A comprehensive, hands-on workshop repository for learning Vyper smart contract development. Perfect for Python developers transitioning to blockchain development and Web3 enthusiasts.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/he2plus/vyper-devs.git
cd vyper-devs

# Open Remix IDE
# Visit: https://remix.ethereum.org
# Upload contracts from contracts/ directory
# Deploy to any EVM-compatible testnet
```

## ✨ Features

- 🐍 **Python to Vyper Guide**: Side-by-side comparisons and migration patterns
- 📝 **Interactive Templates**: Hands-on coding exercises with hints
- 🎯 **Complete Solutions**: Production-ready smart contracts
- 🌐 **Web3 Frontend**: Interactive dApp with MetaMask integration
- 📚 **Comprehensive Docs**: From blockchain basics to advanced deployment
- 🛠️ **Deployment Scripts**: Automated testing and deployment tools
- 🎓 **Workshop Materials**: Ready-to-use teaching resources

## 📁 Repository Structure

```
vyper-devs/
├── 📄 README.md                    # This file
├── 📄 LICENSE                      # MIT License
├── 📄 .gitignore                   # Git ignore rules
├── 📁 contracts/                   # Smart contracts
│   ├── 📁 dev/                     # Development templates
│   │   ├── 📄 ExpenseSplitter_Template.vy
│   │   ├── 📄 hints.md
│   │   └── 📄 exercises.md
│   └── 📁 solutions/               # Complete solutions
│       ├── 📄 ExpenseSplitter_Basic.vy
│       └── 📄 ExpenseSplitter_Complete.vy
├── 📁 frontend/                    # Web3 frontend
│   ├── 📄 index.html
│   ├── 📄 app.js
│   ├── 📄 styles.css
│   └── 📄 abi.json
├── 📁 docs/                        # Documentation
│   ├── 📄 01_blockchain_basics.md
│   ├── 📄 02_smart_contracts.md
│   ├── 📄 03_vyper_guide.md
│   ├── 📄 04_python_to_vyper.md
│   └── 📄 05_deployment_guide.md
├── 📁 scripts/                     # Automation scripts
│   ├── 📄 deploy.py
│   └── 📄 interact.py
├── 📁 resources/                   # Additional resources
│   ├── 📄 testnet_faucets.md
│   ├── 📄 useful_links.md
│   └── 📄 troubleshooting.md
└── 📄 WORKSHOP_GUIDE.md            # Complete workshop guide
```

## 🎯 Learning Path

### 1. **Blockchain Basics** (30 minutes)
- Understanding blockchain fundamentals
- EVM and smart contract concepts
- Gas, transactions, and accounts

### 2. **Vyper Introduction** (45 minutes)
- Python vs Vyper syntax comparison
- Type system and data structures
- Function decorators and events

### 3. **Hands-on Development** (90 minutes)
- Complete the ExpenseSplitter template
- Learn security best practices
- Test on Remix IDE

### 4. **Frontend Integration** (60 minutes)
- Build Web3 frontend with ethers.js
- Connect to MetaMask
- Interact with deployed contracts

### 5. **Deployment & Testing** (45 minutes)
- Deploy to testnets
- Verify contracts on block explorers
- Test all functionality

## 🛠️ Prerequisites

- **MetaMask Wallet**: [Install MetaMask](https://metamask.io/)
- **Testnet Tokens**: Get from faucets (links in resources/)
- **Remix IDE**: [remix.ethereum.org](https://remix.ethereum.org)
- **Basic Python Knowledge**: Helpful but not required

## 🚀 Installation & Setup

### Option 1: Remix IDE (Recommended for Beginners)

1. **Open Remix IDE**
   ```
   Visit: https://remix.ethereum.org
   ```

2. **Create New Workspace**
   - Click "Create New Workspace"
   - Name: "VyperVerse Workshop"
   - Template: "Default"

3. **Upload Contracts**
   - Copy files from `contracts/` directory
   - Paste into Remix file explorer
   - Start with `ExpenseSplitter_Template.vy`

### Option 2: Local Development

```bash
# Clone repository
git clone https://github.com/he2plus/vyper-devs.git
cd vyper-devs

# Install Vyper (optional, for local compilation)
pip install vyper

# Open frontend
cd frontend
python -m http.server 8000
# Visit: http://localhost:8000
```

## 📖 Workshop Modules

### Module 1: Smart Contract Template
**File**: `contracts/dev/ExpenseSplitter_Template.vy`
- Learn Vyper syntax through guided exercises
- Complete function implementations
- Understand security patterns

### Module 2: Complete Solution
**File**: `contracts/solutions/ExpenseSplitter_Complete.vy`
- Production-ready implementation
- Advanced features and optimizations
- Best practices demonstration

### Module 3: Web3 Frontend
**File**: `frontend/index.html`
- Interactive dApp interface
- MetaMask integration
- Real-time contract interaction

### Module 4: Python to Vyper Guide
**File**: `docs/04_python_to_vyper.md`
- Side-by-side code comparisons
- Migration patterns and tips
- Common pitfalls to avoid

## 🌐 Supported Networks

| Network | RPC URL | Faucet | Explorer |
|---------|---------|--------|----------|
| **Celo Testnet** | `https://alfajores-forno.celo-testnet.org` | [faucet.celo.org](https://faucet.celo.org/) | [explorer.celo.org](https://explorer.celo.org/alfajores) |
| **Monad Testnet** | `https://testnet-rpc.monad.xyz` | [faucet.monad.xyz](https://faucet.monad.xyz) | [testnet-explorer.monad.xyz](https://testnet-explorer.monad.xyz) |
| **Berachain Testnet** | `https://testnet-rpc.berachain.com` | [faucet.berachain.com](https://faucet.berachain.com) | [testnet-scan.berachain.com](https://testnet-scan.berachain.com) |
| **Ethereum Sepolia** | `https://rpc.sepolia.org` | [sepoliafaucet.com](https://sepoliafaucet.com) | [sepolia.etherscan.io](https://sepolia.etherscan.io) |

## 🎓 Workshop Guide

Follow the complete workshop guide in `WORKSHOP_GUIDE.md` for:
- Step-by-step instructions
- Learning objectives
- Assessment criteria
- Troubleshooting tips

## 🔧 Development Tools

### Smart Contract Development
- **Remix IDE**: [remix.ethereum.org](https://remix.ethereum.org)
- **Vyper Compiler**: Version 0.4.3
- **EVM Version**: Cancun

### Frontend Development
- **ethers.js**: Version 5.7.2
- **MetaMask**: Browser extension
- **Local Server**: Python HTTP server

### Testing & Deployment
- **Testnets**: Multiple EVM-compatible networks
- **Block Explorers**: Contract verification
- **Gas Optimization**: Best practices included

## 🐛 Troubleshooting

### Common Issues

1. **Contract Won't Compile**
   - Check Vyper version (0.4.1)
   - Verify EVM version (Cancun)
   - Review syntax errors in console

2. **MetaMask Connection Failed**
   - Ensure MetaMask is unlocked
   - Check network configuration
   - Refresh page and try again

3. **Transaction Stuck**
   - Increase gas price in MetaMask
   - Check network congestion
   - Wait for confirmation

4. **Frontend Not Loading**
   - Check browser console for errors
   - Verify contract address is correct
   - Ensure ABI matches deployed contract

### Getting Help

- 📖 **Documentation**: Check `docs/` directory
- 🔍 **Troubleshooting**: See `resources/troubleshooting.md`
- 💬 **Issues**: Open GitHub issue
- 📧 **Contact**: [@he2plus](https://x.com/he2plus)

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

### Contribution Areas
- 🐛 Bug fixes and improvements
- 📚 Documentation updates
- 🎨 Frontend enhancements
- 🔧 Tooling and scripts
- 🎓 Educational content

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 VyperVerse Workshop

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

## 🙏 Acknowledgments

- **Workshop Designer**: [Prakhar Tripathi](https://x.com/he2plus)
- **Vyper Team**: For the amazing Python-like smart contract language
- **Ethereum Foundation**: For the EVM and ecosystem
- **Community**: All contributors and workshop participants

## 📞 Contact & Support

- **Twitter**: [@he2plus](https://x.com/he2plus)
- **GitHub**: [he2plus](https://github.com/he2plus)
- **Workshop**: VyperVerse Web3 Development Series
- **Location**: India

---

## 🎯 Success Criteria

After completing this workshop, you will:
- ✅ Understand blockchain and smart contract fundamentals
- ✅ Write Vyper smart contracts from scratch
- ✅ Deploy contracts to multiple testnets
- ✅ Build Web3 frontends with MetaMask integration
- ✅ Apply security best practices
- ✅ Debug and troubleshoot common issues
- ✅ Have a complete project for your portfolio

**Ready to start your Web3 journey? Let's build the future together! 🚀**

---

*This workshop is designed for educational purposes. Always test thoroughly on testnets before mainnet deployment.*
