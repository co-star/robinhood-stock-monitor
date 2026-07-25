# Robinhood Official Stock Token Liquidity Monitor & Web3 LP Manager

An ultra-high precision, state-of-the-art Web3 liquidity monitoring terminal and LP management dashboard for official **Robinhood Stock Tokens (Chain ID 4663 / 7332)** on Uniswap V3 & V4.

## 🌟 Key Features

1. **Official Uniswap Data Integration**:
   - Directly queries Uniswap's official `ListRankedRwas` API for all 20 official Robinhood stock tokens (NVDA, GME, SPCX, TSLA, AAPL, GOOGL, MSFT, COIN, etc.).
   - Filters USDG pools with fee tier $\le 20\%$.

2. **30-Minute Fee Surge Warning System**:
   - Calculates dynamic pool-level 30-minute fee growth rates $\Delta \text{Fee}_{30m}$.
   - Displays dynamic yellow surge alert badges (`⚡ 30m激增 +XX.X%`) when surge $\ge 25\%$.

3. **Uniswap V3 / V4 Pool Comparison Sub-Tables**:
   - Click any stock token row to expand top 5 USDG pools.
   - UI state persistence prevents accidental collapsing during auto-refreshes.

4. **Web3 LP Wallet Position Management (Robinhood Chain)**:
   - Queries real-time LP positions via Uniswap `ListPositions` API.
   - **Real On-Chain Contract Interactions (Ethers.js)**:
     - 💰 `collectFeePos`: Single-click 100% fee extraction.
     - 🚀 `collectAllFees`: One-click batch fee extraction across all Robinhood chain LPs.
     - 📉 `withdrawLpPos`: Safe 2-step removal (`decreaseLiquidity` -> `collect`).
     - ➕ `addLpPos`: Increase LP liquidity directly on-chain.

## 🚀 Live Demo

- **GitHub Pages / Live Site**: [https://co-star.github.io/robinhood-stock-monitor/](https://co-star.github.io/robinhood-stock-monitor/)
- **GitHub Repository**: [https://github.com/co-star/robinhood-stock-monitor](https://github.com/co-star/robinhood-stock-monitor)

## 🛠️ Local Development & Running

### Option 1: Run Web Monitor Service
```bash
python monitor_service.py
```
Then open `http://localhost:8080` in your browser.

### Option 2: Build Standalone Executable
```bash
pyinstaller --noconfirm --onedir --name "Robinhood_Stock_Monitor" --add-data "web;web" --add-data "data;data" app_launcher.py
```

---
*Created for Robinhood Chain LP Traders.*
