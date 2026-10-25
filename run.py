# Purpose of this file is to test the code and Check Output.

# You can clean this file if any code exists. And write your own code.

#---------------------------------------------------------------------------------------

class Company:
  def __init__(self, employees):
    self.employees = employees

  def __len__(self):
    return len(self.employees)

c1 = Company(["Emil", "Tobias", "Linus"])

print(len(c1))