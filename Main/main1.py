import tkinter as tk
from tkinter import scrolledtext, filedialog
import google.generativeai as genai
import warnings
from pathlib import Path as p
from langchain import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

warnings.filterwarnings("ignore")

api = "AIzaSyAxPJTpSHwA2Ng-rZ7FPXyUuhXc8Jgs_nE"  # Replace 'YOUR_API_KEY' with your actual Google API key
genai.configure(api_key=api)
model = genai.GenerativeModel(model_name="gemini-pro")


class QAApplication:
    def __init__(self, master):
        self.master = master
        master.title("Question Answering System")

        # Get the screen width and height
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        # Set the window size to fit the screen
        master.geometry(f"{screen_width}x{screen_height}")

        # Set the background color to blue and white
        master.config(bg="blue")

        # Create a frame for the top section
        top_frame = tk.Frame(master, bg="blue")
        top_frame.pack(side=tk.TOP, fill=tk.X)

        # Upload PDF
        self.label = tk.Label(top_frame, text="Upload PDF:", bg="blue", fg="white")
        self.label.pack(side=tk.LEFT, padx=10, pady=5)

        self.pdf_entry = tk.Entry(top_frame, width=50)
        self.pdf_entry.pack(side=tk.LEFT, padx=5, pady=5)

        self.upload_button = tk.Button(top_frame, text="Browse", command=self.select_pdf_file, bg="white", fg="blue")
        self.upload_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.load_button = tk.Button(top_frame, text="Load PDF", command=self.load_pdf, bg="white", fg="blue")
        self.load_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Question Entry
        self.label = tk.Label(master, text="Enter your question:", bg="blue", fg="white")
        self.label.pack(pady=(20, 5))

        self.question_entry = tk.Entry(master, width=100, font=("Arial", 12))
        self.question_entry.pack(pady=5, padx=10)

        # Output Text
        self.output_text = scrolledtext.ScrolledText(master, width=100, height=20, font=("Arial", 14))
        self.output_text.pack(pady=10, fill=tk.BOTH, expand=True)

        # Buttons
        button_frame = tk.Frame(master, bg="blue")
        button_frame.pack(pady=10)

        self.continue_button = tk.Button(button_frame, text="Ask", command=self.ask_question, bg="white", fg="blue",
                                         font=("Arial", 12))
        self.continue_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(button_frame, text="Clear", command=self.clear_output, bg="white", fg="blue",
                                      font=("Arial", 12))
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.quit_button = tk.Button(button_frame, text="Quit", command=master.quit, bg="white", fg="blue",
                                     font=("Arial", 12))
        self.quit_button.pack(side=tk.LEFT, padx=5)

        self.qa_chain = None

    def select_pdf_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.pdf_entry.delete(0, tk.END)  # Clear the entry
            self.pdf_entry.insert(0, file_path)  # Insert the selected file path

    def load_pdf(self):
        pdf_path = self.pdf_entry.get()
        if pdf_path:
            pdf_loader = PyPDFLoader(pdf_path)
            pages = pdf_loader.load_and_split()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
            context = "\n\n".join(str(p.page_content) for p in pages)
            texts = text_splitter.split_text(context)
            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api)
            vector_index = Chroma.from_texts(texts, embeddings).as_retriever(search_kwargs={"k": 5})

            model_base = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api,
                                                temperature=0.2, convert_system_message_to_human=True)
            template = """

            Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer.
            {context}
            Question: {question}
            Helpful Answer:


"""

            QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
            self.qa_chain = RetrievalQA.from_chain_type(model_base,
                                                        retriever=vector_index,
                                                        return_source_documents=True,
                                                        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})

    def ask_question(self):
        if not self.qa_chain:
            self.output_text.insert(tk.END, "Please load a PDF first.\n")
            return
        question = self.question_entry.get()
        result = self.qa_chain(question)
        answer = result['result']
        self.output_text.insert(tk.END, f"Question: {question}\nAnswer: {answer}\n\n")

    def clear_output(self):
        self.output_text.delete(1.0, tk.END)


# Create an instance of Tkinter window
root = tk.Tk()

# Create an instance of your QAApplication
app = QAApplication(root)

# Run the Tkinter event loop
root.mainloop()