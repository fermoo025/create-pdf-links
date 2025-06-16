import tkinter as tk
from tkinter import messagebox
import downPdfs  # Make sure this file is in the same folder
import os
import readPdfs

def submit():
    val1 = entry1.get().strip()
    val2 = entry2.get().strip()
    val3 = entry3.get().strip()
    if os.path.exists(val1):
        result = messagebox.askokcancel("Confirm", f"{val1} folder exists. Do you want to continue? If OK, existing PDFs are used.")
        if not result:
            return
    downPdfs.main(val1, val2, val3)
    readPdfs.saveAllText(val1)
    
root = tk.Tk()
root.title("Wider Form")
root.geometry("500x270") 
label1 = tk.Label(root, text="FOLDER ID:", anchor='w')
label1.pack(fill='x', padx=20, pady=(20, 5))
entry1 = tk.Entry(root, width=60)
entry1.pack(padx=20, pady=5)
label2 = tk.Label(root, text="SHEET ID:", anchor='w')
label2.pack(fill='x', padx=20, pady=5)
entry2 = tk.Entry(root, width=60)
entry2.pack(padx=20, pady=5)
label3 = tk.Label(root, text="TAB NAME:", anchor='w')
label3.pack(fill='x', padx=20, pady=5)
entry3 = tk.Entry(root, width=60)
entry3.pack(padx=20, pady=5)
submit_button = tk.Button(root, text="Submit", width=20, height=3, command=submit)
submit_button.pack(pady=20)
entry1.insert(0, '1c6l8cZRLqtbeyyvKlp9Nm2xOJHNkaDBf')  # <-- Predefined value for entry1
entry2.insert(0, '1CVAAilMvM8LsrZIelRz6nf4SRvFeoawGonw6L4QlSC8')  # <-- Predefined value for entry1
entry3.insert(0, '250615')  # <-- Predefined value for entry1
root.mainloop()
