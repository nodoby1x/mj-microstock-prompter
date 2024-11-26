import streamlit as sl
from gemini_page import GeminiPage
from bulk_prompt import BulkPrompt

sl.set_page_config(page_title="MJ Prompter")

def main():
    # Sidebar navigation
    sl.sidebar.title("MJ Prompter")
    pages = {
        "Gemini" : GeminiPage,
        "Bulk Prompt": BulkPrompt,
    }

    sidebar = sl.sidebar.radio("Menu", list(pages.keys()))

    # Render the selected page
    pages[sidebar]()

if __name__ == "__main__":
    main()
