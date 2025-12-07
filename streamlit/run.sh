#!/bin/bash
# Launcher script for Holiday Greeting QR Code Generator

echo "🎄 Starting Holiday Greeting QR Code Generator..."
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null
then
    echo "❌ Streamlit is not installed."
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

# Check if in correct directory
if [ ! -f "app.py" ]; then
    echo "❌ app.py not found. Please run this script from the streamlit directory."
    exit 1
fi

echo "✅ All checks passed!"
echo "🚀 Launching application..."
echo ""

# Run streamlit
streamlit run app.py
