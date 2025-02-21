# TapTools - API Documentation

## OpenAPI
```
openapi: 3.0.0
```

## Info

**Title:** TapTools - API Documentation  
**Version:** 1.7.2  
**Description:**
```
TapTools is a data provider that offers onchain data for assets on the Cardano network.

# Introduction
This API includes many of the same endpoints that power the [TapTools website](https://taptools.io).
We have indexed onchain market data for both fungible and non-fungible tokens, as well as
included endpoints to query raw onchain data.

# Rate Limiting
This API implements rate limiting to ensure resources aren’t overwhelmed. This rate limit varies by plan.
```
**Terms of Service"**: https://taptools.io/terms  
**Contact:**
```
name: API Support
url: https://taptools.io
email: support@taptools.io
```
**x-logo:**
```
url: https://taptools-public.s3.amazonaws.com/images/taptools-name.png
altText: TapTools
```

---

## Servers
1. **URL:** https://openapi.taptools.io/api/v1  
   **Description:** TapTools OpenAPI

---

## Security

The API key must be provided in the header as `x-api-key`.

```
security:
  - ApiAuthKey:
      - x-api-key
```

---

## Tags & Tag Groups

```yaml
tags:
  - name: Metrics
  - name: Market
  - name: "Market » NFTs"
  - name: "Market » Tokens"
  - name: "Onchain » Asset"
  - name: "Onchain » Address"
  - name: "Onchain » Transaction"
  - name: "Wallet » Portfolio"
  - name: Integration

x-tagGroups:
  - name: Metrics
    tags:
      - Metrics
  - name: Market
    tags:
      - Market
      - "Market » NFTs"
      - "Market » Tokens"
  - name: Onchain
    tags:
      - "Onchain » Asset"
      - "Onchain » Address"
      - "Onchain » Transaction"
  - name: Wallet
    tags:
      - "Wallet » Portfolio"
  - name: Integration
    tags:
      - Integration
```

---

## Paths

Below are all paths, their methods, parameters, and response schemas.

### **GET** `/address/info`
**Tag:** Onchain » Address  
**Summary:** Address info  
**Description:**  
Get address payment credential and stake address, along with its current aggregate lovelace and multi asset balance.  
Either `address` or `paymentCred` can be provided, but one must be provided.

**Parameters:**
- `address` (query, string, optional)  
  Example: `addr1q9j5jqhqak5nmqphdqt4cj9kq0gppa49afyznggw03hjzhwxr0exydkt78th5wwrjphxh0h6rrgghzwxse6q3pdf9sxqkg2mmq`
- `paymentCred` (query, string, optional)  
  Example: `654902e0eda93d803768175c48b603d010f6a5ea4829a10e7c6f215d`

**Responses:**
- **200**: Address info  
  Content: `application/json` → `#/components/schemas/onchain_address_info`
- **400**: Bad Request  
  Content: `application/json` → `#/components/responses/400`
- **401**: Not authorized  
  Content: `application/json` → `#/components/responses/401`
- **404**: Item not found  
  Content: `application/json` → `#/components/responses/404`
- **429**: Rate limit exceeded  
  Content: `application/json` → `#/components/responses/429`
- **500**: Internal Server Error  
  Content: `application/json` → `#/components/responses/500`

---

### **GET** `/address/utxos`
**Tag:** Onchain » Address  
**Summary:** Address UTxOs  
**Description:**  
Get current UTxOs at an address/payment credential. Either `address` or `paymentCred` can be provided, but one must be provided.

**Parameters:**
- `address` (query, string, optional)  
  Example: `addr1q9j5jqhqak5nmqphdqt4cj9kq0gppa49afyznggw03hjzhwxr0exydkt78th5wwrjphxh0h6rrgghzwxse6q3pdf9sxqkg2mmq`
- `paymentCred` (query, string, optional)  
  Example: `654902e0eda93d803768175c48b603d010f6a5ea4829a10e7c6f215d`
- `page` (query, integer, optional)  
  Default: 1
- `perPage` (query, integer, optional)  
  Maximum: 100, Default: 100

**Responses:**
- **200**: Address UTxOs  
  Content: `application/json` → `#/components/schemas/onchain_address_utxos`
- **400**, **401**, **404**, **429**, **500** (same as above)

---

### **GET** `/asset/supply`
**Tag:** Onchain » Asset  
**Summary:** Asset supply  
**Description:**  
Get onchain supply for a token.

**Parameters:**
- `unit` (query, string, required)  
  Example: `8fef2d34078659493ce161a6c7fba4b56afefa8535296a5743f6958741414441`

**Responses:**
- **200**: Asset supply  
  Content: `application/json` → `#/components/schemas/onchain_asset_supply`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/integration/asset`
**Tag:** Integration  
**Summary:** Token by ID  
**Description:**  
Returns details of a given token by its address.

**Parameters:**
- `id` (query, string, required)  
  Example: `b46b12f0a61721a0358988f806a7c1562e1e622d5886a73194051f336d6131`

**Responses:**
- **200**: Token info  
  Content: `application/json` → `#/components/schemas/integration_asset`
- **400**, **401**, **429**, **500**

---

### **GET** `/integration/block`
**Tag:** Integration  
**Summary:** Block  
**Description:**  
Returns a specific block using either the number of the block or its timestamp.

**Parameters:**
- `number` (query, integer, optional)  
  Example: `10937538`
- `timestamp` (query, integer, optional)  
  Example: `1728408176`

**Responses:**
- **200**: Block info  
  Content: `application/json` → `#/components/schemas/integration_block`
- **400**, **401**, **429**, **500**

---

### **GET** `/integration/events`
**Tag:** Integration  
**Summary:** Events  
**Description:**  
List of events occurred in a range of blocks.

**Parameters:**
- `fromBlock` (query, integer, required)  
  Example: `10937538`
- `toBlock` (query, integer, required)  
  Example: `10937542`
- `limit` (query, integer, optional)  
  Defaults to `1000`, maximum of `1000`.

**Responses:**
- **200**: Events info  
  Content: `application/json` → `#/components/schemas/integration_events`
- **400**, **401**, **429**, **500**

---

### **GET** `/integration/exchange`
**Tag:** Integration  
**Summary:** DEX  
**Description:**  
Return details of a given DEX by its factory address or alternative id.

**Parameters:**
- `id` (query, string, required)  
  Example: `7`

**Responses:**
- **200**: Exchange info  
  Content: `application/json` → `#/components/schemas/integration_exchange`
- **400**, **401**, **429**, **500**

---

### **GET** `/integration/latest-block`
**Tag:** Integration  
**Summary:** Latest block  
**Description:**  
Returns the latest block processed in the blockchain/DEX.

**Parameters:** None

**Responses:**
- **200**: Block info  
  Content: `application/json` → `#/components/schemas/integration_latest_block`
- **400**, **401**, **429**, **500**

---

### **GET** `/integration/pair`
**Tag:** Integration  
**Summary:** Pair by ID  
**Description:**  
Returns pair details (aka pool) by its address.

**Parameters:**
- `id` (query, string, required)  
  Example: `nikeswaporderbook.44759dc63605dbf88700b241ee451aa5b0334cf2b34094d836fbdf8642757a7a696542656520.ada`

**Responses:**
- **200**: Pair info  
  Content: `application/json` → `#/components/schemas/integration_pair`
- **400**, **401**, **429**, **500**

---

### **GET** `/market/stats`
**Tag:** Market  
**Summary:** Market stats  
**Description:**  
Get aggregated market stats, including 24h DEX volume and total active addresses onchain.

**Parameters:**
- `quote` (query, string, optional)  
  Quote currency to use (`ADA`, `USD`, `EUR`, `ETH`, `BTC`). Default: `ADA`

**Responses:**
- **200**:  
  Content: `application/json` → `#/components/schemas/market_stats_response`
- **400**, **401**, **429**, **500**

---

### **GET** `/metrics`
**Tag:** Metrics  
**Summary:** Number of requests  
**Description:**  
Get the number of requests made by day over the last 30d.

**Parameters:** None

**Responses:**
- **200**:  
  Content: `application/json` → `#/components/schemas/metrics`
- **400**, **401**, **429**, **500**

---

### **GET** `/nft/asset/sales`
**Tag:** Market » NFTs  
**Summary:** NFT sale history  
**Description:**  
Get a specific asset’s sale history.

**Parameters:**
- `policy` (query, string, required)  
  Example: `40fa2aa67258b4ce7b5782f74831d46a84c59a0ff0c28262fab21728`
- `name` (query, string, optional)  
  Example: `ClayNation3725`

**Responses:**
- **200**: NFT Sale History  
  Content: `application/json` → `#/components/schemas/market_nft_asset_sales`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/nft/asset/stats`
**Tag:** Market » NFTs  
**Summary:** NFT stats  
**Description:**  
Get high-level stats on a certain NFT asset.

**Parameters:**
- `policy` (query, string, required)
- `name` (query, string, required)

**Responses:**
- **200**: NFT stats  
  Content: `application/json` → `#/components/schemas/market_nft_asset_stats`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/nft/asset/traits`
