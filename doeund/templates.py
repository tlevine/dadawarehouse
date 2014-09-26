import tempia

'''CREATE VIEW cube_{{fact_table}} AS
SELECT
{{for dimension in dimensions}}
  {{dimension}},
{{endfor}}
  *
FROM ft_{{fact_table}}
{{for to_table, on_columns in joins}}
  JOIN {{to_table}} ON
  {{for loop, column_pair in looper(on_columns)}}
    {{py: from_column, to_column = column_pair}}
    {{from_column}} = {{to_column}} {{if not loop.last}} AND{{endif}}
  {{endfor}}
{{endfor}}
'''

).substitute(fact_table = fact_table,
                new_columns = rendered_new_columns,
                joins = rendered_joins)

def join(from_table, to_table, on_columns):
    Template('JOIN $to_table ON
