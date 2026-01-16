# Gunicorn Configuration

# Bind to 0.0.0.0 (all interfaces) properly for Render
bind = "0.0.0.0:10000"

# Workers: Reduce to 1 to avoid OOM on free tier (512MB RAM)
# Even 2 workers is too much for LangChain + Pinecone
workers = 1

# Increase timeout to 120 seconds to allow for slow imports (langchain/pinecone)
timeout = 120

# Log to stdout for Render
accesslog = "-"
errorlog = "-"
loglevel = "info"
