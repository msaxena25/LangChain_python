"""

from langchain_community.tools import DuckDuckGoSearchRun

search_tool = DuckDuckGoSearchRun()

#result = search_tool.invoke("What is the latest news of Delhi on protest against the government, India?")
result = search_tool.invoke("What is latest news by apple this weeek 23 october 2026?")
print(result)
'''
Delhi police denied permission for the protest to take place in the centre of the capital, and in the days leading up to Saturday, officials began to barricade roads throughout Delhi. Indian authorities clamp down as 'cockroach' movement launches new protests Demonstrators gathering in Mumbai and New Delhi to demand the resignation of Election Commission chief meet stern ... Delhi Protest Latest breaking news, pictures, photos and Video News. Find Delhi Protest news headlines, photos, videos, comments, blog posts and opinion at The Indian Express. protests in delhi Latest Breaking News, Pictures, Videos, and Special Reports from The Economic Times. protests in delhi Blogs, Comments and Archive News on Economictimes.com Indian authorities have imposed extraordinary security measures to block protesters from joining a demonstration called by the "Cockroach" movement in New Delhi. The main leaders of the party were ...
'''

'''
Find latest Apple News on Gadgets 360. Get the latest apple news headlines including analysis on top apple news, stories, photos and more on apple Apple October 2026 product schedule: Welcome Home event on Oct. 13, iPhone Duo from $1,999 on Oct. 23, and which Mac and iPad news is still only rumored. Apple's October 2026 Launches: 10 New Products Expected (iPhone Duo, OLED MacBook Pro, HomePod mini…) Apple is preparing two waves of launches in October 2026: smart home products on October 13, iPhone Duo on October 23, then new Macs and an OLED iPad mini around October 27. Here is everything expected. Get official Apple news from the Apple Newsroom archive. Access press releases, photos, videos, updates and more today See the latest on Apple. From breaking news to in-depth reporting, Bloomberg tracks the full story in real time.
'''



#--------------------------------------

# Create custom tool

from langchain_core.tools import tool

@tool
def create_fabanaccri_series(n: int) -> list[int]:
    '''This tool returns a Fibonacci series up to n'''
    a, b = 0, 1
    result = [0]
    for _ in range(n):
        a, b = b, a + b
        result.append(a)
    return result

'''
- @tool decorator is used to convert a Python function into a LangChain tool.
- type hints are used to specify the type of the input and output of the function.
- function description is used to describe the function.
'''

result = create_fabanaccri_series.invoke({"n": 7})
print(result) # [0, 1, 1, 2, 3, 5, 8, 13]

print(create_fabanaccri_series.name)
print(create_fabanaccri_series.description)
print(create_fabanaccri_series.args)

print('LLM will receive the following schema:')
print(create_fabanaccri_series.args_schema.model_json_schema())
'''
{
 'description': 'This tool returns a Fibonacci series up to n',
 'properties': {'n': {'title': 'N', 'type': 'integer'}}, 
 'required': ['n'],
 'title': 'create_fabanaccri_series', 
 'type': 'object'
 }
'''



#--------------------------------------

# Method 2: StructuredTool.from_function() with Pydantic Model

'''
Lets Create a Income TAX Calculator tool
If salary < 5 lakhs no tax
if salary 5 to 10 lakhs > 10 %
if salary 10 to 20 lakhs > 20 %
if > 20 lakhs 30%
Return the tax amount

Note - This tax percentages must be configurable by the user with its default values.
'''

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

# Ceate Pydantic Model for the tool
class IncomeTaxCalculatorSchema(BaseModel):
    salary: float = Field(description="The salary of the employee", required=True, ge=0)
    slab1_rate: float = Field(description="The tax rate for the first slab", ge=0, le=1, default=0.10) # 10%
    slab2_rate: float = Field(description="The tax rate for the second slab", ge=0, le=1, default=0.20) # 20%
    slab3_rate: float = Field(description="The tax rate for the third slab", ge=0, le=1, default=0.30) # 30%

# Define the business logic
def income_tax_calculator(salary: float, slab1_rate: float, slab2_rate: float, slab3_rate: float) -> float:
    '''This tool calculates the progressive income tax for the given salary based on the given slab rates'''
    tax_amount = 0

    if salary > 500000:
        tax_amount += min(salary - 500000, 500000) * slab1_rate
    if salary > 1000000:
        tax_amount += min(salary - 1000000, 1000000) * slab2_rate
    if salary > 2000000:
        tax_amount += (salary - 2000000) * slab3_rate

    return tax_amount
    
# Convert the function into a LangChain tool
income_tax_calculator_tool: StructuredTool = StructuredTool.from_function(
    func=income_tax_calculator,
    name="income_tax_calculator",
    description=(
        "This tool calculates the progressive income tax for the given salary based on the given slab rates"
        "If salary <= 5 lakhs no tax"
        "if salary 5 to 10 lakhs = 10%"
        "if salary 10 to 20 lakhs = 20%"
        "if salary > 20 lakhs = 30%"
        "Return the tax amount"
        "Note - This tax percentages must be configurable by the user with its default values."
    ),
    args_schema=IncomeTaxCalculatorSchema
)

result = income_tax_calculator_tool.invoke({"salary": 1100000})
print('Tax amount for salary 11 lakhs is:', result) # 70000.0

'''
result = income_tax_calculator_tool.invoke({"salary": 1500000})
print('Tax amount for salary 15 lakhs is:', result) # 150000.0

result = income_tax_calculator_tool.invoke({"salary": 5000000})
print('Tax amount for salary 50 lakhs is:', result) # 1150000.0

result = income_tax_calculator_tool.invoke({"salary": 500000})
print('Tax amount for salary 5 lakhs is:', result) # 0

# change the slab rates
result = income_tax_calculator_tool.invoke({"salary": 2500000, "slab1_rate": 0.15, "slab2_rate": 0.25, "slab3_rate": 0.35})
print('Tax amount for salary 25 lakhs with new slab rates is:', result) # 500000.0
'''

print('name', income_tax_calculator_tool.name)
print('description', income_tax_calculator_tool.description)
# print LLM schema
print('LLM will receive the following schema:')
print(income_tax_calculator_tool.args_schema.model_json_schema())
'''
{'properties':
    {'salary': {'description': 'The salary of the employee', 'minimum': 0, 'required': True, 'title': 'Salary', 'type': 'number'}, 
    'slab1_rate': {'default': 0.1, 'description': 'The tax rate for the first slab', 'maximum': 1, 'minimum': 0, 'title': 'Slab1 Rate', 'type': 'number'},
    'slab2_rate': {'default': 0.2, 'description': 'The tax rate for the second slab', 'maximum': 1, 'minimum': 0, 'title': 'Slab2 Rate', 'type': 'number'}, 
    'slab3_rate': {'default': 0.3, 'description': 'The tax rate for the third slab', 'maximum': 1, 'minimum': 0, 'title': 'Slab3 Rate', 'type': 'number'}}, 
    'required': ['salary'], 
    'title': 'IncomeTaxCalculatorSchema',
    'type': 'object'}
'''

"""

