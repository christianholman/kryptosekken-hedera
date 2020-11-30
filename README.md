# Usage

1. [Get a DragonGlass API access key](https://app.dragonglass.me/hedera/apiview)

2. Copy the sample env file

```bash
cp .env.sample .env
```

3. Paste your DragonGlass API access key in the `.env`

```env
DRAGONGLASS_API_KEY=xxxxxxxxxxxxx
```

4. Run the program, specifying the Hedera account ID 

```bash
python3 script.py <account-id>
```
