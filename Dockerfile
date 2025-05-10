# ✅ Use Node.js base image
FROM node:18-slim

# Set working directory
WORKDIR /app

# ✅ Install system packages needed for Python + pip
RUN apt-get update && apt-get install -y python3 python3-pip

# ✅ Create isolated Python environment (prevents system package issues)
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# ✅ Install Python dependencies inside venv
RUN pip install --no-cache-dir requests

# ✅ Copy Node.js dependencies
COPY package*.json ./
RUN npm install

# ✅ Copy all project files (handler.ts, rofl-agent/, Python scripts, etc)
COPY . .

# ✅ Run handler.ts with ts-node ESM mode
CMD ["node", "--loader", "ts-node/esm", "rofl-agent/handler.ts", "0x1f371bB099180FAfA5d8bAd44498cC13A4cefBd8"]

