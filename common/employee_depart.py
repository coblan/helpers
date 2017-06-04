import employee

def get_admin(BasicInfo,
                    EmployeeModel):
    emp_admin=employee.get_admin(BasicInfo, EmployeeModel)
    
    class EmployeeItem(emp_admin['EmployeeItem']):
        template=''
    
    emp_admin['EmployeeItem']=EmployeeItem
    emp_admin['EmpGroup'].tabs[0]={'name':'emp','label':'Ô±¹¤','page_cls':EmployeeItem}
    return emp_admin
    