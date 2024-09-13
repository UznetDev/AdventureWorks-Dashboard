package main

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/denisenkom/go-mssqldb"
)

var (
	server   = "localhost"
	port     = 1433
	user     = "sa"
	password = "your_password"
	database = "SampleDB"
)

// CreateEmployee create an employee
func CreateEmployee(db *sql.DB, name string, location string) (int64, error) {
	tsql := fmt.Sprintf("INSERT INTO TestSchema.Employees (Name, Location) VALUES ('%s','%s');",
		name, location)
	result, err := db.Exec(tsql)
	if err != nil {
		fmt.Println("Error inserting new row: " + err.Error())
		return -1, err
	}
	return result.LastInsertId()
}

// ReadEmployees read all employees
func ReadEmployees(db *sql.DB) (int, error) {
	tsql := fmt.Sprintf("SELECT Id, Name, Location FROM TestSchema.Employees;")
	rows, err := db.Query(tsql)
	if err != nil {
		fmt.Println("Error reading rows: " + err.Error())
		return -1, err
	}
	defer rows.Close()
	count := 0
	for rows.Next() {
		var name, location string
		var id int
		err := rows.Scan(&id, &name, &location)
		if err != nil {
			fmt.Println("Error reading rows: " + err.Error())
			return -1, err
		}
		fmt.Printf("ID: %d, Name: %s, Location: %s\n", id, name, location)
		count++
	}
	return count, nil
}

// UpdateEmployee update an employee's information
func UpdateEmployee(db *sql.DB, name string, location string) (int64, error) {
	tsql := fmt.Sprintf("UPDATE TestSchema.Employees SET Location = '%s' WHERE Name= '%s'",
		location, name)
	result, err := db.Exec(tsql)
	if err != nil {
		fmt.Println("Error updating row: " + err.Error())
		return -1, err
	}
	return result.LastInsertId()
}

// DeleteEmployee delete an employee from database
func DeleteEmployee(db *sql.DB, name string) (int64, error) {
	tsql := fmt.Sprintf("DELETE FROM TestSchema.Employees WHERE Name='%s';", name)
	result, err := db.Exec(tsql)
	if err != nil {
		fmt.Println("Error deleting row: " + err.Error())
		return -1, err
	}
	return result.RowsAffected()
}

func main() {
	// Connect to database
	connString := fmt.Sprintf("server=%s;user id=%s;password=%s;port=%d;database=%s;",
		server, user, password, port, database)
	conn, err := sql.Open("mssql", connString)
	if err != nil {
		log.Fatal("Open connection failed:", err.Error())
	}
	fmt.Printf("Connected!\n")
	defer conn.Close()

	// Create employee
	createID, err := CreateEmployee(conn, "Jake", "United States")
	if err != nil {
		log.Fatal("CreateEmployee failed:", err.Error())
	}
	fmt.Printf("Inserted ID: %d successfully.\n", createID)

	// Read employees
	count, err := ReadEmployees(conn)
	if err != nil {
		log.Fatal("ReadEmployees failed:", err.Error())
	}
	fmt.Printf("Read %d rows successfully.\n", count)

	// Update from database
	updateID, err := UpdateEmployee(conn, "Jake", "Poland")
	if err != nil {
		log.Fatal("UpdateEmployee failed:", err.Error())
	}
	fmt.Printf("Updated row with ID: %d successfully.\n", updateID)

	// Delete from database
	rows, err := DeleteEmployee(conn, "Jake")
	if err != nil {
		log.Fatal("DeleteEmployee failed:", err.Error())
	}
	fmt.Printf("Deleted %d rows successfully.\n", rows)
}
