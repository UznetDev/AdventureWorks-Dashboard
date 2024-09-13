DROP TABLE IF EXISTS Todo

GO

CREATE TABLE Todo (
	id int IDENTITY PRIMARY KEY,
	title nvarchar(30) NOT NULL,
	description nvarchar(4000),
	completed bit,
	dueDate datetime2 default (dateadd(day, 3, getdate()))
)

GO

INSERT INTO Todo (title, description, completed, dueDate)
VALUES
('Install SQL Server 2016','Install RTM version of SQL Server 2016', 0, '2016-06-01'),
('Get new samples','Go to github and download new samples', 0, '2016-06-02'),
('Try new samples','Install new Management Studio to try samples', 0, '2016-06-02')