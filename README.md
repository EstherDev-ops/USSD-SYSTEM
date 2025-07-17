# USSD STUDENT INFORMATION SYSTEM BACKEND
- 
A lightweight Python backend for a **USSD-based Student Information System** allowing students to retrieve data using simple USSD codes — no internet required!

## 🚀 Overview

This backend powers a USSD interface that students can use to:

- ✅ Check **exam results**
- ✅ View **missed exams**
- ✅ Check **fee balance**

Ideal for use with both smartphones and feature phones, it's especially useful when student portals are slow or internet access is unreliable.

## 📦 Features

- **Offline Access** via USSD
- **Simple Menu System** implemented in `app.py`
- **Testable Locally** using `ussd_test.py`
- **Public Endpoint** setup with Ngrok to receive USSD callbacks

## 🛠️ Setup & Installation

1. **Clone this repo**  
   ```bash
   git clone https://github.com/EstherDev-ops/USSD-SYTEM.git
   cd USSD-SYTEM.

   ## HOW IT WORKS##
   1. Register a USSD Code with Your Provider
      Contact your USSD gateway or mobile network operator to obtain a shortcode, e.g., *123#.

      The provider will link this code to your backend server via a callback URL. 
       github.com

2. Run Backend Locally
   Ensure your project folder contains:

app.py (USSD logic)

ussd_test.py (local USSD simulation)

Start the application:


python app.py
By default, it listens on http://127.0.0.1:5000.

3. Expose Server with Ngrok
Use ngrok to generate a public webhook URL:


ngrok http 5000
Copy the HTTPS forwarding address (e.g., https://abcd1234.ngrok.io).

Based on ngrok docs, this enables mobile networks to send USSD session requests to your local server 
sedemquame.medium.com
ngrok.com
.

4. Configure the USSD Gateway
In your USSD provider dashboard:

Set the callback URL to the ngrok address plus your app endpoint, e.g.:

https://abcd1234.ngrok.io/ussd
This directs incoming USSD sessions to your local backend .

5. Test Your USSD Flow
 a) Via Provider Simulator:
  Many platforms (e.g., Africa's Talking) offer a USSD simulator.

Dial your code and interact with the menu (e.g., select results, missed exams).

b) Locally with ussd_test.py:
Run:


python ussd_test.py
It mimics a USSD session and prints out responses from your backend.

📖 How USSD Works
User initiates session by dialing *123#.

Mobile network sends a request to your server.

Your server runs the code in app.py to generate the menu.

Menu appears on user’s phone; they enter options.

The session continues until the system returns a final "END" message.

   
