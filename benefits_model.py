from peewee import *

db = SqliteDatabase('benefits_model.db')

class Contract_Report(Model):
    institution = CharField()
    term = CharField()
    empl_id = CharField()
    name = CharField(null=True)
    empl_rcd = CharField(null=True)
    contract_type = CharField(null=True)
    contract_number = CharField(null=True)
    class_number = CharField(null=True)
    subject = CharField(null=True)
    catalog = CharField(null=True)
    description = CharField(null=True)
    std_census_enrl = IntegerField(null=True)
    pay_group = CharField(null=True)
    contract_dept = CharField(null=True)
    contract_begin_date = CharField(null=True)
    contract_end_date = CharField(null=True)
    department = CharField(null=True)
    combo_code = CharField(null=True)
    earnings_code = CharField(null=True)
    sequence_number = CharField(null=True)
    base_contact_hours = IntegerField(null=True)
    contract_hours = FloatField(null=True)
    contact_hours = FloatField(null=True)
    fte_percentage = FloatField(null=True)
    total_pay = FloatField(null=True)
    contract_signed = CharField(null=True)
    contract_rescinded = CharField(null=True)
    contract_approved = CharField(null=True)

    class Meta:
        database = db 

class FTE_Analysis(Model):
    term = CharField(null=True)
    empl_id = CharField(null=True)
    name = CharField(null=True)
    class_number = CharField(null=True)
    subject = CharField(null=True)
    catalog = CharField(null=True)
    std_census_enrl = IntegerField(null=True)
    base_contact_hours = IntegerField(null=True)
    contract_hours = FloatField(null=True)
    contact_hours = FloatField(null=True)
    adjusted_fte_percentage = FloatField(null=True)
    total_pay = FloatField(null=True)

    class Meta:
        database = db 


class FTE_Combined_Grid(Model):
    term = CharField(null=True)
    empl_id = CharField(null=True)
    name = CharField(null=True)
    total_adjusted_fte_percentage = FloatField(null=True)

    class Meta:
        database = db 


class FT_Employee(Model):
    empl_id = CharField(null=True)

    class Meta:
        database = db 


class Bene_Eligible(Model):
    empl_id = CharField(null=True)

    class Meta:
        database = db 


class JBLM_Contract_Type(Model):
    jblm_type = CharField(null=True)

    class Meta:
        database = db 


class Class_Mode(Model):
    term = CharField(null=True)
    class_number = CharField(null=True)
    mode = CharField(null=True)

    class Meta:
        database = db 


class Result(Model):
    empl_id = CharField(null=False)
    name = CharField(null=True)    
    eight = DecimalField(null=True, default = 0)
    seven = DecimalField(null=True, default = 0)
    six = DecimalField(null=True, default = 0)
    five = DecimalField(null=True, default = 0)
    four = DecimalField(null=True, default = 0)
    three = DecimalField(null=True, default = 0)
    two = DecimalField(null=True, default = 0)
    current = DecimalField(null=True, default = 0)
    comment = CharField(null=True, default = "")

    class Meta:
        database = db 

db.connect()

db.create_tables([Contract_Report, FTE_Analysis, FT_Employee, JBLM_Contract_Type, Class_Mode, Bene_Eligible, FTE_Combined_Grid, Result])
