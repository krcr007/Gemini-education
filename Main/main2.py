import tkinter as tk
from tkinter import filedialog, messagebox
import PIL.Image
import google.generativeai as genai

# Define the API key
api = "AIzaSyAxPJTpSHwA2Ng-rZ7FPXyUuhXc8Jgs_nE"

class ImageUploaderApp:
    def __init__(self, master):
        self.master = master
        master.title("Image Uploader")

        self.label = tk.Label(master, text="Upload Image:")
        self.label.pack()

        self.image_path_entry = tk.Entry(master, width=50)
        self.image_path_entry.pack()

        self.upload_button = tk.Button(master, text="Browse", command=self.select_image_file)
        self.upload_button.pack()

        self.generate_button = tk.Button(master, text="Generate", command=self.generate_content)
        self.generate_button.pack()

        self.clear_button = tk.Button(master, text="Clear", command=self.clear_all)
        self.clear_button.pack()

        self.output_text = tk.Text(master, width=60, height=10, font=("Helvetica", 12))
        self.output_text.pack(fill=tk.BOTH, expand=True)

    def select_image_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file_path:
            self.image_path_entry.delete(0, tk.END)
            self.image_path_entry.insert(0, file_path)

    def generate_content(self):
        image_path = self.image_path_entry.get()
        if not image_path:
            messagebox.showerror("Error", "Please select an image file.")
            return

        try:
            img = PIL.Image.open(image_path)
            # Configure Google API
            genai.configure(api_key=api)
            model = genai.GenerativeModel('gemini-pro-vision')
            response = model.generate_content([
                "Explain the complete thing in detail if it is educational then give some links to the topic also and explain in Step by Step in atleast 500 words. Analyze the image correctly and give accurate result according to the image",
                img], stream=True)
            response.resolve()

            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete('1.0', tk.END)

            # Concatenate text from all parts of the response
            output_text = ""
            for part in response.candidates[0].content.parts:
                output_text += part.text

            self.output_text.insert(tk.END, output_text)
            self.output_text.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def clear_all(self):
        self.image_path_entry.delete(0, tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete('1.0', tk.END)
        self.output_text.config(state=tk.DISABLED)

root = tk.Tk()
app = ImageUploaderApp(root)
root.mainloop()

