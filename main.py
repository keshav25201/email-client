from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from tkinter import *
import smtplib
from tkinter import messagebox,filedialog
class App(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = MIMEMultipart()
        self.title('Email Client')
        self.geometry("730x700")
        #email
        self.label_email = Label(text="E-mail address: ")
        self.input_email = Entry()
        self.label_email.grid(row= 0,column=0,padx=10)
        self.input_email.grid(row = 0,column=1)
        #password
        self.label_password = Label(text="Password: ")
        self.input_password = Entry()
        self.label_password.grid(row = 0,column=2)
        self.input_password.grid(row = 0,column=3)
        
        #smtp server
        self.label_smtp = Label(text="smtp server: ")
        self.input_smtp = Entry()
        self.label_smtp.grid(row=1,column=0,sticky='W',padx=10)
        self.input_smtp.grid(row=1,column=1)
        #port
        self.label_port = Label(text="port server: ")
        self.input_port = Entry()
        self.label_port.grid(row = 1,column=2)
        self.input_port.grid(row = 1,column = 3)
        
        #login button
        self.login_btn = Button(text="Login",command=self.login)
        self.login_btn.grid(row = 1,column=4)

        #To
        self.label_to = Label(text="To: ")
        self.input_to = Entry()
        self.label_to.grid(row = 2,column=0,sticky='w',padx=10)
        self.input_to.grid(row = 2,column=1,columnspan=4,sticky='nesw')

        #subject
        self.label_subject = Label(text="Subject: ")
        self.input_subject = Entry()
        self.label_subject.grid(row = 3,column=0,sticky='W',padx=10)
        self.input_subject.grid(row = 3,column=1,columnspan=3,sticky='ew')

        #add attachment button
        self.add_attach_btn = Button(text="Add Attachment",state=DISABLED,command=self.attach_file)
        self.add_attach_btn.grid(row=3,column=4)

        #message box
        # self.rowconfigure(5,weight=3)
        self.text_box_label = Label(text="Mail text:")
        self.text_box = Text(height=35)
        self.text_box_label.grid(row=4,column=0,sticky='W',padx=10)
        self.text_box.grid(row=5,columnspan=5,sticky="nesw",padx=10,pady=10)
        #filenames for attachments
        self.label_attachments = Label(text='files: ')
        self.label_filenames = Label(text = '')
        self.label_attachments.grid(row = 6,column = 0)
        self.label_filenames.grid(row = 6,column=1)
        #send
        self.send_btn = Button(text="send",state=DISABLED,command=self.send)
        self.send_btn.grid(row = 7,column=0)
    def login(self):
        try:
            print(self.input_smtp.get())
            self.server = smtplib.SMTP(self.input_smtp.get(),self.input_port.get())
            self.server.ehlo()
            self.server.starttls()
            self.server.ehlo()
            self.server.login(self.input_email.get(),self.input_password.get())
            self.send_btn["state"] = "normal"
            self.add_attach_btn["state"] = "normal"
            print("login successful")
        except Exception as e:
            print(e)
            pass
    def send(self):
        response = messagebox.askyesno(message="Do you want to send this email")
        if(response == True):
            try:
                self.message['From'] = self.input_email.get()
                self.message['To'] = self.input_to.get()
                self.message['Subject'] = self.input_subject.get()
                self.message.attach(MIMEText(self.text_box.get("1.0",'end-1c'),'plain'))
                text = self.message.as_string()
                self.server.sendmail(self.input_email.get(),self.input_to.get(),text)
                self.message = MIMEMultipart()
                messagebox.showinfo(message="email sent🤓")
            except Exception as e:
                print(e)
                pass
    def attach_file(self):
        filenames = filedialog.askopenfilenames(initialdir='/',title="select files")
        if filenames != []:
            for filename in filenames:
                attachment = open(filename,"rb")
                filename = filename[filename.rfind("/") + 1:]
                payload = MIMEBase('application','octet-stream')
                payload.set_payload(attachment.read())
                encoders.encode_base64(payload)
                payload.add_header("Content-Disposition",f"attachment; filename={filename}")
                self.message.attach(payload)
                self.label_filenames.configure(text = self.label_filenames.cget("text") + filename + ", ")

if __name__ == "__main__":
    app = App()
    app.mainloop()
