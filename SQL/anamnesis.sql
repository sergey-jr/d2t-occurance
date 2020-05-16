select distinct(anamnesis.patient_id), value_string, string_value, time_scheduled
from anamnesis_item  
join anamnesis_item_type on anamnesis_type_id = anamnesis_item_type.id
join anamnesis on anamnesis_id = anamnesis.id
join strings on anamnesis_item_type.name_string_id = string_id
join patient_visit on patient_visit.id=patient_visit_id
where upper(value_string) like upper('%диабет 2%') and language_id=1
order by anamnesis.patient_id, time_scheduled