#---------------------------------------

# Method 3 base Tool

'''
Create a tool to get a Grade in exams 
If total obtained number >= 75% then grade A+
If number >= 60% then grade A
If number >= 50% then grade B
If number >= 35% then grade C
Below 35% = Fail

Input = 
tota obtained marks, 
total exam marks: by default it will be 500

'''


from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

# create schema
class GradeToolSchema(BaseModel):
    obtained_marks: float = Field(description='optained marks in the exam', ge=0, required=True)
    total_exam_marks: int = Field(description='total exam marks', default=500, gt=0)
    
class GradeTool(BaseTool):
    name: str = 'Grade_Calculator' # Dont give spaces, Gemini does not allow in tool names.
    description: str = '''
    Create a tool to get a Grade in exams 
    If total obtained number >= 75% then grade A+
    If number >= 60% then grade A
    If number >= 50% then grade B
    If number >= 35% then grade C
    Below 35% = Fail
    '''
    args_schema: Type[BaseModel] = GradeToolSchema
    
    def _run(self, obtained_marks: float, total_exam_marks: int  = 500) -> dict:
        grade = ''
        percentage = (obtained_marks / total_exam_marks) * 100
        if percentage >= 75:
            grade = 'A+'
        elif percentage >= 60:
            grade = 'A'
        elif percentage >= 50:
            grade = 'B'
        elif percentage >= 35:
            grade = 'C'
        else:
            grade = 'Fail'
        return { 'percentage': percentage, 'grade': grade }
        #return f"Percentage: {percentage:.2f}%, Grade: {grade}"

                    