**Tag:** Market » NFTs  
**Summary:** NFT traits  
**Description:**  
Get a specific NFT’s traits and trait prices.

**Parameters:**
- `policy` (query, string, required)
- `name` (query, string, required)
- `prices` (query, string, optional)  
  `0` or `1`. Default: `1`

**Responses:**
- **200**: NFT traits  
  Content: `application/json` → `#/components/schemas/market_nft_asset_traits`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/nft/collection/assets`
**Tag:** Market » NFTs  
**Summary:** Collection assets  
**Description:**  
Get all NFTs from a collection, with ability to sort/filter by traits, price/rank, etc.

**Parameters:**
- `policy` (query, string, required)
- `sortBy` (query, string, optional)  
  Options: `price`, `rank`. Default: `price`
- `order` (query, string, optional)  
  Options: `asc`, `desc`. Default: `asc`
- `search` (query, string, optional)
- `onSale` (query, string, optional)  
  `0` or `1`. Default: `0`
- `page` (query, integer, optional)  
  Default: `1`
- `perPage` (query, integer, optional)  
  Max: `100`, Default: `100`

**Responses:**
- **200**: Collection assets  
  Content: `application/json` → `#/components/schemas/market_nft_collection_assets`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/nft/collection/holders/distribution`
**Tag:** Market » NFTs  
**Summary:** Holder distribution  
**Description:**  
Get distribution of NFTs in a collection by grouping how many NFTs each holder has.

**Parameters:**
- `policy` (query, string, required)

**Responses:**
- **200**: Collection holder distribution  
  Content: `application/json` → `#/components/schemas/market_nft_collection_holders_distribution`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/nft/collection/holders/top`
**Tag:** Market » NFTs  
**Summary:** Top holders  
**Description:**  
Get top holders for a collection.

**Parameters:**
- `policy` (query, string, required)
- `page` (query, integer, optional)  
  Default: `1`
- `perPage` (query, integer, optional)  
  Max: `100`, Default: `10`
- `excludeExchanges` (query, integer, optional)  
  `0` or `1`

**Responses:**
- **200**: Collection top holders  
  Content: `application/json` → `#/components/schemas/market_nft_collection_holders_top`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/nft/collection/holders/trended`
**Tag:** Market » NFTs  
**Summary:** Trended holders  
**Description:**  
Get holders trended by day for a particular NFT collection.

**Parameters:**
- `policy` (query, string, required)
- `timeframe` (query, string, optional)  
  Options: `7d`, `30d`, `90d`, `180d`, `1y`, `all`. Default: `30d`

**Responses:**
- **200**: Collection trended holders  
  Content: `application/json` → `#/components/schemas/market_nft_collection_holders_trended`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/nft/collection/info`
**Tag:** Market » NFTs  
**Summary:** Collection info  
**Description:**  
Get basic info about a collection (name, socials, logo, etc.).

**Parameters:**
- `policy` (query, string, required)

**Responses:**
- **200**: Collection info  
  Content: `application/json` → `#/components/schemas/market_nft_collection_info`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/nft/collection/listings`
**Tag:** Market » NFTs  
**Summary:** Number of active listings  
**Description:**  
Get the amount of active listings and total supply for a collection.

**Parameters:**
- `policy` (query, string, required)

**Responses:**
- **200**: Active listings  
  Content: `application/json` → `#/components/schemas/market_nft_collection_listings`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/nft/collection/listings/depth`
**Tag:** Market » NFTs  
**Summary:** NFT listings depth  
**Description:**  
Get cumulative amount of listings at each price point, from floor upward.

**Parameters:**
- `policy` (query, string, required)
- `items` (query, integer, optional)  
  Max: `1000`, default `500`

**Responses:**
- **200**: Depth data  
  Content: `application/json` → `#/components/schemas/market_nft_collection_listings_depth`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/nft/collection/listings/individual`
**Tag:** Market » NFTs  
**Summary:** Get list of active listings  
**Description:**  
List active listings with supporting information, supports pagination and sorting.

**Parameters:**
- `policy` (query, string, required)
- `sortBy` (query, string, optional)  
  `price` or `time`. Default: `price`
- `order` (query, string, optional)  
  `asc` or `desc`. Default: `asc`
- `page` (query, integer, optional)  
  Default: `1`
- `perPage` (query, integer, optional)  
  Max: `100`, Default: `100`

**Responses:**
- **200**: NFT collection listings  
  Content: `application/json` → `#/components/schemas/market_nft_collection_listings_individual`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/nft/collection/listings/trended`
**Tag:** Market » NFTs  
**Summary:** NFT listings trended  
**Description:**  
Get trended number of listings and floor price for a collection.

**Parameters:**
- `policy` (query, string, required)
- `interval` (query, string, required)  
  Options: `3m`, `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `12h`, `1d`, `3d`, `1w`, `1M`
- `numIntervals` (query, integer, optional)

**Responses:**
- **200**: NFT collection trended listings  
  Content: `application/json` → `#/components/schemas/market_nft_collection_listings_trended`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/nft/collection/ohlcv`
**Tag:** Market » NFTs  
**Summary:** NFT floor price OHLCV  
**Description:**  
Get OHLCV data (open, high, low, close, volume) of floor price for a collection.

**Parameters:**
- `policy` (query, string, required)
- `interval` (query, string, required)
- `numIntervals` (query, integer, optional)

**Responses:**
- **200**: NFT collection OHLCV  
  Content: `application/json` → `#/components/schemas/market_nft_collection_ohlcv`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/nft/collection/stats`
**Tag:** Market » NFTs  
**Summary:** Collection stats  
**Description:**  
Get basic stats about a collection (floor price, volume, supply, etc.).

**Parameters:**
- `policy` (query, string, required)

**Responses:**
- **200**: Collection stats  
  Content: `application/json` → `#/components/schemas/market_nft_collection_stats`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/nft/collection/stats/extended`
**Tag:** Market » NFTs  
**Summary:** Collection stats (extended)  
**Description:**  
Similar to `/nft/collection/stats`, but includes % changes.

**Parameters:**
- `policy` (query, string, required)
- `timeframe` (query, string, optional)  
  Options: `24h`, `7d`, `30d`. Default: `24h`

**Responses:**
- **200**: Extended stats  
  Content: `application/json` → `#/components/schemas/market_nft_collection_stats_extended`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/nft/collection/trades`
**Tag:** Market » NFTs  
**Summary:** Trades  
**Description:**  
Get individual trades for a collection or entire NFT market (if no policy passed).

**Parameters:**
- `policy` (query, string, optional)
- `timeframe` (query, string, optional)  
  Options: `1h`, `4h`, `24h`, `7d`, `30d`, `90d`, `180d`, `1y`, `all`. Default: `30d`
- `sortBy` (query, string, optional)  
  `amount` or `time`. Default: `time`
- `order` (query, string, optional)  
  `asc` or `desc`. Default: `desc`
- `minAmount` (query, integer, optional)
- `from` (query, integer, optional) (UNIX timestamp)
- `page` (query, integer, optional)  
  Default: `1`
- `perPage` (query, integer, optional)  
  Max: `100`, Default: `100`

**Responses:**
- **200**: Individual trades  
  Content: `application/json` → `#/components/schemas/market_nft_collection_trades`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/nft/collection/trades/stats`
**Tag:** Market » NFTs  
**Summary:** Trading stats  
**Description:**  
Get trading stats like volume and sales for a collection.

**Parameters:**
- `policy` (query, string, required)
- `timeframe` (query, string, optional)  
  `1h`, `4h`, `24h`, `7d`, `30d`, `all`. Default: `24h`

**Responses:**
- **200**: Trading stats  
  Content: `application/json` → `#/components/schemas/market_nft_collection_trades_stats`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/nft/collection/traits/price`
**Tag:** Market » NFTs  
**Summary:** Collection trait prices  
**Description:**  
Get a list of traits in a collection and each trait’s floor price.

**Parameters:**
- `policy` (query, string, required)
- `name` (query, string, optional)

**Responses:**
- **200**: Collection trait prices  
  Content: `application/json` → `#/components/schemas/market_nft_collection_traits_price`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/nft/collection/traits/rarity`
**Tag:** Market » NFTs  
**Summary:** Collection metadata rarity  
**Description:**  
Get every metadata attribute and how likely it is to occur within the NFT collection.

**Parameters:**
- `policy` (query, string, required)

**Responses:**
- **200**: Collection metadata rarity  
  Content: `application/json` → `#/components/schemas/market_nft_collection_rarity`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/nft/collection/traits/rarity/rank`
**Tag:** Market » NFTs  
**Summary:** NFT rarity rank  
**Description:**  
Get rank of an NFT’s rarity within a collection.

**Parameters:**
- `policy` (query, string, required)
- `name` (query, string, required)

**Responses:**
- **200**: NFT rarity rank  
  Content: `application/json` → `#/components/schemas/market_nft_collection_rarity_rank`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/nft/collection/volume/trended`
**Tag:** Market » NFTs  
**Summary:** NFT volume trended  
**Description:**  
Get trended volume and sales for a collection.

**Parameters:**
- `policy` (query, string, required)
- `interval` (query, string, required)
- `numIntervals` (query, integer, optional)

**Responses:**
- **200**: NFT collection trended volume  
  Content: `application/json` → `#/components/schemas/market_nft_collection_volume_trended`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/nft/market/stats`
