from streamlit.web import cli as stcli
import sys, os

def handler(event, context):
    sys.argv = [
        "streamlit",
        "run",
        "app.py",
        "--server.port=8501",
        "--server.address=0.0.0.0",
        "--server.headless=true",
        "--browser.gatherUsageStats=false"
    ]
    try:
        stcli.main()
    except SystemExit:
        pass
    return {
        "statusCode": 200,
        "body": "Streamlit running"
    }

if __name__ == "__main__":
    handler({}, {})