grade_tool_obj = GradeTool()

result = grade_tool_obj.invoke({'obtained_marks': 450})
print(result) # {'percentage': 90.0, 'grade': 'A+'}

'''
result = grade_tool_obj.invoke({'obtained_marks': 100})
print(result) # {'percentage': 20.0, 'grade': 'Fail'}

result = grade_tool_obj.invoke({'obtained_marks': 300})
print(result) # {'percentage': 60.0, 'grade': 'A'}

print(grade_tool_obj.name)
print(grade_tool_obj.description)
'''

#------------------------------------------------

# Create another tool - Scholarship Calculator tool

'''
when grade A+, student is eligible for 50k scholarship.
When grade A, then 30K
no scholorship below grade A.
'''

from langchain_core.tools import tool

@tool
def scholarship_calculator_tool(grade: str) -> dict:
    '''Calculate scholarship eligibility and amount based on the student's grade.'''
    scholarship = {}
    if (grade == 'A+'):
        scholarship = {'eligible': True, 'scholarship_amount': 50000}
    elif (grade == 'A'):
        scholarship = {'eligible': True, 'scholarship_amount': 30000}
    else:
        scholarship = {'eligible': False, 'scholarship_amount': 0}
    return scholarship
    
#result =  scholarship_calculator_tool.invoke({'grade': 'A'})
#print('scholarship ', result)  # {'eligible': True, 'scholarship_amount': 30000}

# Toolkit

'''
We'll combine existing Grade Calculator Tool with a new Scholarship Calculator Tool using a LangChain toolkit.

The workflow will be:
1. The grade tool calculates the student's percentage and grade.
2. The scholarship tool checks the grade and returns the eligible scholarship amount.
3. The toolkit groups both tools together so they can be provided to an agent.
'''

from langchain_core.tools import BaseToolkit

class StudentToolkit(BaseToolkit):
    '''Toolkit for student grading and scholarship calculations.'''
    
    def get_tools(self) -> list[BaseTool]:
        return [grade_tool_obj, scholarship_calculator_tool]
    
# Now get all tools from toolkit

student_toolkit = StudentToolkit()

print('tool names from toolkit')
tools = student_toolkit.get_tools()
print('total tools', len(tools)) # 2
for tool in student_toolkit.get_tools():
    print(tool.name)
    
# Grade Calculator
# scholarship_calculator_tool

'''
Notes -

If we create tools using class (Method 2 & 3) then we pass object of that class into get_tools method.
If we create tools using @tool decorator, we can pass that tool function into get_tools method.
The toolkit groups the tools, but it does not automatically execute them in sequence.
'''

# How to use that toolkit?
print('Use of toolkit...')
tools = student_toolkit.get_tools()

grade = tools[0].invoke({'obtained_marks': 350})
scholorship = tools[1].invoke({'grade': grade.get('grade')})
print(scholorship)

#--------------------------------------------------------------------