**Tag:** Market » NFTs  
**Summary:** Market-wide NFT stats  
**Description:**  
Get high-level market stats across the entire NFT market.

**Parameters:**
- `timeframe` (query, string, required)  
  Options: `1h`, `4h`, `24h`, `7d`, `30d`, `all`. Default: `24h`

**Responses:**
- **200**: NFT market stats  
  Content: `application/json` → `#/components/schemas/market_nft_market_stats`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/nft/market/stats/extended`
**Tag:** Market » NFTs  
**Summary:** Market-wide NFT stats (extended)  
**Description:**  
Like `/nft/market/stats` but with more fields (pctChg, etc.).

**Parameters:**
- `timeframe` (query, string, required)

**Responses:**
- **200**: Extended NFT market stats  
  Content: `application/json` → `#/components/schemas/market_nft_market_stats_extended`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/nft/market/volume/trended`
**Tag:** Market » NFTs  
**Summary:** NFT market volume  
**Description:**  
Get trended volume for entire NFT market.

**Parameters:**
- `timeframe` (query, string, required)  
  `7d`, `30d`, `90d`, `180d`, `1y`, `all`. Default: `30d`

**Responses:**
- **200**: NFT market volume trended  
  Content: `application/json` → `#/components/schemas/market_nft_market_volume_trended`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/nft/marketplace/stats`
**Tag:** Market » NFTs  
**Summary:** NFT Marketplace stats  
**Description:**  
Get high-level NFT marketplace stats.

**Parameters:**
- `timeframe` (query, string, optional)  
  `24h`, `7d`, `30d`, `90d`, `180d`, `all`. Default: `7d`
- `marketplace` (query, string, optional)
- `lastDay` (query, integer, optional)  
  `0` or `1`

**Responses:**
- **200**: NFT marketplace stats  
  Content: `application/json` → `#/components/schemas/market_nft_marketplace_stats`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/nft/top/timeframe`
**Tag:** Market » NFTs  
**Summary:** NFT top rankings  
**Description:**  
Get top NFT rankings based on total market cap, volume, or top price gainers/losers.

**Parameters:**
- `ranking` (query, string, required)  
  Options: `marketCap`, `volume`, `gainers`, `losers`
- `items` (query, integer, optional)  
  Max: `100`, Default: `25`

**Responses:**
- **200**: NFT Top Rankings  
  Content: `application/json` → `#/components/schemas/market_nft_top_timeframe`
- **400**, **401**, **404**, **406**, **429**, **500**

---

### **GET** `/nft/top/volume`
**Tag:** Market » NFTs  
**Summary:** Top volume collections  
**Description:**  
Get top NFT collections by trading volume over a given timeframe.

**Parameters:**
- `timeframe` (query, string, optional)  
  `1h`, `4h`, `24h`, `7d`, `30d`, `all`. Default: `24h`
- `page` (query, integer, optional)  
  Default: `1`
- `perPage` (query, integer, optional)  
  Max: `100`, Default: `10`

**Responses:**
- **200**: Top NFT collections by volume  
  Content: `application/json` → `#/components/schemas/market_nft_top_volume`
- **400**, **401**, **429**, **500**

---

### **GET** `/nft/top/volume/extended`
**Tag:** Market » NFTs  
**Summary:** Top volume collections (extended)  
**Description:**  
Same as `/nft/top/volume` but with percent changes included.

**Parameters:**
- `timeframe` (query, string, optional)  
- `page` (query, integer, optional)  
  Default: `1`
- `perPage` (query, integer, optional)  
  Max: `100`, Default: `10`

**Responses:**
- **200**: Top NFT collections by volume (extended)  
  Content: `application/json` → `#/components/schemas/market_nft_top_volume_extended`
- **400**, **401**, **429**, **500**

---

### **GET** `/token/debt/loans`
**Tag:** Market » Tokens  
**Summary:** Active loans  
**Description:**  
Get active P2P loans for a token (Lenfi, Levvy).

**Parameters:**
- `unit` (query, string, required)
- `include` (query, string, optional)  
  Comma separated: `collateral,debt,interest` (default: `collateral,debt`)
- `sortBy` (query, string, optional)  
  `time` or `expiration`. Default: `time`
- `order` (query, string, optional)  
  `asc` or `desc`. Default: `desc`
- `page` (query, integer, optional)  
- `perPage` (query, integer, optional)  
  Default: `100`

**Responses:**
- **200**: P2P loans  
  Content: `application/json` → `#/components/schemas/token_debt_loans_response`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/token/debt/offers`
**Tag:** Market » Tokens  
**Summary:** Loan offers  
**Description:**  
Get active P2P loan offers not associated with any loan (Lenfi, Levvy).

**Parameters:**
- `unit` (query, string, required)
- `include` (query, string, optional)  
  Default: `collateral,debt`
- `sortBy` (query, string, optional)  
  `time` or `duration`. Default: `time`
- `order` (query, string, optional)  
  Default: `desc`
- `page` (query, integer, optional)  
- `perPage` (query, integer, optional)  
  Default: `100`

**Responses:**
- **200**: P2P offers  
  Content: `application/json` → `#/components/schemas/token_debt_offers_response`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/token/holders`
**Tag:** Market » Tokens  
**Summary:** Token holders  
**Description:**  
Get total number of holders for a specific token, aggregated by stake key.

**Parameters:**
- `unit` (query, string, required)

**Responses:**
- **200**: Number of holders  
  Content: `application/json` → `#/components/schemas/token_holders_response`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/token/holders/top`
**Tag:** Market » Tokens  
**Summary:** Top token holders  
**Description:**  
Get top token holders.

**Parameters:**
- `unit` (query, string, required)
- `page` (query, integer, optional)  
  Default: `1`
- `perPage` (query, integer, optional)  
  Max: `100`, Default: `20`

**Responses:**
- **200**: Top holders  
  Content: `application/json` → `#/components/schemas/token_holders_top_response`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/token/indicators`
**Tag:** Market » Tokens  
**Summary:** Token price indicators  
**Description:**  
Get indicator values (EMA, RSI, MACD, etc.) for a token.

**Parameters:**  
- `unit` (required)  
- `interval` (required)  
- `items` (optional)  
- `indicator` (optional)  
  Options: `ma`, `ema`, `rsi`, `macd`, `bb`, `bbw`
- `length` (optional)  
- `smoothingFactor` (optional)  
- `fastLength`, `slowLength`, `signalLength` (for MACD)  
- `stdMult` (optional, for Bollinger Bands)  
- `quote` (optional)

**Responses:**
- **200**: Token indicator values  
  Content: `application/json` → `#/components/schemas/token_indicators_response`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/token/links`
**Tag:** Market » Tokens  
**Summary:** Token links  
**Description:**  
Get a token’s social links.

**Parameters:**
- `unit` (query, string, required)

**Responses:**
- **200**: Token links  
  Content: `application/json` → `#/components/schemas/token_links_response`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/token/mcap`
**Tag:** Market » Tokens  
**Summary:** Token market cap  
**Description:**  
Get supply and market cap info for a token.

**Parameters:**
- `unit` (query, string, required)

**Responses:**
- **200**: Supply & market cap  
  Content: `application/json` → `#/components/schemas/token_mcap_response`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/token/ohlcv`
**Tag:** Market » Tokens  
**Summary:** Token price OHLCV  
**Description:**  
Get aggregated or pair-specific OHLCV data for a token.

**Parameters:**
- `unit` (query, string, optional)
- `onchainID` (query, string, optional)
- `interval` (query, string, required)
- `numIntervals` (query, integer, optional)

**Responses:**
- **200**: Token OHLCV data  
  Content: `application/json` → `#/components/schemas/token_ohlcv_response`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/token/pools`
**Tag:** Market » Tokens  
**Summary:** Token liquidity pools  
**Description:**  
Get a token’s active liquidity pools or a specific pool by `onchainID`.

**Parameters:**
- `unit` (query, string, optional)
- `onchainID` (query, string, optional)
- `adaOnly` (query, integer, optional)  
  `0` or `1`

**Responses:**
- **200**: Liquidity pools  
  Content: `application/json` → `#/components/schemas/token_pools_response`
- **400**, **401**, **404**, **429**, **500**

---

### **POST** `/token/prices`
**Tag:** Market » Tokens  
**Summary:** Token prices  
**Description:**  
Get token prices in a batch. Max batch size: 100 tokens.

**Request Body**:
- JSON array of token units

**Responses:**
- **200**: Prices  
  Content: `application/json` → `#/components/schemas/token_prices_response`
- **400**, **401**, **429**, **500**

---

### **GET** `/token/prices/chg`
**Tag:** Market » Tokens  
**Summary:** Token price percent change  
**Description:**  
Get a token’s price percent change over various timeframes.

