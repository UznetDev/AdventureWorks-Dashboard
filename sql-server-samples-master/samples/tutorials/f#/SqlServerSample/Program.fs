// Learn more about F# at http://fsharp.org

open System
open System.Data.SqlClient

[<EntryPoint>]
let main argv =
    printfn "Connect to SQL Server and demo Create, Read, Update and Delete operations."
    let builder = new SqlConnectionStringBuilder()
    builder.DataSource <- "localhost"
    builder.UserID <- "sa"
    builder.Password <- "your_password"
    builder.InitialCatalog <- "master"

    printf "Connecting to SQL Server ... "
    use connection = new SqlConnection(builder.ConnectionString)

    try
        connection.Open()
        printfn "Done."

        // Create a sample database
        printf "Dropping and creating database 'FSharpSampleDB' ... "
        let sql = "DROP DATABASE IF EXISTS [FSharpSampleDB]; CREATE DATABASE [FSharpSampleDB]"
        use command = new SqlCommand(sql, connection)
        command.ExecuteNonQuery() |> ignore
        printfn "Done."

        // Create a Table and insert some sample data
        printf "Creating sample table with data, press any key to continue..."
        Console.ReadKey(true) |> ignore
        let sql = "
            USE FSharpSampleDB;
            CREATE TABLE Employees (
             Id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
             Name NVARCHAR(50),
             Location NVARCHAR(50)
            );
            INSERT INTO Employees (Name, Location) VALUES
            (N'Tom', N'United States'),
            (N'Krzysztof', N'Poland'),
            (N'Isaac', N'Germany'); "

        use command = new SqlCommand(sql, connection)
        command.ExecuteNonQuery() |> ignore
        printfn "Done."

        // INSERT demo
        printf "Inserting a new row into table, press any key to continue... "
        Console.ReadKey(true) |> ignore
        let sql = "
            INSERT Employees (Name, Location)
            VALUES (@name, @location);"
        use command = new SqlCommand(sql, connection)
        command.Parameters.AddWithValue("@name", "Don") |> ignore
        command.Parameters.AddWithValue("@location", "United Kingdom") |> ignore
        let rowsAffected = command.ExecuteNonQuery()
        printfn "%i row(s) inserted" rowsAffected

        // UPDATE demo
        let userToUpdate = "Tom";
        printf "Updating 'Location' for user '%s', press any key to continue... " userToUpdate
        Console.ReadKey(true) |> ignore
        let sql = "UPDATE Employees SET Location = N'United Kingdom' WHERE Name = @name"
        use command = new SqlCommand(sql, connection)
        command.Parameters.AddWithValue("@name", userToUpdate) |> ignore
        let rowsAffected = command.ExecuteNonQuery()
        printfn "%i row(s) updated" rowsAffected

        // DELETE demo
        let userToDelete = "Don";
        printf "Deleting user '%s', press any key to continue... " userToDelete
        Console.ReadKey(true) |> ignore
        let sql = "DELETE FROM Employees WHERE Name = @name;"
        use command = new SqlCommand(sql, connection)
        command.Parameters.AddWithValue("@name", userToDelete) |> ignore
        let rowsAffected = command.ExecuteNonQuery()
        printfn "%i row(s) deleted" rowsAffected

        // READ demo
        printfn "Reading data from table, press any key to continue... "
        Console.ReadKey(true) |> ignore
        let sql = "SELECT Id, Name, Location FROM Employees;"
        use command = new SqlCommand(sql, connection)
        use reader = command.ExecuteReader()

        while reader.Read() do
            printfn "%i %s %s" (reader.GetInt32(0)) (reader.GetString(1)) (reader.GetString(2))

    with
    | ex -> printfn "%O" ex

    printfn "All done. Press the any key to finish..."
    Console.ReadKey(true) |> ignore

    0 // return an integer exit code
