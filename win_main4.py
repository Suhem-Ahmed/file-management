import tkinter as tk
from tkinter import filedialog
from reportlab.pdfgen import canvas
from PIL import Image
from datetime import date
import os

class ContactApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Anaam Farms Fuel Mentanace ")
        self.master.maxsize(250,100)
        self.master.minsize(250,100)


        # Create labels and entry widgets for name, phone number, and date
        tk.Label(master, text="Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(master)
        self.name_entry.grid(row=0, column=1)
        self.name_entry.bind('<Return>', lambda event: self.phone_entry.focus_set()) # bind <Return> key to move focus to phone_entry
        tk.Label(master, text="AMOUNT:").grid(row=1, column=0)
        self.phone_entry = tk.Entry(master)
        self.phone_entry.grid(row=1, column=1)
        self.phone_entry.bind('<Return>', lambda event: self.date_entry.focus_set()) # bind <Return> key to move focus to date_entry
        tk.Label(master, text="Date:").grid(row=2, column=0)
        self.date_entry = tk.Entry(master)
        self.date_entry.insert(0, date.today().strftime('%Y-%m-%d')) # set default to current date
        self.date_entry.grid(row=2, column=1)
        self.date_entry.bind('<Return>', lambda event: self.browse_photo()) # bind <Return> key to trigger browse_photo method

        # Create a button to browse for a photo
        self.browse_button = tk.Button(master, text="Browse", command=self.browse_photo)
        self.browse_button.grid(row=3, column=0)
    
        # Create a button to submit the data
        self.submit_button = tk.Button(master, text="Submit", command=self.save_data)
        self.submit_button.grid(row=3, column=1)

    def browse_photo(self):
        # Set the initial directory to the Downloads folder
        initialdir = os.path.join(os.path.expanduser("~"), "Downloads")

        # Open a file dialog to allow the user to select a photo
        filename = filedialog.askopenfilename(initialdir=initialdir)

        # Store the selected filename in a class variable for later use
        self.filename = filename

        # Move focus to the submit button when a photo is selected
        self.submit_button.focus_set()


    def save_data(self, event=None, from_button=False):
        # Check if the function was called from the submit button or the Enter key
        if not from_button and event and event.widget != self.submit_button:
            return

        name = self.name_entry.get()
        phone = self.phone_entry.get()
        date_str = self.date_entry.get()
        date = date_str
      

        # Create a directory with the date as the name
        dirname = date_str
        os.makedirs(os.path.join(os.path.expanduser("~"), "Desktop\Anaam Farms Fuel Manegment", dirname), exist_ok=True)

        # Set the filename for the PDF
        filename = os.path.join(os.path.expanduser("~"), "Desktop\Anaam Farms Fuel Manegment", dirname, f"{name} {phone}.pdf")

        # Create a PDF document and draw the contact information
        c = canvas.Canvas(filename)
        c.drawString(100, 300, "NAME: {}".format(name))
        c.drawString(100, 280, "AMOUNT: {}".format(phone))
        c.drawString(100, 260, "Date: {}".format(date_str))


        if hasattr(self, "filename"):
            try:
                img = Image.open(self.filename)
                width, height = img.size
                if width > height:
                    width, height = 400, 300
                else:
                    width, height = 300, 400
                c.drawImage(self.filename, 100, 400, width=width, height=height)
            except:
                pass
        c.showPage()
        c.save()

        # Notify the user that the data was saved
        tk.messagebox.showinfo("Success", "Data saved to file.")

        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)



root = tk.Tk()
#root.title("ANAAM FARMS VECHICLE MENTANENCE")
app = ContactApp(root)
root.mainloop()
