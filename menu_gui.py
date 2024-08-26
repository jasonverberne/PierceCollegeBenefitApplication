import main_gui
import sys
import time
import benefits_model as bene_model


def load_all_files():
    try:
        start = time.time()
        print("\nProcessing...\n")
        print('Loading Contract File\n')
        main_gui.load_contract_file()
        print('Contract File Loaded\n')
        print('Loading Class Mode File\n')
        main_gui.load_class_mode_file()
        print('Class Mode File Loaded\n')
        print('Loading Full Time Employee File\n')
        main_gui.load_ft_employee_file()
        print('Full Time Employee File Loaded\n')
        print('Loading Benefit Eligible File\n')
        main_gui.load_bene_eligible_file()
        print('Benefit Eligible File Loaded\n')
        print('Loading JBLM Contract File\n')
        main_gui.load_jblm_contract_type_file()
        print('JBLM Contract Type File Loaded\n')
        print("File Load Complete\n")
        end = time.time()
        print(f"Load time: {end - start} seconds")
    except:
        print("An error has occurred")

def load_contract_data():
    try:
        main_gui.load_contract_file()
    except:
        print("An error has occurred, the file was not loaded.")


def load_full_time_employee():
    try:
        main_gui.load_ft_employee_file()
    except:
        print("An error has occurred, the file was not loaded.")


def load_class_mode_data():
    try:
        main_gui.load_class_mode_file()
    except:
        print("An error has occurred, the file was not loaded.")


def load_benefit_eligible_data():
    try:
        main_gui.load_bene_eligible_file()
    except:
        print("An error has occurred, the file was not loaded.")


def load_jblm_contract_type_data():
    try:
        main_gui.load_jblm_contract_type_file()
    except:
        print("An error has occurred, the file was not loaded.")


def current_term_input(term):
    main_gui.current_term = term


def add_stacking(stk_id, stk_name, stk_term, stk_fte):
    try:
        empl_id = stk_id
        name = stk_name
        term = stk_term
        fte = stk_fte

        main_gui.stacking(stk_id, stk_name, stk_term, stk_fte)
    except:
        print("\nAn error occurred. No data was entered")


def delete_stacking(all_or_one,  del_empl_id="", del_term=""):
    try:
        main_gui.delete_stacking_record(all_or_one, del_empl_id, del_term)
    except:
        print("\nAn error occurred.")


def clear_all_data_tables():
        main_gui.delete_contract_report_records()
        main_gui.delete_aggrigate_records()
        main_gui.delete_bene_eligible_records()
        main_gui.delete_class_mode_records()
        main_gui.delete_ft_employee_records()
        main_gui.delete_fte_analysis_records()
        main_gui.delete_jblm_contract_type_records()
        main_gui.delete_result_records()
        print("\nThe tables were deleted.")
        


def perform_analysis():
    try:
        start = time.time()
        print("\nProcessing...\n")
        print('Analyzing FTE\n')
        main_gui.fte_analysis()
        print('FTE Analysis Complete\n')
        print('Aggrigating Records\n')
        main_gui.aggrigate_records()
        print('Aggrigate Records Complete\n')
        print('Updating Final Results\n')
        main_gui.results()
        print('Results Complete\n')
        print("Analysis Complete\n")
        end = time.time()
        print(f"Analysis time: {end - start} seconds")
    except:
        print("An error occurred, please ensure all files are properly loaded.")


def view_stacking_data():
    try:
        results = main_gui.view_stacking_data()
        return results
    except:
        print("\nAn error has occurred.\n")


def load_stacked_data():
    try:
        print("\nLoading stacked data from file")
        main_gui.load_stacking_file()
        print("\nStacked file loaded\n")
    except:
        print("\nAn error has occurred")



def download_final_results():
    try:
        main_gui.download_final_results()
        print('\nFinal Results Downloaded\n')
    except:
        print("\nAn error has occurred")


def download_stacked_data():
    try:
        main_gui.download_stacked_data()
        print('\nStacked Data Downloaded\n')
    except:
        print("\nAn error has occurred\n")


def view_contract_records():
    try:
        records = main_gui.view_contract_records()
        return records
    except:
        print("\nAn error has occurred\n")


def view_contract_single_emplid_records(desired_id):
    try:
        result = main_gui.view_single_contract_records(desired_id)
        return result
    except:
        print("\nAn error has occurred\n")


def view_result_single(desired_id):
    try:
        query = main_gui.view_single_result(desired_id)
        return query
    except:
        print("\nAn error has occurred\n")


def view_final_results():
    try:
        query = main_gui.view_final_results()
        return query
    except:
        print("\nAn error has occurred\n")


def view_review_result():
    try:
        query = main_gui.view_final_review_results()
        return query
    except:
        print("\nAn error has occurred\n")


def quit():
    "Quits the program"
    sys.exit()


def close_database():
     bene_model.db.close()
     sys.exit()