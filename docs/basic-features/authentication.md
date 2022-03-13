# Authentication


```python
headers = {
    'x-api-key': 'your_api_key',
}
```

```shell
# With shell, you can just pass the correct header with each request
curl "api_endpoint_here" \
  -H "x-api-key: your_api_key"
```

```javascript
const headers = {
  'x-api-key': 'your_api_key'
}
```
> Make sure to replace `your_api_key` with your own API key.

Palenca uses API keys to allow access to the API.

The API key must be included in all API requests in a header that looks like the following:

`x-api-key: your_api_key`

<aside class="notice">
You must replace <code>your_api_key</code> with your personal API key.
</aside>
