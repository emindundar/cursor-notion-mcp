# Cursor Notion Assistant - Your Coding Companion's Best Friend

Imagine being able to instantly save brilliant ideas, to-do lists, or critical code snippets to Notion while coding. What if, instead of wondering "What did I do today?", you could generate a complete Git history summary with a single command?

**Cursor Notion Assistant** does exactly that. Use Notion as your personal database and Git as your memory, all without leaving your Cursor IDE.

## 🎯 What Can It Do?

- **💾 Your Memory Bank:** Save code blocks, notes, and tasks directly to Notion.
- **📊 Daily Report Assistant:** Run `git log` and `git diff` commands to prepare all your daily changes for analysis. Just say "Add this summary to Notion as a report" and it's done.
- **🔍 Search Notion:** Don't think "Where was that API link I saved last week?" The assistant searches your entire Notion workspace for you.
- **✅ Manage Your Tasks:** Instantly add any task that comes to mind to your Notion task list.

---

## 🚀 Installation (Just 5 Minutes)

> **⚠️ IMPORTANT:** This project requires **Python 3.10 or higher**. If your system has Python 3.9 or older, you must install Python 3.10+ first.

### Step 0: Check Python Version

Run this command in your terminal:

```bash
python3 --version
```

If the version is less than 3.10 (e.g., Python 3.9.6), follow these steps:

**For macOS - Install Python 3.12 with Homebrew:**

```bash
# Install Homebrew if you don't have it:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.12:
brew install python@3.12

# Verify installation:
python3.12 --version
```

**For Linux:**

```bash
sudo apt update
sudo apt install python3.12 python3.12-venv
```

### Step 1: Navigate to Project Directory

Open your terminal and navigate to the project folder:

```bash
cd /path/to/cursor-notion-mcp
```

> **💡 Note:** Replace `/path/to/` with the actual path where you cloned the project.
> Example: `cd ~/Documents/cursor-notion-mcp`

### Step 2: Virtual Environment and Libraries

Let's set up the project in an isolated virtual environment.

- **macOS / Linux (if Python 3.10+ is installed):**
  ```bash
  # If you installed Python 3.12:
  python3.12 -m venv venv
  source venv/bin/activate
  
  # OR if your system Python is 3.10+:
  python3 -m venv venv
  source venv/bin/activate
  ```

- **Windows:**
  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```

Install required libraries:

```bash
pip install -r requirements.txt
```

### Step 3: How to Get Notion API Key?

1. Go to [Notion My Integrations](https://www.notion.so/my-integrations) and create a **"+ New integration"**.
2. Give your integration a name (e.g., "Cursor Assistant") and click "Submit".
3. Copy the **"Internal Integration Token"** from the "Secrets" section.
4. **⚠️ Most Important Step:** Go to the Notion page where you want to add notes, click the three dots (`...`) in the top right, select **"+ Add connections"** and choose the integration you just created.

### Step 4: Create `.env` File

Copy `.env.example` to create a new `.env` file:

```bash
cp .env.example .env
```

Paste your **API Key** from Notion and the **Page ID** (32-character code from the URL) of the page where you want to add notes.

```ini
NOTION_API_KEY=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_PAGE_ID=a1b2c3d4e5f678901234567890abcdef
```

> **💡 Tip:** A Notion page URL looks like this:
> `https://www.notion.so/My-Page-a1b2c3d4e5f678901234567890abcdef`
> The last 32 characters (`a1b2c3d4e5f678901234567890abcdef`) is your Page ID.

---

## 🔧 Cursor Integration

1. In Cursor, open the command palette with `Ctrl/Cmd + Shift + P` and select **"Configure Agent (MCP)"**.
2. Add the following configuration to the opened `mcp.json` file:

```json
{
  "mcpServers": {
    "notion-assistant": {
      "command": "/FULL/PATH/TO/PROJECT/venv/bin/python",
      "args": [
        "/FULL/PATH/TO/PROJECT/server.py"
      ]
    }
  }
}
```

> **⚠️ IMPORTANT:** 
> - Replace `/FULL/PATH/TO/PROJECT/` with the **actual full path** to your project
> - Use the **virtual environment's Python** in the `command` field (full path)
> - While in the project folder, type `pwd` (macOS/Linux) or `cd` (Windows) in the terminal to get the full path
> 
> **Example paths:**
> - macOS/Linux: `/Users/username/Documents/cursor-notion-mcp/venv/bin/python`
> - Windows: `C:\\Users\\username\\Documents\\cursor-notion-mcp\\venv\\Scripts\\python.exe`

3. Save the file and restart Cursor.

---

## 💬 Example Prompts

You're now ready to chat with `@NotionAssistant`!

### 📝 Creating End-of-Day Report (2 Steps)

1. **Extract Git summary:**
   ```
   @NotionAssistant extract a summary of all git changes I made today.
   ```

2. **Save to Notion:**
   ```
   @NotionAssistant add this text to Notion with the title "Today's End-of-Day Report".
   ```

### 💻 Saving Code

```
@NotionAssistant save this code in javascript with the description "Custom hook for user authentication".
```

### ✅ Adding Tasks

```
@NotionAssistant add a task "Test new UI components".
```

### 🔍 Searching

```
@NotionAssistant search Notion for "Stripe API keys".
```

### 📌 Adding Notes

```
@NotionAssistant add a note with title "React hooks pattern I learned today": "When using useState and useEffect together, pay attention to the dependency array."
```

---

## 🛠️ Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `add_note` | Adds a note with title and content to Notion | `content` (required), `title` (optional) |
| `add_todo` | Adds a task to the to-do list | `task` (required) |
| `save_code_snippet` | Saves code snippet with syntax highlighting | `code` (required), `language` (default: python), `description` (optional) |
| `search_in_notion` | Searches in Notion workspace | `query` (required) |
| `get_git_summary` | Extracts Git commit and patch summary | `since` (default: 6am), `project_path` (optional) |

---

## 🐛 Troubleshooting

### Getting "Missing environment variable" error

- Make sure the `.env` file is in the project folder
- Verify that `NOTION_API_KEY` and `NOTION_PAGE_ID` are correctly entered

### "Notion client could not be initialized" error

- Ensure your API key is valid
- Check that your Notion integration is active

### Getting "Notion API error"

- Make sure you've granted your integration access to the target page
- Verify your Page ID is correct

### Git summary not working

- Ensure your project folder is a Git repository
- Check that the `git` command is installed on your system

---

## 📄 License

This project is open source and freely available for use.

---

## 🤝 Contributing

Bug reports, feature requests, and pull requests are welcome!

---

**Happy coding! 🚀**
