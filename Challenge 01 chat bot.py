import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import google.generativeai as genai
import subprocess
import sys

# ========= Ensure tkinter is installed ==========
try:
    import tkinter
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tk"])

# ========= Gemini API Key Setup ==========
genai.configure(api_key="AIzaSyDmkFW5kOKNDS1IVZdDOjiUFxB-ANXnfWk")  
model = genai.GenerativeModel("models/gemini-1.5-flash")

# ========= PDF Reading Function ==========
def read_pdf_text(path):
    try:
        with open(path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read PDF: {e}")
        return ""

# ========= Ask Gemini Function ==========
def ask_gemini():
    question = question_entry.get("1.0", tk.END).strip()

    # Exit shortcut
    if question.lower() in ["bye", "quit", "exit"]:
        messagebox.showinfo("Exit", "Thanks for using Tech Drogon Chatbot!")
        root.destroy()
        return

    if not pdf_content:
        messagebox.showwarning("Warning", "Please load a PDF file first.")
        return

    if not question:
        messagebox.showwarning("Warning", "Please enter your question.")
        return

    try:
        prompt = f"""You are a multilingual assistant. The PDF content is below. Answer the user's question in the same language the question was asked, whether it is Tamil or English.

PDF Content:
{pdf_content}

Question:
{question}
"""
        response = model.generate_content(prompt)

        # Replace old answer
        answer_text.delete("1.0", tk.END)
        answer_text.insert(tk.END, response.text)

        # Clear question for next input
        question_entry.delete("1.0", tk.END)
        question_entry.focus()

    except Exception as e:
        messagebox.showerror("Error", f"Gemini error: {e}")

# ========= PDF File Picker ==========
def load_pdf():
    global pdf_content
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        pdf_content = read_pdf_text(file_path)
        pdf_label.config(text=f"PDF loaded: {file_path.split('/')[-1]}")

# ========= UI Setup ==========
pdf_content = ""

root = tk.Tk()
root.title("Tech Dragon Chatbot – Ask Anything")
root.geometry("620x530")

load_button = tk.Button(root, text="📁 Load PDF", command=load_pdf, bg="#007acc", fg="white")
load_button.pack(pady=10)

pdf_label = tk.Label(root, text="No PDF loaded", fg="blue", font=("Arial", 10, "bold"))
pdf_label.pack()

question_label = tk.Label(root, text="Ask anything (Tamil or English):")
question_label.pack(pady=(20, 5))

question_entry = tk.Text(root, height=3, width=70, bg="#fff9cc")  # Light yellow for question
question_entry.pack()

ask_button = tk.Button(root, text="Ask", command=ask_gemini, bg="#28a745", fg="white")
ask_button.pack(pady=10)

answer_label = tk.Label(root, text="Answer:")
answer_label.pack()

# === Answer box with scrollbar and blue bg ===
answer_frame = tk.Frame(root)
answer_frame.pack()

scrollbar = tk.Scrollbar(answer_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

answer_text = tk.Text(answer_frame, height=10, width=70, bg="#e0f0ff", yscrollcommand=scrollbar.set, wrap="word")
answer_text.pack(side=tk.LEFT)

scrollbar.config(command=answer_text.yview)

# === Start GUI ===
root.mainloop()