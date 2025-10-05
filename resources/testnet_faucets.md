# 💧 Testnet Faucets

## Overview

Testnet faucets provide free test tokens for development and testing purposes. These tokens have no real value and are used to test smart contracts and dApps without spending real money.

## Supported Networks

### 1. Celo Alfajores Testnet

#### Network Details
- **Chain ID**: 44787
- **RPC URL**: `https://alfajores-forno.celo-testnet.org`
- **Explorer**: [explorer.celo.org/alfajores](https://explorer.celo.org/alfajores)
- **Native Token**: CELO
- **Stablecoin**: cUSD

#### Faucets
- **Primary Faucet**: [faucet.celo.org](https://faucet.celo.org/)
- **Alternative**: [celo.org/developers/faucet](https://celo.org/developers/faucet)
- **Discord Faucet**: Available in Celo Discord server

#### How to Use
1. Connect your MetaMask to Celo Alfajores testnet
2. Visit the faucet website
3. Enter your wallet address
4. Complete CAPTCHA if required
5. Receive test tokens

#### Token Amounts
- **CELO**: 0.5 CELO per request
- **cUSD**: 10 cUSD per request
- **Cooldown**: 24 hours between requests

### 2. Monad Testnet

#### Network Details
- **Chain ID**: 41434
- **RPC URL**: `https://testnet-rpc.monad.xyz`
- **Explorer**: [testnet-explorer.monad.xyz](https://testnet-explorer.monad.xyz)
- **Native Token**: MON

#### Faucets
- **Primary Faucet**: [faucet.monad.xyz](https://faucet.monad.xyz)
- **Discord Faucet**: Available in Monad Discord server

#### How to Use
1. Connect your MetaMask to Monad testnet
2. Visit the faucet website
3. Enter your wallet address
4. Complete verification if required
5. Receive test tokens

#### Token Amounts
- **MON**: 1 MON per request
- **Cooldown**: 24 hours between requests

### 3. Berachain Testnet

#### Network Details
- **Chain ID**: 80085
- **RPC URL**: `https://testnet-rpc.berachain.com`
- **Explorer**: [testnet-scan.berachain.com](https://testnet-scan.berachain.com)
- **Native Token**: BERA

#### Faucets
- **Primary Faucet**: [faucet.berachain.com](https://faucet.berachain.com)
- **Discord Faucet**: Available in Berachain Discord server

#### How to Use
1. Connect your MetaMask to Berachain testnet
2. Visit the faucet website
3. Enter your wallet address
4. Complete verification if required
5. Receive test tokens

#### Token Amounts
- **BERA**: 1 BERA per request
- **Cooldown**: 24 hours between requests

### 4. Ethereum Sepolia Testnet

#### Network Details
- **Chain ID**: 11155111
- **RPC URL**: `https://rpc.sepolia.org`
- **Explorer**: [sepolia.etherscan.io](https://sepolia.etherscan.io)
- **Native Token**: ETH

#### Faucets
- **Primary Faucet**: [sepoliafaucet.com](https://sepoliafaucet.com)
- **Alchemy Faucet**: [sepoliafaucet.com](https://sepoliafaucet.com)
- **Infura Faucet**: [infura.io/faucet/sepolia](https://infura.io/faucet/sepolia)

#### How to Use
1. Connect your MetaMask to Ethereum Sepolia testnet
2. Visit the faucet website
3. Enter your wallet address
4. Complete CAPTCHA if required
5. Receive test tokens

#### Token Amounts
- **ETH**: 0.1 ETH per request
- **Cooldown**: 24 hours between requests

## MetaMask Configuration

### Adding Testnet Networks

#### Celo Alfajores
```json
{
  "chainId": "0xAEF3",
  "chainName": "Celo Alfajores Testnet",
  "rpcUrls": ["https://alfajores-forno.celo-testnet.org"],
  "nativeCurrency": {
    "name": "CELO",
    "symbol": "CELO",
    "decimals": 18
  },
  "blockExplorerUrls": ["https://explorer.celo.org/alfajores"]
}
```

#### Monad Testnet
```json
{
  "chainId": "0xA1BA",
  "chainName": "Monad Testnet",
  "rpcUrls": ["https://testnet-rpc.monad.xyz"],
  "nativeCurrency": {
    "name": "MON",
    "symbol": "MON",
    "decimals": 18
  },
  "blockExplorerUrls": ["https://testnet-explorer.monad.xyz"]
}
```

#### Berachain Testnet
```json
{
  "chainId": "0x138A5",
  "chainName": "Berachain Testnet",
  "rpcUrls": ["https://testnet-rpc.berachain.com"],
  "nativeCurrency": {
    "name": "BERA",
    "symbol": "BERA",
    "decimals": 18
  },
  "blockExplorerUrls": ["https://testnet-scan.berachain.com"]
}
```

#### Ethereum Sepolia
```json
{
  "chainId": "0xAA36A7",
  "chainName": "Sepolia Testnet",
  "rpcUrls": ["https://rpc.sepolia.org"],
  "nativeCurrency": {
    "name": "ETH",
    "symbol": "ETH",
    "decimals": 18
  },
  "blockExplorerUrls": ["https://sepolia.etherscan.io"]
}
```

## Faucet Best Practices

### 1. **Request Management**
- Don't request tokens more frequently than allowed
- Keep track of your last request time
- Use multiple wallets if needed for testing

### 2. **Security**
- Never share your private keys
- Use testnet tokens only for testing
- Be cautious of phishing sites

### 3. **Efficiency**
- Request only what you need
- Share tokens with team members if possible
- Use gas optimization techniques

### 4. **Troubleshooting**
- Check network connection
- Verify wallet address
- Try different faucets if one is down
- Check Discord for alternative faucets

## Alternative Token Sources

### 1. **Discord Faucets**
Many blockchain projects have Discord servers with faucet bots:
- Join the official Discord server
- Look for faucet channels
- Follow the bot instructions
- Usually faster than web faucets

### 2. **Community Faucets**
- Reddit communities often share faucet links
- Twitter accounts may provide faucet access
- Developer communities share resources

### 3. **Paid Faucets**
- Some services offer paid testnet tokens
- Usually faster and more reliable
- Good for production testing

## Troubleshooting

### Common Issues

#### 1. **Faucet Not Working**
- Check if faucet is operational
- Verify network connection
- Try different browser
- Clear browser cache

#### 2. **Tokens Not Received**
- Wait 5-10 minutes
- Check transaction on block explorer
- Verify wallet address
- Check network configuration

#### 3. **Cooldown Period**
- Wait for cooldown to expire
- Use different wallet address
- Try alternative faucets
- Check Discord for help

#### 4. **Network Issues**
- Verify RPC URL is correct
- Check network status
- Try different RPC endpoint
- Restart MetaMask

### Getting Help

#### 1. **Official Channels**
- Discord servers
- Telegram groups
- GitHub issues
- Documentation

#### 2. **Community Support**
- Reddit communities
- Stack Overflow
- Developer forums
- Social media

#### 3. **Professional Support**
- Paid support services
- Consulting services
- Development teams
- Blockchain experts

## Tips for Success

### 1. **Preparation**
- Set up multiple testnet wallets
- Bookmark faucet websites
- Join Discord servers
- Follow project updates

### 2. **Testing Strategy**
- Start with small amounts
- Test all functions thoroughly
- Use different networks
- Document issues and solutions

### 3. **Resource Management**
- Monitor token balances
- Use gas optimization
- Share resources with team
- Plan testing sessions

### 4. **Documentation**
- Keep track of faucet URLs
- Document network configurations
- Record successful transactions
- Share knowledge with team

## Conclusion

Testnet faucets are essential for blockchain development. By following this guide, you can efficiently obtain test tokens and focus on building your smart contracts and dApps. Remember to use testnet tokens responsibly and always test thoroughly before deploying to mainnet.

---

**Next**: [Useful Links](useful_links.md)
