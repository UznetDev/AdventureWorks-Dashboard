package main

import (
	"database/sql"
	"fmt"
	"log"
	"time"

	_ "github.com/denisenkom/go-mssqldb"
)

var (
	server   = "localhost"
	port     = 1433
	user     = "sa"
	password = "your_password"
	database = "SampleDB"
)

// ExecuteAggregateStatement output summary of prices
func ExecuteAggregateStatement(db *sql.DB) {
	result, err := db.Prepare("SELECT SUM(Price) as sum FROM Table_with_5M_rows")
	if err != nil {
		fmt.Println("Error preparing query: " + err.Error())
	}

	row := result.QueryRow()
	var sum string
	err = row.Scan(&sum)
	fmt.Printf("Sum: %s\n", sum)
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

	t1 := time.Now()
	fmt.Printf("Start time: %s\n", t1)

	ExecuteAggregateStatement(conn)

	t2 := time.Since(t1)
	fmt.Printf("The query took: %s\n", t2)
}
