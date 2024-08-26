import benefits_model as bene_model
import menu
import csv
from peewee import chunked
from peewee import fn

current_term = ""

def load_contract_file():
    with open('load_files/contract_data.csv', encoding="utf-8-sig") as file_handler:
                file_content = csv.DictReader(file_handler)
                with bene_model.db.atomic():
                        for batch in chunked(file_content, 100):
                            for row in batch: 
                                    query = bene_model.Contract_Report.delete().where(
                                            bene_model.Contract_Report.empl_id == row['empl_id'],
                                            bene_model.Contract_Report.term == row['term'], 
                                            bene_model.Contract_Report.class_number == row['class_number']
                                            )
                                    query.execute()
                            bene_model.Contract_Report.insert_many(batch).execute()


def load_ft_employee_file():
    delete_ft_employee_records()
    with open('load_files/ft_employee.csv', encoding="utf-8-sig") as file_handler:
                file_content = csv.DictReader(file_handler)
                with bene_model.db.atomic():
                        for batch in chunked(file_content, 100):
                                bene_model.FT_Employee.insert_many(batch).execute()


def load_jblm_contract_type_file():
    delete_jblm_contract_type_records()
    with open('load_files/jblm_contract_type.csv', encoding="utf-8-sig") as file_handler:
                file_content = csv.DictReader(file_handler)
                with bene_model.db.atomic():
                        for batch in chunked(file_content, 100):
                                bene_model.JBLM_Contract_Type.insert_many(batch).execute()


def load_class_mode_file():
    delete_class_mode_records()
    with open('load_files/class_mode.csv', encoding="utf-8-sig") as file_handler:
                file_content = csv.DictReader(file_handler)
                with bene_model.db.atomic():
                        for batch in chunked(file_content, 100):
                                bene_model.Class_Mode.insert_many(batch).execute()


def load_bene_eligible_file():
    delete_bene_eligible_records()
    with open('load_files/bene_eligible.csv', encoding="utf-8-sig") as file_handler:
                file_content = csv.DictReader(file_handler)
                with bene_model.db.atomic():
                        for batch in chunked(file_content, 100):
                                bene_model.Bene_Eligible.insert_many(batch).execute()


def stacking(empl_id, name, term, fte):
    stacking_empl_id = empl_id
    stacking_name = name
    stacking_term = term
    stacking_fte = fte
    bene_model.Contract_Report.insert(institution = 'WA110', empl_id = stacking_empl_id, term = stacking_term, name = stacking_name, fte_percentage = stacking_fte, class_number = "stack").execute()


def delete_stacking_record(all_or_one, del_empl_id="", del_term=""):
    if all_or_one.lower().strip() == 'all':
        bene_model.Contract_Report.delete().where(bene_model.Contract_Report.class_number == 'stack').execute()
    if all_or_one.lower().strip() == 'single':
        bene_model.Contract_Report.delete().where(bene_model.Contract_Report.class_number == 'stack', bene_model.Contract_Report.empl_id == del_empl_id, bene_model.Contract_Report.term == del_term).execute()


def load_stacking_file():
    with open('load_files/stacked_data.csv', encoding="utf-8-sig") as file_handler:
                file_content = csv.DictReader(file_handler)
                with bene_model.db.atomic():
                        for batch in chunked(file_content, 100):
                            for row in batch: 
                                    query = bene_model.Contract_Report.delete().where(
                                            bene_model.Contract_Report.empl_id == row['empl_id'],
                                            bene_model.Contract_Report.term == row['term'], 
                                            bene_model.Contract_Report.class_number == row['class_number']
                                            )
                                    query.execute()
                            bene_model.Contract_Report.insert_many(batch).execute()


def view_stacking_data():
    query = bene_model.Contract_Report.select().order_by(bene_model.Contract_Report.name, bene_model.Contract_Report.term).where(bene_model.Contract_Report.class_number == 'stack').execute()
    return query


