from tkinter import filedialog  
from tkinter import *

import re
root=Tk()
editor=Text(root)
editor.pack(expand='yes')
editor.storeobj={}
def hello():
    print ("hello!")


def open_file():
     path = filedialog.askopenfilename()
     if path:
         data=open(path,"rb").read()
         editor.delete('1.0','end')
         editor.insert("1.0", data)
         editor.storeobj['OpenFile']=path
         trigger(None)
     return


def save_file():
  if not editor.storeobj['OpenFile']:
   path = filedialog.asksaveasfilename()
  else:
   path = editor.storeobj['OpenFile']
  if path:
   data = editor.get("1.0",'end')
   f_=open(path,"w+")
   f_.write(data)
   f_.close()
   editor.storeobj['OpenFile']=path
  return


def save_as():
  path = filedialog.asksaveasfilename()
  if path:
   data = editor.get("1.0",'end')
   f_=open(path,"w+")
   f_.write(data)
   f_.close()
  return


def quit():
  import sys
  sys.exit(0)
  return



    



def analyzer():
    keyword=r"(\b)+(?P<KEYWORD>False|None|True|and|as|assert|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\b"
    comment =r"(?P<COMMENT>#[^\n]*)"
    string1 =r"(?P<STRING>'[^'\\\n]*'?)"
    string2=r'(?P<STRING2>"[^"\\\n]*"?)'
    string3=r"(?P<STRING3>'''.*)"
    string4=r'(?P<STRING4>""".*)'
    fstring3=r"(?P<STRING5>'''.*(''(?!'))*('''))"
    fstring4=r'(?P<STRING6>""".*("(?!""))*("""))'
    return keyword + "|" + comment + "|" + fstring4 +"|"  + string4 + "|" + string2 + "|" + fstring3 + "|" + string3 + "|" + string1

def myfun():
    editor.insert("This app was created by Mohit Agrawal" )
    return

def findcords(start,end,string):
    srow=string[:start].count('\n')+1 # starting row
    splitlines=string[:start].split('\n')
    if len(splitlines)!=0:
        splitlines=splitlines[len(splitlines)-1]
    scol=len(splitlines)# Ending Column
    lrow=string[:end+1].count('\n')+1
    lcolsplitlines=string[:end].split('\n')
    if len(lcolsplitlines)!=0:
        lcolsplitlines=lcolsplitlines[len(lcolsplitlines)-1]
    lcol=len(lcolsplitlines)+1# Ending Column
    return '{}.{}'.format(srow, scol),'{}.{}'.format(lrow, lcol)

def check(k={}):
    if k['COMMENT']!=None:
    	return 'comment','red'
    elif k['KEYWORD']!=None:
    	return 'keyword','blue'
    elif k['STRING5']!=None:
       # print("hhhhhhhhh")
        return 'string','green'    	
    elif k['STRING3']!=None:
       # print("sab sahi hai")
        return 'string','green'
    elif k['STRING2']!=None:
    	return 'string','green'
    elif k['STRING']!=None:
        #print("kuch to gadbad hai")
        return 'string','green'
    elif k['STRING4']!=None:
    	return 'string','green'
    elif k['STRING6']!=None:
    	return 'string','green'    
    else:
    	return 'ss','NILL'
        
s=re.compile(analyzer(),re.S)

def trigger(event):
    txt=editor.get('1.0','end')
    if len(txt)==1:
        return
    for i in ['comment','string','keyword']:
            editor.tag_remove(i,'1.0','end')
    for i in s.finditer(txt):
            start=i.start()
            end=i.end()-1
            
            ttype,color=check(k=i.groupdict())
            if color!='NILL':
                ind1,ind2=findcords(start,end,txt)
                #print ind1, ind2
                editor.tag_add(ttype,ind1, ind2)
                editor.tag_config(ttype,foreground=color)


editor.bind("<Any-KeyPress>", trigger)
editor.pack()
menubar = Menu(root)
    
    
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=open_file)
filemenu.add_command(label="Save", command=save_file)
filemenu.add_command(label="SaveAs", command=save_as)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=quit)
menubar.add_cascade(label="File", menu=filemenu)


helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=myfun)
menubar.add_cascade(label="Help", menu=helpmenu)

# display the menu
root.config(menu=menubar)


root.mainloop()






