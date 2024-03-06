from tkinter import *
import sqlite3
from tkinter import messagebox


class contact(Tk):
    def create_database(self):

        self.my_cursor.execute('CREATE TABLE IF NOT EXISTS save_contact(Full_name TEXT,Phone_number TEXT UNIQUE)')

    def __init__(self):

        Tk.__init__(self)
        self.geometry('178x145+400+250')
        self.title('Contact')


        self.conector=sqlite3.connect('contact.db')
        self.my_cursor=self.conector.cursor()

        self.btn_add=Button(self,text='Add item',font=('Times New Roman',20),width=14,command=self.add)
        self.btn_add.grid(row=0,column=0)
        self.btn_search=Button(self,text='Search item',font=('Times New Roman',20),width=14,command=self.search)
        self.btn_search.grid(row=1,column=0)
        self.btn_updel=Button(self,text='Delete',font=('Times New Roman',20),width=14,command=self.delete)
        self.btn_updel.grid(row=2,column=0)
        self.btn_updel=Button(self,text='Exit',font=('Times New Roman',20),width=14,command=lambda:self.destroy())
        self.btn_updel.grid(row=3,column=0)

    def by_pn(self):
        if self.rdt_val.get()==1:
            self.ent2.config(state='normal')
            self.ent2.delete(0,END)
            self.ent2.config(state='disabled')
            self.ent2.config(state='disabled')
            self.ent1.config(state='normal')
        elif self.rdt_val.get()==2:
            self.ent1.config(state='normal')
            self.ent1.delete(0,END)
            self.ent1.config(state='disabled')
            self.ent1.config(state='disabled')
            self.ent2.config(state='normal')

    def add(self):
        self.save_number=Toplevel(self)
        self.save_number.title('save')
        self.save_number.geometry('340x150+600+250')

        self.lbl1=Label(self.save_number,text='Full name',font=('Times New Roman',20))
        self.lbl2=Label(self.save_number,text='Phone number',font=('Times New Roman',20))

        self.ent1=Entry(self.save_number,width=20,border=3,relief='solid')
        self.ent2=Entry(self.save_number,width=20,border=3,relief='solid')

        self.btn1=Button(self.save_number,text='Add',font=('Times New Roman',20),width=30,command=self.add_item)
        self.btn2=Button(self.save_number,text='Exit',font=('Times New Roman',20),width=30,command=lambda:self.save_number.destroy())

        self.lbl1.grid(row=0,column=0)
        self.lbl2.grid(row=1,column=0)
        self.ent1.grid(row=0,column=1)
        self.ent2.grid(row=1,column=1)
        self.btn1.grid(row=2,column=0,columnspan=2)
        self.btn2.grid(row=3,column=0,columnspan=2)

    def add_item(self):
        try:

            if len(self.ent1.get())>0 and len(self.ent2.get())>0:
                if self.ent2.get().startswith('09') and len(self.ent2.get())==11:
                    name = self.ent1.get()
                    number = self.ent2.get()
                    file = [name, number]
                    self.my_cursor.execute('INSERT INTO save_contact(Full_name, Phone_number) VALUES (?, ?)', file)
                    self.conector.commit()
                    self.ent1.delete(0,END)
                    self.ent2.delete(0,END)
                else:
                    messagebox.showerror("invalid number","enter correct phone number!")
            else:
                messagebox.showerror("empty fields","The fields are empty!")
        except:
                messagebox.showerror("duplicate number","It is a duplicate number!")

    def search(self):
        self.search_number=Toplevel(self)
        self.search_number.title('Search')
        self.search_number.geometry('340x210+600+250')

        self.lbl1=Label(self.search_number,text='Full name',font=('Times New Roman',20))
        self.lbl2=Label(self.search_number,text='Phone number',font=('Times New Roman',20))
        

        self.ent1=Entry(self.search_number,width=20,border=3,relief='solid',state='disabled')
        self.ent1.bind("<KeyRelease>",self.search_item)       
        self.ent2=Entry(self.search_number,width=20,border=3,relief='solid',state='disabled')
        self.ent2.bind("<KeyRelease>",self.search_item)
        self.lbl3=Listbox(self.search_number,height=5)

        self.lbl1.grid(row=1,column=0)
        self.lbl2.grid(row=2,column=0)
        self.ent1.grid(row=1,column=1)
        self.ent2.grid(row=2,column=1)
        self.lbl3.grid(row=3,column=0,columnspan=2)

        self.btn1=Button(self.search_number,text='Exit',font=('Times New Roman',20),width=30,command=lambda:self.search_number.destroy())        
        self.btn1.grid(row=4,column=0,columnspan=2)

        self.rdt_val=IntVar()
        self.rdt1=Radiobutton(self.search_number,text='by name',variable=self.rdt_val,value=1,command=self.by_pn)
        self.rdt2=Radiobutton(self.search_number,text='by phone number',variable=self.rdt_val,value=2,command=self.by_pn) 

        self.rdt1.grid(row=0,column=0)
        self.rdt2.grid(row=0,column=1)

    def search_item(self,x):
        if self.rdt_val.get() == 1:
            self.ent2.config(state='normal')
            self.ent2.delete(0,END)
            self.ent2.config(state='disabled')
            self.lbl3.delete(0,END)
            self.ent1.config(state='normal')
            self.my_cursor.execute(f"SELECT * FROM save_contact WHERE Full_name LIKE '%{self.ent1.get()}%' ")
            result = self.my_cursor.fetchall()
            for i in result:
                self.lbl3.insert(END,i)

        elif self.rdt_val.get() == 2:
            self.ent1.config(state='normal')
            self.ent1.delete(0,END)
            self.ent1.config(state='disabled')
            self.lbl3.delete(0,END)
            self.ent2.config(state='normal')
            self.my_cursor.execute(f"SELECT * FROM save_contact WHERE Phone_number LIKE '%{self.ent2.get()}%' ")
            result = self.my_cursor.fetchall()
            for i in result:
                self.lbl3.insert(END,i)

    def delet_item(self):
        if self.rdt_val.get()==1:
            if len(self.ent1.get())>0:
                self.my_cursor.execute(f'DELETE FROM save_contact WHERE Full_name="{self.ent1.get()}"')
                self.conector.commit()
                messagebox.showinfo('deleted',f'{self.ent1.get()} was deleted')
                self.ent1.delete(0,END)
            else:
                messagebox.showerror('empty','Full name is empty')
        elif self.rdt_val.get()==2:
            if len(self.ent2.get())>0:
                self.my_cursor.execute(f'DELETE FROM save_contact WHERE Phone_number="{self.ent2.get()}"')
                self.conector.commit()
                messagebox.showinfo('deleted',f'{self.ent2.get()} was deleted')
                self.ent2.delete(0,END)
            else:
                messagebox.showerror('empty','Phone number is empty')

    def delete(self):

        self.delete_number=Toplevel(self)
        self.delete_number.title('Delete')
        self.delete_number.geometry('340x150+600+250')

        self.lbl1=Label(self.delete_number,text='Full name',font=('Times New Roman',20))
        self.lbl2=Label(self.delete_number,text='Phone number',font=('Times New Roman',20))
        

        self.ent1=Entry(self.delete_number,width=20,border=3,relief='solid',state='disabled')
        self.ent2=Entry(self.delete_number,width=20,border=3,relief='solid',state='disabled')

        self.lbl1.grid(row=1,column=0)
        self.lbl2.grid(row=2,column=0)
        self.ent1.grid(row=1,column=1)
        self.ent2.grid(row=2,column=1)
 


        self.btn1=Button(self.delete_number,text='Delete',font=('Times New Roman',20),width=30,command=self.delet_item)        
        self.btn1.grid(row=3,column=0,columnspan=2)
        self.btn2=Button(self.delete_number,text='Exit',font=('Times New Roman',20),width=30,command=lambda:self.delete_number.destroy())        
        self.btn2.grid(row=4,column=0,columnspan=2)

        self.rdt_val=IntVar()
        self.rdt1=Radiobutton(self.delete_number,text='by name',variable=self.rdt_val,value=1,command=self.by_pn)
        self.rdt2=Radiobutton(self.delete_number,text='by phone number',variable=self.rdt_val,value=2,command=self.by_pn) 

        self.rdt1.grid(row=0,column=0)
        self.rdt2.grid(row=0,column=1)




if __name__ == "__main__":
    main = contact()
    main.create_database()
    main.mainloop()