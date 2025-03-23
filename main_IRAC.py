import tkinter as tk
from tkinter import messagebox
from law_manager import load_data, get_sorted_law_codes, get_law_description

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

# Function to analyze and display the pasted text
def analyze_text():
    # Get the inserted text from the input fields
    plaintiff_text = plaintiff_input.get("1.0", "end-1c")
    defendant_text = defendant_input.get("1.0", "end-1c")
    issue_text = issue_input.get("1.0", "end-1c")
    facts_text = facts_input.get("1.0", "end-1c")
    rule_text = rule_input.get("1.0", "end-1c")

    # Check if any of the required fields are empty
    if not plaintiff_text or not defendant_text or not issue_text or not facts_text or not rule_text:
        messagebox.showwarning("Input Error", "Please fill out all fields before proceeding.")
        return  # Stop the function if any field is empty

    # Extract the law reference (e.g., MD.000)
    law_reference = rule_text.split()[0] if rule_text else " [Rule not found.] "

    # Retrieve the law description from the dictionary
    law_description = get_law_description(law_reference)

    # Generate analysis based on the Issue, Facts, and Rule
    analysis = (
        f"The issue is whether {plaintiff_text} can file a(n) {issue_text.lower()} claim (lawsuit) against {defendant_text}. "
        f"Under the {law_reference}, {law_description} "
        f"Here, {plaintiff_text} can file this lawsuit under {law_reference} because {facts_text}. "
        f"Based on these key facts, it demonstrates the element(s) of {issue_text.lower()} under {law_reference}. "
        f"In conclusion, {plaintiff_text} can file a(n) {issue_text.lower()} claim (lawsuit) under the {law_reference} as the evidence(s) "
        f"fulfill(s) all the required element(s) of {issue_text.lower()} under {law_reference}."
    )

    # Combine the input texts into a formatted result string
    result_text = f"--- Lawsuit Type ---\n{issue_text}\n\n--- Facts ---\n{facts_text}\n\n--- Rule ---\n{rule_text}\n\n--- IRAC Analysis: ---\n\n{analysis}"

    # Output the combined text (input + analysis) to the output area
    output_label.config(state=tk.NORMAL)
    output_label.delete(1.0, tk.END)  # Clear previous text
    output_label.insert(tk.END, result_text)  # Insert the combined result
    output_label.config(state=tk.DISABLED)

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
output_label = tk.Text(root, height=20, width=50, wrap=tk.WORD, state=tk.DISABLED)
output_label.pack()

# Load laws from the text file when the program starts
load_data()

# Run the main loop
root.mainloop()
