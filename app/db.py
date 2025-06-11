import sqlite3

DB_PATH = './app/database/history.db'
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS history(
    id INTEGER PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    tokenIn TEXT,
    tokenOut TEXT,
    amountIn TEXT,
    odosOut TEXT,
    odosLatency TEXT,
    oneinchOut TEXT,
    oneinchLatency TEXT,
    best TEXT
)''')
conn.commit()