import streamlit as st

from indiv_api_model_inserts.model_insert import model_configurations_insert,\
     model_versions_insert, model_keys_insert, model_blob_storage_insert, generate_id
st.title("Generate Indiv Api Model Configuration SQL Insert statements")


def check_widget_value_is_numeric(widget):
    try:
        val = int(widget.title())
        return True
    except:
        return False

def get_widget_value(widget):
    return widget.title()


st.sidebar.subtitle("Parameters")

client_id_widget = st.sidebar.text_input('Enter Client Id (eg 1): ')

payrun_id_widget = st.sidebar.text_input('Enter PayRun Id (eg 2): ')

paygroup_name_widget = st.sidebar.text_input('Enter PayGroup Name (eg bi-weekly): ')

model_id_widget = st.sidebar.text_input('Enter Model Id (default 4): ', '4')

username_widget = st.sidebar.text_input('Enter your username (eg Russell): ')


if st.button("Generate"):
    if len(client_id_widget.title()) == 0:
        st.error('Please enter client id')
    elif not check_widget_value_is_numeric(client_id_widget):
        st.error("Please enter numeric model id")
    elif  len(payrun_id_widget.title()) == 0:
        st.error('Please enter payrun_id')
    elif not check_widget_value_is_numeric(payrun_id_widget):
        st.error("Please enter numeric model id")
    elif  len(paygroup_name_widget.title()) == 0:
        st.error('Please enter pay group name')
    elif len(model_id_widget.title()) == 0:
        st.error("Please enter model id")
    elif not check_widget_value_is_numeric(model_id_widget):
        st.error("Please enter numeric model id")
    elif len(username_widget.title()) == 0:
        st.error("Please enter your username")
    else:
        client_id = get_widget_value(client_id_widget)
        payrun_id = get_widget_value(payrun_id_widget)
        paygroup_name = get_widget_value(paygroup_name_widget)
        username = get_widget_value(username_widget)
        model_id = get_widget_value(model_id_widget)

        generated_id = generate_id(client_id, payrun_id)
        result = f'<div style="background-color:#F0F8FF">SQL Insert statements generated for <ul><li>Client Id: <b>{client_id}</b></li><li>Pay Run Id: <b>{payrun_id}</b></li><li>Pay Group name: <b>{paygroup_name}</b></li><br>' \
                 f'<li>Model Id: <b>{model_id}</b></li> <li>Model Version Id: <b>{generated_id}</b></li></ul>' \
                 f'Please run each of the following SQL INSERT statements in the relevant DB environment:<br>' \
                 f'<small><i>Note:</i> If ModelConfigurations SQL insert fails with duplicate key, just ignore (ie necessary record already exists)</small></div>'
        #st.markdown(html_string, unsafe_allow_html=True)
        st.markdown(result, unsafe_allow_html=True)
        query = model_configurations_insert(4, 'Rusty')
        st.subheader("payAnomaly.ModelConfigurations SQL INSERT statements:")
        st.success(query)

        query = model_versions_insert(model_id, model_version_id=generated_id,
                                      pay_group_name=paygroup_name, username=username)
        st.subheader("payAnomaly.ModelVersions SQL INSERT statements:")
        st.success(query)


        query = model_keys_insert(client_id, payrun_id=payrun_id, username=username, model_key_id=generated_id)
        st.subheader("payAnomaly.ModelKeys SQL INSERT statements:")
        st.success(query)

        query = model_blob_storage_insert(client_id, payrun_id=payrun_id, username=username,
                                          model_blob_storage_id=generated_id, model_id=model_id,
                                          model_version_id=generated_id)
        st.subheader("payAnomaly.ModelBlobStorage SQL INSERT statements:")
        st.success(query)
