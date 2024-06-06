import openai
import PyPDF2


class OpenAiFileChatBot:

    def __init__(self, api_key, fname, sys_msg):
        self.api_key = api_key
        openai.api_key = self.api_key
        self.fname = fname
        self.messages = [
            {"role": "system", "content": sys_msg},
        ]
        self.detected_text = ""
        self.read_file()
        self.init_chatbot()

    def read_file(self):
        pdf_file_obj = open(self.fname, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
        num_pages = pdf_reader.pages
        for page_num in num_pages:
            self.detected_text += page_num.extract_text() + '\n\n'
        pdf_file_obj.close()

    def init_chatbot(self):
        info = "store above file data and based on this data answer my questions."
        user_msg = self.detected_text + "\n\n" + info
        self.messages.append({"role": "user", "content": user_msg})
        chat_completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        chat_message = chat_completion.choices[0].message.content
        self.messages.append({"role": "assistant", "content": chat_message})

    def ask(self, query):
        self.messages.append({"role": "user", "content": query})
        chat_completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        chat_message = chat_completion.choices[0].message.content
        self.messages.append({"role": "assistant", "content": chat_message})
        return chat_message


if __name__ == "__main__":

    openai_key = ""
    sys_msg = "You are a helpful financial advisor."
    fname = 'test.pdf'

    chat_bot = OpenAiFileChatBot(openai_key, fname, sys_msg)

    query = "just give me the list the Stock Ideas with positive and negative Trend Reversal in json combined array format without explaination with key ptr and ntr"
    op = chat_bot.ask(query)
    print(op)
