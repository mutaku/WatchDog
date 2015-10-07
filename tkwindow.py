from Tkinter import *
from Queue import Empty, Full


class Report(object):
    def __init__(self, q):
        self.root = Tk()
        self.root.title("WatchDog")
        self.root.config(bg="grey")

        self.report = LabelFrame()
        self.report.config(
                bg="lightgrey",
                padx=2,
                pady=2,
                relief=GROOVE,
                borderwidth=1)
        self.report.grid()

        self.scrollyMSG = Scrollbar(
                self.report,
                orient=VERTICAL)
        self.scrollxMSG = Scrollbar(
                self.report,
                orient=HORIZONTAL)
        self.msg = Listbox(
                self.report,
                selectmode=EXTENDED,
                fg="black",
                activestyle="none",
                selectbackground="grey",
                width=120,
                height=20,
                xscrollcommand=self.scrollxMSG.set,
                yscrollcommand=self.scrollyMSG.set)
        self.scrollyMSG.config(
                command=self.msg.yview,
                highlightbackground="white")
        self.scrollyMSG.grid(
                row=1,
                column=1,
                rowspan=4,
                sticky=N+S)
        self.scrollxMSG.config(
                command=self.msg.xview,
                highlightbackground="white")
        self.scrollxMSG.grid(
                column=0,
                sticky=E+W)
        self.msg.grid(
                row=1,
                column=0,
                rowspan=4,
                sticky=E+W)

        self.root.after(100,
                self.CheckQueuePoll,
                q)

    def CheckQueuePoll(self, c_queue):
        try:
            data = c_queue.get(0)
            self.updateMSG(data)
        except Empty:
            pass
        finally:
            self.root.after(100,
                    self.CheckQueuePoll,
                    c_queue)

    def updateMSG(self, data):
        self.msg.insert(END, data)
        self.msg.see(END)
