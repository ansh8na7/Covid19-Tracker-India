# track covid 19 cases in India using web scrapping
# importing libraries
import requests
import bs4
import tkinter as tk
import plyer
import time
import os
import datetime
import threading


def corona_details_india():
    url = "https://www.mohfw.gov.in/"
    html_doc = requests.get(url)
    soup = bs4.BeautifulSoup(html_doc.text, 'html.parser')
    soup = soup.find("div", class_='site-stats-count').find_all("strong")
    text_list = ['Active Cases : ', 'Cured/Discharged : ', 'Deaths : ', 'Migrated : ']
    text = ""
    for i, element in enumerate(soup):
        text = text + text_list[i] + element.get_text() + "\n"

    return text

def refresh():
    print("Refreshing...")
    newdata = corona_details_india()
    Details['text'] = newdata

# notification:
def notify():
    while True:
        title = "new Covid 19 cases: "
        message = corona_details_india()
        os.system("""
                      osascript -e 'display notification "{}" with title "{}"'
                      """.format(message, title))
        time.sleep(30)



# making gui
root = tk.Tk()
root.geometry("700x600")
root.title("Covid 19 Tracker - India")
root.iconbitmap("icon.ico")
titleImg = tk.PhotoImage(file="emblem.png")
tk.Label(root, image=titleImg).pack()
tk.Label(root, text="from GOI").pack()
Details = tk.Label(root, text=corona_details_india(), font=("Roboto", 25, "bold"))
Details.pack()

refresh_button = tk.Button(root, text="Refresh", font=("Roboto", 25, "bold"), relief='solid', command=refresh)
refresh_button.pack()

# threading for notification
t1 = threading.Thread(target=notify)
t1.setDaemon(True)
t1.start()

if __name__ == '__main__':
    root.mainloop()