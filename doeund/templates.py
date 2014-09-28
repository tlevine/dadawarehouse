from tempita import Template

drop_view = Template('DROP VIEW IF EXISTS cube_{{fact_table_base}};')

create_view = Template('''CREATE VIEW cube_{{fact_table_base}} AS
SELECT
{{for loop, column in looper(columns)}}
  {{column}}{{if not loop.last}},{{endif}}
{{endfor}}
FROM ft_{{fact_table_base}}
{{for to_table, on_columns in joins}}
    LEFT JOIN {{to_table}} ON
  {{if jointype == 'normal'}}
    {{for loop, column_pair in looper(on_columns)}}
      {{py: from_column, to_column = column_pair}}
      {{from_column}} = {{to_column}} {{if not loop.last}} AND{{endif}}
    {{endfor}}
  {{elif jointype == 'left-array'}}
    {{py: from_column, to_column = on_columns[0]}}
    ANY ({{from_column}}) = {{to_column}}
  {{elif jointype == 'right-array'}}
    {{py: from_column, to_column = on_columns[0]}}
    {{from_column}} = ANY ({{to_column}})
  {{elif jointype == 'full-array'}}
    {{py: from_column, to_column = on_columns[0]}}
    ANY ({{from_column}}) = ANY ({{to_column}})
  {{endif}}
{{endfor}}
{{for union in unions}}
UNION ALL
SELECT
  {{for loop, column in looper(union['selects'])}}
  {{column}}{{if not loop.last}},{{endif}}
  {{endfor}}
FROM {{union['table']}}
{{endfor}}
;''')
