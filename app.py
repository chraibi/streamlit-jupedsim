import configparser
import os
import subprocess
from io import StringIO
from pathlib import Path

import lovely_logger as logging
import streamlit as st

path = Path(__file__)
ROOT_DIR = path.parent.absolute()
home_path = str(Path.home())


def file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)


def run_and_display_stdout(*cmd_with_args):
    lines = ""
    result = subprocess.Popen(cmd_with_args, stdout=subprocess.PIPE)
    for line in iter(lambda: result.stdout.readline(), b""):
        lines = lines + line.decode("utf-8") + "\n"

    output.code(lines)


def set_state_variables():
    if "old_configs" not in st.session_state:
        st.session_state.old_configs = ""

    if "lib_id" not in st.session_state:
        st.session_state.lib_id = 0

    if "lib_type" not in st.session_state:
        st.session_state.lib_type = "no"


def read_inifile(confParser):
    st.session_state.lib_id = int(confParser.get("zotero-config", "library_id"))
    api_key = confParser.get("zotero-config", "api_key")
    st.session_state.lib_type = confParser.get("zotero-config", "library_type")


if __name__ == "__main__":
    set_state_variables()
    st.header("JPscore")
    Inifile = "/Users/chraibi/workspace/jupedsim/jpscore/demos/03_corner/results/corner_ini.xml"
    jpscore_path = "/Users/chraibi/workspace/jupedsim/jpscore/build/bin/jpscore"

    inifile = st.sidebar.file_uploader(
        "📙Choose a config file ",
        type=["cfg", "xml"],
        help="Load config file",
    )

    st.sidebar.markdown("-------")
    #jpscore_exe = st.sidebar.text_input("jpscore")
    #st.sidebar.info(jpscore_exe)
    msg_status = st.sidebar.empty()

    if inifile:
        st.info(inifile)
        print(inifile.name)
        configFilePath = os.path.join(ROOT_DIR, inifile.name)
        confParser = configparser.RawConfigParser()
        stringio = StringIO(inifile.getvalue().decode("utf-8"))
        string_data = stringio.read()
        try:
            confParser.read_string(string_data)
            if string_data != st.session_state.old_configs:
                st.session_state.old_configs = string_data
                try:
                    # st.info("readinifile")
                    read_inifile(confParser)
                except Exception as e:
                    msg_status.error(
                        f"""Can't parse the config file.
                        Error: {e}"""
                    )
                    st.stop()

        except Exception as e:
            logging.error(f"can not read file {configFilePath} with error {str(e)}")

    sim = st.expander("Simulation")
    with sim:
        config = st.form("config")
        with config:
            c1, _, c2, _, c3, _, c4 = st.columns((1, 0.2, 1, 0.2, 1, 0.2, 1))
            c1.text_input("lib_id", value=st.session_state.lib_id)
            c2.text_input("lib_type", value=st.session_state.lib_type)
            c3.text_input("lib_type2", value=st.session_state.lib_type)
            c4.text_input("lib_id2", value=st.session_state.lib_id)

            c1.text_input("1lib_id", value=st.session_state.lib_id)
            c2.text_input("1lib_type", value=st.session_state.lib_type)
            c3.text_input("1lib_type2", value=st.session_state.lib_type)
            c4.text_input("1lib_id2", value=st.session_state.lib_id)

        start = config.form_submit_button(label="🚦Start")

    output = st.empty()
    
    vis = st.expander("Visualisation")
    with vis:
        filename = file_selector()
        st.write('You selected `%s`' % filename)
        
    if start:
        run_and_display_stdout(jpscore_path, Inifile)
