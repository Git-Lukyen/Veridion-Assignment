import asyncio
import tkinter
import customtkinter
from tkinter import filedialog as fd
from Scripts import main_script


class MainMenu:
    output_type = 'parquet'
    running = True
    input_file_path = ''

    def __init__(self):
        # Init theme
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        # Init window
        self.menu_root = customtkinter.CTk()
        self.menu_root.geometry("400x500")
        self.menu_root.resizable(False, False)
        self.menu_root.protocol("WM_DELETE_WINDOW", self.close_menu)

        # Init window bar
        self.menu_root.title("Company Address Scraper")
        self.menu_root.iconbitmap("program_icon.ico")

        # Setting top title
        self.app_title = customtkinter.CTkLabel(master=self.menu_root,
                                                text="COMPANY ADDRESS SCRAPER",
                                                font=("Roboto", 24))
        self.app_title.pack(pady=10)

        self.open_input_selector_button = customtkinter.CTkButton(
            self.menu_root,
            height=30,
            width=150,
            text='Input File',
            command=self.open_input_file_dialog,
            fg_color='#5e0023',
            hover_color='#630a2b',
            font=("Roboto", 14)
        )

        self.open_input_selector_button.pack(pady=(15, 3))

        self.input_file_label = customtkinter.CTkLabel(master=self.menu_root,
                                                       text="No File Selected ( .parquet required )",
                                                       font=("Roboto", 16),
                                                       justify="center")
        self.input_file_label.pack()

        self.output_type_label = customtkinter.CTkLabel(master=self.menu_root,
                                                        text="Select Output Type: ",
                                                        font=("Roboto", 16),
                                                        justify="center")
        self.output_type_label.pack(pady=(25, 5))

        self.file_type_select = customtkinter.CTkComboBox(master=self.menu_root,
                                                          values=["parquet", "json"],
                                                          font=("Roboto", 14),
                                                          dropdown_font=("Roboto", 14),
                                                          height=30, width=150,
                                                          fg_color='#5e0023',
                                                          dropdown_fg_color='#5e0023',
                                                          bg_color='#5e0023',
                                                          border_color='#5e0023',
                                                          dropdown_hover_color='#630a2b',
                                                          button_color='#5e0023',
                                                          button_hover_color='#630a2b')

        self.file_type_select.pack()

        self.timeout_label = customtkinter.CTkLabel(master=self.menu_root,
                                                    text="Request Timeout (seconds): 100\nRecommended: >= 100",
                                                    font=("Roboto", 16),
                                                    justify="center")
        self.timeout_label.pack(pady=(35, 5))

        self.timeout_slider = customtkinter.CTkSlider(master=self.menu_root,
                                                      from_=1, to=180,
                                                      fg_color="#5e0023",
                                                      progress_color="#9e335a",
                                                      button_color="#750e72",
                                                      button_hover_color="#750e72",
                                                      command=self.change_timeout_value)
        self.timeout_slider.set(100)
        self.timeout_slider.pack(pady=(10, 0))

        self.retry_failed_checkbox = customtkinter.CTkCheckBox(master=self.menu_root,
                                                               text=" Retry Failed Connections",
                                                               font=("Roboto", 16),
                                                               fg_color="#5e0023",
                                                               hover_color="#630a2b")
        self.retry_failed_checkbox.pack(pady=(35, 5))

        self.search_links_checkbox = customtkinter.CTkCheckBox(master=self.menu_root,
                                                               text=" Search Links in Page",
                                                               font=("Roboto", 16),
                                                               fg_color="#5e0023",
                                                               hover_color="#630a2b")
        self.search_links_checkbox.select()
        self.search_links_checkbox.pack(pady=(10, 5))

        self.start_scrape_button = customtkinter.CTkButton(
            self.menu_root,
            height=40,
            width=160,
            text='Start',
            command=self.start_main_script,
            fg_color='#5e0023',
            hover_color='#630a2b',
            font=("Roboto", 18),
            state='disabled'
        )

        self.start_scrape_button.pack(pady=(25, 0))

        self.stop_scrape_button = customtkinter.CTkButton(
            self.menu_root,
            height=40,
            width=160,
            text='Stop',
            command=self.stop_main_script,
            fg_color='#5e0023',
            hover_color='#630a2b',
            font=("Roboto", 18),
            state='disabled'
        )

        # self.stop_scrape_button.pack(pady=(15, 15))

    def open_input_file_dialog(self):
        filetypes = [
            ('All files', '*.parquet')
        ]

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        if filename != '':
            self.start_scrape_button.configure(state='normal')
            self.input_file_path = filename
            self.input_file_label.configure(text=filename, font=("Roboto", 11))

    def change_timeout_value(self, value):
        self.timeout_label.configure(text=f"Request Timeout (seconds): {int(value)}\nRecommended: >= 100")

    def start_main_script(self):
        main_script.start(self.input_file_path,
                          self.file_type_select.get(),
                          int(self.timeout_slider.get()),
                          _scraping_aux=int(self.search_links_checkbox.get()),
                          _scraping_failed=int(self.retry_failed_checkbox.get()))

        self.start_scrape_button.configure(state='disabled')
        self.stop_scrape_button.configure(state='normal')

    def stop_main_script(self):
        self.start_scrape_button.configure(state='normal')
        self.stop_scrape_button.configure(state='disabled')

    def update_menu(self):
        self.menu_root.update()

    def close_menu(self):
        self.running = False
        self.menu_root.quit()


def main():
    main_menu = MainMenu()

    while main_menu.running:
        main_menu.update_menu()
        resp = main_script.update()
        if resp == 1:
            main_menu.stop_main_script()


if __name__ == '__main__':
    main()
