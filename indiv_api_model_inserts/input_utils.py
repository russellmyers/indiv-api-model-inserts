import streamlit as st
import indiv_api_model_inserts

def check_widget_value_is_numeric(widget):
    try:
        _ = int(widget)
        return True
    except:
        return False


def get_params():
    st.sidebar.subheader("Parameters")

    selected_client_id = st.sidebar.text_input('Enter Client Id (eg 2): ')

    selected_payrun_id = st.sidebar.text_input('Enter PayRun Id (eg 58): ')

    selected_paygroup_name = st.sidebar.text_input('Enter PayGroup Name (eg bi-weekly_58): ')

    selected_model_id = st.sidebar.text_input('Enter Model Id (default 4): ', '4')

    selected_username = st.sidebar.text_input('Enter your username (eg Russell): ')

    notes = f"""
    <div><small>Notes:<br>
        <ul><li>Client Id = Id field from business.Clients table</li>
            <li>Payrun Id = Id field from payroll.PayRuns table</li>
            <li>PayGroup Name = pay_group_name field from payroll.PayGroups table</li>
            <li>Model Id = Id field from payAnomaly.ModelConfigurations table. Recommendation is to leave this as "4"</li>
            <li>username = Name to be placed in "Created by/Modified by" fields in insert statements</li>
        </ul>
    </small></div>
    """
    st.sidebar.markdown(notes, unsafe_allow_html=True)

    st.sidebar.caption(f"Version: {indiv_api_model_inserts.__version__}")

    return selected_client_id, selected_payrun_id, selected_paygroup_name, selected_model_id, selected_username


def check_for_input_errors(selected_client_id, selected_payrun_id, selected_paygroup_name,
                           selected_model_id, selected_username):
    if len(selected_client_id) == 0:
        st.error('Please enter client id')
    elif not check_widget_value_is_numeric(selected_client_id):
        st.error("Please enter numeric model id")
    elif len(selected_payrun_id) == 0:
        st.error('Please enter payrun_id')
    elif not check_widget_value_is_numeric(selected_payrun_id):
        st.error("Please enter numeric model id")
    elif len(selected_paygroup_name) == 0:
        st.error('Please enter pay group name')
    elif len(selected_model_id) == 0:
        st.error("Please enter model id")
    elif not check_widget_value_is_numeric(selected_model_id):
        st.error("Please enter numeric model id")
    elif len(selected_username) == 0:
        st.error("Please enter your username")
    else:
        return False

    return True
