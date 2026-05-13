import streamlit as st
from pathlib import Path
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="File Manager",
    page_icon="🗂️",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Syne:wght@400;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

/* Background */
.stApp {
    background: #0d0d0d;
    color: #f0f0f0;
}

h1, h2, h3 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111 !important;
    border-right: 1px solid #2a2a2a;
}

/* Buttons */
.stButton > button {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    background: #e8ff47;
    color: #0d0d0d;
    border: none;
    border-radius: 4px;
    padding: 0.5rem 1.4rem;
    transition: all 0.15s ease;
    letter-spacing: 0.03em;
}
.stButton > button:hover {
    background: #fff;
    color: #0d0d0d;
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(232,255,71,0.3);
}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea textarea {
    font-family: 'JetBrains Mono', monospace;
    background: #1a1a1a !important;
    border: 1px solid #2e2e2e !important;
    border-radius: 4px;
    color: #f0f0f0 !important;
}
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: #e8ff47 !important;
    box-shadow: 0 0 0 2px rgba(232,255,71,0.15) !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: #1a1a1a !important;
    border: 1px solid #2e2e2e !important;
    color: #f0f0f0 !important;
    font-family: 'JetBrains Mono', monospace;
}

/* Radio */
.stRadio label {
    font-family: 'JetBrains Mono', monospace;
    color: #aaa;
}

/* Success / Error / Warning / Info */
.stSuccess, .stAlert {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
}

/* Code / file listing box */
.file-list {
    background: #141414;
    border: 1px solid #2a2a2a;
    border-radius: 6px;
    padding: 1rem 1.2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: #9effa0;
    max-height: 240px;
    overflow-y: auto;
    line-height: 1.8;
}

/* Tag pill */
.tag {
    display: inline-block;
    background: #1f1f1f;
    border: 1px solid #333;
    border-radius: 3px;
    padding: 1px 8px;
    font-size: 0.75rem;
    font-family: 'JetBrains Mono', monospace;
    color: #e8ff47;
    margin-right: 4px;
}

