from pos_sistem.modules.employees.add_employee import add_employee
from pos_sistem.modules.employees.delete_employee import delete_employee
from pos_sistem.modules.employees.list_employees import list_employees

def main():
    print(" Employee Management Test")

    #Crear empleados
    add_employee("Ana Martínez", "ana@example.com", "Cajera")
    add_employee("Carlos Ruiz", "carlos@example.com", "Supervisor")

    #Listar empleados
    list_employees()

    #Eliminar empleado por ID 
    delete_employee(1)

    #Listar nuevamente
    list_employees()

if __name__ == "__main__":
    main()