**Parameters:**
- `unit` (query, string, required)
- `timeframes` (query, string, optional)  
  e.g. `1h,4h,24h,7d,30d`

**Responses:**
- **200**: Price changes  
  Content: `application/json` → `#/components/schemas/token_prices_chg_response`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/token/quote`
**Tag:** Market » Tokens  
**Summary:** Quote price  
**Description:**  
Get current quote price (like ADA/USD).

**Parameters:**
- `quote` (query, string, optional)  
  `USD`, `EUR`, `ETH`, `BTC`. Default: `USD`

**Responses:**
- **200**: Current Quote price  
  Content: `application/json` → `#/components/schemas/token_quote_response`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/token/quote/available`
**Tag:** Market » Tokens  
**Summary:** Available quote currencies  
**Description:**  
Get all currently available quote currencies.

**Parameters:** None

**Responses:**
- **200**: Available quote currencies  
  Content: `application/json` → `#/components/schemas/token_quote_available_response`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/token/top/liquidity`
**Tag:** Market » Tokens  
**Summary:** Top liquidity tokens  
**Description:**  
Get tokens ranked by DEX liquidity (AMM and order book combined).

**Parameters:**
- `page` (query, integer, optional)  
  Default: `1`
- `perPage` (query, integer, optional)  
  Max: `100`, Default: `10`

**Responses:**
- **200**: Top liquidity tokens  
  Content: `application/json` → `#/components/schemas/token_top_liquidity_response`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/token/top/mcap`
**Tag:** Market » Tokens  
**Summary:** Top market cap tokens  
**Description:**  
Get tokens with top market cap in descending order.

**Parameters:**
- `type` (query, string, optional)  
  `mcap` or `fdv`
- `page` (query, integer, optional)  
  Default: `1`
- `perPage` (query, integer, optional)  
  Max: `100`, Default: `20`

**Responses:**
- **200**: Top market cap tokens  
  Content: `application/json` → `#/components/schemas/token_top_mcap_response`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/token/top/volume`
**Tag:** Market » Tokens  
**Summary:** Top volume tokens  
**Description:**  
Get tokens with top volume for a given timeframe.

**Parameters:**
- `timeframe` (query, string, optional)  
  `[1h, 4h, 12h, 24h, 7d, 30d, 180d, 1y, all]`. Default: `24h`
- `page` (query, integer, optional)  
  Default: `1`
- `perPage` (query, integer, optional)  
  Max: `100`, Default: `20`

**Responses:**
- **200**: Top volume tokens  
  Content: `application/json` → `#/components/schemas/token_top_volume_response`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/token/trades`
**Tag:** Market » Tokens  
**Summary:** Token trades  
**Description:**  
Get token trades across the entire DEX market.

**Parameters:**
- `timeframe` (query, string, optional)  
  Default: `30d`
- `sortBy` (query, string, optional)  
  `amount` or `time`. Default: `amount`
- `order` (query, string, optional)  
  `asc` or `desc`. Default: `desc`
- `unit` (query, string, optional)
- `minAmount` (query, integer, optional)
- `from` (query, integer, optional)  
  UNIX timestamp
- `page` (query, integer, optional)
- `perPage` (query, integer, optional)  
  Max: `100`, Default: `10`

**Responses:**
- **200**: Token trades  
  Content: `application/json` → `#/components/schemas/token_market_trades_response`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/token/trading/stats`
**Tag:** Market » Tokens  
**Summary:** Trading stats  
**Description:**  
Get aggregated trading stats (buy/sell volume, # of buyers/sellers, etc.) for a token.

**Parameters:**
- `unit` (query, string, required)
- `timeframe` (query, string, optional)  
  `[15m, 1h, 4h, 12h, 24h, 7d, 30d, 90d, 180d, 1y, all]`. Default: `24h`

**Responses:**
- **200**: Trading stats  
  Content: `application/json` → `#/components/schemas/token_trading_stats_response`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/transaction/utxos`
**Tag:** Onchain » Transaction  
**Summary:** Transaction UTxOs  
**Description:**  
Get UTxOs from a specific transaction.

**Parameters:**
- `hash` (query, string, optional)

**Responses:**
- **200**: Transaction UTxOs  
  Content: `application/json` → `#/components/schemas/onchain_transaction_utxos`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/wallet/portfolio/positions`
**Tag:** Wallet » Portfolio  
**Summary:** Portfolio positions  
**Description:**  
Get a wallet’s current portfolio positions with market data.

**Parameters:**
- `address` (query, string, optional)

**Responses:**
- **200**: Portfolio positions  
  Content: `application/json` → `#/components/schemas/portfolio_positions_response`
- **400**, **401**, **404**, **429**, **500**

---

### **GET** `/wallet/trades/tokens`
**Tag:** Wallet » Portfolio  
**Summary:** Trade history (tokens)  
**Description:**  
Get the token trade history for a particular wallet, optionally filter by token unit.

**Parameters:**
- `address` (query, string, required)
- `unit` (query, string, optional)
- `page` (query, integer, optional)
- `perPage` (query, integer, optional)  
  Max: `100`, Default: `100`

**Responses:**
- **200**: Wallet trade history  
  Content: `application/json` → `#/components/schemas/wallet_trades_tokens_response`
- **400**, **401**, **404**, **406**, **429**, **500**

---

### **GET** `/wallet/value/trended`
**Tag:** Wallet » Portfolio  
**Summary:** Portfolio trended value  
**Description:**  
Get historical trended value of an address in 4hr intervals.

**Parameters:**
- `address` (query, string, required)
- `timeframe` (query, string, optional)  
  `[24h, 7d, 30d, 90d, 180d, 1y, all]`. Default: `30d`
- `quote` (query, string, optional)  
  `[ADA, USD, EUR, ETH, BTC]`. Default: `ADA`

**Responses:**
- **200**: Portfolio trended value  
  Content: `application/json` → `#/components/schemas/portfolio_value_trended_response`
- **400**, **401**, **404**, **406**, **429**, **500**

---

## Components

### Security Schemes

```yaml
securitySchemes:
  ApiAuthKey:
    type: apiKey
    name: x-api-key
    in: header
    description: "Contact TapTools to get an API key"
```

### Responses

Below are the common response components used throughout:

#### 400
```yaml
description: Bad Request
content:
  application/json:
    schema:
      type: object
      properties:
        error:
          type: string
          example: "Bad Request"
        message:
          type: string
          example: "Ensure all required parameters are passed"
        status:
          type: integer
          example: 400
```

#### 401
```yaml
description: Not Authorized
content:
  application/json:
    schema:
      type: object
      properties:
        error:
          type: string
          example: "Not authorized"
        message:
          type: string
          example: "Ensure you are using a valid API key"
        status:
          type: integer
          example: 401
```

#### 404
```yaml
description: Not Found
content:
  application/json:
    schema:
      type: object
      properties:
        error:
          type: string
          example: "Item not found"
        message:
          type: string
          example: "Could not find item based on query parameters"
        status:
          type: integer
          example: 404
```

#### 406
```yaml
description: Not acceptable
content:
  application/json:
    schema:
      type: object
      properties:
        error:
          type: string
          example: "Not acceptable"
        message:
          type: string
          example: "Invalid query parameters"
        status:
          type: integer
          example: 406
```

#### 429
```yaml
description: Rate Limit Exceeded
content:
  application/json:
    schema:
      type: object
      properties:
        error:
          type: string
          example: "Rate limit exceeded"
        message:
          type: string
          example: "Your rate limit has been exceeded"
        status:
          type: integer
          example: 429
```

#### 500
```yaml
description: Interval Server Error
content:
  application/json:
    schema:
      type: object
      properties:
        error:
          type: string
          example: "Internal Server Error"
        message:
          type: string
          example: "An unexpected response was received from the backend."
        status:
          type: integer
          example: 500
```

---

### Schemas

Below are all schemas referenced in the specification.

#### `integration_asset`
```yaml
type: object
required:
  - asset
properties:
  asset:
    type: object
    example:
      id: "b46b12f0a61721a0358988f806a7c1562e1e622d5886a73194051f336d6131"
      name: "snek coin"
      symbol: "SNEK"
      circulatingSupply: 1500000
      totalSupply: 2000000
```

#### `integration_block`
```yaml
type: object
required:
  - block
properties:
  block:
    type: object
    example:
      blockNumber: 10937538
      blockTimestamp: 1728408176
```

