from datetime import datetime


def format_datetime_now():

    dt = datetime.utcnow()
    dt_formatted = dt.strftime('%Y-%m-%d %H:%M:%S')
    return dt_formatted


def generate_id(client_id, payrun_id):
    generated_id = f'{int(client_id)}{int(payrun_id):02}'
    return int(generated_id)


def model_configurations_insert(model_id, username):

    now_formatted = format_datetime_now()

    query = f"""
    SET IDENTITY_INSERT payAnomaly.ModelConfigurations ON;
    INSERT
    INTO
    payAnomaly.ModelConfigurations
    (Id, Model_Name, Model_Description, Model_Type, Created_By, Created_Ts, Last_Modified_By, Last_Modified_Ts)
    VALUES
    ({model_id},
    N'GaussianNormalWeighted',
    N'Implementation of Gaussian Normal Distribution that allows for weighting',
    N'Probablistic modeling',
    N'{username}',
    N'{now_formatted}',
    N'{username}',
    N'{now_formatted}');
    SET IDENTITY_INSERT payAnomaly.ModelConfigurations OFF
    """

    print(f'Inserting ModelConfigurations: {query}')
    return query


def model_versions_insert(model_id, model_version_id, pay_group_name, username):
    now_formatted = format_datetime_now()

    query = f"""
    SET IDENTITY_INSERT payAnomaly.ModelVersions ON;
    INSERT
    INTO
    payAnomaly.ModelVersions
    (Id, Version, Version_Description, Model_Id, Model_Hyper_Parameters, Model_Features, Model_Functions, Model_Query_Parameters, Model_Workflow, Is_Production, Created_By, Created_Ts, Last_Modified_By, Last_Modified_Ts)
    VALUES
    ({model_version_id},
     N'0.0.0',
     N'{pay_group_name} config, forward, weighting with drop outliers',
     {model_id},
     N'{{"Range":1,"Level_Type":"EL","Base_Query":"SELECT * FROM payroll.PayDataHistory", "Base_Shelve_Key":"","weight":0.5,"drop_outliers":"False"}}',
     N'{{"Selection_Features":["Company_Id","Employee_Id","Pay_Period","Pay_Group", "Paydate","Year","Month","Day","Employee_Status","Variable_Id","Tolerance", "Value"], "Results_Features":["Pay_Group","Company_Id","Employee_Id","Employee_Status", "Variable_Id","Values"], "Target":"Value","Model_Key":["Employee_Id","Employee_Status"], "History_Key":["Pay_Group","Company_Id","Employee_Id","Paydate","Variable_Id"]}}',
     N'',
     N'{{"Base_Query":  "SELECT a.Run_Id, a.Pay_Period, a.Period_Start_Date, a.Period_End_Date,a.Company_Id, a.Employee_Id, b.Employee_Status, a.Paydate, Variable_Id, Tolerance, Value, Year, Month, Week,Day, a.Pay_Group, Retro_Period, Sub_Period FROM payroll.PayDataHistory a INNER JOIN payAnomaly.EmployeePayState b ON b.Employee_Id = a.Employee_Id AND b.Run_Id = a.Run_Id INNER JOIN payAnomaly.Variables c ON c.Id = a.Variable_Id INNER JOIN business.Companies d ON d.Id = a.Company_Id", "Selection_Parameters":{{"a.Pay_Group":"{pay_group_name}"}}, "Results_Query":"SELECT * FROM payAnomaly.AnomalyResults"}}',
     N'{{"production":{{"train": ["train_GN","insert_file_to_db"], "fit":["predict_GN","bulk_insert"]}}, "adhoc":{{"predict": ["predict_GN","bulk_insert"]}}, "test":{{"train": ["train_GN","insert_file_to_db"], "fit":["predict_GN","bulk_insert"]}}}}',
     1,
     N'{username}', N'{now_formatted}',
     N'{username}', N'{now_formatted}');
     SET IDENTITY_INSERT payAnomaly.ModelVersions OFF
     """

    print(f'Inserting ModelVersions: {query}')
    return query


def model_keys_insert(client_id, payrun_id, username, model_key_id):
    now_formatted = format_datetime_now()

    query = f"""
    SET IDENTITY_INSERT payAnomaly.ModelKeys ON;
    INSERT INTO
    payAnomaly.ModelKeys
    (Id, Model_key, Client_Id, Created_By, Created_Ts, Last_Modfied_By, Last_Modified_Ts, PayRun_Id,
     Is_Active, Model_Workflow)
    VALUES
    ({model_key_id},
     N'{client_id}_{payrun_id}',
     {client_id},
     N'{username}',
     N'{now_formatted}',
     N'{username}',
     N'{now_formatted}',
     {payrun_id},
     1,
     N'{{"Models":["GaussianNormalWeighted"]}}');
     SET IDENTITY_INSERT payAnomaly.ModelKeys OFF
    """

    print(f'Inserting ModelKeys: {query}')

    return query


def model_blob_storage_insert(client_id, payrun_id, username, model_blob_storage_id, model_id, model_version_id):
    now_formatted = format_datetime_now()

    query = f"""
    SET IDENTITY_INSERT payAnomaly.ModelBlobStorage ON;
    INSERT INTO
    payAnomaly.ModelBlobStorage
    (Id, Client_Id, PayRun_Id, Model_Key, Model_File_Path, Model_Id, Model_Version_Id, Model_Blob, File_Type, Is_Active, Created_By, Created_Ts, Last_Modified_By, Last_Modified_Ts)
    VALUES
    ({model_blob_storage_id},
      {client_id},
      {payrun_id},
      N'{client_id}_{payrun_id}',
      N'client_{client_id}/models/model_{model_id}_version_{model_version_id}_models',
      {model_id},
      {model_version_id},
      null,
      N'dat',
      1,
      N'{username}', N'{now_formatted}',
      N'{username}', N'{now_formatted}');
      SET IDENTITY_INSERT payAnomaly.ModelBlobStorage OFF
    """

    print(f'Inserting ModelBlobStorage: {query}')
    return query


if __name__ == '__main__':
    sel_client_id = 1
    sel_payrun_id = 63
    sel_model_id = 4
    sel_model_version_id = 51
    sel_model_key_id = 51
    sel_model_blob_storage_id = 451
    sel_pay_group_name = 'monthly'
    sel_username = 'Rusty'

    model_configurations_insert(sel_model_id, sel_username)

    model_versions_insert(sel_model_id, sel_model_version_id, sel_pay_group_name, sel_username)

    model_keys_insert(sel_client_id, sel_payrun_id, sel_username, sel_model_key_id)

    model_blob_storage_insert(sel_client_id, sel_payrun_id, sel_username, sel_model_blob_storage_id,
                              sel_model_id, sel_model_version_id)
