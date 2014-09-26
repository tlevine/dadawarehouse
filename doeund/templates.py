from tempita import Template

drop_view = Template('DROP VIEW IF EXISTS cube_{{fact_table_base}};')

create_view = Template('''CREATE VIEW cube_{{fact_table_base}} AS
SELECT
{{for dimension in dimensions}}
  {{dimension}},
{{endfor}}
  *
FROM ft_{{fact_table_base}}
{{for to_table, on_columns in joins}}
  JOIN {{to_table}} ON
  {{for loop, column_pair in looper(on_columns)}}
    {{py: from_column, to_column = column_pair}}
    {{from_column}} = {{to_column}} {{if not loop.last}} AND{{endif}}
  {{endfor}}
{{endfor}};
''')
