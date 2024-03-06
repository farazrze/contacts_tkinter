    def search(self):
        self.search_number=Toplevel(self)
        self.search_number.title('Search')
        self.search_number.geometry('340x180+600+250')

        self.lbl1=Label(self.search_number,text='Full name',font=('Times New Roman',20))
        self.lbl2=Label(self.search_number,text='Phone number',font=('Times New Roman',20))
        

        self.ent1=Entry(self.search_number,width=20,border=3,relief='solid',state='disabled')
        self.ent1.bind("<KeyRelease>",self.search_item)       
        self.ent2=Entry(self.search_number,width=20,border=3,relief='solid',state='disabled')
        self.ent2.bind("<KeyRelease>",self.search_item)
        self.lbl3=Label(self.search_number,height=3)

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
            self.lbl3.config(text='')
            self.ent1.config(state='normal')
            self.my_cursor.execute(f"SELECT * FROM save_contact WHERE Full_name LIKE '%{self.ent1.get()}%' ")
            result = self.my_cursor.fetchall()
            for i in result:
                self.lbl3.config(text=i)

        elif self.rdt_val.get() == 2:
            self.lbl3.config(text='')
            self.ent2.config(state='normal')
            self.my_cursor.execute(f"SELECT * FROM save_contact WHERE Phone_number LIKE '%{self.ent2.get()}%' ")
            result = self.my_cursor.fetchall()
            for i in result:
                self.lbl3.config(text=i)
