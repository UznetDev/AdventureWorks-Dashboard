DROP TABLE IF EXISTS Comments
GO

CREATE TABLE Comments (
	id int IDENTITY PRIMARY KEY,
	author nvarchar(30) NOT NULL,
	text nvarchar(4000)
)
GO

INSERT INTO Comments (author, text)
VALUES
('John','This is great!'),
('Jane','I like the fact that it is simple.')