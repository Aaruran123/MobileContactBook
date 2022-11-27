from tkinter import *
import random

contactFileName = 'contactDB.txt'
# initialize the name of the text file to store and retrive data

# Class contains details of each contact
class Contact:
    def __init__(self,name,email,phone, isFav):
        self.name= name
        self.email = email
        self.phone = phone
        self.isFav = isFav
    
    # Appends the data in the object to the file 
    def saveToFile(self):
        contactFile = open(contactFileName, 'a+') 
        contactFile.write(self.name + "|" + self.email + "|" + self.phone + "|"+ "{}".format(self.isFav)+ "|" + '\n' ) 
        contactFile.close() 

    # Make the object a favourite contact and edit the text file
    def makeFavourite(self,e):
        if(not self.isFav):
            self.isFav = True
            contactFile = open(contactFileName, 'r') 
            rawData = contactFile.readlines()
            contactFile = open(contactFileName, 'w') 
            for data in rawData:
                if(data.split("|")[0] == self.name):
                    contactFile.write(self.name + "|" + self.email + "|" + self.phone + "|"+ "{}".format(self.isFav)+ "|" + '\n' ) 
                else:
                    contactFile.write(data)
            contactFile.close()
    # embed contact details in to a frame
    def packToComponent(self,masterFrame,includeFavBtn):
        contactFrame = Frame(masterFrame)
        nameLbl = Label(contactFrame,text=self.getDetails(), width=200)
        nameLbl.pack(fill=Y)
        if(includeFavBtn):
            markAsFavBtn = Button(contactFrame, text="Mark as Favourite")
            markAsFavBtn.bind("<Button-1>",self.makeFavourite)
            markAsFavBtn.pack()
        contactFrame.pack(fill=X)

    def getDetails(self):
        return self.name + ' - ' + self.phone + ' - ' + self.email
    def getName(self):
        return self.name
    def checkIsFavourite(self):
        return self.isFav

# Class managing the UI and the list of all contacts 
class ContactBook:
    def __init__(self):
        self.allContacts = []
        self.allSearchResults = []

        self.ContactBookUI = Tk()
        self.ContactBookUI.geometry("600x600")
        actionBtnFrame = Frame(self.ContactBookUI)
        topLbl = Label(actionBtnFrame, text="Contact Manager", fg='orange')
        topLbl.pack(pady=(10,15))

        addNewBtn = Button(actionBtnFrame, text="Add New Contact")
        addNewBtn.bind("<Button-1>",self.addNewContact)
        addNewBtn.pack(side=LEFT , padx=15)

        searchBtn = Button(actionBtnFrame, text="Search", fg='blue')
        searchBtn.bind("<Button-1>",self.openSearch)
        searchBtn.pack(side=LEFT)
        actionBtnFrame.pack(side=TOP, pady=(5,10))

        self.favouritesFrame = Frame(self.ContactBookUI)
        favouriteLbl = Label(self.favouritesFrame, text="Favourite Contacts")
        favouriteLbl.pack()
        self.refreshBtn = Button(self.favouritesFrame, text="Refresh")
        self.refreshBtn.bind("<Button-1>", self.refreshFavourites)
        
        self.favouritesFrame.pack(side=TOP, pady=10)
        self.loadAllContacts()
        self.ContactBookUI.mainloop()
    
    # Add new Contact Popup
    def addNewContact(self,e):
        self.AddNewContactUI = Tk()
        self.AddNewContactUI.wm_title("Add a new contact")
        self.AddNewContactUI.geometry("300x300")

        nameLbl = Label(self.AddNewContactUI, text="Name")
        self.nameEntry = Entry(self.AddNewContactUI)
        nameLbl.pack()
        self.nameEntry.pack()

        emailLbl = Label(self.AddNewContactUI, text="Email")
        self.emailEntry = Entry(self.AddNewContactUI)
        emailLbl.pack()
        self.emailEntry.pack()

        phoneLbl = Label(self.AddNewContactUI, text="Phone")
        self.phoneEntry = Entry(self.AddNewContactUI)
        phoneLbl.pack()
        self.phoneEntry.pack()

        saveBtn= Button(self.AddNewContactUI, text="Save")
        saveBtn.bind("<Button-1>",self.handleOnSave)
        saveBtn.pack()
    # Hanlde on save trigger event
    def handleOnSave(self,e):
        tempName = self.nameEntry.get()
        tempPhone = self.phoneEntry.get()
        tempEmail = self.emailEntry.get()
        if(len(tempName)> 0 ):
            tempNewContact = Contact(tempName,tempEmail,tempPhone,False)
            self.allContacts.append(tempNewContact)
            tempNewContact.saveToFile()
            self.AddNewContactUI.destroy()
    
    # Loading existing data from the text file
    def loadAllContacts(self):
        contactsFile = open(contactFileName, 'r+') 
        rawContacts = contactsFile.readlines()
        
        for person in rawContacts:
            details = person.split("|")
            isFavContact = False
            if(details[3]== "True"):
                isFavContact = True
            tempContact = Contact(details[0],details[1],details[2], isFavContact)
            self.allContacts.append(tempContact)

        for contact in self.allContacts:
            if(contact.checkIsFavourite()):
                contact.packToComponent(self.favouritesFrame, False)
    # refresh favorites from the list - detected minor bug 
    def refreshFavourites(self,e):
        for contact in self.allContacts:
            self.refreshBtn.pack_forget()
            if(contact.checkIsFavourite()):
                contact.packToComponent(self.favouritesFrame, False)
    # Handle Search UI and results 
    def openSearch(self,e):
        self.refreshBtn.pack()
        self.SearchUI = Tk()
        self.SearchUI.wm_title("Search Contacts")
        self.SearchUI.geometry("400x600")
        self.SearchHeaderFrame = Frame(self.SearchUI)

        self.searchEntry = Entry(self.SearchHeaderFrame)
        self.searchEntry.pack(side=LEFT)

        searchBtn = Button(self.SearchHeaderFrame, text="Search", bg= 'deep sky blue')
        searchBtn.bind("<Button-1>",self.handleOnSearch)
        searchBtn.pack(side=LEFT, padx=10)
        self.SearchHeaderFrame.pack(side=TOP, pady=10)

    # Searches the array using the Membership Operand
    def handleOnSearch(self,e):
        self.SearchHeaderFrame.pack_forget()
        SearchResultsFrame = Frame(self.SearchUI)

        searchTxt = self.searchEntry.get()
        if(len(searchTxt)>0):
            for contact in self.allContacts:
                if(searchTxt.lower() in contact.getName().lower()):
                    contact.packToComponent(SearchResultsFrame,True)
                    self.allSearchResults.append(contact)
        
        SearchResultsFrame.pack(side=TOP)


# Object declaration
THEContactBook = ContactBook()
