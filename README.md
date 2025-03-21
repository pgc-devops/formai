# AI Agentic Form Validator

## Overview
AI-powered form validation tool that compares fields from two different forms (JSON, XML, or Text) and provides structured validation results.

### **Key Features**
- 📄 Upload two forms
- 🤖 AI compares fields
- ✅ Final validated data is saved

## Installation & Setup

### **Ubuntu Server Setup**
1. Clone the repository and navigate to the project directory.
2. Install required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the Streamlit UI:
   ```sh
   chmod +x run_streamlit.sh
   ./run_streamlit.sh
   ```
   or
   ```sh
   streamlit run ui.py
   ```
4. Run in the background (optional):
   ```sh
   nohup ./run_streamlit.sh &
   ```

### **Access the UI**
Visit the application in your browser:
   ```sh
   http://192.168.4.74:8501/
   ```

### **Stopping the Server**
Find the running process and kill it:
   ```sh
   ps ax | grep streamlit
   kill PID
   ```

## Reference
[Project Documentation](https://thepathwaygroup-my.sharepoint.com/:p:/g/personal/ravi_singh_corp_pathcom_com/EQEIZKttm2xLlP4VUIQe_W4BRSOi6LRO-Zh528gICkjJwg?e=krpdkD)