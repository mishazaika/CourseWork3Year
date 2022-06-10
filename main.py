from tkinter import *
from tkinter import messagebox
import loginSystem
import pymysql
import requests
import lxml.html as lh
import pandas as pd
import xlrd as xl
import xlwt
from IPython.display import display

conn = pymysql.connect(host="localhost", user="root", password="uTorrent3.3", db="webscraper")
curs = conn.cursor()

class SocialMedia(object):
    def __init__(self, master):
        self.name = None
        self.master = master

        welcome_canvas = Canvas(master, width=370,height=140)
        welcome_canvas.pack()
        welcome_canvas.create_text(180, 70, fill="blue", text="WELLCOME TO \n WEB SCRAPER", font=("Times", 20, "bold italic"))

        login_button = Button(master, text="Login", command=self.login)
        login_button.config(width=360, pady=3, bd=5, fg="green", relief=GROOVE, font="SNAS 40")
        login_button.pack()

    def login(self):
        loginWin = Toplevel(self.master)
        loginPage = loginSystem.LoginPage(loginWin,self)

    def enter(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        label_heading = Canvas(self.master, width=370,height=100)
        label_heading.pack()
        label_heading.create_text(180, 70, fill="black", text="Top 3 Social Media", font=("Times", 20, "bold italic"))

        self.menuFrame = Frame(self.master)
        self.menuFrame.config(width=360, relief=GROOVE, bd=1)
        self.menuFrame.pack()

        if self.name == None:
            self.displaySocialMedia()

    def displaySocialMedia(self):
        sqlQuery = "SELECT name FROM social_media"

        self.socialFrame = Frame(self.master.master)
        self.socialFrame.pack()

        curs.execute(sqlQuery)
        socialmedias = curs.fetchall()
        for socialmedia in socialmedias:
            b = Radiobutton(self.socialFrame, text=socialmedia[0], variable=socialname, value=socialmedia[0], indicatoron=0)
            b.pack(fill=X)
        self.proceed_button = Button(self.socialFrame, text="Export", command=lambda: self.exportformat(socialname))
        self.proceed_button.config(bg="green3")
        self.proceed_button.pack(side=BOTTOM)

    def exportformat(self, socialmedia):
        self.name = socialmedia.get()
        print("selected socialmedia "+self.name)
        if self.name != '':
            for widget in self.socialFrame.winfo_children():
                widget.destroy()
            self.interactiveMenu()
        else:
            messagebox.showerror(title='Error', message='Please Select a Social Media!')

    def interactiveMenu(self):
        sqlQuery = "SELECT name FROM exportformat"

        self.formatFrame = Frame(self.master)
        self.formatFrame.pack()

        curs.execute(sqlQuery)
        formats = curs.fetchall()
        for format in formats:
            c = Radiobutton(self.formatFrame, text=format[0], variable=formatname, value=format[0], indicatoron=0)
            c.pack(fill=X)

        back_button = Button(self.formatFrame, text="Back", command=self.goback)
        back_button.config(bg="red2")
        back_button.pack(side=BOTTOM)
        back_button.pack()

        proceed_button = Button(self.formatFrame, text="Choose format", command=lambda: self.print_selection(formatname))
        proceed_button.config(bg="green3")
        proceed_button.pack(side=BOTTOM)

    def goback(self):
        self.formatFrame.destroy()
        self.socialFrame.destroy()
        self.displaySocialMedia()

    def print_selection(self,format):
        self.name = format.get()
        if self.name == 'CSV':
            self.exportcsv()
        elif self.name == 'Excel':
            self.exportexcel()
        elif self.name == 'Text':
            self.exporttext()
        else:
            messagebox.showerror(title='Error', message='Please choose a file format')

    def exportexcel(self):
        self.name = socialname.get()
        if self.name == 'Instagram':
            page = requests.get(url1)  # Store the contents of the website under doc
            doc = lh.fromstring(page.content)  # Parse data that are stored between <tr>..</tr> of HTML

            tr_elements = doc.xpath('//tr')  # Create empty list
            res = self.webscraper(tr_elements, 5)

            dictionary = {title: column for (title, column) in res}
            df = pd.DataFrame(dictionary)

            # Excel file
            df.to_excel('instagram.xls', index=False, encoding='utf-8')
            wb = xl.open_workbook('instagram.xls')  # opening & reading the excel file
            s1 = wb.sheet_by_index(0)  # extracting the worksheet
            s1.cell_value(0, 0)  # cell from the excel file mentioned through the cell position

            if s1.nrows != 0:  # Counting the number of rows in Excel file
                self.on_close()
        elif self.name == 'TikTok':
            page = requests.get(url2)  # Store the contents of the website under doc
            doc = lh.fromstring(page.content)  # Parse data that are stored between <tr>..</tr> of HTML

            tr_elements = doc.xpath('//tr')  # Create empty list
            res = self.webscraper(tr_elements, 8)

            dictionary = {title: column for (title, column) in res}
            df = pd.DataFrame(dictionary)

            # Excel file
            df.to_excel('tiktok.xls', index=False, encoding='utf-8')
            wb = xl.open_workbook('tiktok.xls')  # opening & reading the excel file
            s1 = wb.sheet_by_index(0)  # extracting the worksheet
            s1.cell_value(0, 0)  # cell from the excel file mentioned through the cell position

            if s1.nrows != 0:  # Counting the number of rows in Excel file
                self.on_close()
        elif self.name == 'YouTube':
            page = requests.get(url3)  # Store the contents of the website under doc
            doc = lh.fromstring(page.content)  # Parse data that are stored between <tr>..</tr> of HTML

            tr_elements = doc.xpath('//tr')  # Create empty list
            res = self.webscraper(tr_elements, 10)

            dictionary = {title: column for (title, column) in res}
            df = pd.DataFrame(dictionary)

            # Excel file
            df.to_excel('youtube.xls', index=False, encoding='utf-8')
            wb = xl.open_workbook('youtube.xls')  # opening & reading the excel file
            s1 = wb.sheet_by_index(0)  # extracting the worksheet
            s1.cell_value(0, 0)  # cell from the excel file mentioned through the cell position

            if s1.nrows != 0:  # Counting the number of rows in Excel file
                self.on_close()
        else:
            messagebox.showerror(title='Error', message='Please choose a social media')

    def exportcsv(self):
        self.name = socialname.get()
        if self.name == 'Instagram':
            page = requests.get(url1)  # Store the contents of the website under doc
            doc = lh.fromstring(page.content)  # Parse data that are stored between <tr>..</tr> of HTML

            tr_elements = doc.xpath('//tr')  # Create empty list
            res = self.webscraper(tr_elements, 5)

            dictionary = {title: column for (title, column) in res}
            df = pd.DataFrame(dictionary)

            # CSV file
            df.to_csv('instagram.csv', index=False, encoding='utf-8')

            with open('instagram.csv', encoding='utf8') as f:
                row_count = sum(1 for line in f)

            if row_count != 0:
                self.on_close()
        elif self.name == 'TikTok':
            page = requests.get(url2)  # Store the contents of the website under doc
            doc = lh.fromstring(page.content)  # Parse data that are stored between <tr>..</tr> of HTML

            tr_elements = doc.xpath('//tr')  # Create empty list
            res = self.webscraper(tr_elements, 8)

            dictionary = {title: column for (title, column) in res}
            df = pd.DataFrame(dictionary)

            # CSV file
            df.to_csv('tiktok.csv', index=False, encoding='utf-8')

            with open('tiktok.csv', encoding='utf8') as f:
                row_count = sum(1 for line in f)

            if row_count != 0:
                self.on_close()
        elif self.name == 'YouTube':
            page = requests.get(url3)  # Store the contents of the website under doc
            doc = lh.fromstring(page.content)  # Parse data that are stored between <tr>..</tr> of HTML

            tr_elements = doc.xpath('//tr')  # Create empty list
            res = self.webscraper(tr_elements, 10)

            dictionary = {title: column for (title, column) in res}
            df = pd.DataFrame(dictionary)

            # CSV file
            df.to_csv('youtube.csv', index=False, encoding='utf-8')

            with open('youtube.csv', encoding='utf8') as f:
                row_count = sum(1 for line in f)

            if row_count != 0:
                self.on_close()
        else:
            messagebox.showerror(title='Error', message='Please choose a social media')

    def exporttext(self):
        self.name = socialname.get()
        if self.name == 'Instagram':
            page = requests.get(url1)  # Store the contents of the website under doc
            doc = lh.fromstring(page.content)  # Parse data that are stored between <tr>..</tr> of HTML

            tr_elements = doc.xpath('//tr')  # Create empty list
            res = self.webscraper(tr_elements, 5)

            dictionary = {title: column for (title, column) in res}
            df = pd.DataFrame(dictionary)

            # Text file
            with open('instagram.txt', 'w', encoding='utf8', newline='') as f:
                dfAsString = df.to_string(header=True, index=False)
                f.write(dfAsString)

            with open('instagram.txt', 'r', encoding='utf8') as f:
                x = len(f.readlines())

            if x != 0:
                self.on_close()
        elif self.name == 'TikTok':
            page = requests.get(url2)  # Store the contents of the website under doc
            doc = lh.fromstring(page.content)  # Parse data that are stored between <tr>..</tr> of HTML

            tr_elements = doc.xpath('//tr')  # Create empty list
            res = self.webscraper(tr_elements, 8)

            dictionary = {title: column for (title, column) in res}
            df = pd.DataFrame(dictionary)

            # Text file
            with open('tiktok.txt', 'w', encoding='utf8', newline='') as f:
                dfAsString = df.to_string(header=True, index=False)
                f.write(dfAsString)

            with open('tiktok.txt', 'r', encoding='utf8') as f:
                x = len(f.readlines())

            if x != 0:
                self.on_close()
        elif self.name == 'YouTube':
            page = requests.get(url3)  # Store the contents of the website under doc
            doc = lh.fromstring(page.content)  # Parse data that are stored between <tr>..</tr> of HTML

            tr_elements = doc.xpath('//tr')  # Create empty list
            res = self.webscraper(tr_elements, 10)

            dictionary = {title: column for (title, column) in res}
            df = pd.DataFrame(dictionary)

            # Text file
            with open('youtube.txt', 'w', encoding='utf8', newline='') as f:
                dfAsString = df.to_string(header=True, index=False)
                f.write(dfAsString)

            with open('youtube.txt', 'r', encoding='utf8') as f:
                x = len(f.readlines())

            if x != 0:
                self.on_close()
        else:
            messagebox.showerror(title='Error', message='Please choose a social media')

    def on_close(self):
        message_test = messagebox.askyesno(title='Success', message='The file is successfully downloaded. Do you want to exit?')
        if message_test:
            root.destroy()

    def webscraper(self, trelements, breakpoint):
        col = []
        i = 0  # For each row, store each first element (header) and an empty list
        for t in trelements[0]:
            i += 1
            name = t.text_content()
            print('%d:"%s"' % (i, name))
            col.append((name, []))
        # Since out first row is the header, data is stored on the second row onwards
        for j in range(1, len(trelements)):
            # T is our j'th row
            T = trelements[j]

            # If row is not of size 10, the //tr data is not from our table
            if len(T) != breakpoint:
                break

            # i is the index of our column
            i = 0

            # Iterate through each element of the row
            for t in T.iterchildren():
                data = t.text_content()
                # Check if row is empty
                if i > 0:
                    # Convert any numerical value to integers
                    try:
                        data = int(data)
                    except:
                        pass
                # Append the data to the empty list of the i'th column
                col[i][1].append(data)
                # Incremen
                i += 1
        return col

class Facade(object):
    def __init__(self, master):
        self.socialmedia = SocialMedia(master)

if __name__ == "__main__":
    root = Tk()
    root.geometry("360x280")
    root.title("Web Scraper")
    root.iconbitmap("webscraper.ico")
    socialname = StringVar()
    formatname = StringVar()
    url1 = 'https://hotinsocialmedia.com/most-followed-instagram-accounts/'
    url2 = 'https://en.wikipedia.org/wiki/List_of_most-followed_TikTok_accounts'
    url3 = 'https://hypeauditor.com/top-youtube/'
    mainFrame = Frame(root)
    mainFrame.pack()
    f = Facade(master=mainFrame)
    root.mainloop()


