# Translate Markdown Using Google Cloud Translation API

This guide walks you through **setting up Google Cloud Translation API** and **automating Markdown translation** using Python.

## 📌 Prerequisites
- A **Linux machine** (Ubuntu, Linux Mint, Debian, etc.)
- A **Google Cloud account** ([Sign up](https://console.cloud.google.com/))
- **Billing enabled** for API usage
- Python **3.7+** installed

---

## ⚙️ Step 1: Install Google Cloud SDK (`gcloud`)

Google Cloud SDK (`gcloud`) is required to interact with Google Cloud services.

### 👅 Install Google Cloud SDK
```bash
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-$(curl -s https://dl.google.com/dl/cloudsdk/channels/rapid/components-2.json | grep -oP '"version": "\K[^"]+' | head -n1)-linux-x86_64.tar.gz
tar -xf google-cloud-sdk-*-linux-x86_64.tar.gz
sudo mv google-cloud-sdk /opt/
```

### 🔄 Initialize Google Cloud SDK
```bash
/opt/google-cloud-sdk/install.sh
echo 'export PATH=/opt/google-cloud-sdk/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

### ✅ Verify Installation
```bash
gcloud version
```

---

## 🚀 Step 2: Create a New Google Cloud Project
Create a **new Google Cloud project** for Translation API.

```bash
gcloud projects create markdown-translate --set-as-default
```

Set it as your **default project**:
```bash
gcloud config set project markdown-translate
```

Check if the project is correctly set:
```bash
gcloud config list
```

---

## 💰 Step 3: Enable Billing (Required for Translation API)
Find your **billing account ID**:
```bash
gcloud beta billing accounts list
```

Attach billing to your project:
```bash
gcloud beta billing projects link markdown-translate --billing-account=YOUR_BILLING_ACCOUNT_ID
```
> **Note:** The **first 500,000 characters per month** are free. After exceeding this limit, Google charges **$20 per million characters** translated. You can monitor your usage to avoid unexpected charges.

---

## 🌍 Step 4: Enable Google Cloud Translation API
Enable the **Translation API** for your project:
```bash
gcloud services enable translate.googleapis.com
```

Verify that it's enabled:
```bash
gcloud services list --enabled
```

---

## 🔑 Step 5: Create a Service Account for API Access
Create a **service account** for authentication:
```bash
gcloud iam service-accounts create translation-sa \
    --description="Service account for Markdown translation" \
    --display-name="Translation API SA"
```

Grant **Translation API access**:
```bash
gcloud projects add-iam-policy-binding markdown-translate \
    --member="serviceAccount:translation-sa@markdown-translate.iam.gserviceaccount.com" \
    --role="roles/cloudtranslate.user"
```

Generate a **JSON key file**:
```bash
gcloud iam service-accounts keys create ~/translation-key.json \
    --iam-account=translation-sa@markdown-translate.iam.gserviceaccount.com
```

Set the authentication key:
```bash
export GOOGLE_APPLICATION_CREDENTIALS=~/translation-key.json
```
Make it persistent:
```bash
echo 'export GOOGLE_APPLICATION_CREDENTIALS=~/translation-key.json' >> ~/.bashrc
source ~/.bashrc
```

---

## 🐍 Step 6: Install Python Dependencies
Ensure Python is installed:
```bash
python3 --version
```

Install required Python modules:
```bash
pip install google-cloud-translate
```

---

## 📝 Step 7: Download and Run the Markdown Translator
Clone or create the script:
```bash
wget -O translate_markdown_google.py https://raw.githubusercontent.com/example/translate_markdown_google.py
```
> *(If the script is not hosted online, copy-paste it manually into a file.)*

Run the translator:
```bash
python translate_markdown_google.py input.md
```
This creates:
```markdown
input-translated.md
```

For a **custom output filename**:
```bash
python translate_markdown_google.py input.md output.md
```

---

## 📊 Step 8: Check API Usage & Costs
To check **Translation API usage**:
```bash
gcloud beta ml translate translate-text --source-language=ja --target-language=en --content="こんにちは世界"
```

To query **billing costs**:
```bash
gcloud billing accounts get-usage --start-time="7d" --end-time="now"
```

To estimate **cost per file**:
```bash
wc -m input.md
```
> **Google charges $20 per million characters after the free tier.**

---

## 🌟 Additional Features
- **Modify script to exclude specific sections**
- **Batch process multiple Markdown files**
- **Filter certain keywords from translation**

---

## ❓ Troubleshooting
### 🔴 **"Permission denied" error**
Make sure the service account has the correct role:
```bash
gcloud projects add-iam-policy-binding markdown-translate \
    --member="serviceAccount:translation-sa@markdown-translate.iam.gserviceaccount.com" \
    --role="roles/cloudtranslate.user"
```

### 🔴 **"API not enabled" error**
Ensure Translation API is enabled:
```bash
gcloud services list --enabled | grep translate
```
If missing, enable it:
```bash
gcloud services enable translate.googleapis.com
```

### 🔴 **Script not running properly?**
Check Python dependencies:
```bash
pip install --upgrade google-cloud-translate
```

---

## 🎉 Done!
Your **Markdown file is now translated** while keeping the original formatting.

For feedback or improvements, open an issue on **GitHub**! 🚀


