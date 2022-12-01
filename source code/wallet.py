import tkinter as tk
import random, os
from tkinter import ttk
from tkinter import messagebox
from account	import createAccount, encryptAccount, decryptAccount

root = tk.Tk()
root.title("Simple Wallet")
#root.geometry(str(root.winfo_screenwidth())+"x"+str(root.winfo_screenheight())+"+0+0")

#New Account -> input password -> save in encrypted format -> format: pub_key.eea
#Refresh Account -> populate all .eea /encrypted ethereum account

#Listbox -> list of all account
#Delete Account --> delete file  --> delete file
#read account --> input password --> decrypt --> show a window that print private and public account


eeaDB = {}
def refreshAccount():
	global eeaDB 
	eeaDB = {}
	for file in os.listdir():
		print(file)
		if file.endswith(".eea"):
			buf = file.split("_")
			profile = buf[0]
			adr = buf[1].split(".")[0]
			shortadr = profile+"_"+adr[:5]+"_"+adr[-3:]
			eeaDB[shortadr] = file.split(".")[0]
	lb1.delete(0, tk.END)
	for adr in eeaDB:
		lb1.insert(tk.END, adr)


def	btnNewF():
	if not singleton1:
		print("Add new account")
		genTopLevel()
   
def genRandomStr():
	val = str(random.randint(1000000, 9999999))
	for i in range(3):
		val += " " + str(random.randint(1000000, 9999999))
	return val
  
singleton1 = False
def genTopLevel():
	global singleton1
	def clickIt():
		if epwd.get() == epwd2.get():
			profile = ename.get()
			newacc = createAccount(genRandomStr())
			#shortadr = newacc.address[:5]+"_"+newacc.address[-3:]
			encryptAccount(newacc, epwd.get(), profile+"_"+newacc.address+".eea" )
			refreshAccount()
		else:
			messagebox.showerror('Error','The passwords do not match!')
		cekClosing()
	def cekClosing():
		global singleton1
		singleton1 = False
		newWindow.destroy()
	if not singleton1:
		newWindow = tk.Toplevel(root)
		newWindow.title("New Account")
		lblname = tk.Label(newWindow, text = "Profile name:")
		ename = tk.Entry(newWindow, width = 20 )
		
		lblpwd = tk.Label(newWindow, text = "Password:")
		epwd = tk.Entry(newWindow, show="*", width = 20 )
		lblpwd2 = tk.Label(newWindow, text = "Retype:")
		epwd2 = tk.Entry(newWindow, show="*", width = 20 )
		
		
		btnpwd = tk.Button(newWindow, text = "Create Account", command = clickIt)

		lblname.grid(row=0, column = 0, pady=5, padx=3)
		ename.grid(row=0, column = 1, padx=5)
		
		lblpwd.grid(row=2, column = 0, pady=5, padx=3)
		epwd.grid(row=2, column = 1, padx=5)
		lblpwd2.grid(row=3, column = 0, pady=5, padx=3)
		epwd2.grid(row=3, column = 1, padx=5)
		
		btnpwd.grid(row=4, column = 1, pady=5, padx=3)
		newWindow.protocol("WM_DELETE_WINDOW", cekClosing)
		singleton1 = True

btnNew = tk.Button(root, text ="Create New Account", command = btnNewF, width=20)
btnNew.grid(row=0, column = 1, pady =5)

def	btnRefreshF():
	if not singleton1:
		print("Refresh account")
		refreshAccount()

btnRefresh = tk.Button(root, text ="Refresh List", command = btnRefreshF, width=15)
btnRefresh.grid(row=0, column = 0)

lbl1 = tk.Label(root, text = "List of Accounts:",font="Times 10 bold")
lbl1.grid(row=1, column = 0, sticky="nw", padx=5)

lb1 = tk.Listbox(root, height=10, width = 50)#, selectmode = "multiple")
lb1.grid(row=2, column = 0, columnspan=2, padx=5)

selAccount = None
def	lb1Select(event):
	global selAccount
	for k in lb1.curselection():
		seladr = lb1.get(k) 
		print(k, seladr, eeaDB[seladr])
		if not singleton1:
			adr = eeaDB[seladr].split("_")[1]
			eadr.delete(0,tk.END)
			eadr.insert(tk.END, adr)
			selAccount = eeaDB[seladr]
lb1.bind('<<ListboxSelect>>', lb1Select)

def genTopLevel2():
	global singleton1
	def clickIt():
		file = selAccount+".eea"
		pwd= epwd.get()
		decAcc = decryptAccount(file, pwd, True )
		if decAcc != None:
			tpb.delete("1.0",tk.END)
			tpb.insert(tk.END,decAcc.address)
			tpv.delete("1.0", tk.END)
			tpv.insert(tk.END, decAcc.key.hex())
		else:
			messagebox.showerror('Error','Your password is incorrect!')
	def cekClosing():
		global singleton1
		singleton1 = False
		newWindow.destroy()
	if not singleton1:
		newWindow = tk.Toplevel(root)
		newWindow.title("Decrypt Account")
		buf = selAccount.split("_")
		lblProfile = tk.Label(newWindow, text = "Profile: "+buf[0]+" ("+buf[1]+")")
		lblpwd = tk.Label(newWindow, text = "Password:")
		epwd = tk.Entry(newWindow, show="*", width = 32)
		btnpwd = tk.Button(newWindow, text = "Decrypt", command = clickIt)

		lblpb = tk.Label(newWindow, text = "Public Key/Address:")
		tpb = tk.Text(newWindow, height = 1, width = 48)
		
		lblpv = tk.Label(newWindow, text = "Private Key:")
		tpv = tk.Text(newWindow, height = 3, width = 48)
		
		
		#text.insert(tk.END, "")
		
		lblProfile.grid(row=0, column = 0, sticky="nw", columnspan=3)
		lblpwd.grid(row=1, column = 0, sticky="w")
		epwd.grid(row=1, column = 1, sticky="w",padx=5)
		btnpwd.grid(row=1, column = 2)
		
		lblpb.grid(row=2, column = 0, sticky="nw")
		tpb.grid(row=3, column = 0, columnspan=3, sticky="nw",padx=5)
		lblpv.grid(row=4, column = 0, sticky="nw")
		tpv.grid(row=5, column = 0, columnspan=3, sticky="nw", padx=5, pady =5)
		
		newWindow.protocol("WM_DELETE_WINDOW", cekClosing)
		singleton1 = True

def	btnReadF():
	if not singleton1:
		for k in lb1.curselection():
			print("Decrypt",k)
			genTopLevel2()
	
def	btnDeleteF():
	if not singleton1:
		sel = None
		for k in lb1.curselection():
			print("Delete",k)
			sel = lb1.get(k)
			sel = eeaDB[sel]+".eea"
		print(sel)
		if messagebox.askyesno('Confirmation','Delete account: '+lb1.get(k)+'?'):
			print("yes")
			os.remove(sel)
			refreshAccount()
		else:
			print("no")
	
eadr = tk.Entry(root, width = 48 )
#eadr.insert(tk.END, "entry")
eadr.grid(row=3, column = 0, columnspan=2, pady=5)

btnRead = tk.Button(root, text ="Decrypt Account", command = btnReadF, width=15)
btnRead.grid(row=4, column = 0, pady=5)
btnDelete = tk.Button(root, text ="Delete Account", command = btnDeleteF, width=15)
btnDelete.grid(row=4, column = 1, pady=5)

root.mainloop()
