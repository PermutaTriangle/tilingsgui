import pyperclip


def paste(warning=False):
    try:
        return pyperclip.paste()
    except pyperclip.PyperclipException:
        if warning:
            print("Os does not support required c/p operations")
            print("Try: sudo apt-get install xclip")
        return ""