def fte_analysis():
    with bene_model.db.atomic():
        delete_fte_analysis_records()
        query_1 = bene_model.Contract_Report.select()
        query_2 = bene_model.JBLM_Contract_Type.select()
        query_3 = bene_model.Class_Mode.select()
        jblm_contract_type_list = []
        class_mode_dict = {}
        for row in query_3:
            class_mode_dict[row.class_number + row.term] = [row.term, row.mode]
        for row in query_2:
            jblm_contract_type_list.append(row.jblm_type)
        for row in query_1:
            if row.contract_type in jblm_contract_type_list:
                reviewed_fte_calc = round((row.std_census_enrl / 75) * 100, 2)
            elif (row.contract_type =="ADS" and 
                str(class_mode_dict[row.class_number + row.term][1]).lower() == "hy") or (
                        row.contract_type =="ADS" and 
                        str(class_mode_dict[row.class_number + row.term][1]).lower() == "ol"):
                reviewed_fte_calc = round((row.contact_hours / row.base_contact_hours) * 100, 2)
            else:
                reviewed_fte_calc = round(row.fte_percentage, 2)
            bene_model.FTE_Analysis.insert(
                term=row.term, 
                empl_id=row.empl_id, 
                name=row.name, 
                class_number=row.class_number,
                subject=row.subject,
                catalog=row.catalog,
                std_census_enrl=row.std_census_enrl,
                base_contact_hours=row.base_contact_hours,
                contract_hours=row.contract_hours,
                contact_hours=row.contact_hours,
                adjusted_fte_percentage=reviewed_fte_calc,
                total_pay=row.total_pay
                ).execute()


def aggrigate_records():
    with bene_model.db.atomic():
        delete_aggrigate_records()
        query = bene_model.FTE_Analysis.select(bene_model.FTE_Analysis, fn.SUM(bene_model.FTE_Analysis.adjusted_fte_percentage).alias('fte_sum')).group_by(bene_model.FTE_Analysis.empl_id, bene_model.FTE_Analysis.term, )
        for row in query:
            bene_model.FTE_Combined_Grid.insert(
                    term=row.term, 
                    empl_id=row.empl_id, 
                    name=row.name, 
                    total_adjusted_fte_percentage=row.fte_sum
                    ).execute()


def results():
    with bene_model.db.atomic():
        terms = []
        terms.append(current_term)
        for term in range(7):
            if terms[-1][3] == '1':
                past_term = str(int(terms[-1]) - 4)
            else:
                past_term = str(int(terms[-1]) - 2)
            terms.append(past_term)
        employee_in_result_list = []
        delete_result_records()
        query_1 = bene_model.FTE_Combined_Grid.select(bene_model.FTE_Combined_Grid.empl_id).group_by(bene_model.FTE_Combined_Grid.empl_id)
        for row in query_1:
            employee_in_result_list.append(row.empl_id)
            bene_model.Result.insert(empl_id = row.empl_id).execute()
        query_3 = bene_model.FTE_Combined_Grid.select()
        for row in query_3:
            bene_model.Result.update(name = row.name).where(bene_model.Result.empl_id == row.empl_id).execute()
            if row.term in terms:
                index = terms.index(row.term)
                if index == 0:
                    bene_model.Result.update(current = row.total_adjusted_fte_percentage).where(bene_model.Result.empl_id == row.empl_id).execute()
                if index == 1:
                    bene_model.Result.update(two = row.total_adjusted_fte_percentage).where(bene_model.Result.empl_id == row.empl_id).execute()
                if index == 2:
                    bene_model.Result.update(three = row.total_adjusted_fte_percentage).where(bene_model.Result.empl_id == row.empl_id).execute()
                if index == 3:
                    bene_model.Result.update(four = row.total_adjusted_fte_percentage).where(bene_model.Result.empl_id == row.empl_id).execute()
                if index == 4:
                    bene_model.Result.update(five = row.total_adjusted_fte_percentage).where(bene_model.Result.empl_id == row.empl_id).execute()
                if index == 5:
                    bene_model.Result.update(six = row.total_adjusted_fte_percentage).where(bene_model.Result.empl_id == row.empl_id).execute()
                if index == 6:
                    bene_model.Result.update(seven = row.total_adjusted_fte_percentage).where(bene_model.Result.empl_id == row.empl_id).execute()
                if index == 7:
                    bene_model.Result.update(eight = row.total_adjusted_fte_percentage).where(bene_model.Result.empl_id == row.empl_id).execute()
            else:
                print('not in terms')
        ft_employees = []
        query_4 = bene_model.FT_Employee.select()
        for row in query_4:
            ft_employees.append(row.empl_id)
        query_5 = bene_model.Bene_Eligible.select(bene_model.Bene_Eligible.empl_id)
        bene_eligible_employees = []
        for row in query_5:
            bene_eligible_employees.append(row.empl_id)
        query_6 = bene_model.Result.select()
        for row in query_6:
            if row.empl_id in ft_employees:
                bene_model.Result.update(comment = "Full Time Employee").where(bene_model.Result.empl_id == row.empl_id).execute()
            elif row.empl_id not in ft_employees:
                # print(f"current = {bene_model.Result.current} | two = {bene_model.Result.two}")
                bene_model.Result.update(comment = "Maintain - Continue - teaching >= 50 pct and bene eligible").where(row.current >= 50, row.empl_id in bene_eligible_employees, bene_model.Result.empl_id == row.empl_id).execute()
                bene_model.Result.update(comment = "Maintain - Continue - teaching <= 50 pct and not bene eligible").where(row.current <= 50, row.empl_id not in bene_eligible_employees, bene_model.Result.empl_id == row.empl_id).execute()
                bene_model.Result.update(comment = "Review - Now Teaching <= 50 pct and bene eligible").where(row.current <= 50, row.empl_id in bene_eligible_employees, bene_model.Result.empl_id == row.empl_id).execute()
                bene_model.Result.update(comment = "Review - Now Teaching >= 50 pct and not bene eligible ").where(row.current >= 50, row.empl_id not in bene_eligible_employees, bene_model.Result.empl_id == row.empl_id).execute()
            else:
                bene_model.Result.update(comment = "Review - General Required").execute()

