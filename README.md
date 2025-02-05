# Zabbix Host & Group Fetcher  

## Description  
A Flask-based API to fetch host and group data from a Zabbix server and serve it for external use, such as Grafana integration.  

## Setup  

### **1. Clone the Repository**  
```bash
git clone https://github.com/rlggyp/zabbix-host-group-fetcher.git
cd zabbix-host-group-fetcher 
```

### **2. Create a Virtual Environment**  
```bash
cd src/
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### **3. Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **4. Configure Environment Variables**  
edit a `.env` file in the project root and add:  
```env
ZABBIX_URL=http://your-zabbix-server/zabbix/api_jsonrpc.php
ZABBIX_USER=Admin
ZABBIX_PASSWORD=zabbix
```

## How to Run  
```bash
python src/main.py
```

The API will start at `http://0.0.0.0:5000` or `http://localhost:5000` or `http://your_ip_address:5000`.

### **Available Endpoints**  

- **GET /host** → Returns a rotating host from the Zabbix server.  
- **GET /group** → Returns a rotating group from the Zabbix server.  
