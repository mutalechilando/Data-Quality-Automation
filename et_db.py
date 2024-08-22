import os
import pandas as pd
import glob
import pyodbc

# Define the root directory containing the SQL databases
root_directory = r'F:\MDFs_2023-06'

merge_dir = r'C:\SqlCsv'

# Database connection settings
db_server = '.\SMARTCARE40'
db_user = 'sa'
db_password = 'm7r@n$4mAz'
db_name = 'cdc_fdb_db'

# Initialize a DataFrame to store extracted data
all_data = pd.DataFrame()

# Loop through subdirectories representing databases
for database_dir in os.listdir(root_directory):
    database_path = os.path.join(root_directory, database_dir)

    # Establish a connection to the database
    try:
        connection = pyodbc.connect(
            'DRIVER={SQL Server};'
            f'SERVER={db_server};'
            f'DATABASE={db_name};'
            f'UID={db_user};'
            f'PWD={db_password};'
        )

        print("Connected to SQL Server")

        cursor = connection.cursor()

        # Execute SQL query
        query = """
        

DECLARE @STARTDATE DATETIME,
		@ENDDATE DATETIME, 
		@ProvinceId VARCHAR(2), 
		@DistrictId VARCHAR(2), 
		@FacilityGuid VARCHAR(100), 
		@FacilityId VARCHAR(10);

	SET @FacilityId = (SELECT [Value] FROM Setting WHERE [Name] = 'hmiscode');
	SET @ProvinceId = (SELECT [Value] FROM Setting WHERE [Name] = 'ProvinceId');
	SET @DistrictId = (SELECT [Value] FROM Setting WHERE [Name] = 'DistrictId');
	SET @STARTDATE = '2017-01-01';
	SET @ENDDATE = '2023-06-30';

SELECT PatientId, FacilityName, 
art_number, visit_type, visit_date, apt_date, sex, date_of_birth, age, systolic, diastolic, pregnant, art_start_date,
lab_result, lab_date, lab_type, regimen, who_stage, marital_status, hh_income, weight, height, diabetes, patient_status, transfer_in_date, transfer_out_date, dead_date, patient_inactive_date,
patient_reactivated_date, adherence_doses_missed, reason_for_referral

FROM
(SELECT art.PatientId,
F.FacilityName,  
art.ArtNumber art_number, art.VisitType visit_type, art.VisitDate visit_date, art.AppointmentDate apt_date, 
reg.Sex sex, reg.DateOfBirth date_of_birth, dbo.fn_Age(reg.DateOfBirth, GetDate()) age,
vt.SystolicPressure systolic,vt.DiastolicPressure diastolic, art.pregnant, ps.ArtStartDate art_start_date,
lb.LabTestValue + ' ' + lb.Units lab_result, lb.LabOrderDate lab_date, lb.AbbrvSyn lab_type,
cbs.NameARVs regimen, who.WhoStageToday who_stage,
reg.Married marital_status, ic.hh_income, vt.Weight 'weight', vt.Height height, art.diabetes, 
ps.PatientStatus patient_status,
cbs.TransferInDate transfer_in_date, cbs.TransferOutDate transfer_out_date, st.PatientDiedDate dead_date, st.PatientMadeInactiveDate patient_inactive_date, 
st.PatientReactivatedDate patient_reactivated_date, 
CASE fu.adherence_and_medication_how_many_doses_missed WHEN 0 THEN '0' WHEN 1 THEN '1' WHEN 2 THEN 'Greater or Equla to 2' END adherence_doses_missed, 
ref.transfer_out_referral_reason reason_for_referral, 
ROW_NUMBER() OVER (PARTITION BY art.PatientId ORDER BY art.VisitDate DESC)seq 
FROM 
(SELECT  hp.PatientId, hp.ArtNumber, hp.VisitDate, hp.VisitDate AppointmentDate, 'IHAP' VisitType, hp.Location edit_location, 
CASE hp.PatientPregnant WHEN 0 THEN 'Yes' WHEN 1 THEN 'No' END pregnant, 
CASE WHEN db.PatientId IS NOT NULL THEN 'Yes' ELSE 'No' END diabetes
From crtIHAP hp
LEFT JOIN 
(SELECT PatientId, InteractionTime, ShortTitle, OnsetDate, ResolvedDate
 FROM 
 crtProblemEpisode p
 JOIN crctProblemEpisode c ON p.InteractionID = c.InteractionID

 JOIN ICPC2eCodes cod ON c.ICPCProblem = cod.ICPCConceptID
  WHERE ICPCProblem in (538, 539, 602) 
  AND c.Certainty = 0)db ON hp.PatientId = db.PatientId) art
LEFT JOIN 
(SELECT NaturalNumber, OwningGuid 
FROM GuidMap WHERE MappedGuid = OwningGuid)gd
ON art.PatientId = gd.NaturalNumber
LEFT JOIN Registration rg ON gd.OwningGuid = rg.PatientGUID
LEFT JOIN crtRegistrationInteraction reg ON art.PatientId = reg.patientId_int
LEFT JOIN 
(SELECT PatientId, InteractionTime VisitDate, ServiceName, Weight, Height, SystolicPressure, DiastolicPressure 
FROM
(SELECT vt.PatientId, vt.InteractionTime, sc.ServiceName, vt.Weight, vt.Height, vt.SystolicPressure, vt.DiastolicPressure,     
ROW_NUMBER() OVER (PARTITION BY vt.PatientId ORDER BY vt.InteractionTime DESC)seq
FROM crtVitals vt
JOIN ServiceCodes sc ON vt.ServiceCode = sc.ServiceCode
WHERE COALESCE(vt.Weight, vt.Height, vt.SystolicPressure, vt.DiastolicPressure) IS NOT NULL
)vts
WHERE vts.seq = 1) vt 
ON art.PatientId = vt.PatientId
LEFT JOIN 
(SELECT PatId, InteractionID, EditLocation, 
LabOrderDate, LabTestID, AbbrvSyn, LabTestValue, Units

FROM
(SELECT PatId, InteractionID, EditLocation, 
LabOrderDate, LabTestID, AbbrvSyn, LabTestValue, Units, 
ROW_NUMBER() OVER (PARTITION BY PatID ORDER BY LabOrderDate DESC)seq

FROM( 
	SELECT 
		i.PatientReportingId PatId,
		a.InteractionID, 
		a.EditLocation, 
		CASE
            WHEN a.LabOrderDate IS NULL THEN i.InteractionDate 
            ELSE a.LabOrderDate END LabOrderDate, 
		a.LabTestID, 
		c.AbbrvSyn, 
		b.LabTestValue, 
		c.Units
	
	FROM crctLaboratoryOrderDetails a
	JOIN crctLaboratoryResultDetails b ON a.InteractionID = b.InteractionID AND a.LaboratoryOrderID = b.LaboratoryOrderID
	LEFT JOIN Interaction i ON a.InteractionID = i.InteractionID AND ServiceCode = 402 
	LEFT JOIN LabTestsDictionary c ON a.LabTestID = c.LabTestID
		WHERE a.LabTestID IN (102, 103, 104, 105, 106, 107, 108) AND b.LabTestValue IS NOT NULL
		AND a.EditLocation IN (SELECT SubSiteId FROM 
		(SELECT DISTINCT SubSiteId
	FROM dbo.fn_GetFacilitySubSiteIds(@ProvinceId, @DistrictId, @FacilityId))cf		
		))x)y
		WHERE y.seq = 1 AND y.PatId IS NOT NULL)lb 
ON art.PatientId = lb.PatId
LEFT JOIN 
(SELECT chs.PatientId, chs.oldestHivPosTEstDate, chs.ArtStartDate, chs.LastClinicalVisit, ad.NextAppointmentDate,
CASE WHEN dbo.fnGetPatientRegistrationStatusAtFacility(chs.PatientId, @ENDDATE) IS NOT NULL 
THEN dbo.fnGetPatientRegistrationStatusAtFacility(chs.PatientId, @ENDDATE)  
ELSE (CASE WHEN (st.PatientMadeInactive = 1 AND st.PatientReactivatedDate IS NOT NULL)
THEN (CASE WHEN DATEDIFF(day,ad.NextAppointmentDate, @ENDDATE) < 30 THEN 'P' ELSE 'P' END)
WHEN (st.PatientMadeInactive = 1 AND st.PatientMadeInactiveDate IS NOT NULL) 
THEN 'Inactive' WHEN DATEDIFF(day,ad.NextAppointmentDate, @ENDDATE) < 30 THEN 'P' ELSE 'P' END) 
END PatientStatus
FROM ClientHivSummary chs
LEFT JOIN 
(SELECT PatientId, VisitDate, NextAppointmentDate
FROM
(SELECT p.PatientId, p.VisitDate, p.NextAppointmentDate,
ROW_NUMBER() OVER(PARTITION BY p.PatientId ORDER BY p.NextAppointmentDate DESC)seq

FROM crtMedicationsDispensed p
JOIN crctMedicationDispensingDetails c 
ON c.InteractionID = p.InteractionID
WHERE ArvDrugDispensed = 1)x
WHERE x.seq = 1) ad 
ON chs.PatientId = ad.PatientId
LEFT JOIN crtPatientStatus st ON chs.PatientId = st.PatientId
WHERE chs.ARTStartDate is not null) ps 
ON art.PatientId = ps.PatientId
LEFT JOIN ClientCaseBasedSurveillance cbs ON art.PatientId = cbs.PatientId
LEFT JOIN Art45_ClinicalFollowUpInteraction1 fu ON art.PatientId = fu.patient_guid
LEFT JOIN FacilitySubSite FSS ON FSS.SubSiteId = reg.EditLocation
LEFT JOIN Facility F ON F.FacilityGuid = FSS.FacilityGuid
LEFT JOIN crtPatientStatus st ON art.PatientId = st.PatientId
LEFT JOIN 
(SELECT patient_guid PatientId, 
CASE hh_income WHEN 0 THEN 'Less than K500' WHEN 1 THEN 'K500 - K999' WHEN 2 THEN 'K1000 - K1499' WHEN 3 THEN 'K1500 - K1999' 
WHEN 4 THEN 'K2000 - K2999' WHEN 5 THEN 'Greater than K3000' END hh_income
FROM
(SELECT patient_guid, background_house_hold_income2 hh_income, 
ROW_NUMBER() OVER (PARTITION BY patient_guid ORDER BY overview_interaction_time DESC)seq
FROM Art45_PaedsPatientLocatorInteraction1
UNION
SELECT patient_guid, background_house_hold_income hh_income,
ROW_NUMBER() OVER (PARTITION BY patient_guid ORDER BY overview_interaction_time DESC)seq
FROM Art45_PatientLocatorInteraction1)x
WHERE x.seq = 1) ic 
ON art.PatientId = ic.PatientId
LEFT JOIN 
(SELECT PatientId, WhoStageToday, VisitDate 
FROM
(SELECT patientId, WhoStageToday, VisitDate,
ROW_NUMBER() OVER(PARTITION BY PatientId ORDER BY VisitDate DESC)seq
FROM ClientHivWhoStage)x 
WHERE x.seq = 1)who 
ON art.PatientId = who.PatientId
LEFT JOIN 
(SELECT PatientId, visit_date, transfer_out_referral_reason
FROM
(SELECT patient_guid PatientId, overview_interaction_time visit_date,
CASE transfer_out_referral_reason WHEN 0 THEN transfer_out_other_reason_patient_transfer 
WHEN 1 THEN 'Patient request' WHEN 2 THEN 'Discharge from facility' WHEN 3 THEN 'Complicated care'
WHEN 4 THEN 'Routine transfer' END transfer_out_referral_reason, 
ROW_NUMBER() OVER(PARTITION BY patient_guid ORDER BY overview_interaction_time DESC)seq 
FROM Art45_PatientStatusInteraction2)x
WHERE x.seq = 1) ref 
ON art.PatientId = ref.PatientId
WHERE (art.VisitDate >= @STARTDATE OR art.AppointmentDate >= @STARTDATE 
OR ps.ArtStartDate >= @STARTDATE OR lb.LabOrderDate >= @STARTDATE
OR cbs.TransferInDate >= @STARTDATE OR cbs.TransferOutDate >= @STARTDATE
OR st.PatientDiedDate >= @STARTDATE OR st.PatientMadeInactiveDate >= @STARTDATE OR st.PatientReactivatedDate >= @STARTDATE) 
)x
WHERE x.seq = 1;
    
        """
        
        cursor.execute(query)

        # Fetch data and transform into dictionaries
        columns = [column[0] for column in cursor.description]
        data = cursor.fetchall()
        data_dicts = [dict(zip(columns, row)) for row in data]        
        
        data_df = pd.DataFrame(data_dicts) #Create DataFrame from list of dictionaries
        all_data = all_data.append(data_df, ignore_index=True)

        print(f'Finished extracting data for {database_dir}...')

    except pyodbc.Error as e:
        print("Error:", e)
    finally:
        connection.close()

# Save the extracted data to a CSV file
output_csv = os.path.join(merge_dir, 'merged_data.csv')
all_data.to_csv(output_csv, index=False)
print("Merged data saved to", output_csv)
