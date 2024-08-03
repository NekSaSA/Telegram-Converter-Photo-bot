Image Conversion Bot
This bot is designed for converting images into various formats. You can send an image to the bot, choose the format you want to convert it to, and receive the result back.

Features
Welcome Message: When you start the bot, it greets you and explains how to use it.
Image Conversion: Supports the following formats: jpg, jpeg, png, webp, bmp, ppm.
Format Selection: You can choose the format to convert the image from a provided list.
Installation
Clone the repository:
bash
git clone https://github.com/your-username/your-repository.git
Navigate to the project directory:
bash
cd your-repository
Create and activate a virtual environment:
bash

python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
Install dependencies:
bash

pip install -r requirements.txt
Configuration
Create a .env file in the root directory of the project.
Add your Telegram bot token to the file:
plaintext

API_TOKEN=your_token
Running
Start the bot using the command:

bash

python main.py
Notes
Make sure you have all necessary libraries and tools installed.
If you encounter issues with dependency installation, try installing them manually.
Contributors
If you have suggestions for improvements, please create an issue or pull request.
