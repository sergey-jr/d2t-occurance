﻿select * from strings 
where
string_value is not Null and (upper(string_value) LIKE upper('%Билирубин%') or upper(string_value) LIKE upper('%bilirubin'))