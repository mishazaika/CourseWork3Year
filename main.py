from tkinter import *
from tkinter import messagebox
import loginSystem
import pymysql
import operator
import socialmenu

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

    def __del__(self):
        conn.close()

    def login(self):
        loginWin = Toplevel(self.master)
        loginPage = loginSystem.LoginPage(loginWin,self)

    def enter(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        label_heading = Canvas(self.master, width=370,height=140)
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
        socialname = StringVar()
        socialname.set("My_Shop")
        for socialmedia in socialmedias:
            b = Radiobutton(self.socialFrame, text=socialmedia[0], variable=socialname, value=socialmedia[0], indicatoron=0)
            b.pack(fill=X)
        self.proceed_button = Button(self.socialFrame, text="Export", command=lambda: self.exportformat(socialname))
        self.proceed_button.config(bg="green3")
        self.proceed_button.pack(side=BOTTOM)

    def exportformat(self, socialmedia):
        self.name = socialmedia.get()
        print("selected socailedia "+self.name)
        if self.name != None:
            for widget in self.socialFrame.winfo_children():
                widget.destroy()
            self.getMenu()
            self.interactiveMenu()
            self.customer()
        else:
            print("Please Select a Shop!")

    def interactiveMenu(self):
        for widget in self.menuFrame.winfo_children():
                widget.destroy()
        label_name = Label(self.menuFrame,text="Format")
        label_name.grid(row=0,column=0)
        self.order = {}
        self.quantity = {}
        r = 1
        for socialmedia in (sorted(self.menu.menu.values(), key=operator.attrgetter("rank"), reverse=True)):
            self.order[socialmedia.name] = IntVar(0)
            self.quantity[socialmedia.name] = 0
            b = Checkbutton(self.menuFrame, text=socialmedia.name, variable=self.order[socialmedia.name])
            b.grid(row=r, column=0, sticky=W)
            r += 1

        proceed_button = Button(self.socialFrame, text="Export", command=lambda: self.export(socialmedia))
        proceed_button.config(bg="green3")
        proceed_button.pack(side=BOTTOM)

    def displayMenu(self):
        for widget in self.menuFrame.winfo_children():
            widget.destroy()
        label_name = Label(self.menuFrame, text="Format")
        label_name.grid(row=0,column=0)
        r = 1
        for socialmedia in (sorted(self.menu.menu.values(), key=operator.attrgetter("rank"), reverse=True)):
            label_name = Label(self.menuFrame,text=socialmedia.name)
            label_name.grid(row=r, column=0)
            r += 1

    def getMenu(self):
        self.menu = socialmenu.Menu()
        sqlQuery = "SELECT * FROM ExportFormat"
        curs.execute(sqlQuery)
        socialmedias = curs.fetchall()
        for values in socialmedias:
            socialmedia = socialmenu.SocialMedia(*values)
            self.menu.add(socialmedia)

    def export(self,socialmedia):
        for widget in self.orderFrame.winfo_children():
            widget.destroy()

        url= "https://www.pararius.com/apartments/amsterdam?ac=1"
        page = requests.get(url)

        soup = BeautifulSoup(page.content, 'html.parser')
        lists = soup.find_all('section', class_="listing-search-item")

        with open('housing.csv', 'w', encoding='utf8', newline='') as f:
            thewriter = writer(f)
            header = ['Title', 'Location', 'Price', 'Area']
            thewriter.writerow(header)

            for list in lists:
                title = list.find('h2', class_="listing-search-item__title").text.replace('\n', '')
                location = list.find('div', class_="listing-search-item__location").text.replace('\n', '')
                price = list.find('div', class_="listing-search-item__price").text.replace('\n', '')
                area = list.find('div', class_="listing-search-item__features").text.replace('\n', '')

                info = [title, location, price, area]
                thewriter.writerow(info)

        with open('housing.csv') as f:
            row_count = sum(1 for line in f)

        if row_count != 0:
            self.on_close()

    def customer(self):
        self.master.master.title(self.name)

        self.orderFrame = Frame(self.master,relief=GROOVE,pady=10)
        self.orderFrame.config(width=360)
        self.orderFrame.pack()

        label_test = Label(self.orderFrame,text="Please choose a format")
        label_test.pack()

    def on_close(self):
        message_test = messagebox.askyesno(title='Success', message='The file is successfully downloaded. Do you want to exit?')
        if message_test:
            root.destroy()

class Facade(object):
    def __init__(self, master):
        self.socialmedia = SocialMedia(master)

if __name__ == "__main__":
    root = Tk()
    root.geometry("360x280")
    root.title("Web Scraper")
    root.iconbitmap("webscraper.ico")
    mainFrame = Frame(root)
    mainFrame.pack()
    f = Facade(master=mainFrame)
    root.mainloop()


