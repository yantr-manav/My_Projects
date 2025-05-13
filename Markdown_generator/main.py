import streamlit as st

# Page configuration
st.set_page_config(page_title="Markdown Generator", page_icon=":guardsman:", layout="wide")
st.title("Markdown Generator")
st.markdown("This app generates a Markdown file with the specified content. You can add text, images, tables, code snippets, and more. Once you're done, you can download the generated Markdown file.")

st.write("## Instructions")
st.write("""
1. Choose the type of content you want to add to the Markdown file from the dropdown menu.
2. Fill in the required fields for the selected content type.
3. Click the 'Add to Markdown' button to add the content to the Markdown file.
4. Click the 'Download Markdown' button to download the generated Markdown file.
""")
st.divider()



# Columns layout
left,right = st.columns([2,1])

# Initialize markdown content
if "markdown_content" not in st.session_state:
    st.session_state.markdown_content = ""

with right:
    pass

with st.sidebar:
    option = st.selectbox("Choose what to add in the Markdown file", 
                          options=["Title", "Text", "Image", "Table", "Code", "List", "Link", "Quote", "Horizontal Line", 
                                   "Checkbox", "Button", "Select Box", "Radio Button", "Date Input", "Time Input", 
                                   "File Uploader", "Progress Bar", "Spinner", "Expander", "Sidebar", "Markdown"],
                          label_visibility="collapsed")
    
    content = ""
    if option == "Title":
        title = st.text_input("Enter the title", label_visibility="collapsed")
        level = st.selectbox("Select the level of the title", options=["1", "2", "3", "4", "5", "6"], label_visibility="collapsed")
        content = f"{'#' * int(level)} {title}\n\n"
    elif option == "Text":
        text = st.text_area("Enter the text", label_visibility="collapsed")
        content = f"{text}\n\n"
    elif option == "Image":
        image_url = st.text_input("Enter the image URL", label_visibility="collapsed")
        alt_text = st.text_input("Enter the alt text", label_visibility="collapsed")
        content = f"![{alt_text}]({image_url})\n\n"
    elif option == "Table":
        table_data = st.text_area("Enter the table data (comma-separated)", label_visibility="collapsed")
        rows = table_data.split("\n")
        if rows:
            content = "| " + " | ".join(rows[0].split(",")) + " |\n"
            content += "|" + "|".join(["---"] * len(rows[0].split(","))) + "|\n"
            for row in rows[1:]:
                content += "| " + " | ".join(row.split(",")) + " |\n"
            content += "\n"
    elif option == "Code":
        code = st.text_area("Enter the code", label_visibility="collapsed")
        language = st.selectbox("Select the programming language", options=["python", "javascript", "html", "css"], label_visibility="collapsed")
        content = f"```{language}\n{code}\n```\n\n"
        
        # List ka output change kr .. not that good
        
    elif option == "List":
        list_items = st.text_area("Enter the list items (comma-separated)", label_visibility="collapsed")
        
        items = list_items.split(",")
        content = "- " + "\n- ".join(items) + "\n\n"
    elif option == "Link":
        link_text = st.text_input("Enter the link text", label_visibility="collapsed")
        link_url = st.text_input("Enter the link URL", label_visibility="collapsed")
        content = f"[{link_text}]({link_url})\n\n"
    elif option == "Quote":
        quote_text = st.text_area("Enter the quote text", label_visibility="collapsed", placeholder="Quote text")
        quote_author = st.text_input("Enter the quote author", label_visibility="collapsed",placeholder="Quote author")
        content = f"> {quote_text}\n> \n> - {quote_author}\n\n"
    elif option == "Horizontal Line":
        content = "---\n\n"
    elif option == "Checkbox":
        checkbox_text = st.text_input("Enter the checkbox text", label_visibility="collapsed")
        content = f"- [ ] {checkbox_text}\n\n"
    elif option == "Button":
        button_text = st.text_input("Enter the button text", label_visibility="collapsed")
        button_url = st.text_input("Enter the button URL", label_visibility="collapsed")
        content = f"[{button_text}]({button_url})\n\n"
    elif option == "Select Box":
        select_box_text = st.text_input("Enter the select box text", label_visibility="collapsed")
        select_box_options = st.text_area("Enter the select box options (comma-separated)", label_visibility="collapsed")
        options = select_box_options.split(",")
        content = f"{select_box_text}:\n- " + "\n- ".join(options) + "\n\n"
    elif option == "Radio Button":
        radio_button_text = st.text_input("Enter the radio button text", label_visibility="collapsed")
        radio_button_options = st.text_area("Enter the radio button options (comma-separated)", label_visibility="collapsed")
        options = radio_button_options.split(",")
        content = f"{radio_button_text}:\n- " + "\n- ".join(options) + "\n\n"
    elif option == "Date Input":
        date_input_text = st.text_input("Enter the date input text", label_visibility="collapsed")
        date = st.date_input("Select a date")
        content = f"{date_input_text}: {date}\n\n"
    elif option == "Time Input":
        time_input_text = st.text_input("Enter the time input text", label_visibility="collapsed")
        time = st.time_input("Select a time")
        content = f"{time_input_text}: {time}\n\n"
    elif option == "File Uploader":
        file_uploader_text = st.text_input("Enter the file uploader text", label_visibility="collapsed")
        st.file_uploader("Upload a file")
        content = f"{file_uploader_text}: [File uploaded]\n\n"
    elif option == "Progress Bar":
        progress_bar_text = st.text_input("Enter the progress bar text", label_visibility="collapsed")
        st.progress(0)
        content = f"{progress_bar_text}: [Progress bar]\n\n"
    elif option == "Spinner":
        spinner_text = st.text_input("Enter the spinner text", label_visibility="collapsed")
        with st.spinner(spinner_text):
            st.write("Loading...")
        content = f"{spinner_text}: Loading...\n\n"
    elif option == "Expander":
        expander_text = st.text_input("Enter the expander text", label_visibility="collapsed")
        with st.expander(expander_text):
            st.write("This is the content inside the expander.")
        content = f"{expander_text}: This is the content inside the expander.\n\n"
    elif option == "Sidebar":
        sidebar_text = st.text_input("Enter the sidebar text", label_visibility="collapsed")
        with st.sidebar:
            st.write(sidebar_text)
        content = f"{sidebar_text}: This is the content inside the sidebar.\n\n"
    elif option == "Markdown":
        markdown_text = st.text_area("Enter the Markdown text", label_visibility="collapsed")
        content = f"{markdown_text}\n\n"

    if st.button("Add to Markdown"):
        st.session_state.markdown_content += content

# Center column for preview and downloads
with left:
    st.write("## Markdown Preview")
    st.markdown(st.session_state.markdown_content)

    st.download_button("Download Markdown", st.session_state.markdown_content, "markdown.md", "text/markdown")

    st.write("## Markdown Content")
    st.text_area("Markdown Content", st.session_state.markdown_content, height=300)

    st.write("## Clear Markdown Content")
    if st.button("Clear Markdown Content"):
        st.session_state.markdown_content = ""
        st.write("Markdown content cleared.")
    else:
        st.write("Click the button to clear the Markdown content.")
        
