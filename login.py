from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import sqlite3
import os
import smtplib
import time

class Login_System:
    def __init__(self,root):
        self.root=root
        self.root.title("Inventory Management System Login Page ")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#fafafa")
        self
        self.otp = ''
        
        # ====images============
        self.phone_image = ImageTk.PhotoImage(file="images/phone.png")
        self.lbl_phone_image = Label(self.root, image=self.phone_image, bd=0)
        self.lbl_phone_image.place(x=200, y=90)
        
        # =======Login Frame=====
        self.employee_id = StringVar()
        self.password = StringVar()
        
        login_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        login_frame.place(x=650, y=90, width=350, height=460)
        
        title = Label(login_frame, text="Login Page", font=("Arial", 30, "bold"), bg="white")
        title.place(x=0, y=30, relwidth=1)
        
        lbl_user = Label(login_frame, text="Employee ID", font=("Andalus", 15), bg="white", fg="#767171")
        lbl_user.place(x=50, y=100)
        txt_employee_id = Entry(login_frame, textvariable=self.employee_id, font=("times now roman", 15), bg="#ECECEC")
        txt_employee_id.place(x=50, y=140, width=250)
        
        lbl_pass = Label(login_frame, text="Password", font=("Andalus", 15), bg="white", fg="#767171")
        lbl_pass.place(x=50, y=200)
        txt_pass = Entry(login_frame, textvariable=self.password, show="*", font=("times now roman", 15), bg="#ECECEC")
        txt_pass.place(x=50, y=240, width=250)
        
        btn_login = Button(login_frame, command=self.login, text="Log In", font=("Arial Rounded MT Bold", 15), bg="#00B0F0", activebackground="#00B0F0", fg="white", activeforeground="white", cursor="hand2")
        btn_login.place(x=50, y=300, width=250, height=35)
        
        hr = Label(login_frame, bg="lightgray")
        hr.place(x=50, y=370, width=250, height=2)
        or_ = Label(login_frame, text="OR", bg="white", fg="lightgray", font=("times new roman", 15, "bold"))
        or_.place(x=150, y=355)

        btn_forget = Button(login_frame, text="Forget Password", command=self.forget_window, font=("times new roman", 13), bg="white", fg="#00759E", bd=0, activebackground="white", activeforeground="#00759E", cursor="hand2")
        btn_forget.place(x=100, y=390)

        # ====frame2=======
        register_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        register_frame.place(x=650, y=570, width=350, height=60)
        
        lbl_reg = Label(register_frame, text=("Don't have an account ?"), font=("times new roman", 13, "bold"), bg="white")
        lbl_reg.place(x=0, y=20, relwidth=1)

        # ===animation images=============
        self.im1 = ImageTk.PhotoImage(file="images/im1.png")
        self.im2 = ImageTk.PhotoImage(file="images/im2.png")
        self.im3 = ImageTk.PhotoImage(file="images/im3.png")

        self.lbl_change_image = Label(self.root, bg="gray")
        self.lbl_change_image.place(x=367, y=195, width=240, height=428) 
        
        self.animate()
        #self.send_email('xyz')
        # Uncomment to send email
        

    # ==============all functions================

    def animate(self):
        self.im = self.im1
        self.im1 = self.im2
        self.im2 = self.im3
        self.im3 = self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000, self.animate)    

    def login(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.employee_id.get() == "" or self.password.get() == "":
                messagebox.showerror("Error", "All fields are required", parent=self.root)
            else:
                cur.execute("Select utype from employee where eid=? AND pass=?", (self.employee_id.get(), self.password.get()))
                user = cur.fetchone()
                if user is None:
                    messagebox.showerror("Error", "Invalid USERNAME / PASSWORD", parent=self.root)
                else:
                    if user[0] == "Admin": 
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def forget_window(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.employee_id.get() == "":
                messagebox.showerror("Error", "Employee ID must be required", parent=self.root)
            else:
                cur.execute("Select email from employee where eid=?", (self.employee_id.get(),))
                email = cur.fetchone()
                if email is None:
                    messagebox.showerror("Error", "Invalid Employee ID, try again", parent=self.root)
                else:
                    # ======forget window==============
                    self.var_otp = StringVar()
                    self.var_new_pass = StringVar()
                    self.var_conf_pass = StringVar()
                    # ==call send email function===
                    self.forget_win = Toplevel(self.root)
                    self.forget_win.title('RESET PASSWORD')
                    self.forget_win.geometry('400x350+500+100')
                    self.forget_win.focus_force()
                    
                    title = Label(self.forget_win, text="Reset Password", font=('goudy old style', 15, "bold"), bg="#3f51b5", fg="white")
                    title.pack(side=TOP, fill=X)
                    
                    lbl_reset = Label(self.forget_win, text="Enter OTP Sent on Registered email", font=("times now roman", 15))
                    lbl_reset.place(x=20, y=60)
                    
                    txt_reset = Entry(self.forget_win, textvariable=self.var_otp, font=("times now roman", 15), bg="lightyellow")
                    txt_reset.place(x=20, y=100, width=250, height=30)
                    
                    btn_reset = Button(self.forget_win, text="SUBMIT", command=self.verify_otp, cursor="hand2", font=("times now roman", 15), bg="lightblue")
                    btn_reset.place(x=280, y=100, width=100, height=30)
                    
                    lbl_new_pass = Label(self.forget_win, text="New Password", font=("times now roman", 15))
                    lbl_new_pass.place(x=20, y=160)
                    
                    txt_new_pass = Entry(self.forget_win, textvariable=self.var_new_pass, font=("times now roman", 15), bg="lightyellow")
                    txt_new_pass.place(x=20, y=190, width=250, height=30)
                    
                    lbl_c_pass = Label(self.forget_win, text="Confirm Password", font=("times now roman", 15))
                    lbl_c_pass.place(x=20, y=225)
                    
                    txt_c_pass = Entry(self.forget_win, textvariable=self.var_conf_pass, font=("times now roman", 15), bg="lightyellow")
                    txt_c_pass.place(x=20, y=255, width=250, height=30)
                    
                    self.btn_update = Button(self.forget_win, text="UPDATE", command=self.update_password, cursor="hand2", state='disabled', font=("times now roman", 15), bg="lightblue")
                    self.btn_update.place(x=150, y=300, width=100, height=30)
                  
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
            
    def send_email(self, to_):
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        email_ = 'your_email@gmail.com'  # Update with your email
        pass_ = 'your_password'  # Update with your password
        
        s.login(email_, pass_)
        
        self.otp = str(time.strftime("%H%M%S")) + str(time.strftime("%S"))
        message = f'Subject: OTP for Password Reset\n\nYour OTP is: {self.otp}'
        s.sendmail(email_, to_, message)
        s.quit()
        
    def verify_otp(self):
        if self.var_otp.get() == self.otp:
            self.btn_update.config(state='normal')
            messagebox.showinfo("Success", "OTP verified successfully!")
        else:
            messagebox.showerror("Error", "Invalid OTP!")
            
    def update_password(self):
        new_pass = self.var_new_pass.get()
        conf_pass = self.var_conf_pass.get()
        
        if new_pass == conf_pass:
            # Update password in the database
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            cur.execute("UPDATE employee SET pass=? WHERE eid=?", (new_pass, self.employee_id.get()))
            con.commit()
            con.close()
            
            messagebox.showinfo("Success", "Password updated successfully!")
            self.forget_win.destroy()
        else:
            messagebox.showerror("Error", "Passwords do not match!")
            
root = Tk()
obj = Login_System(root)
root.mainloop()

