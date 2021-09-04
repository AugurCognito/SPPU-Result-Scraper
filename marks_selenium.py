from selenium import webdriver
import re
import argparse

if __name__ == "__main__":

    parser= argparse.ArgumentParser(description="""
    Webscraps SPPU exam result from CSV.
    CSV should in in the format-
    <Seatno>,<Student Name>,<Student's Mother's name>
    """)
    parser.add_argument("--inputFile","-i",metavar="<File Name>",default="input.csv",type=str,help="CSV file name from which data will be collected, deafult is input.csv")
    parser.add_argument("--outputFile","-o",metavar="<File Name>",default="output.csv",type=str,help="CSV file name in which data will be written, deafult is output.csv")
    args=parser.parse_args()

    browser = webdriver.Firefox()

    # here we input link where input fields are
    browser.get(
        "http://results.unipune.ac.in/MCOM2013_Credit.aspx?Course_Code=70119&Course_Name=F.E.(2019+CREDIT+PAT.)+APR-MAY+2021"
    )

    # here we create regular expression for finding sgpa
    rslt_re = re.compile(r"(YEAR SGPA :- )(\d\.\d\d)")

    # Opening files to Read and Write data
    input_csv = open(args.inputFile, "r")
    output_csv = open(args.outputFile, "w")

    for line in input_csv.readlines():
        seat_field = browser.find_element_by_id("ctl00_ContentPlaceHolder1_txtSeatno")
        mother_field = browser.find_element_by_id("ctl00_ContentPlaceHolder1_txtMother")
        result_btn = browser.find_element_by_id("ctl00_ContentPlaceHolder1_btnSubmit")

        data = line.split(",")
        print(data[1], "result ", end=">")

        # Clears Fields
        seat_field.clear()
        mother_field.clear()

        # Enter Seats Number, Mother's name and click on result button
        seat_field.send_keys(data[0])
        mother_field.send_keys(data[2])
        result_btn.click()

        # If data is wrong, or result page isnt present for this specific person, skip
        try:
            tables = browser.find_elements_by_tag_name("table")
        except:
            print("Data Present is Wrong")
            browser.back()
            continue
        result_string = tables[1].text
        match = rslt_re.search(result_string)
        try:
            print(match.group(2))
            output_csv.write(f"{data[1]},{match.group(2)}\n")
        except:
            print("Error")
            output_csv.write(f"{data[1]},\n")