def delete_aggrigate_records():
    bene_model.FTE_Combined_Grid.delete().execute()  


def delete_fte_analysis_records():
    bene_model.FTE_Analysis.delete().execute()  

def delete_ft_employee_records():
     bene_model.FT_Employee.delete().execute()


def delete_class_mode_records():
     bene_model.Class_Mode.delete().execute()


def delete_jblm_contract_type_records():
     bene_model.JBLM_Contract_Type.delete().execute()


def delete_bene_eligible_records():
     bene_model.Bene_Eligible.delete().execute()


def delete_result_records():
     bene_model.Result.delete().execute()


def delete_contract_report_records():
     bene_model.Contract_Report.delete().where(bene_model.Contract_Report.class_number != 'stack').execute()


def download_final_results():
    query = bene_model.Result.select().dicts().execute()

    field_names = ['id', 'empl_id', 'name', 'eight', 'seven', 'six', 'five', 'four', 'three', 'two', 'current', 'comment']

    with open("report/report_final_results.csv", "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names, lineterminator='\n')
        writer.writeheader()
        writer.writerows(query)



def download_stacked_data():
    query = bene_model.Contract_Report.select(bene_model.Contract_Report.empl_id, bene_model.Contract_Report.name, bene_model.Contract_Report.term, bene_model.Contract_Report.fte_percentage).dicts().where(bene_model.Contract_Report.class_number == 'stack').execute()

    field_names = ['empl_id', 'name', 'term', 'fte_percentage']

    with open("report/report_stacked_data.csv", "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names, lineterminator='\n')
        writer.writeheader()
        writer.writerows(query)


def search_record():
    desired_id = input("Please enter the EMPL ID you wish to pull: ")
    query = bene_model.Contract_Report.select().where(bene_model.Contract_Report.empl_id == desired_id)
    [print([employee.empl_id, employee.name, employee.subject, employee.catalog, employee.total_pay, employee.fte_percentage]) for employee in query]


def view_single_contract_records(desired_id):
    query = bene_model.Contract_Report.select().order_by(bene_model.Contract_Report.name, bene_model.Contract_Report.term, bene_model.Contract_Report.class_number).where(bene_model.Contract_Report.empl_id == desired_id)
    for item in query:
         print(item.empl_id, item.fte_percentage)
    return query
 

def view_contract_records():
    query = bene_model.Contract_Report.select().order_by(bene_model.Contract_Report.name, bene_model.Contract_Report.term, bene_model.Contract_Report.class_number).where(bene_model.Contract_Report.class_number != 'stack')
    return query


def view_final_results():
    query = bene_model.Result.select().order_by(bene_model.Result.name)
    return query


def view_single_result(desired_id):
    query = bene_model.Result.select().where(bene_model.Result.empl_id == desired_id)
    return query


def view_final_review_results():
    query = bene_model.Result.select().order_by(bene_model.Result.name).where(bene_model.Result.comment.contains("Review"))
    query_count = bene_model.Result.select(fn.COUNT(bene_model.Result.empl_id).alias("row_count")).where(bene_model.Result.comment.contains("Review"))
    print("\n Row count: " + str([x.row_count for x in query_count][0])+ "\n")
    return query
   

if __name__ == '__main__':
     pass

       
