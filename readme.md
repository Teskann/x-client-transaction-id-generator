[![Test workflow](https://github.com/Teskann/x-client-transaction-id-generator/actions/workflows/tests.yml/badge.svg)](https://github.com/Teskann/x-client-transaction-id-generator/actions/workflows/tests.yml)

# X Client transaction server

Wrapper of [XClientTransaction](https://github.com/iSarabjitDhiman/XClientTransaction/) in a Flask server. 🐦

### 🌐 Public instance: [https://x-client-transaction-id-generator.xyz](https://x-client-transaction-id-generator.xyz)

## 🔧 Setup

```bash
chmod +x setup.sh
./setup.sh
```

```bash
python app.py
```

## 📚 API Reference

### `/generate-x-client-transaction-id`

Type: `GET`

Get a `x-client-transaction-id` header value.

**Parameters**:

- `path`: Path to the x API.
  - **Required**
  - Example value: `/i/api/graphql/1VOOyvKkiI3FMmkeDNxM9A/UserByScreenName`

**Returned value**

Type: JSON
```json
{"x-client-transaction-id": "<transaction_id>"}
```

> [!CAUTION]
> If `path` is missing, returns code 400 with response:
> ```json
> {"error": "Missing required parameter 'path'"}
> ```

**Example**

[/generate-x-client-transaction-id?path=/i/api/graphql/1VOOyvKkiI3FMmkeDNxM9A/UserByScreenName](https://x-client-transaction-id-generator.xyz/generate-x-client-transaction-id?path=/i/api/graphql/1VOOyvKkiI3FMmkeDNxM9A/UserByScreenName)

### `/reset-session`

Type: `GET`

Reset the session managing the creation of transaction IDs.

It might be useful to call this once, if the generated `x-client-transaction-id` don't work anymore

**Parameters**:

- `token`: token that gives you the right to reset the session.
An unique token is created when you call run [./setup.sh](./setup.sh) and is stored in
[reset-session-token-secret.txt](./reset-session-token-secret.txt).
The request succeeds only if the passed token matches the one in [reset-session-token-secret.txt](./reset-session-token-secret.txt) 
  - **Required**
  - Example value: `64nHYRvXaWElVBMHPp6xTedpGuzelTgrhOft4ESrzvTQ4whuQKeUO_i-i9s-Oz4QkOQFvgfjxQcvJG5LK9rfmQ==`

**Returned value**

Type: JSON

```json
{"message": "Session reinitialized successfully"}
```

> [!CAUTION]
> If `token` is missing, or invalid, returns 401 error with the following body:
> ```json
> {"error": "Invalid token"}
> ```

**Example**

[/reset-session?token=64nHYRvXaWElVBMHPp6xTedpGuzelTgrhOft4ESrzvTQ4whuQKeUO_i](https://x-client-transaction-id-generator.xyz/reset-session?token=64nHYRvXaWElVBMHPp6xTedpGuzelTgrhOft4ESrzvTQ4whuQKeUO_i)
