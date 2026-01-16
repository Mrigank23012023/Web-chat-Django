# Gunicorn Configuration

# Bind to 0.0.0.0 (all interfaces) properly for Render
bind = "0.0.0.0:10000"

# Workers: Reduce to 2 to avoid OOM on free tier (512MB RAM)
# Default was likely 4, which is too high for LangChain + Django
workers = 2

# Increase timeout to 120 seconds to allow for slow imports (langchain/pinecone)
timeout = 120

# Log to stdout for Render
accesslog = "-"
errorlog = "-"
loglevel = "info"