#### `integration_events`
```yaml
type: object
required:
  - events
properties:
  events:
    type: array
    items:
      description: UTxOs
      type: object
      required:
        - block
        - txnId
        - txnIndex
        - eventIndex
        - maker
        - pairId
        - eventType
        - amount0
        - amount1
        - asset0In
        - asset1Out
        - asset0Out
        - asset1In
        - reserves
      properties:
        amount0:
          type: string
        amount1:
          type: string
        asset0In:
          type: string
          example: "0"
        asset0Out:
          type: string
          example: "200"
        asset1In:
          type: string
          example: "10"
        asset1Out:
          type: string
          example: "0"
        block:
          type: object
          required:
            - blockNumber
            - blockTimestamp
          example:
            blockNumber: 10937538
            blockTimestamp: 1728408176
        eventIndex:
          type: integer
          example: 10937538000000
        eventType:
          type: string
          example: "swap"
        maker:
          type: string
          example: "addr1q8ete2wpeulwq5yxutftpqdmgu2rntld85x7ztswahs2t0daytnqe6ea4p09jpv8mz3umpsdk9gkqvkhca7nngxrp2lqnh0x4l"
        pairId:
          type: string
          example: "nikeswaporderbook.44759dc63605dbf88700b241ee451aa5b0334cf2b34094d836fbdf8642757a7a696542656520.ada"
        reserves:
          type: object
          required:
            - asset0
            - asset1
          example:
            asset0: "20000000"
            asset1: "10000"
        txnId:
          type: string
          example: "a88d97638faf9fa63e4f4f8b4fd4664ae3505ae050bc48afde48f3c1e7b1e07b"
        txnIndex:
          type: integer
          example: 115981434
```

#### `integration_exchange`
```yaml
type: object
required:
  - exchange
properties:
  exchange:
    type: object
    example:
      factoryAddress: "3"
      name: "Minswap"
      logoURL: "https://www.logos.com/minswap.png"
```

#### `integration_latest_block`
```yaml
type: object
required:
  - block
properties:
  block:
    type: object
    example:
      blockNumber: 10937538
      blockTimestamp: 1728408176
```

#### `integration_pair`
```yaml
type: object
required:
  - pair
properties:
  pair:
    type: object
    example:
      asset0Id: "279c909f348e533da5808898f87f9a14bb2c3dfbbacccd631d927a3f534e454b"
      asset1Id: "000000000000000000000000000000000000000000000000000000006c6f76656c616365"
      createdAtBlockNumber: 10937538
      createdAtBlockTimestamp: 1728408176
      createdAtTxnId: 115981434
      factoryAddress: "4"
      id: "nikeswaporderbook.44759dc63605dbf88700b241ee451aa5b0334cf2b34094d836fbdf8642757a7a696542656520.ada"
```

#### `market_nft_asset_sales`
```yaml
type: array
items:
  description: NFT Sales.
  type: object
  required:
    - buyerStakeAddress
    - price
    - sellerStakeAddress
    - time
  properties:
    buyerStakeAddress:
      type: string
      example: "stake1address2"
    price:
      type: number
      example: 8000
    sellerStakeAddress:
      type: string
      example: "stake1address1"
    time:
      type: integer
      example: 16000840
```

#### `market_nft_asset_stats`
```yaml
type: object
required:
  - timesListed
  - owners
  - sales
  - volume
  - lastSoldTime
  - lastSoldPrice
  - lastListedTime
  - lastListedPrice
  - isListed
properties:
  isListed:
    type: bool
    example: true
  lastListedPrice:
    type: number
    example: 3850
  lastListedTime:
    type: integer
    example: 160002490
  lastSoldPrice:
    type: number
    example: 4800
  lastSoldTime:
    type: integer
    example: 160008490
  owners:
    type: integer
    example: 6
  sales:
    type: integer
    example: 5
  timesListed:
    type: integer
    example: 8
  volume:
    type: number
    example: 54234
```

#### `market_nft_asset_traits`
```yaml
type: object
required:
  - rank
  - traits
properties:
  rank:
    type: integer
    example: 51
  traits:
    type: array
    items:
      description: Traits info
      type: object
      required:
        - category
        - name
        - rarity
        - price
      properties:
        category:
          type: string
          example: "background"
        name:
          type: string
          example: "red"
        rarity:
          type: number
          example: 0.4
        price:
          type: number
          example: 100
```

#### `market_nft_collection_assets`
```yaml
type: array
items:
  description: Collection assets.
  type: object
  required:
    - name
    - rank
    - price
    - image
  properties:
    image:
      type: string
      example: "ipfs://QmeDi3J1exQYnGAuwZv7b6sAuDBAo2hYdAMM1KGgS7KFa4"
    name:
      type: string
      example: "ClayNation3725"
    price:
      type: number
      example: 20
    rank:
      type: integer
      example: 2
```

#### `market_nft_collection_holders_distribution`
```yaml
type: object
required:
  - "1"
  - "2-4"
  - "5-9"
  - "10-24"
  - "25+"
properties:
  "1":
    type: integer
    example: 1154
  "2-4":
    type: integer
    example: 631
  "5-9":
    type: integer
    example: 327
  "10-24":
    type: integer
    example: 60
  "25+":
    type: integer
    example: 2
```

#### `market_nft_collection_holders_top`
```yaml
type: array
items:
  description: Top collection holders
  type: object
  required:
    - address
    - amount
  properties:
    address:
      type: string
      example: "stake1u8mvwfn298a4dkm92hrgeupnnuzhxfwl5lauzuejl5cf8esrtjn6w"
    amount:
      type: integer
      example: 27
```

#### `market_nft_collection_holders_trended`
```yaml
type: array
items:
  description: Trended collection holders
  type: object
  required:
    - time
    - holders
  properties:
    holders:
      type: integer
      example: 3125
    time:
      type: integer
      example: 1705874400
```

#### `market_nft_collection_info`
```yaml
type: object
required:
  - name
  - logo
  - supply
  - twitter
  - discord
  - website
  - description
properties:
  description:
    type: string
    example: "The Ape Society is a collection of 7,000 NFTs generated on the Cardano blockchain."
  discord:
    type: string
    example: "https://discord.gg/theapesociety"
  logo:
    type: string
    example: "ipfs://QmVT8QGerKMLaJkxdUqefw7V7fjccGgcKjLnbMavisELsf"
  name:
    type: string
    example: "The Ape Society"
  supply:
    type: integer
    example: 10000
  twitter:
    type: string
    example: "https://twitter.com/the_ape_society"
  website:
    type: string
    example: "https://www.theapesociety.io/"
```

#### `market_nft_collection_listings`
```yaml
type: object
required:
  - listings
  - supply
properties:
  listings:
    type: integer
    example: 168
  supply:
    type: integer
    example: 1000
```

#### `market_nft_collection_listings_depth`
```yaml
type: array
items:
  description: Listings depth
  type: object
  required:
    - count
    - price
    - avg
    - total
  properties:
    avg:
      type: number
      example: 4850.0
    count:
      type: integer
      example: 96
    price:
      type: number
      example: 9600.0
    total:
      type: number
      example: 456000.0
```

#### `market_nft_collection_listings_individual`
```yaml
type: array
items:
  description: Information about listing
  type: object
  required:
    - name
    - image
    - price
    - time
  properties:
    image:
      type: string
      example: "ipfs://QmdnZKmDWd85BLKfsHnrJExRKE71zPGawwy7jWhc2wBwmM"
    market:
      type: string
      example: "jpg.store"
    name:
      type: string
      example: "ClayNation3725"
    price:
      type: number
      example: 4925
    time:
      type: integer
      example: 1680135943
```

#### `market_nft_collection_listings_trended`
```yaml
type: array
items:
  description: Listings
  type: object
  required:
    - time
    - listings
    - price
  properties:
    listings:
      type: integer
      example: 592
    price:
      type: number
      example: 205
    time:
      type: integer
      example: 1680574100
```

#### `market_nft_collection_ohlcv`
```yaml
type: array
items:
  description: OHLCV interval
  type: object
  required:
    - time
    - open
    - high
    - low
    - close
    - volume
  properties:
    close:
      type: number
      example: 4150
    high:
      type: number
      example: 4150
    low:
      type: number
      example: 3950
    open:
      type: number
      example: 4000
    time:
      type: integer
      example: 1680574100
    volume:
      type: number
      example: 61480
```

#### `market_nft_collection_rarity`
```yaml
type: object
properties:
  Accessories:
    type: object
    example:
      Bowtie: 0.0709
      Collar: 0.1184
  Background:
    type: object
    example:
      Cyan: 0.1316
      Lilac: 0.147
```

#### `market_nft_collection_rarity_rank`
```yaml
type: object
required:
  - rank
properties:
  rank:
    type: integer
    example: 7346
```

#### `market_nft_collection_stats`
```yaml
type: object
required:
  - volume
  - supply
  - price
  - owners
  - listings
  - topOffer
properties:
  listings:
    type: integer
    example: 673
  owners:
    type: integer
    example: 1124
  price:
    type: number
    example: 450
  sales:
    type: integer
    example: 4782
  supply:
    type: integer
    example: 10000
  topOffer:
    type: number
    example: 400
  volume:
    type: number
    example: 16844521
```

#### `market_nft_collection_stats_extended`
```yaml
type: object
required:
  - listings
  - listingsPctChg
  - owners
  - ownersPctChg
  - price
  - pricePctChg
  - supply
  - volume
  - volumePctChg
  - sales
  - salesPctChg
  - topOffer
properties:
  listings:
    type: integer
    example: 673
  listingsPctChg:
    type: number
    example: 0.11
  owners:
    type: integer
    example: 1124
  ownersPctChg:
    type: number
    example: 0.05
  price:
    type: number
    example: 450
  pricePctChg:
    type: number
    example: 0.024
  sales:
    type: integer
    example: 5431
  salesPctChg:
    type: number
    example: 0.008
  supply:
    type: integer
    example: 10000
  topOffer:
    type: number
    example: 380
  volume:
    type: number
    example: 16844521
  volumePctChg:
    type: number
    example: 0.014
```

