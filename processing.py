import datetime as dt
import pandas as pd
from io import StringIO

'''
    input: any number of strings specifying the organization along with unit names
    names should be input in hierarchical order, from highest to lowest
    in the hierarchy

    output: string with the below structure

    ORG: <unit #1>; <unit#2>; etc
'''

class StringBuilder:
     _file_str = None

     def __init__(self):
         self._file_str = StringIO()

     def append(self, str):
         self._file_str.write(str)

     def __str__(self):
         return self._file_str.getvalue()

def write_ORG(*units):

    if len(units) == 0:
        return ""

    newunits = []

    for i in range(0,len(units)):
        newunits.append(units[i].replace(',','\\,'))


    ret = "ORG:" + ";".join(newunits) + '\r\n'

    return ret

'''
description: Function for creating N field in VCF
inputs:
    - familyName string
    - givenName string
    - addName string
    - honorPref string
    - honorSuf string

output: string in the format below
    N: <familyName>;<givenName>;<addName>;<honorPref>;<honorSuf>

'''

def write_N(
    familyName="",
    givenName="",
    addName="",
    honorPref="",
    honorSuf=""
):
    
    familyName = familyName.replace(",","\\,")
    givenName = givenName.replace(",","\\,")
    addName = addName.replace(",","\\,")
    honorPref = honorPref.replace(",","\\,")
    honorSuf = honorSuf.replace(",","\\,")

    res = f'N:{familyName};{givenName};{addName};{honorPref};{honorSuf}\r\n'
    
    return res


'''
description: functin for creating FN type
inputs:
    - name string
outpus: formatted string
    FN:<name>
'''
def write_FN(name=""):

    if len(name) < 3:
        name = "See Company"

    name = name.replace(',','\\,')

    ret = f'FN:{name}\r\n'
    return ret

'''
description: functin for creating ROLE type
inputs:
    - role string
outpus: formatted string
    ROLE:<name>

    USE TITLE INSTEAD
'''
def write_ROLE(role=""):
    if role == "":
        return ""

    role = role.replace(',','\\,')

    ret = f'ROLE:{role}\r\n'
    return ret


def write_TITLE(title=""):
    if title == "":
        return ""

    title = title.replace(',','\\,')

    ret = f'TITLE:{title}\r\n'
    return ret



''' 
description: create type
inputs: 
    - pobox string
    - extendedAdr string
    - streetLine1 string
    - streetLine2 string
    - streetLine3 string
    - locality string
    - region string
    - type enum tuple [dom, intl,postal,parcel,home,work]

output: string in the followign format

    ADR;TYPE=<type>:<pobox>;<extendedAdr>;<streetLine1>\,<streetLine2>\,<streetLine3>;<locality;<region>

'''

def write_ADR(
    pobox="",
    extendedAdr="",
    streetLine1="",
    streetLine2="",
    streetLine3="",
    locality="",
    region="",
    postalCode="",
    countryName="United States",
    type="HOME"
):

    if (pobox == "" and extendedAdr == "" and streetLine1 == "" and streetLine2 == "" 
    and streetLine3 == "" and locality == "" and region == "" and postalCode == ""):
        return ""

    # fix commas
    pobox = pobox.replace(',','\\,')
    extendedAdr = extendedAdr.replace(',','\\,')
    streetLine1 = streetLine1.replace(',','\\,').replace('\n',"")
    streetLine2 = streetLine2.replace(',','\\,').replace('\n',"")
    streetLine3 = streetLine3.replace(',','\\,').replace('\n',"")
    locality = locality.replace(',','\\,')
    region = region.replace(',','\\,')
    postalCode = postalCode.replace(',','\\,')
    countryName = countryName.replace(',','\\,')

    # add commas to street lines
    if len(streetLine2) > 0:
        streetLine2 = '\\n' + streetLine2

    if len(streetLine3) > 0:
        streetLine3 = '\\n' + streetLine3

    ret = f'ADR;TYPE={type}:{pobox};{extendedAdr};{streetLine1}{streetLine2}{streetLine3};{locality};\
{region};{postalCode};{countryName}\r\n'
    return ret

'''
description: create telephone type
input: 
- tel string
- type string

output: string with the folowing format
    TEL;TYPE=<type>:<tel>
'''

