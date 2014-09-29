from tempita import Template

drop_view = Template('DROP VIEW IF EXISTS cube_{{fact_table_base}};')

create_view = Template('''CREATE VIEW cube_{{fact_table_base}} AS
{{if len(unions) > 0:}}
SELECT * FROM (
{{endif}}

SELECT
{{for loop, column in looper(columns)}}
  {{column}}{{if not loop.last}},{{endif}}
{{endfor}}
FROM ft_{{fact_table_base}}
{{for to_table, on_columns in joins}}
LEFT JOIN {{to_table}} ON
{{for loop, column_pair in looper(on_columns)}}
  {{py: from_column, to_column = column_pair}}
  {{from_column}} = {{to_column}} {{if not loop.last}} AND{{endif}}
{{endfor}}
{{endfor}}
{{for union in unions}}
{{py: selects, table, joins = union}}
UNION ALL
SELECT
  {{for loop, column in looper(selects)}}
  {{column}}{{if not loop.last}},{{endif}}
  {{endfor}}
FROM {{table}}


{{for to_table, on_columns in joins}}
LEFT JOIN {{to_table}} ON
{{for loop, column_pair in looper(on_columns)}}
  {{py: from_column, to_column = column_pair}}
  {{from_column}} = {{to_column}} {{if not loop.last}} AND{{endif}}
{{endfor}}
{{endfor}}


{{endfor}}

{{if len(unions) > 0:}}
) AS potential_duplicates GROUP BY
{{for loop, column in looper(primary_keys)}}
  {{column}}{{if not loop.last}},{{endif}}
{{endfor}}
{{endif}}
;''')
