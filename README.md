# 🚀 Odos vs 1inch Benchmark

This project benchmarks token swap quotes from **Odos** and **1inch** aggregators. It supports both HTTP API and CLI interfaces to fetch and compare swap quotes.

---

## 📦 Features

- 🖁️ Compare quotes between **Odos** and **1inch**
- 🪪 Batch benchmarking via CLI or API
- ⚡ FastAPI server
- 🐳 Fully containerized with **Docker Compose**
- ✅ Includes **pytest** for testing
- 🧰 Developer CLI powered by **Typer**
- 🔄 Auto-selects the best route (based on `amountOut`)

---

## 🛠 Requirements

- Docker
- Docker Compose

---

## 🚀 Getting Started

### 🔧 Build and Run

```bash
docker compose up --build
```

This will start the FastAPI app at:

```
http://localhost:8000
```

---

## 📱 API Endpoints

### 🔹 Benchmark a Single Quote

**GET** `/benchmark`

**Example:**

```http
http://localhost:8000/benchmark?tokenIn=0xdac17f958d2ee523a2206206994597c13d831ec7&tokenOut=0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9&amount=1000000000000000000
```

**Response:**

```json
{
  "input": {
    "tokenIn": "0xdac17f958d2ee523a2206206994597c13d831ec7",
    "tokenOut": "0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9",
    "amount": 1000000000000000000
  },
  "quotes": {
    "odos": {
      "amountOut": "50409521411203247636480",
      "latencyMs": 3539,
      "route": "odos"
    },
    "1inch": {
      "amountOut": "3040000000",
      "latencyMs": 10000,
      "route": "1inch"
    }
  },
  "best": "odos"
}
```

---

### 🔹 Batch Quote Comparison

**POST** `/benchmark/batch`

**Request:**

```json
{
  "requests": [
    {
      "tokenIn": "0xdac17f958d2ee523a2206206994597c13d831ec7",
      "tokenOut": "0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9",
      "amount": 1000000000000000000
    },
    {
      "tokenIn": "0xdac17f958d2ee523a2206206994597c13d831ec7",
      "tokenOut": "0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9",
      "amount": 1000000000000000000
    }
  ]
}
```

**Response:** Array of comparison results.

---

## 💾 CLI Usage

The CLI is defined in `cli.py` and supports both single and batch quote comparisons.

### 🔹 Inside the container:

#### Enter the container:

```bash
docker exec -it <container_name> bash
```

#### Run a single quote comparison:

```bash
python cli.py run \
  --token-in 0xdac17f958d2ee523a2206206994597c13d831ec7 \
  --token-out 0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9 \
  --amount 1000000000000000000
```

#### Run batch benchmark:

Prepare `batch.json` file:

```json
[
  {
    "tokenIn": "0xdac17f958d2ee523a2206206994597c13d831ec7",
    "tokenOut": "0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9",
    "amount": 1000000000000000000
  },
  {
    "tokenIn": "0xdac17f958d2ee523a2206206994597c13d831ec7",
    "tokenOut": "0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9",
    "amount": 1000000000000000000
  }
]
```

Run:

```bash
python cli.py batch --file batch.json
```

---

## 🪪 Testing

To run tests inside the container:

```bash
docker exec -it <container_name> bash -e
pytest
```

All tests are located in the `tests/` directory.

---

## 📁 Project Structure

```
.
├── app/
│   ├── main.py               # FastAPI app entry
│   ├── models.py             # Pydantic models
│   ├── service/
│   │   └── compare.py        # Routing comparison logic
├── cli.py                    # Typer CLI interface
├── tests/
│   └── test_benchmark.py     # Pytest test suite
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🐋 Docker Compose Setup

### `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### `docker-compose.yml`

```yaml
version: '3.9'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 📌 Notes

- You’ll need valid API keys for **Odos** and **1inch** stored in environment variables or config files.
- Supports mainnet tokens — confirm your token decimals when interpreting results.
- JSON outputs are automatically pretty-printed.

---

## 📨 Contributing

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/feature-name`)
3. Commit your changes
4. Push to the branch (`git push origin feature/feature-name`)
5. Open a Pull Request

---

## 📜 License

MIT License