#### `market_nft_collection_trades`
```yaml
type: array
items:
  description: Information about trade
  type: object
  required:
    - name
    - price
    - market
    - time
    - image
    - buyerAddress
    - sellerAddress
    - policy
    - collectionName
    - hash
  properties:
    buyerAddress:
      type: string
      example: "addr1qxvpuw8dmmwvzs4lvjmuamn7l748n9wuvrumuz27v8mt6kzktn257cny8gcw0f99ft99apqdakca6grf9stpptjdyevqffsm7e"
    collectionName:
      type: string
      example: "Clay Nation"
    hash:
      type: string
      example: "505cb5a55f7bbe0ed70e58d97b105220ea662fb91bbd89e915ca85f07500a9b9"
    image:
      type: string
      example: "ipfs://QmdnZKmDWd85BLKfsHnrJExRKE71zPGawwy7jWhc2wBwmM"
    market:
      type: string
      example: "jpg.store"
    name:
      type: string
      example: "ClayNation3725"
    policy:
      type: string
      example: "40fa2aa67258b4ce7b5782f74831d46a84c59a0ff0c28262fab21728"
    price:
      type: number
      example: 4925
    sellerAddress:
      type: string
      example: "addr1q9wmpjmp767fewhqswq89lua7csns8a704hrjljdt5r40ssstt62h0erkvx72zarcydnlldp0sj0ml02w3k06r8mpy8qm8eqkf"
    time:
      type: integer
      example: 1680135943
```

#### `market_nft_collection_trades_stats`
```yaml
type: object
required:
  - volume
  - sales
  - buyers
  - sellers
properties:
  buyers:
    type: integer
    example: 35
  sales:
    type: integer
    example: 42
  sellers:
    type: integer
    example: 16
  volume:
    type: number
    example: 247521
```

#### `market_nft_collection_traits_price`
```yaml
type: object
description: Collection Traits Prices.
properties:
  background:
    type: object
    example:
      blue: 5
      red: 8
  hair:
    type: object
    example:
      black: 10
      blonde: 30
```

#### `market_nft_collection_volume_trended`
```yaml
type: array
items:
  description: Volume
  type: object
  required:
    - time
    - volume
    - sales
    - price
  properties:
    price:
      type: number
      example: 205
    sales:
      type: integer
      example: 153
    time:
      type: integer
      example: 1680574100
    volume:
      type: number
      example: 12034
```

#### `market_nft_market_stats`
```yaml
type: object
required:
  - volume
  - sales
  - addresses
  - buyers
  - sellers
properties:
  addresses:
    type: integer
    example: 5321
  buyers:
    type: integer
    example: 3451
  sales:
    type: integer
    example: 7832
  sellers:
    type: integer
    example: 3110
  volume:
    type: number
    example: 876345
```

#### `market_nft_market_stats_extended`
```yaml
type: object
required:
  - volume
  - volumePctChg
  - sales
  - salesPctChg
  - addresses
  - addressesPctChg
  - buyers
  - buyersPctChg
  - sellers
  - sellersPctChg
properties:
  addresses:
    type: integer
    example: 5321
  addressesPctChg:
    type: number
    example: -0.11
  buyers:
    type: integer
    example: 3451
  buyersPctChg:
    type: number
    example: 0.08
  sales:
    type: integer
    example: 7832
  salesPctChg:
    type: number
    example: 0.02
  sellers:
    type: integer
    example: 3110
  sellersPctChg:
    type: number
    example: -0.15
  volume:
    type: number
    example: 876345
  volumePctChg:
    type: number
    example: 0.08
```

#### `market_nft_market_volume_trended`
```yaml
type: array
items:
  description: Trended NFT market volume
  type: object
  required:
    - time
    - value
  properties:
    time:
      type: integer
      example: 1690171200
    value:
      type: number
      example: 783125
```

#### `market_nft_marketplace_stats`
```yaml
type: array
items:
  description: Marketplace stats
  type: object
  required:
    - name
    - volume
    - sales
    - avgSale
    - listings
    - users
    - fees
    - liquidity
    - royalties
  properties:
    avgSale:
      type: number
      example: 100.5
    fees:
      type: number
      example: 41210.512
    liquidity:
      type: number
      example: 14341.1231
    listings:
      type: integer
      example: 300
    name:
      type: string
      example: "jpg.store"
    royalties:
      type: number
      example: 645432.3123
    sales:
      type: integer
      example: 7832
    users:
      type: integer
      example: 5321
    volume:
      type: number
      example: 876345.312
```

#### `market_nft_top_timeframe`
```yaml
type: array
items:
  description: NFT Rankings.
  type: object
  required:
    - rank
    - price24hChg
    - price7dChg
    - price30dChg
    - listings
    - logo
    - marketCap
    - name
    - policy
    - price
    - supply
    - volume24h
    - volume7d
    - volume30d
    - volume24hChg
    - volume7dChg
    - volume30dChg
  properties:
    listings:
      type: integer
      example: 15
    logo:
      type: string
      example: "https://linktologo4.com"
    marketCap:
      type: number
      example: 25000
    name:
      type: string
      example: "testCollection4"
    policy:
      type: string
      example: "e3ff4ab89245ede61b3e2beab0443dbcc7ea8ca2c017478e4e8990e2"
    price:
      type: number
      example: 500
    price24hChg:
      type: number
      example: 0.5
    price7dChg:
      type: number
      example: 0.6
    price30dChg:
      type: number
      example: 0.7
    rank:
      type: integer
      example: 1
    supply:
      type: integer
      example: 50
    volume24h:
      type: number
      example: 4000
    volume24hChg:
      type: number
      example: 0.11
    volume30d:
      type: number
      example: 6000
    volume30dChg:
      type: number
      example: 0.05
    volume7d:
      type: number
      example: 5000
    volume7dChg:
      type: number
      example: -0.11
```

#### `market_nft_top_volume`
```yaml
type: object
required:
  - policy
  - name
  - logo
  - price
  - volume
  - listings
  - supply
  - sales
properties:
  listings:
    type: integer
    example: 583
  logo:
    type: string
    example: "ipfs://QmZ3mjsA4YL58HZQ6pxhAp1EaibmTi15uzTNAmDekZDzNf"
  name:
    type: string
    example: "Stag Alliance"
  policy:
    type: string
    example: "1fcf4baf8e7465504e115dcea4db6da1f7bed335f2a672e44ec3f94e"
  price:
    type: integer
    example: 175
  sales:
    type: integer
    example: 215
  supply:
    type: integer
    example: 7200
  volume:
    type: integer
    example: 49606
```

#### `market_nft_top_volume_extended`
```yaml
type: object
required:
  - policy
  - name
  - logo
  - price
  - pricePctChg
  - volume
  - volumePctChg
  - listings
  - listingsPctChg
  - supply
  - sales
  - salesPctChg
  - holders
  - holdersPctChg
properties:
  listings:
    type: integer
    example: 583
  listingsPctChg:
    type: number
    example: 0.11
  logo:
    type: string
    example: "ipfs://QmZ3mjsA4YL58HZQ6pxhAp1EaibmTi15uzTNAmDekZDzNf"
  name:
    type: string
    example: "Stag Alliance"
  owners:
    type: integer
    example: 542
  ownersPctChg:
    type: number
    example: -0.031
  policy:
    type: string
    example: "1fcf4baf8e7465504e115dcea4db6da1f7bed335f2a672e44ec3f94e"
  price:
    type: integer
    example: 175
  pricePctChg:
    type: number
    example: 0.024
  sales:
    type: integer
    example: 50
  salesPctChg:
    type: number
    example: 0.34
  supply:
    type: integer
    example: 7200
  volume:
    type: integer
    example: 49606
  volumePctChg:
    type: number
    example: 0.014
```

#### `market_stats_response`
```yaml
type: object
properties:
  activeAddresses:
    type: integer
    example: 24523
  dexVolume:
    type: float
    example: 8134621.35
```

#### `metrics`
```yaml
type: array
items:
  description: Requests count
  type: object
  required:
    - time
    - calls
  properties:
    calls:
      type: integer
      example: 4837
    time:
      type: integer
      example: 1692781200
```

#### `onchain_address_info`
```yaml
type: object
required:
  - address
  - paymentCred
  - lovelace
  - assets
properties:
  address:
    type: string
    example: "addr1q9j5jqhqak5nmqphdqt4cj9kq0gppa49afyznggw03hjzhwxr0exydkt78th5wwrjphxh0h6rrgghzwxse6q3pdf9sxqkg2mmq"
  assets:
    type: array
    items:
      description: Native asset balances
      type: object
      required:
        - unit
        - quantity
      properties:
        unit:
          type: string
          example: "dda5fdb1002f7389b33e036b6afee82a8189becb6cba852e8b79b4fb0014df1047454e53"
        value:
          type: string
          example: "12000000"
  lovelace:
    type: string
    example: "45000000"
  paymentCred:
    type: string
    example: "654902e0eda93d803768175c48b603d010f6a5ea4829a10e7c6f215d"
  stakeAddress:
    type: string
    example: "stake1u8rphunzxm9lr4m688peqmnthmap35yt38rgvaqgsk5jcrqdr2vuc"
```

