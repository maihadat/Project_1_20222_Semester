from tkinter import *
from Database import *
from tkinter import ttk
from Crawler import *
from Sorter import *


class Table:
    def __init__(self, root, total_rows, total_columns, lst):

        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):
                self.entry = Entry(root, width=40, foreground="blue", background='lightblue', font=('Times', 15, "bold"))
                self.entry.grid(row=i, column=j)
                self.entry.insert(END, lst[i][j])


class MainScreen:
    def __init__(self, database):
        self.platform_dic = database[1]
        self.support_dic = database[2]
        self.training_dic = database[3]
        self.typical_dic = database[4]
        self.re_crawled = False
        self.root = Tk()
        self.root.title("Cloud Service Crawler")
        self.root.configure(background='skyblue')
        self.list_of_items = database[0]
        self.list_of_items_to_show = self.list_of_items[:]
        self.frame1 = Frame(self.root, background="skyblue")
        self.frame2 = Frame(self.root, background="skyblue")
        self.scroll_bar = Scrollbar(self.frame1, orient=VERTICAL)
        self.list_box = Listbox(self.frame1, width=50, height=20, background="skyblue4", foreground="white",
                                yscrollcommand=self.scroll_bar.set, font=("Times", 20))
        self.scroll_bar.config(command=self.list_box.yview)
        self.scroll_bar.pack(side=RIGHT, fill=Y, pady=60)
        for i in self.list_of_items_to_show:
            self.list_box.insert('end', i.get_string())
        self.list_box.pack(pady=60)
        self.entry = Entry(self.root, width=40, borderwidth=2, font=("Times", 20))
        self.entry.grid(row=0, column=0,  pady=10)

        def search_button_clicked():
            search_item = self.entry.get()
            tmp = []
            for service in self.list_of_items:
                if search_item.lower() in service.name.lower():
                    tmp.append(service)
            self.list_of_items_to_show = tmp[:]
            self.list_box.delete(0, 'end')
            for i in self.list_of_items_to_show:
                self.list_box.insert('end', i.get_string())

        def reset_button_clicked():
            if self.re_crawled is True:
                database = get_service_from_db()
                list_of_items = database[0]
                self.platform_dic = database[1]
                self.support_dic = database[2]
                self.training_dic = database[3]
                self.typical_dic = database[4]
                self.list_of_items = list_of_items
                self.list_of_items_to_show = list_of_items[:]
                self.re_crawl = False
            tmp = []
            for i in self.list_of_items:
                tmp.append(i)
            self.list_of_items_to_show = tmp[:]
            self.list_box.delete(0, 'end')
            self.combobox1.current(0)
            self.combobox2["values"] = ["----------"]
            self.combobox2.current(0)
            for i in self.list_of_items:
                self.list_box.insert('end', i.get_string())
            self.entry.delete(0, 'end')

        def choose():
            choice = self.list_box.get(ANCHOR)
            comma_ind = choice.find(",")
            index = int(choice[4:comma_ind])
            for service in self.list_of_items:
                if service.id == index:
                    chosen_service = service
                    break
            top = Toplevel()
            top.title("Chosen Service")
            top.config(background="lightblue")
            # top.config(background="yellow")
            frame3 = Frame(top, background="lightblue")
            frame1 = Frame(frame3, background="lightblue3")
            frame2 = Frame(frame3, background="lightblue4")
            sub_frame3 = Frame(top, background="lightblue3")
            sub_frame1 = Frame(sub_frame3, background="lightblue3")
            sub_frame2 = Frame(sub_frame3, background="lightblue4")
            frame4 = Frame(top, background="lightblue")
            frame5 = Frame(top, background="lightblue")
            name_title = Label(frame1, text="Name:", width=15, justify=LEFT, anchor="w", background="lightblue3", font=("Times", 15))
            name_title.grid(row=0, column=0, pady=5)
            name = Label(frame2, text=chosen_service.name, width=120, justify=LEFT, anchor="w", background="lightblue4", font=("Times", 15))
            name.grid(row=0, column=0, pady=5)
            star_title = Label(frame1, text="Star:", width=15, justify=LEFT, anchor="w", background="lightblue3", font=("Times", 15))
            star_title.grid(row=1, column=0)
            star = Label(frame2, text=str(round(chosen_service.star, 1)), width=120, justify=LEFT, anchor="w", background="lightblue4", font=("Times", 15))
            star.grid(row=1, column=0)
            platform_title = Label(frame1, text="Platform: ", width=15, justify=LEFT, anchor="w", background="lightblue3", font=("Times", 15))
            platform_title.grid(row=2, column=0, pady=5)
            platform = Label(frame2, text=chosen_service.platform[0].replace("\n", ","), width=120, justify=LEFT, anchor="w", background="lightblue4", font=("Times", 15))
            platform.grid(row=2, column=0, pady=5)
            support_title = Label(frame1, text="Support:", width=15, justify=LEFT, anchor="w", background="lightblue3", font=("Times", 15))
            support_title.grid(row=3, column=0)
            support = Label(frame2, text=chosen_service.support[0].replace("\n", ","), width=120, justify=LEFT, anchor="w", background="lightblue4", font=("Times", 15))
            support.grid(row=3, column=0)
            training_title = Label(frame1, text="Training:", width=15, justify=LEFT, anchor="w", background="lightblue3", font=("Times", 15))
            training_title.grid(row=4, column=0, pady=5)
            training = Label(frame2, text=chosen_service.training[0].replace("\n", ","), width=120, justify=LEFT, anchor="w", background="lightblue4", font=("Times", 15))
            training.grid(row=4, column=0, pady=5)
            typical_title = Label(frame1, text="Typical:", width=15, justify=LEFT, anchor="w", background="lightblue3", font=("Times", 15))
            typical_title.grid(row=5, column=0)
            typical = Label(frame2, text=chosen_service.typical[0].replace("\n", ","), width=120, justify=LEFT, anchor="w", background="lightblue4", font=("Times", 15))
            typical.grid(row=5, column=0)
            time_title = Label(frame1, text="Time Crawled:", width=15, justify=LEFT, anchor="w", background="lightblue3", font=("Times", 15))
            time_title.grid(row=6, column=0)
            time = Label(frame2, text=chosen_service.time, width=120, justify=LEFT, anchor="w", background="lightblue4", font=("Times", 15))
            time.grid(row=6, column=0)
            price_title = Label(sub_frame1, text="Price:", width=15, justify=LEFT, anchor="w", pady=20, background="lightblue3", font=("Times", 15))
            price_title.grid(row=0, column=0)
            price = Label(sub_frame2, text=line_separate(chosen_service.price), width=120, justify=LEFT, anchor="w", pady=20, background="lightblue4", font=("Times", 15))
            price.grid(row=0, column=0)
            reviews = chosen_service.reviews
            good_reviews, bad_reviews = reviews[0].split("\n"), reviews[1].split("\n")
            list = [("Good Reviews", "Bad Reviews")]
            if len(good_reviews) == len(bad_reviews):
                for i in range(len(good_reviews)):
                    list.append((good_reviews[i], bad_reviews[i]))
                review_table = Table(frame4, len(good_reviews) + 1, 2, list)
            else:
                diff = abs(len(good_reviews) - len(bad_reviews))
                if len(good_reviews) > len(bad_reviews):
                    for i in range(len(good_reviews) - diff):
                        list.append((good_reviews[i], bad_reviews[i]))
                    for i in range(diff):
                        list.append((good_reviews[i+diff], ""))
                    review_table = Table(frame4, len(good_reviews) + 1, 2, list)
                else:
                    for i in range(len(bad_reviews) - diff):
                        list.append((good_reviews[i], bad_reviews[i]))
                    for i in range(diff):
                        list.append(("", bad_reviews[i + diff]))
                    review_table = Table(frame4, len(bad_reviews) + 1, 2, list)
            security_label = Label(frame5, text="Security Service Entry:", background="lightblue", foreground="blue", font=("Times", 15, "bold"))
            security_label.grid(row=0, column=0)

            def update_button_clicked():
                chosen_service.secure = security_entry.get()
                service_table = DatabaseConnector('service')
                service_table.update_security_service(chosen_service.secure, str(chosen_service.id))

            security_entry = Entry(frame5, background="lightblue3", width=50, foreground="darkblue", font=("Times", 15))
            if chosen_service.secure != "":
                security_entry.insert(END, chosen_service.secure)
            security_entry.grid(row=1, column=0)
            update_button = Button(frame5, text="Update", padx=50, width=4, height=1, font=("Times", 15),
                                   foreground="purple", command=update_button_clicked)
            update_button.grid(row=2, column=0, pady=10)
            frame1.grid(row=0, column=0)
            frame2.grid(row=0, column=1)
            sub_frame1.grid(row=1, column=0)
            sub_frame2.grid(row=1, column=1)
            frame3.pack()
            sub_frame3.pack()
            frame4.pack(pady=10)
            frame5.pack()

        def sort_by_star():
            for i in range(len(self.list_of_items_to_show)):
                for j in range(len(self.list_of_items_to_show)-1):
                    if self.list_of_items_to_show[j].less_than_star(self.list_of_items_to_show[j+1]):
                        tmp = self.list_of_items_to_show[j]
                        self.list_of_items_to_show[j] = self.list_of_items_to_show[j+1]
                        self.list_of_items_to_show[j+1] = tmp
            self.list_box.delete(0, 'end')
            for i in self.list_of_items_to_show:
                self.list_box.insert('end', i.get_string())

        def sort_by_name():
            for i in range(len(self.list_of_items_to_show)):
                for j in range(len(self.list_of_items_to_show)-1):
                    if not self.list_of_items_to_show[j].less_than_name(self.list_of_items_to_show[j+1]):
                        tmp = self.list_of_items_to_show[j]
                        self.list_of_items_to_show[j] = self.list_of_items_to_show[j+1]
                        self.list_of_items_to_show[j+1] = tmp
            self.list_box.delete(0, 'end')
            for i in self.list_of_items_to_show:
                self.list_box.insert('end', i.get_string())

        def combobox1_clicked(event):
            result = self.combobox1.get()
            if result == "All":
                self.combobox2["values"] = ["----------"]
                self.combobox2.current(0)
                self.list_box.delete(0, 'end')
                for i in self.list_of_items_to_show:
                    self.list_box.insert('end', i.get_string())
            elif result == "Typical Customer":
                self.combobox2["values"] = [self.typical_dic[x][0] for x in self.typical_dic.keys()] + ["----------"]
            elif result == "Support options":
                self.combobox2["values"] = [self.support_dic[x][0] for x in self.support_dic.keys()] + ["----------"]
            elif result == "Training options":
                self.combobox2["values"] = [self.training_dic[x][0] for x in self.training_dic.keys()] + ["----------"]
            elif result == "Platform using":
                self.combobox2["values"] = [self.platform_dic[x][0] for x in self.platform_dic.keys()] + ["----------"]

        def combobox2_clicked(event):
            result1 = self.combobox1.get()
            result2 = self.combobox2.get()
            tmp = []
            if result2 != "----------":
                for service in self.list_of_items_to_show:
                    if result1 == "Typical Customer" and service.typical[0] == result2:
                        tmp.append(service)
                    elif result1 == "Support options" and service.support[0] == result2:
                        tmp.append(service)
                    elif result1 == "Training options" and service.training[0] == result2:
                        tmp.append(service)
                    elif result1 == "Platform using" and service.platform[0] == result2:
                        tmp.append(service)
                self.list_box.delete(0, 'end')
                for i in tmp:
                    self.list_box.insert('end', i.get_string())
            else:
                self.list_box.delete(0, 'end')
                for i in self.list_of_items_to_show:
                    self.list_box.insert('end', i.get_string())

        def recrawl():
            self.re_crawl = True
            self.list_of_items = []
            self.platform_dic = []
            self.support_dic = []
            self.training_dic = []
            self.typical_dic = []
            self.list_of_items_to_show = []
            self.list_box.delete(0, 'end')
            crawler = Crawler()
            crawler.crawl()
            sort = Sorter(crawler.list_of_services)
            sort.sort()
            insert_info_ele(sort.training, 'training_option')
            insert_info_ele(sort.support, 'support_options')
            insert_info_ele(sort.typical, 'typical_customer')
            insert_info_ele(sort.platform, 'platform')
            insert_info_service_review(sort.reviews, 'review')
            insert_info_service_review(sort.info, 'info')
            insert_info_service_review(sort.service, 'service')

        self.search_button = Button(self.root, text="Search", padx=50, width=4, height=1, font=("Times", 15),
                                    foreground="blue", command=search_button_clicked)
        self.search_button.grid(row=0, column=1)
        self.reset_button = Button(self.root, text="Reset", padx=50, width=4, height=1, font=("Times", 15),
                                   foreground="red", command=reset_button_clicked)
        self.reset_button.grid(row=0, column=2)
        self.choose = Button(self.frame2, text="Choose", padx=50, width=4, height=1, font=("Times", 15),
                                   foreground="darkblue", command=choose)
        self.choose.pack(pady=30)
        self.sort_by_star = Button(self.frame2, text="Sort by star", padx=50, width=4, height=1, font=("Times", 15),
                                   foreground="purple", command=sort_by_star)
        self.sort_by_star.pack()
        self.sort_by_name = Button(self.frame2, text="Sort by name", padx=50, width=4, height=1, font=("Times", 15),
                                   foreground="purple", command=sort_by_name)
        self.sort_by_name.pack(pady=30)
        clicked1 = StringVar()
        clicked1.set("All")
        options1 = ["All", "Typical Customer", "Support options", "Training options", "Platform using"]
        clicked2 = StringVar()
        clicked2.set("----------")
        options2 = ["----------"]
        self.combobox1 = ttk.Combobox(self.frame2, value=options1, width=20, height=20, font=("Times", 15),
                                      foreground="darkgreen", background="yellow")
        self.combobox1.current(0)
        self.combobox1.bind("<<ComboboxSelected>>", combobox1_clicked)
        self.combobox1.pack(pady=20)
        self.combobox2 = ttk.Combobox(self.frame2, value=options2, width=20, height=20, font=("Times", 15),
                                      foreground="darkgreen", background="yellow")
        self.combobox2.current(0)
        self.combobox2.bind("<<ComboboxSelected>>", combobox2_clicked)
        self.combobox2.pack(pady=20)
        self.re_crawl = Button(self.frame2, text="Re-Crawling", padx=50, width=4, height=1, font=("Times", 15),
                               foreground="red", command=recrawl)
        self.re_crawl.pack(pady=10)
        self.frame1.grid(row=1, column=0, padx=40)
        self.frame2.grid(row=1, column=1)
        self.root.mainloop()


if __name__=="__main__":
    main_screen = MainScreen(get_service_from_db())


