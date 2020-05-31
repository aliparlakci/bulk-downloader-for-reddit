# Interpret from source code
## Requirements
### 🐍 Python 3 Interpreter
- Python 3 is required. See if it is already installed, [here](#finding-the-correct-keyword-for-python).  
- If not, download the matching release for your platform [here](https://www.python.org/downloads/) and install it. If you are a *Windows* user, selecting **Add Python 3 to PATH** option when installing the software is **mandatory**.   

### 📚 Repository
[Download the repository](https://github.com/aliparlakci/bulk-downloader-for-reddit/archive/master.zip) and extract the zip into a folder.

## 💻 Using the command line
Open the [Command Promt](https://youtu.be/bgSSJQolR0E?t=18), [Powershell](https://youtu.be/bgSSJQolR0E?t=18) or [Terminal](https://youtu.be/Pz4yHAB3G8w?t=31) in the folder that contains the script.py file (click on the links to see how)

### Finding the correct keyword for Python
Enter these lines to the terminal window until it prints out the a version starting with **`3.`**:
  
- `python --version`
- `python3 --version`
- `py --version`
- `py -3 --version`
  
Once it does, your keyword is without the `--version` part. 

## Installing dependencies
Enter the line below to terminal window when you are in the directory where script.py is, use your keyword instead of `python`:
```console
python -m pip install -r requirements.txt
```

## Running the code
Type below code into command line, use your keyword instead of `python`:
```console
python script.py
```
  
The program should guide you though. **However**, you can also use custom options. See [Options](../README.md#⚙-Options)