#### `onchain_address_utxos`
```yaml
type: array
items:
  description: UTxOs
  type: object
  required:
    - hash
    - index
    - lovelace
    - assets
  properties:
    assets:
      type: array
      items:
        description: Native asset balances
        type: object
        required:
          - unit
          - quantity
        properties:
          unit:
            type: string
            example: "dda5fdb1002f7389b33e036b6afee82a8189becb6cba852e8b79b4fb0014df1047454e53"
          quantity:
            type: string
            example: "12000000"
    hash:
      type: string
      example: "a88d97638faf9fa63e4f4f8b4fd4664ae3505ae050bc48afde48f3c1e7b1e07b"
    index:
      type: integer
      example: 0
    lovelace:
      type: string
      example: "3703342"
```

#### `onchain_asset_supply`
```yaml
type: object
required:
  - supply
properties:
  supply:
    type: number
    example: 233838354
```

#### `onchain_transaction_utxos`
```yaml
type: object
required:
  - hash
  - inputs
  - outputs
properties:
  hash:
    type: string
    example: "8be33680ec04da1cc98868699c5462fbbf6975529fb6371669fa735d2972d69b"
  inputs:
    type: array
    items:
      description: UTxOs
      type: object
      required:
        - hash
        - index
        - lovelace
        - assets
      properties:
        hash:
          type: string
          example: "a88d97638faf9fa63e4f4f8b4fd4664ae3505ae050bc48afde48f3c1e7b1e07b"
        index:
          type: integer
          example: 0
        lovelace:
          type: string
          example: "3703342"
        assets:
          type: array
          items:
            description: Native asset balances
            type: object
            required:
              - unit
              - quantity
            properties:
              unit:
                type: string
                example: "dda5fdb1002f7389b33e036b6afee82a8189becb6cba852e8b79b4fb0014df1047454e53"
              quantity:
                type: string
                example: "12000000"
  outputs:
    type: array
    items:
      description: UTxOs
      type: object
      required:
        - hash
        - index
        - lovelace
        - assets
      properties:
        hash:
          type: string
          example: "a88d97638faf9fa63e4f4f8b4fd4664ae3505ae050bc48afde48f3c1e7b1e07b"
        index:
          type: integer
          example: 0
        lovelace:
          type: string
          example: "3703342"
        assets:
          type: array
          items:
            description: Native asset balances
            type: object
            required:
              - unit
              - quantity
            properties:
              unit:
                type: string
                example: "dda5fdb1002f7389b33e036b6afee82a8189becb6cba852e8b79b4fb0014df1047454e53"
              quantity:
                type: string
                example: "12000000"
```

#### `portfolio_positions_response`
```yaml
type: object
required:
  - adaValue
  - adaBalance
  - numFTs
  - numNFTs
  - liquidValue
  - positionsFt
  - positionsNft
  - positionsLp
properties:
  adaBalance:
    type: number
    example: 10
  adaValue:
    type: number
    example: 10010
  liquidValue:
    type: number
    example: 10010
  numFTs:
    type: integer
    example: 2
  numNFTs:
    type: integer
    example: 1
  positionsFt:
    type: array
    items:
      description: Fungible token positions
      type: object
      required:
        - ticker
        - balance
        - unit
        - fingerprint
        - price
        - adaValue
        - 24h
        - 7d
        - 30d
        - liquidBalance
        - liquidValue
      properties:
        "24h":
          type: number
          example: 0.11
        "7d":
          type: number
          example: 0.03
        "30d":
          type: number
          example: -0.32
        adaValue:
          type: number
          example: 10000
        balance:
          type: number
          example: 200
        fingerprint:
          type: string
          example: "fingerprint1"
        liquidBalance:
          type: number
          example: 200
        liquidValue:
          type: number
          example: 10000
        price:
          type: number
          example: 100
        ticker:
          type: string
          example: "TEST1"
        unit:
          type: string
          example: "b46b12f0a61721a0358988f806a7c1562e1e622d5886a73194051f336d6131"
  positionsLp:
    type: array
    items:
      description: LP tokens positions
      type: object
      required:
        - ticker
        - unit
        - amountLP
        - tokenA
        - tokenAName
        - tokenAAmount
        - tokenB
        - tokenBName
        - tokenBAmount
        - adaValue
        - exchange
      properties:
        adaValue:
          type: number
          example: 400
        amountLP:
          type: number
          example: 100
        exchange:
          type: string
          example: "Minswap"
        ticker:
          type: string
          example: "TEST2 / ADA LP"
        tokenA:
          type: string
          example: "63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32"
        tokenAAmount:
          type: number
          example: 100
        tokenAName:
          type: string
          example: "TEST2"
        tokenB:
          type: string
        tokenBAmount:
          type: number
          example: 200
        tokenBName:
          type: string
          example: "ADA"
        unit:
          type: string
          example: "f22d56bc0daec9ff1e2d4d90061563517d279d3c998747d55234822874657374746f6b656e"
  positionsNft:
    type: array
    items:
      description: Non-fungible token positions
      type: object
      required:
        - name
        - policy
        - balance
        - adaValue
        - floorPrice
        - 24h
        - 7d
        - 30d
        - listings
        - liquidValue
      properties:
        "24h":
          type: number
          example: 0.11
        "7d":
          type: number
          example: 0.03
        "30d":
          type: number
          example: -0.32
        adaValue:
          type: number
          example: 10000
        balance:
          type: integer
          example: 2
        floorPrice:
          type: number
          example: 1
        liquidValue:
          type: number
          example: 10
        listings:
          type: integer
          example: 3
        name:
          type: string
          example: "testCollection"
        policy:
          type: string
          example: "4048d53202b57aec6eb8edd8e9e4196d8eeb9a5fe1dd50d6dfc67be3"
```

#### `portfolio_value_trended_response`
```yaml
type: array
items:
  description: Interval value
  type: object
  required:
    - time
    - value
  properties:
    time:
      type: integer
      example: 1692781200
    value:
      type: number
      example: 57
```

#### `token_debt_loans_response`
```yaml
type: array
items:
  description: Active P2P Loan
  type: object
  required:
    - time
    - expiration
    - hash
    - protocol
    - interestToken
    - debtToken
    - collateralToken
    - interestAmount
    - debtAmount
    - collateralAmount
    - interestValue
    - debtValue
    - collateralValue
    - health
  properties:
    collateralAmount:
      type: number
      example: 120.131
    collateralToken:
      type: string
      example: "b46b12f0a61721a0358988f806a7c1562e1e622d5886a73194051f336d6131"
    collateralValue:
      type: number
      example: 84.466
    debtAmount:
      type: number
      example: 100
    debtToken:
      type: string
      example: "b46b12f0a61721a0358988f806a7c1562e1e622d5886a73194051f336d6131"
    debtValue:
      type: number
      example: 70.3123
    expiration:
      type: integer
      example: 1722995180
    hash:
      type: string
      example: "0002464b78a10d0a0dc6345666764caf519befa28d2ccb2efc711376320d54ef"
    health:
      type: number
      example: 1.172
    interestAmount:
      type: number
      example: 2.131
    interestToken:
      type: string
      example: "b46b12f0a61721a0358988f806a7c1562e1e622d5886a73194051f336d6131"
    interestValue:
      type: number
      example: 1.75
    protocol:
      type: string
      example: "Levvy"
    time:
      type: integer
      example: 1721908780
```

#### `token_debt_offers_response`
```yaml
type: array
items:
  description: Active P2P Offer
  type: object
  required:
    - time
    - duration
    - hash
    - protocol
    - interestToken
    - debtToken
    - collateralToken
    - interestAmount
    - debtAmount
    - collateralAmount
    - interestValue
    - debtValue
    - collateralValue
    - health
  properties:
    collateralAmount:
      type: number
      example: 120.131
    collateralToken:
      type: string
      example: "b46b12f0a61721a0358988f806a7c1562e1e622d5886a73194051f336d6131"
    collateralValue:
      type: number
      example: 84.466
    debtAmount:
      type: number
      example: 100
    debtToken:
      type: string
      example: "b46b12f0a61721a0358988f806a7c1562e1e622d5886a73194051f336d6131"
    debtValue:
      type: number
      example: 70.3123
    duration:
      type: integer
      example: 1209600
    hash:
      type: string
      example: "0002464b78a10d0a0dc6345666764caf519befa28d2ccb2efc711376320d54ef"
    health:
      type: number
      example: 1.172
    interestAmount:
      type: number
      example: 2.131
    interestToken:
      type: string
      example: "b46b12f0a61721a0358988f806a7c1562e1e622d5886a73194051f336d6131"
    interestValue:
      type: number
      example: 1.75
    protocol:
      type: string
      example: "Levvy"
    time:
      type: integer
      example: 1692781200
```

