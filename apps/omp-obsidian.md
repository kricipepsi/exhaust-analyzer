

## 2. Force the Agent to Read Your Vault
Because oh-my-pi automatically scans files on boot, you can link your Obsidian vault directly to the terminal workspace using a standard Linux symbolic link. [7] 
Navigate to your workspace directory and map the vault: [7] 

ln -s /path/to/your/obsidian/vault/codespace ./.omp_vault

## 3. Inject Context Rules via .claude or .cursor Files
oh-my-pi natively maps project rules from standard AI configuration folders at startup. To program the agent to respect Obsidian's file links and structure, create a text configuration file: [7] 
Create a file named .cursorrules or .clauderules in your project root, and paste this text: [7] 

- The codebase resides inside an Obsidian markdown vault.
- Read developer logs and todo tasks directly from the markdown notes using internal search tools.
- Never write console logs for debugging that could break the omp TUI engine.
- Maintain engineering records using standard [[WikiLinks]] notation for cross-file associations.

## 4. Boot the Workspace
Launch the session inside your linked directory while explicitly enforcing local tool restrictions if you want to bypass heavy web tools: [7] 

omp --tools read,edit,bash,search

------------------------------
If errors still pop up, let me know:

* What exact error text appears in your terminal when running omp?
* Can you check the error output under your local log directory by running tail ~/.omp/logs/omp.*.log? [1] 


[1] [https://github.com](https://github.com/can1357/oh-my-pi/blob/main/AGENTS.md)
[2] [https://pi.dev](https://pi.dev/packages/context-mode)
[3] [https://www.reddit.com](https://www.reddit.com/r/OnlyAICoding/comments/1ry7iyf/any_thoughts_about_ohmypi_coding_agent/)
[4] [https://github.com](https://github.com/can1357/oh-my-pi)
[5] [https://context7.com](https://context7.com/can1357/oh-my-pi)
[6] [https://www.turnkeylinux.org](https://www.turnkeylinux.org/blog/python-externally-managed-environment)
[7] [https://note.com](https://note.com/kudoucraft/n/n991c4bb46fd0?hl=en)




## 1. Launch omp Directly in Your Vault
The easiest way to give the agent full access to your Obsidian notes and source code is to navigate directly to your vault folder in Linux and launch the tool from there.

cd /path/to/your/obsidian/vault
omp

Once inside, the agent will automatically index all markdown files and code files in that directory tree.
## 2. Configure Obsidian-Specific Rules Locally
To explicitly tell the agent how to interact with your Obsidian vault (such as understanding [[WikiLinks]]), create a project rules file right in the root of that folder.
Run this command in your terminal to create the file:

nano .clauderules

(If you use an OpenAI model instead of Claude, name the file .cursorrules instead).
Paste the following instructions into the file, then save and exit:

- You are operating inside an Obsidian Markdown vault where source code and notes coexist.
- You have full access to read and edit files in this directory tree.
- Use local file search and read tools to navigate project documentation.
- When creating references between notes, use Obsidian's standard [[WikiLinks]] format.

## 3. Use the Built-In omp Tools
When omp boots up inside your vault, you don't need custom plugins to read files. You can interact with the agent using your microphone or text interface and give it direct commands like:

* "Search my vault for a note called 'Deployment Guide' and check the steps."
* "Read Todo.md and write a Python script based on the requirements listed there."
* "Update my Index.md file to link to the new module I just created."

------------------------------



