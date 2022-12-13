import gradescope_auto_py as gap

grader_config = gap.GraderConfig.from_txt('example_hw_config.txt')
grader = gap.Grader(grader_config)


from math import pi

def get_circle_area(radius):
    return pi * radius
assert 3 + 2 == 5, 'this assert should be ignored (for points)'
grader._assert(passes=get_circle_area(radius=1) == pi, msg="assert get_circle_area(radius=1) == pi, 'get_circle_area(radius=1)  (1 pts)'")
grader._assert(passes=get_circle_area(radius=10) == 100 * pi, msg="assert get_circle_area(radius=10) == 100 * pi, 'get_circle_area(radius=1) (2912849128 pts)'")

#print markdown table of results
df = grader.get_df()
del df['ast_assert']
print(df.to_markdown())