#### `token_holders_response`
```yaml
type: object
properties:
  holders:
    type: integer
    example: 1024
```

#### `token_holders_top_response`
```yaml
type: array
items:
  description: Token holder
  type: object
  required:
    - address
    - amount
  properties:
    address:
      type: string
      example: "stake1uyqj8nukxpcal7h6zdjr958wfk5yhqcns2ard8c7appyd0gt06k67"
    amount:
      type: number
      example: 13432.34
```

#### `token_indicators_response`
```yaml
type: array
items:
  description: Token indicator data
  type: integer
  example: 2.33521
```

#### `token_links_response`
```yaml
type: object
properties:
  description:
    type: string
    example: "LENFI is a utility token integral to a decentralized lending and borrowing protocol on the Cardano blockchain"
  discord:
    type: string
    example: "https://discord.gg/lenfi"
  email:
    type: string
    example: "project@gmail.com"
  facebook:
    type: string
    example: "https://www.facebook.com/WorldMobileTeam/"
  github:
    type: string
    example: "https://github.com/lenfiLabs"
  instagram:
    type: string
    example: "https://www.instagram.com/WorldMobileTeam/"
  medium:
    type: string
  reddit:
    type: string
    example: "https://www.reddit.com/r/worldmobile/"
  telegram:
    type: string
    example: "http://t.me/lenfi"
  twitter:
    type: string
    example: "https://twitter.com/LenfiOfficial"
  website:
    type: string
    example: "https://lenfi.io"
  youtube:
    type: string
    example: "https://www.youtube.com/@WorldMobileTeam"
```

#### `token_market_trades_response`
```yaml
type: array
items:
  description: Token trades
  type: object
  required:
    - tokenA
    - tokenAName
    - tokenB
    - tokenBName
    - tokenAAmount
    - tokenBAmount
    - action
    - time
    - exchange
    - address
    - price
    - hash
    - lpTokenUnit
  properties:
    action:
      type: string
      example: "buy"
    address:
      type: string
      example: "addr1q9j5jqhqak5nmqphdqt4cj9kq0gppa49afyznggw03hjzhwxr0exydkt78th5wwrjphxh0h6rrgghzwxse6q3pdf9sxqkg2mmq"
    exchange:
      type: string
      example: "Minswap"
    hash:
      type: string
      example: "8df1c6f66c0d02153f604ea588e792582908d3299ef6d322ae0448001791a24f"
    lpTokenUnit:
      type: string
      example: "f5808c2c990d86da54bfc97d89cee6efa20cd8461616359478d96b4c35e27e3c7b4bef4824e5a4989a97e017fb8a1156d9823c20821e4d2f1fa168e4"
    price:
      type: number
      example: 100
    time:
      type: integer
      example: 1692781200
    tokenA:
      type: string
      example: "63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32"
    tokenAAmount:
      type: number
      example: 100
    tokenAName:
      type: string
      example: "TEST2"
    tokenB:
      type: string
    tokenBAmount:
      type: number
      example: 200
    tokenBName:
      type: string
      example: "ADA"
```

#### `token_mcap_response`
```yaml
type: object
required:
  - ticker
  - circSupply
  - totalSupply
  - price
  - mcap
  - fdv
properties:
  circSupply:
    type: number
    example: 1036194689.027126
  fdv:
    type: number
    example: 184018358.12
  mcap:
    type: number
    example: 63559615.43
  price:
    type: number
    example: 0.0613
  ticker:
    type: string
    example: "MIN"
  totalSupply:
    type: number
    example: 3000000000
```

#### `token_ohlcv_response`
```yaml
type: array
items:
  description: Token ohlcv data
  type: object
  required:
    - time
    - open
    - high
    - low
    - close
    - volume
  properties:
    close:
      type: number
      example: 1.33
    high:
      type: number
      example: 1.38
    low:
      type: number
      example: 1.33
    open:
      type: number
      example: 1.34
    time:
      type: integer
      example: 1692738000
    volume:
      type: number
      example: 103432.3324
```

#### `token_pools_response`
```yaml
type: array
items:
  description: Pool info
  type: object
  required:
    - tokenA
    - tokenATicker
    - tokenB
    - tokenBTicker
    - lpTokenUnit
    - onchainID
    - tokenALocked
    - tokenBLocked
    - exchange
properties:
  exchange:
    type: string
    example: "Minswap"
  lpTokenUnit:
    type: string
    example: "e4214b7cce62ac6fbba385d164df48e157eae5863521b4b67ca71d8639b9b709ac8605fc82116a2efc308181ba297c11950f0f350001e28f0e50868b"
  onchainID:
    type: string
    example: "0be55d262b29f564998ff81efe21bdc0022621c12f15af08d0f2ddb1.39b9b709ac8605fc82116a2efc308181ba297c11950f0f350001e28f0e50868b"
  tokenA:
    type: string
    example: "8fef2d34078659493ce161a6c7fba4b56afefa8535296a5743f6958741414441"
  tokenALocked:
    type: number
    example: 522963.34
  tokenATicker:
    type: string
    example: "LENFI"
  tokenB:
    type: string
    example: "{empty for ADA}"
  tokenBLocked:
    type: number
    example: 4393379.12
  tokenBTicker:
    type: string
    example: "ADA"
```

#### `token_prices_body`
```yaml
type: array
items:
  type: string
  example: "dda5fdb1002f7389b33e036b6afee82a8189becb6cba852e8b79b4fb0014df1047454e53"
```

#### `token_prices_chg_response`
```yaml
type: object
properties:
  "1h":
    type: number
    example: 0.007
  "4h":
    type: number
    example: -0.061
  "5m":
    type: number
    example: 0.024
```

#### `token_prices_response`
```yaml
type: object
required:
  - unit
  - price
properties:
  dda5fdb1002f7389b33e036b6afee82a8189becb6cba852e8b79b4fb0014df1047454e53:
    type: number
    example: 5.0
```

#### `token_quote_available_response`
```yaml
type: array
items:
  type: string
  example: "USD"
```

#### `token_quote_response`
```yaml
type: object
required:
  - price
properties:
  price:
    type: number
    example: 0.61
```

#### `token_top_liquidity_response`
```yaml
type: array
items:
  description: Top liquidity tokens
  type: object
  required:
    - unit
    - ticker
    - price
    - liquidity
  properties:
    liquidity:
      type: number
      example: 504421.3324
    price:
      type: number
      example: 0.537
    ticker:
      type: string
      example: "AGIX"
    unit:
      type: string
      example: "b46b12f0a61721a0358988f806a7c1562e1e622d5886a73194051f336d6131"
```

#### `token_top_mcap_response`
```yaml
type: array
items:
  description: Top market cap tokens
  type: object
  required:
    - unit
    - ticker
    - price
    - mcap
    - fdv
    - circSupply
    - totalSupply
  properties:
    circSupply:
      type: number
      example: 1252742236.022414
    fdv:
      type: number
      example: 1074222392.55
    mcap:
      type: number
      example: 689889366.5
    price:
      type: number
      example: 0.537
    ticker:
      type: string
      example: "AGIX"
    totalSupply:
      type: number
      example: 1374050373.74311
    unit:
      type: string
      example: "b46b12f0a61721a0358988f806a7c1562e1e622d5886a73194051f336d6131"
```

#### `token_top_volume_response`
```yaml
type: array
items:
  description: Top volume tokens
  type: object
  required:
    - unit
    - ticker
    - price
    - volume
  properties:
    price:
      type: number
      example: 0.537
    ticker:
      type: string
      example: "AGIX"
    unit:
      type: string
      example: "b46b12f0a61721a0358988f806a7c1562e1e622d5886a73194051f336d6131"
    volume:
      type: number
      example: 103432.3324
```

#### `token_trading_stats_response`
```yaml
type: object
required:
  - buyers
  - sellers
  - buyVolume
  - sellVolume
  - buys
  - sells
properties:
  buyVolume:
    type: number
    example: 234123.342
  buyers:
    type: integer
    example: 134
  buys:
    type: integer
    example: 189
  sellVolume:
    type: number
    example: 187432.654
  sellers:
    type: integer
    example: 89
  sells:
    type: integer
    example: 92
```

#### `wallet_trades_tokens_response`
```yaml
type: array
items:
  description: Wallet trades
  type: object
  required:
    - action
    - time
    - tokenA
    - tokenAName
    - tokenAAmount
    - tokenB
    - tokenBName
    - tokenBAmount
  properties:
    action:
      type: string
      example: "Buy"
    hash:
      type: string
      example: "505cb5a55f7bbe0ed70e58d97b105220ea662fb91bbd89e915ca85f07500a9b9"
    time:
      type: integer
      example: 1692781200
    tokenA:
      type: string
      example: "63bb8054f9142b46582198e280f489b3c928dfecb390b0cb39a5cbfe74657374746f6b656e32"
    tokenAAmount:
      type: number
      example: 10
    tokenAName:
      type: string
      example: "TEST1"
    tokenB:
      type: string
    tokenBAmount:
      type: number
      example: 5
    tokenBName:
      type: string
      example: "ADA"
```
