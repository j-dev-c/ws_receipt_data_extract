import os,csv
from PyPDF2 import PdfReader


def find_pdfs(root_dif):
  pdf_files=[]
  for dirpath,dirname,filenames in os.walk(root_dif):
      for filename in filenames:
          if filename.lower().endswith(".pdf"):
            pdf_files.append(os.path.join(dirpath,filename))
  return pdf_files


def extract_data(pdf_list):
  data=[]
  for pdf_file in pdf_list:
    try:
      with open(pdf_file,'rb') as f :
        reader = PdfReader(f).pages[0].extract_text()

            
        date = reader[reader.find("20"):reader.find("20")+10]
        account_name = reader[reader.find("Name:")+5:].split("\n")[0].strip().replace(" ","")
        trans = reader[reader.find("ty\n")+3:].split("\n")[0]
        quantity, details = trans.split("$")
        price = details[:details.find("D")-2].replace(" ","")
        currency, symbol, *company = details.replace(details[:details.find("D")-2], "").split()
        company= " ".join(company).replace("-","").strip()
        
        more_details= reader[reader.find("Account Number"):].split("\n")
        account_num= more_details[0].replace("Account Number:","").strip()
        order_num, gross = more_details[3].split("Gross: $")
        order_num = order_num.replace("Order Number:","").replace(" ","")
        # gross=gross.replace(currency,"").strip()

        commision = more_details[4].replace("Commission: $","").strip()
        exchange = more_details[5].replace("Exchange:","").strip()
        net_ammount = more_details[7].replace("Net Amount: $","").strip()
        posted = more_details[8].replace("For Settlement On:","").strip()


        data.append({"date":date,"name":account_name,
                     "quantity":quantity, "price":price,"currency" :currency,
                     "symbol":symbol ,"company":company,"account_number":account_num, 
                     "order_num":order_num,"gross":gross ,"commision":commision,"exchange":exchange,
                     "net_ammount":net_ammount,"posted":posted})
     
    except  Exception as e :
       print("error",e)

  return data


def csv_export(data):
   with open("output.csv", 'w') as csvfile:
    
    writer = csv.DictWriter(csvfile, fieldnames = data[0].keys())
    
    # Write the header
    writer.writeheader()
    
    # Write the data rows
    writer.writerows(data)

def main():
   root_dir ="./"
   csv_export(extract_data(find_pdfs(root_dir)))


if __name__ =="__main__":
   main()
