import streamlit as st
import base64

from indiv_api_model_inserts.model_insert_queries import model_configurations_insert,\
     model_versions_insert, model_keys_insert, model_blob_storage_insert, generate_id
from indiv_api_model_inserts.input_utils import get_params, check_for_input_errors


st.title("Generate Indiv Api Model Configuration SQL Insert statements")
st.caption("This app generates SQL Insert statements ready to be applied in the"
           " relevant Eloise SQL Database environment")

selected_client_id, selected_payrun_id, selected_paygroup_name, selected_model_id, selected_username\
    = get_params()


if st.button("Generate"):
    errors_found = check_for_input_errors(selected_client_id, selected_payrun_id, selected_paygroup_name,
                                          selected_model_id, selected_username)

    if errors_found:
        pass
    else:
        # Output results

        generated_id = generate_id(selected_client_id, selected_payrun_id)
        result = f"<div style='background-color:#F0F8FF'>SQL Insert statements generated below for: " \
                 f"<ul><li>Client Id: <b>{selected_client_id}</b></li>" \
                 f"<li>Pay Run Id: <b>{selected_payrun_id}</b></li>" \
                 f"<li>Pay Group name: <b>{selected_paygroup_name}</b></li><br>" \
                 f"<li>Model Id: <b>{selected_model_id}</b></li>" \
                 f" <li>Model Version Id: <b>{generated_id}</b></li></ul>"\

        st.markdown(result, unsafe_allow_html=True)

        st.header("SQL INSERT statements")

        LOGO_IMAGE = './img/attn.png'
        tst = base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()
        result = f"<div style='background-color:#F0F8FF'><img src='data:image/png;base64,{tst}' width='30px'></img><b> Please apply each of the following SQL INSERT statements in the relevant DB environment:</b>" \
                 f"<br><small><i>Note:</i> If the <i>payAnomaly.ModelConfigurations</i> SQL insert fails with  a 'duplicate key' message," \
                 f" just ignore and proceed with the next insert (ie this just implies that the necessary payAnomaly.ModelConfigurations record already exists)" \
                 f"</small></div>"
        st.markdown(result, unsafe_allow_html=True)

        query = model_configurations_insert(selected_model_id, selected_username)
        st.subheader("1 - payAnomaly.ModelConfigurations INSERT statement")
        st.success(query)

        query = model_versions_insert(selected_model_id, model_version_id=generated_id,
                                      pay_group_name=selected_paygroup_name, username=selected_username)
        st.subheader("2 - payAnomaly.ModelVersions INSERT statement")
        st.success(query)

        query = model_keys_insert(selected_client_id, payrun_id=selected_payrun_id, username=selected_username,
                                  model_key_id=generated_id)

        st.subheader("3 - payAnomaly.ModelKeys INSERT statement")
        st.success(query)

        query = model_blob_storage_insert(selected_client_id, payrun_id=selected_payrun_id, username=selected_username,
                                          model_blob_storage_id=generated_id, model_id=selected_model_id,
                                          model_version_id=generated_id)
        st.subheader("4 - payAnomaly.ModelBlobStorage INSERT statement")
        st.success(query)
