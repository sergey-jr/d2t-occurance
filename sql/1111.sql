select mr.id, string_value from strings inner join measurement mr on strings.string_id=mr.name_string_id
where mr.id in (27, 128, 1581, 8542, 8561, 1581, 1582)