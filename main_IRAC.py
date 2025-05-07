import tkinter as tk
from tkinter import messagebox
from law_manager import load_data, get_sorted_law_codes, get_law_description
from openai import OpenAI
import openai
from openai.types.chat import ChatCompletionUserMessageParam
# created idea in 2024 and in 2025 modified it
import ctypes
# Enable DPI awareness (for high-DPI displays)
# prevents a Blurry GUI
if ctypes.windll.shcore.SetProcessDpiAwareness:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

# Function to show the law codes in a new window
def search_law():
    # Create a new Toplevel window for searching laws
    search_window = tk.Toplevel(root)
    search_window.title("Search Law")

    # Create a listbox in the search window to show law codes
    law_listbox = tk.Listbox(search_window, height=15, width=50)
    law_listbox.pack(pady=10)

    # Populate the Listbox with sorted law codes
    for law_code in get_sorted_law_codes():
        law_listbox.insert(tk.END, law_code)

    # Function to handle clicking on a law code
    def on_law_code_click(event):
        selected_index = law_listbox.curselection()
        if selected_index:
            law_code = law_listbox.get(selected_index)
            law_description = get_law_description(law_code)
            messagebox.showinfo("Law Description", f"Law Code: {law_code}\nDescription: {law_description}")
        else:
            messagebox.showerror("Selection Error", "Please select a law code.")

    # Bind the law listbox click event
    law_listbox.bind("<ButtonRelease-1>", on_law_code_click)

# did not include API key as I need to conceal it.
# I may add flask/server later on.
# for now you can try it with your own and it should work
# this project is meant to be simple to comprehend how API keys are used for these cases
client = OpenAI(
    api_key="sk-"  # Use your own OpenAI API key
)

def analyze_text():
    # Get the inserted text from the input fields
    plaintiff_text = plaintiff_input.get("1.0", "end-1c").strip()
    defendant_text = defendant_input.get("1.0", "end-1c").strip()
    issue_text = issue_input.get("1.0", "end-1c").strip()
    facts_text = facts_input.get("1.0", "end-1c").strip()
    rule_text = rule_input.get("1.0", "end-1c").strip()

    # Validate required fields
    if not all([plaintiff_text, defendant_text, issue_text, facts_text, rule_text]):
        messagebox.showwarning("Input Error", "Please fill out all fields before proceeding.")
        return

    # Extract law reference from rule input
    law_reference = rule_text.split()[0] if rule_text else "[Rule not found.]"

    # Get law description from local database
    law_description = get_law_description(law_reference)

    # Construct prompt for OpenAI
    prompt = f"""
You are a legal assistant. Use the IRAC method to analyze the following legal scenario.

Plaintiff: {plaintiff_text}
Defendant: {defendant_text}
Issue: {issue_text}
Facts: {facts_text}

Here is the relevant law:
- Law Code: {law_reference}
- Law Description: {law_description}

Format the answer clearly with sections labeled: Issue, Rule, Application, and Conclusion.
"""

    try:
        # Call OpenAI
        messages: list[ChatCompletionUserMessageParam] = [
            {"role": "user", "content": prompt}
        ]

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=messages
        )
        # Get IRAC analysis from OpenAI
        irac_output = completion.choices[0].message.content

        # Combine input and AI response
        result_text = (
            f"--- Lawsuit Type ---\n{issue_text}\n\n"
            f"--- Facts ---\n{facts_text}\n\n"
            f"--- Rule ---\n{rule_text}\n\n"
            f"--- Law Description ---\n{law_description}\n\n"
            f"--- IRAC Analysis ---\n\n{irac_output}"
        )

        # Display in output box
        output_label.config(state="normal")
        output_label.delete(1.0, tk.END)
        output_label.insert(tk.END, result_text)
        output_label.config(state="disabled")

    except Exception as e:
        messagebox.showerror("AI Error", f"Failed to generate IRAC analysis:\n{e}")


# Function to clear the input fields
def clear_inputs():
    issue_input.delete(1.0, tk.END)
    facts_input.delete(1.0, tk.END)
    rule_input.delete(1.0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Tort Law Statue IRAC Generator")

# Create the labels and textboxes for the Plaintiff and Defendant
tk.Label(root, text="Plaintiff:").pack()
plaintiff_input = tk.Text(root, height=1, width=50)
plaintiff_input.pack()

tk.Label(root, text="Defendant:").pack()
defendant_input = tk.Text(root, height=1, width=50)
defendant_input.pack()

# Create the labels and textboxes for Issue, Facts, and Rule
tk.Label(root, text="Type of lawsuit claim (e.g., negligence, assault, etc.):").pack()
issue_input = tk.Text(root, height=2, width=50)
issue_input.pack()

tk.Label(root, text="Key Facts Only (e.g., AI threatens Bot):").pack()
facts_input = tk.Text(root, height=5, width=50)
facts_input.pack()

tk.Label(root, text="Only one Rule (e.g., MD.Sect.5_101):").pack()
rule_input = tk.Text(root, height=2, width=50)
rule_input.pack()

# Create the Search Law button
search_button = tk.Button(root, text="Search Law", command=search_law)
search_button.pack()

# Create the analyze button
analyze_button = tk.Button(root, text="Analyze", command=analyze_text)
analyze_button.pack()

# Create the clear button to reset the input fields
clear_button = tk.Button(root, text="Clear Inputs", command=clear_inputs)
clear_button.pack()

# Create the output label (text area to display the results)
tk.Label(root, text="Output:").pack()
output_label = tk.Text(root, height=20, width=50, wrap="word", state="disabled")
output_label.pack()

# Load laws from the text file when the program starts
load_data()

# Run the main loop
root.mainloop()