def write_TEL(tel="",type="HOME"):

    if tel == "":
        return ""

    ret = f'TEL;TYPE={type}:{tel}\r\n'
    return ret
    
def write_BDAY(bday=""):
    if bday == "":
        return ""

    if bday =="0/0/00":
        return ""

    # assuming format is mm/dd/yyyy
    dateobj = bday.split('/')

    dateobj = dt.date(int(dateobj[2]),int(dateobj[0]),int(dateobj[1]))
    dateobj = dateobj.isoformat()

    ret = f'BDAY:{dateobj}\r\n'
    return ret

def write_EMAIL(email="",type="HOME"):

    if email.lower().startswith("/o"):
        return ""

    if email =="":
        return ""

    ret = f'EMAIL;TYPE={type}:{email}\r\n'
    return ret

def write_NOTE(prefix,text):
    return ""

def write_URL(url=""):
    if url=="":
        return ""

    ret = f'URL:{url}\r\n'
    return ret

        
f = open("out.vcf",'w')
f.write("")
f.close()



## MAIN
## MAIN
## MAIN

df = pd.read_csv("./Contacts.csv")

df = df.fillna('')


count = 0
fileCount = 0

for i in range(0,len(df)):

    sb = StringBuilder()

    cur = df.iloc[i]

    sb.append("BEGIN:VCARD\r\n")
    sb.append("VERSION:3.0\r\n")

    fullName = cur["First Name"] + " " + cur["Last Name"]
    sb.append(write_FN(fullName))

    sb.append(write_N(familyName=cur["Last Name"],givenName=cur["First Name"],addName=cur["Middle Name"]))

    sb.append(write_ORG(cur["Company"],cur["Department"]))

    sb.append(write_TITLE(cur["Job Title"]))

    sb.append(write_ADR(
        streetLine1=cur["Business Street"],
        locality=cur["Business City"],
        region=cur["Business State"],
        postalCode=cur["Business Postal Code"],
        type="WORK"
    ))

    sb.append(write_ADR(
        streetLine1=cur["Home Street"],
        locality=cur["Home City"],
        region=cur["Home State"],
        postalCode=cur["Home Postal Code"],
        type="HOME"
    ))

    sb.append(write_TEL(cur["Business Phone"],type="WORK"))
    sb.append(write_TEL(cur["Home Phone"],type="HOME"))
    sb.append(write_TEL(cur["Mobile Phone"],type="Mobile"))

    sb.append(write_EMAIL(cur["E-mail Address"],type="WORK"))
    sb.append(write_EMAIL(cur["E-mail 2 Address"]))
    sb.append(write_EMAIL(cur["E-mail 3 Address"]))




    #notes
    sb.append("NOTE:")

    rawnotes = cur["Notes"].split("\r\n")
    notes = StringBuilder()
    for note in rawnotes:
        if note != "":
            notes.append(note + "\\n")

    notes = notes.__str__()
    if notes != "0" and notes != "" and len(notes) > 0:
        sb.append(notes + "\\n")

    account = cur["Account"]
    if account != "":
        sb.append("Acccount:" + account + "\\n")

    anniverary = cur["Anniversary"]
    if anniverary != "0/0/00" and anniverary != "":
        sb.append("Anniversary:" + anniverary + "\\n")

    birthday = cur["Birthday"]
    if birthday != "" and birthday != "0/0/00":
        sb.append("Birthday:" + birthday + "\\n")

    initials = cur["Initials"]
    if initials != "":
        sb.append("Initials:" + initials + "\\n")

    manager = cur["Manager's Name"]
    if  not manager.lower().startswith("/o") and manager != "":
        sb.append("Manager:" + manager + "\\n")

    officeLoc = cur["Office Location"]
    if officeLoc != "":
        sb.append("Office Location:" + officeLoc + "\\n")
    
    user = cur["User 1"]
    if user != "":
        sb.append("User:" + user + "\\n")
    
    sb.append("\r\n")

    sb.append("END:VCARD\r\n")

    f = open("./out/out" + str(fileCount) + ".vcf",'a')
    f.write(sb.__str__())
    f.close()

    count = count + 1
    if count > 100:
        fileCount = fileCount + 1
        count = 0