/* Divider accent */
hr { border-color: #2a2a2a; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────

def list_items() -> list:
    """Return all files/folders relative to cwd."""
    return sorted(Path('').rglob('*'))


def render_file_list():
    items = list_items()
    if not items:
        st.markdown('<div class="file-list">📭 No files or folders found.</div>',
                    unsafe_allow_html=True)
        return
    rows = "".join(
        f'<div>{"📁" if item.is_dir() else "📄"} {item}</div>'
        for item in items
    )
    st.markdown(f'<div class="file-list">{rows}</div>', unsafe_allow_html=True)


# ── Header ────────────────────────────────────────────────────────────────────

st.markdown("## 🗂️ File Manager")
st.markdown("CRUD operations for files & folders")
st.divider()

# ── Sidebar – operation picker ────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### Operations")
    operation = st.selectbox(
        "Choose an action",
        [
            "📄 Create File",
            "👁️ Read File",
            "✏️ Update File",
            "🗑️ Delete File",
            "🔤 Rename File",
            "📁 Create Folder",
            "🗑️ Delete Folder",
            "📋 List All",
        ],
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown("**Current directory**")
    st.code(str(Path.cwd()), language=None)

# ── Main panel ────────────────────────────────────────────────────────────────

# ── 1. CREATE FILE ────────────────────────────────────────────────────────────
if operation == "📄 Create File":
    st.markdown("### 📄 Create File")
    render_file_list()
    st.write("")
    file_name = st.text_input("File name (e.g. notes.txt)")
    content   = st.text_area("Content", height=160, placeholder="Type your content here…")
    if st.button("Create File"):
        if not file_name.strip():
            st.warning("Please enter a file name.")
        else:
            p = Path(file_name.strip())
            if p.exists():
                st.error(f"'{file_name}' already exists.")
            else:
                try:
                    p.write_text(content)
                    st.success(f"✅ '{file_name}' created successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")

# ── 2. READ FILE ──────────────────────────────────────────────────────────────
elif operation == "👁️ Read File":
    st.markdown("### 👁️ Read File")
    render_file_list()
    st.write("")
    file_name = st.text_input("File name to read")
    if st.button("Read File"):
        if not file_name.strip():
            st.warning("Please enter a file name.")
        else:
            p = Path(file_name.strip())
            if not p.exists():
                st.error(f"'{file_name}' not found.")
            elif p.is_dir():
                st.warning("That is a folder, not a file.")
            else:
                try:
                    data = p.read_text()
                    st.markdown(f'<span class="tag">📄 {file_name}</span>', unsafe_allow_html=True)
                    st.code(data, language=None)
                except Exception as e:
                    st.error(f"Error: {e}")

# ── 3. UPDATE FILE ────────────────────────────────────────────────────────────
elif operation == "✏️ Update File":
    st.markdown("### ✏️ Update File")
    render_file_list()
    st.write("")
    file_name = st.text_input("File name to update")
    mode      = st.radio("Update mode", ["Overwrite", "Append"], horizontal=True)
    content   = st.text_area("New content", height=140)
    if st.button("Update File"):
        if not file_name.strip():
            st.warning("Please enter a file name.")
        else:
            p = Path(file_name.strip())
            if not p.exists():
                st.error(f"'{file_name}' not found.")
            else:
                try:
                    if mode == "Overwrite":
                        p.write_text(content)
                        st.success("✅ File overwritten successfully!")
                    else:
                        with open(p, 'a') as f:
                            f.write("\n" + content)
                        st.success("✅ Content appended successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")

# ── 4. DELETE FILE ────────────────────────────────────────────────────────────
elif operation == "🗑️ Delete File":
    st.markdown("### 🗑️ Delete File")
    render_file_list()
    st.write("")
    file_name = st.text_input("File name to delete")
    if st.button("Delete File", type="primary"):
        if not file_name.strip():
            st.warning("Please enter a file name.")
        else:
            p = Path(file_name.strip())
            if not p.exists():
                st.error(f"'{file_name}' not found.")
            elif p.is_dir():
                st.warning("That is a folder. Use 'Delete Folder' instead.")
            else:
                try:
                    os.remove(p)
                    st.success(f"✅ '{file_name}' deleted.")
                except Exception as e:
                    st.error(f"Error: {e}")

# ── 5. RENAME FILE ────────────────────────────────────────────────────────────
elif operation == "🔤 Rename File":
    st.markdown("### 🔤 Rename File")
    render_file_list()
    st.write("")
    file_name = st.text_input("Current file name")
    new_name  = st.text_input("New file name")
    if st.button("Rename File"):
        if not file_name.strip() or not new_name.strip():
            st.warning("Please fill in both fields.")
        else:
            p = Path(file_name.strip())
            if not p.exists():
                st.error(f"'{file_name}' not found.")
            else:
                try:
                    p.rename(new_name.strip())
                    st.success(f"✅ Renamed to '{new_name}'.")
                except Exception as e:
                    st.error(f"Error: {e}")

# ── 6. CREATE FOLDER ──────────────────────────────────────────────────────────
elif operation == "📁 Create Folder":
    st.markdown("### 📁 Create Folder")
    render_file_list()
    st.write("")
    folder_name = st.text_input("Folder name")
    if st.button("Create Folder"):
        if not folder_name.strip():
            st.warning("Please enter a folder name.")
        else:
            p = Path(folder_name.strip())
            if p.exists():
                st.error(f"'{folder_name}' already exists.")
            else:
                try:
                    p.mkdir(parents=True)
                    st.success(f"✅ Folder '{folder_name}' created!")
                except Exception as e:
                    st.error(f"Error: {e}")

# ── 7. DELETE FOLDER ──────────────────────────────────────────────────────────
elif operation == "🗑️ Delete Folder":
    st.markdown("### 🗑️ Delete Folder")
    render_file_list()
    st.write("")
    folder_name = st.text_input("Folder name to delete")
    st.caption("⚠️ Folder must be empty before deleting.")
    if st.button("Delete Folder", type="primary"):
        if not folder_name.strip():
            st.warning("Please enter a folder name.")
        else:
            p = Path(folder_name.strip())
            if not p.exists():
                st.error(f"'{folder_name}' not found.")
            elif not p.is_dir():
                st.warning("That is a file, not a folder.")
            else:
                try:
                    p.rmdir()
                    st.success(f"✅ Folder '{folder_name}' deleted.")
                except OSError:
                    st.error("Folder is not empty. Remove contents first.")
                except Exception as e:
                    st.error(f"Error: {e}")

# ── 8. LIST ALL ───────────────────────────────────────────────────────────────
elif operation == "📋 List All":
    st.markdown("### 📋 All Files & Folders")
    items = list_items()
    if items:
        st.caption(f"{len(items)} item(s) found")
        render_file_list()
    else:
        st.info("No files or folders in the current directory.")