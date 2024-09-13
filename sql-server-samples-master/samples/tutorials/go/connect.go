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
)

func main() {
	connString := fmt.Sprintf("server=%s;user id=%s;password=%s;port=%d",
		server, user, password, port)

	conn, err := sql.Open("mssql", connString)
	if err != nil {
		log.Fatal("Open connection failed:", err.Error())
	}
	fmt.Printf("Connected!\n")
	defer conn.Close()
	stmt, err := conn.Prepare("select @@version")
	row := stmt.QueryRow()
	var result string

	err = row.Scan(&result)
	if err != nil {
		log.Fatal("Scan failed:", err.Error())
	}
	fmt.Printf("%s\n", result)
}
